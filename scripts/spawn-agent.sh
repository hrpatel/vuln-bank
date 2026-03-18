#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $(basename "$0") <agent-name> [--branch <branch-name>]"
  echo ""
  echo "Creates an isolated agent workspace (git worktree + beads identity)."
  echo "Run from the main repo root. Then open the new folder in your editor."
  echo ""
  echo "Options:"
  echo "  --branch <name>   Git branch for the worktree (default: <agent-name>/work)"
  echo ""
  echo "Examples:"
  echo "  $(basename "$0") cursor-a"
  echo "  $(basename "$0") cursor-b --branch cursor/02-xss-fix"
  exit 1
}

die() { echo "ERROR: $1" >&2; exit 1; }

# --- Parse arguments ---
AGENT_NAME=""
BRANCH=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --branch)
      [[ $# -lt 2 ]] && die "--branch requires a value"
      BRANCH="$2"; shift 2 ;;
    -h|--help)
      usage ;;
    -*)
      die "Unknown option: $1" ;;
    *)
      [[ -n "$AGENT_NAME" ]] && die "Only one agent name allowed"
      AGENT_NAME="$1"; shift ;;
  esac
done

[[ -z "$AGENT_NAME" ]] && usage

# Validate agent name: alphanumeric + hyphens only
[[ "$AGENT_NAME" =~ ^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$ ]] \
  || die "Agent name must be alphanumeric with hyphens (no leading/trailing hyphen): '$AGENT_NAME'"

# Default branch
[[ -z "$BRANCH" ]] && BRANCH="${AGENT_NAME}/work"

# --- Verify we're in the main repo root ---
git rev-parse --is-inside-work-tree >/dev/null 2>&1 \
  || die "Not inside a git repository"
[[ -d ".beads" ]] \
  || die "No .beads/ directory — is this a beads-enabled repo? Run 'bd init' first."
[[ ! -f ".bd-agent-identity" ]] \
  || die "Found .bd-agent-identity — you're inside an agent worktree. Run from the main repo root."

REPO_ROOT="$(git rev-parse --show-toplevel)"
REPO_BASENAME="$(basename "$REPO_ROOT")"
WORKTREE_PATH="$(cd "$REPO_ROOT/.." && pwd)/${REPO_BASENAME}-${AGENT_NAME}"

[[ ! -d "$WORKTREE_PATH" ]] \
  || die "Worktree path already exists: $WORKTREE_PATH"

# --- Create worktree via bd ---
echo "Creating worktree at $WORKTREE_PATH (branch: $BRANCH)..."
bd worktree create "$WORKTREE_PATH" --branch "$BRANCH"

# --- Enable per-worktree config (idempotent) ---
git config set extensions.worktreeConfig true

# --- Set per-worktree identity ---
git -C "$WORKTREE_PATH" config --worktree set user.name "$AGENT_NAME"

# --- Write identity marker ---
echo "$AGENT_NAME" > "$WORKTREE_PATH/.bd-agent-identity"

# --- Summary ---
echo ""
echo "========================================="
echo "  Agent workspace ready"
echo "========================================="
echo "  Agent:     $AGENT_NAME"
echo "  Worktree:  $WORKTREE_PATH"
echo "  Branch:    $BRANCH"
echo "  Identity:  git user.name = $AGENT_NAME"
echo ""
echo "  Open this folder in your editor/agent."
echo "========================================="
echo ""
echo "Active worktrees:"
git worktree list
