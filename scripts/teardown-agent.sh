#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $(basename "$0") <agent-name> [--force]"
  echo ""
  echo "Removes an agent workspace created by spawn-agent.sh."
  echo "Run from the main repo root."
  echo ""
  echo "Options:"
  echo "  --force   Remove even if worktree has uncommitted changes"
  exit 1
}

die() { echo "ERROR: $1" >&2; exit 1; }

# --- Parse arguments ---
AGENT_NAME=""
FORCE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force) FORCE=true; shift ;;
    -h|--help) usage ;;
    -*)  die "Unknown option: $1" ;;
    *)
      [[ -n "$AGENT_NAME" ]] && die "Only one agent name allowed"
      AGENT_NAME="$1"; shift ;;
  esac
done

[[ -z "$AGENT_NAME" ]] && usage

# --- Verify we're in the main repo root ---
git rev-parse --is-inside-work-tree >/dev/null 2>&1 \
  || die "Not inside a git repository"
[[ -d ".beads" ]] \
  || die "No .beads/ directory — is this a beads-enabled repo?"
[[ ! -f ".bd-agent-identity" ]] \
  || die "Found .bd-agent-identity — you're inside an agent worktree. Run from the main repo root."

REPO_ROOT="$(git rev-parse --show-toplevel)"
REPO_BASENAME="$(basename "$REPO_ROOT")"
WORKTREE_PATH="$(cd "$REPO_ROOT/.." && pwd)/${REPO_BASENAME}-${AGENT_NAME}"

[[ -d "$WORKTREE_PATH" ]] \
  || die "Worktree not found: $WORKTREE_PATH"

# --- Check for uncommitted changes ---
if [[ "$FORCE" != "true" ]]; then
  if ! git -C "$WORKTREE_PATH" diff --quiet || ! git -C "$WORKTREE_PATH" diff --cached --quiet; then
    die "Worktree has uncommitted changes. Use --force to remove anyway."
  fi
  UNTRACKED="$(git -C "$WORKTREE_PATH" ls-files --others --exclude-standard | head -1)"
  if [[ -n "$UNTRACKED" ]]; then
    die "Worktree has untracked files. Use --force to remove anyway."
  fi
fi

# --- Clean up identity marker ---
rm -f "$WORKTREE_PATH/.bd-agent-identity"

# --- Remove worktree ---
echo "Removing agent workspace: $AGENT_NAME ($WORKTREE_PATH)..."
if [[ "$FORCE" == "true" ]]; then
  bd worktree remove "$WORKTREE_PATH" --force 2>/dev/null \
    || git worktree remove "$WORKTREE_PATH" --force
else
  bd worktree remove "$WORKTREE_PATH" 2>/dev/null \
    || git worktree remove "$WORKTREE_PATH"
fi

echo ""
echo "Agent workspace '$AGENT_NAME' removed."
echo ""
echo "Remaining worktrees:"
git worktree list
