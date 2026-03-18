# Agent Identity & Filesystem Isolation Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prevent identity and filesystem collisions when multiple AI agents run in parallel on the same machine, by providing operator-run scripts that create isolated, identity-aware worktrees.

**Architecture:** A `spawn-agent.sh` script creates per-agent git worktrees with distinct `git config --worktree user.name` values so `bd` commands automatically resolve to the correct agent identity. A `teardown-agent.sh` script cleans up. Workflow docs are updated to enforce a session-start identity check.

**Tech Stack:** Bash scripts, git worktree, git config `--worktree`, `bd worktree create`, Markdown docs.

**Spec:** [docs/specs/2026-03-18-agent-identity-isolation-design.md](../specs/2026-03-18-agent-identity-isolation-design.md)

---

## File Structure

| File | Action | Responsibility |
|------|--------|----------------|
| `scripts/spawn-agent.sh` | Create | Provisions an isolated agent workspace (worktree + identity) |
| `scripts/teardown-agent.sh` | Create | Cleans up an agent workspace |
| `.gitignore` | Modify | Add `.bd-agent-identity` |
| `.cursorrules` | Modify | Add Step 0 identity verification |
| `CLAUDE.md` | Modify | Add Step 0 identity verification |
| `AGENTS.md` | Modify | Add "Agent Identity" section |
| `.workflow/START HERE.md` | Modify | Add Step 0 to session start; update parallel agents guidance |
| `.workflow/onboarding.md` | Modify | Replace manual worktree instructions with `spawn-agent.sh` |
| `.workflow/beads-coordination.md` | Modify | Update parallel agents and claiming sections |
| `.workflow/Tips & Lessons.md` | Modify | Add identity collision lesson learned |

---

## Chunk 1: Scripts and .gitignore

### Task 1: Create `scripts/spawn-agent.sh`

**Files:**
- Create: `scripts/spawn-agent.sh`

- [ ] **Step 1: Create the script with argument parsing and validation**

```bash
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
```

- [ ] **Step 2: Make it executable**

```bash
chmod +x scripts/spawn-agent.sh
```

- [ ] **Step 3: Verify syntax**

```bash
bash -n scripts/spawn-agent.sh
```

Expected: no output (no syntax errors).

- [ ] **Step 4: Commit**

```bash
git add scripts/spawn-agent.sh
git commit -m "feat: add spawn-agent.sh for per-agent worktree provisioning"
```

### Task 2: Create `scripts/teardown-agent.sh`

**Files:**
- Create: `scripts/teardown-agent.sh`

- [ ] **Step 1: Create the script**

```bash
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
```

- [ ] **Step 2: Make it executable**

```bash
chmod +x scripts/teardown-agent.sh
```

- [ ] **Step 3: Verify syntax**

```bash
bash -n scripts/teardown-agent.sh
```

Expected: no output (no syntax errors).

- [ ] **Step 4: Commit**

```bash
git add scripts/teardown-agent.sh
git commit -m "feat: add teardown-agent.sh for agent workspace cleanup"
```

### Task 3: Update `.gitignore`

**Files:**
- Modify: `.gitignore`

- [ ] **Step 1: Add `.bd-agent-identity` to `.gitignore`**

Append to `.gitignore`:

```
# Agent identity marker (per-worktree, not committed)
.bd-agent-identity
```

- [ ] **Step 2: Verify**

```bash
cat .gitignore
```

Expected: `.bd-agent-identity` appears at the end.

- [ ] **Step 3: Commit**

```bash
git add .gitignore
git commit -m "chore: gitignore .bd-agent-identity (per-worktree marker)"
```

---

## Chunk 2: Workflow doc updates

### Task 4: Update `.workflow/START HERE.md`

**Files:**
- Modify: `.workflow/START HERE.md`

- [ ] **Step 1: Add Step 0 to "How to Start a Session"**

In the "How to Start a Session" section (currently steps 1-5), insert a new **step 0** before the existing step 1:

```markdown
0. **Verify agent identity.** Check that `.bd-agent-identity` exists in the current working directory. If found, read the agent name and verify `git config get user.name` returns the same value. If **not** found, stop and tell the operator: _"This workspace was not created with `spawn-agent.sh`. Run `scripts/spawn-agent.sh <name>` from the main repo, then open that folder."_ Do not proceed without a valid agent identity.
```

- [ ] **Step 2: Update the "Parallel agents" sentence in section "Task Dependencies & Parallel Work"**

Replace the existing sentence:

```
**Parallel agents on one machine:** Use a **git worktree** per agent so checkouts do not collide (see [.workflow/onboarding.md](onboarding.md)).
```

With:

```
**Parallel agents on one machine:** Run `scripts/spawn-agent.sh <name>` from the main repo to create an isolated worktree with a distinct agent identity. Each agent gets its own directory, branch, and `bd` identity. See [.workflow/onboarding.md](onboarding.md).
```

- [ ] **Step 3: Verify changes read correctly**

```bash
head -55 .workflow/START\ HERE.md
```

- [ ] **Step 4: Commit**

```bash
git add ".workflow/START HERE.md"
git commit -m "docs: add Step 0 identity check to START HERE session start"
```

### Task 5: Update `.workflow/onboarding.md`

**Files:**
- Modify: `.workflow/onboarding.md`

- [ ] **Step 1: Replace the "Parallel agents on one machine" section**

Replace the entire section starting at `## Parallel agents on one machine (filesystem isolation)` through the end of the `### Beads with multiple worktrees` subsection (i.e., everything from `## Parallel agents on one machine` to the `---` separator before `*Last updated*`) with:

```markdown
## Parallel agents on one machine (filesystem isolation)

**Problem:** Two AI agents using the **same directory** will fight over the working tree when each checks out a different branch. They also share the same `git user.name`, which makes `bd` claims indistinguishable.

**Fix: `spawn-agent.sh`.** Run it once per agent from the main repo root. It creates a sibling worktree with a distinct agent identity.

```bash
cd ~/code/vuln-bank                                # main repo (base camp)
scripts/spawn-agent.sh cursor-a                    # creates ../vuln-bank-cursor-a
scripts/spawn-agent.sh cursor-b --branch cursor/02-fix  # creates ../vuln-bank-cursor-b
```

Point each agent at its own folder. The main repo is the "base camp" — no agent should work directly in it.

**What the script does:**
1. Creates a git worktree via `bd worktree create` (shares `.beads` database)
2. Sets `git config --worktree user.name <agent-name>` so `bd` commands use a distinct identity
3. Writes `.bd-agent-identity` so agents can verify their workspace at session start

**Teardown:**

```bash
scripts/teardown-agent.sh cursor-a            # removes ../vuln-bank-cursor-a
scripts/teardown-agent.sh cursor-b --force    # force-remove even with uncommitted changes
```

**Listing active workspaces:**

```bash
git worktree list
```

### Beads with multiple worktrees

All worktrees share the same Beads database (the spawn script sets up the `.beads` redirect). Run `bd ready`, `bd update <id> --claim`, and `bd close` from **any** worktree — claims are globally visible because the database is shared.

Each worktree has a distinct `git user.name`, so `bd` records a different assignee per agent. This prevents the cross-claim confusion that occurs when all agents share one identity.
```

- [ ] **Step 2: Verify the file reads correctly**

```bash
tail -40 .workflow/onboarding.md
```

- [ ] **Step 3: Commit**

```bash
git add .workflow/onboarding.md
git commit -m "docs: replace manual worktree instructions with spawn-agent.sh"
```

### Task 6: Update `.workflow/beads-coordination.md`

**Files:**
- Modify: `.workflow/beads-coordination.md`

- [ ] **Step 1: Update "Parallel agents and directories" subsection**

Replace the `### Parallel agents and directories (B)` subsection (the heading and its two paragraphs) with:

```markdown
### Parallel agents and directories

Two agents in the **same directory** overwrite each other's checkouts and share the same `git user.name`, making `bd` claims indistinguishable. **Use `scripts/spawn-agent.sh`** to create an isolated worktree per agent (see [.workflow/onboarding.md](onboarding.md)).

Each agent's worktree has a distinct `git config --worktree user.name`, so `bd` automatically uses the correct identity for claims, updates, and closes. No `BD_ACTOR` env var is needed.
```

- [ ] **Step 2: Update "Multi-Agent Claiming" subsection**

Replace the existing `### Multi-Agent Claiming` subsection (the heading and its paragraph) with:

```markdown
### Multi-Agent Claiming

`bd update <id> --claim` is atomic. The claim records the agent's `git user.name` as the assignee. When agents have distinct identities (set by `spawn-agent.sh`), a second agent's claim on the same task will fail because the assignee doesn't match.

If a claim fails, the agent must pick another task — never proceed with implementation. Re-run `bd ready --unassigned` after a failed claim.

**Defensive check:** After claiming, verify the assignee matches your identity:

```bash
bd show <id> --json | jq -r '.assignee'
# Should match: git config get user.name
```
```

- [ ] **Step 3: Commit**

```bash
git add .workflow/beads-coordination.md
git commit -m "docs: update beads coordination with agent identity isolation"
```

### Task 7: Update `.cursorrules`

**Files:**
- Modify: `.cursorrules`

- [ ] **Step 1: Add Step 0 as the first item in Quick Start**

Insert the following as a new paragraph **immediately before** the line `1. Read .workflow/START HERE.md for session rules and task workflow` (i.e., at the top of the Quick Start numbered list):

```markdown
**Step 0 — Verify identity (before anything else):** Check that `.bd-agent-identity` exists in the current working directory. Read the agent name from it and confirm `git config get user.name` matches. If the file is missing, tell your operator: _"This workspace was not created with `spawn-agent.sh`. Run it from the main repo root, then open the new folder."_ Do not proceed without a valid identity.

```

- [ ] **Step 2: Commit**

```bash
git add .cursorrules
git commit -m "docs: add identity verification to .cursorrules Quick Start"
```

### Task 8: Update `CLAUDE.md`

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Add Step 0 as the first item in Quick Start**

Insert the following as a new paragraph **immediately before** the line `1. Read `.workflow/START HERE.md` for session rules and task workflow` (i.e., at the top of the Quick Start numbered list):

```markdown
**Step 0 — Verify identity (before anything else):** Check that `.bd-agent-identity` exists in the current working directory. Read the agent name from it and confirm `git config get user.name` matches. If the file is missing, tell your operator: _"This workspace was not created with `spawn-agent.sh`. Run it from the main repo root, then open the new folder."_ Do not proceed without a valid identity.

```

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: add identity verification to CLAUDE.md Quick Start"
```

### Task 9: Update `AGENTS.md`

**Files:**
- Modify: `AGENTS.md`

- [ ] **Step 1: Add "Agent Identity" section after the "Quick Reference" section**

After the Quick Reference code block (after the closing ` ``` ` around line 12), add:

```markdown

## Agent Identity (Parallel Agents)

When running multiple agents on the same machine, each agent **must** work in its own worktree with a distinct identity. The operator provisions these before starting agents:

```bash
# From the main repo root:
scripts/spawn-agent.sh cursor-a            # creates ../vuln-bank-cursor-a
scripts/spawn-agent.sh claude-1            # creates ../vuln-bank-claude-1

# When done:
scripts/teardown-agent.sh cursor-a
```

Each agent's worktree has `git config --worktree user.name` set to the agent name. Since `bd` falls back to `git user.name`, all `bd` commands automatically use the correct identity. No `BD_ACTOR` env var needed.

**Session start check:** Every agent must verify `.bd-agent-identity` exists in its working directory before doing any work. If missing, tell the operator to run `spawn-agent.sh`.
```

- [ ] **Step 2: Update the "Workflow for AI Agents" section**

In the existing workflow list (around line 90), update step 1 from:

```
1. **Check ready work**: `bd ready` shows unblocked issues
```

To:

```
1. **Verify identity**: Confirm `.bd-agent-identity` exists and `git config get user.name` matches
2. **Check ready work**: `bd ready` shows unblocked issues
```

And renumber subsequent steps (2→3, 3→4, etc.).

- [ ] **Step 3: Commit**

```bash
git add AGENTS.md
git commit -m "docs: add agent identity section and update workflow in AGENTS.md"
```

### Task 10: Update `.workflow/Tips & Lessons.md`

**Files:**
- Modify: `.workflow/Tips & Lessons.md`

- [ ] **Step 1: Add entry to "Multi-Model Coordination" section**

After the existing entries in the `## Multi-Model Coordination` section, add:

```markdown
- **Agent identity must be unique per agent.** `[Hrdayesh]` When two agents share the same `git user.name`, `bd update --claim` can't distinguish them — both see the same assignee and assume the claim is theirs. Fix: `scripts/spawn-agent.sh` creates per-agent worktrees with distinct `git config --worktree user.name`. Same fix prevents filesystem collisions (shared worktree confusion).
```

- [ ] **Step 2: Move from "Friction Points (Unresolved)" if this was logged there**

If the Friction Points section has any entry about agent identity or claim confusion, move it to the resolved Multi-Model Coordination section. If Friction Points is empty (`_(none currently)_`), leave it as-is.

- [ ] **Step 3: Commit**

```bash
git add ".workflow/Tips & Lessons.md"
git commit -m "docs: add agent identity collision lesson to Tips & Lessons"
```
