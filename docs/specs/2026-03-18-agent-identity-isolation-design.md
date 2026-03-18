# Agent Identity & Filesystem Isolation Design

**Date:** 2026-03-18
**Status:** Draft
**Author:** Cursor (brainstorming session with Hrdayesh)

---

## Problem

When multiple AI agents run on the same machine against the same repository, two critical coordination failures occur:

1. **Identity collision:** All agents resolve to the same `BD_ACTOR` (defaults to `git user.name`). When Agent A claims a beads task, Agent B sees the same assignee name and interprets it as *its own* successful claim. Both agents proceed to implement the same task.

2. **Filesystem collision:** Workflow docs instruct agents to use git worktrees, but nothing enforces it. When Agent A creates a worktree, Agent B (sharing the same working directory) discovers it and assumes it's its own. Both agents work in the same worktree, causing checkout conflicts and overwritten changes.

**Root cause:** No per-agent identity mechanism. All agents on a machine look identical to `bd` and to each other.

## Constraints

- Editor-agnostic: must work for Cursor, Claude Code, Aider, or any agent
- Scales to arbitrary N agents
- Uses existing `bd worktree` infrastructure (no changes to `bd` itself)
- Supports both agent self-registration and operator provisioning

## Design

### 1. Spawn Script (`scripts/spawn-agent.sh`)

Creates an isolated agent workspace. Can be run by an operator (with an explicit name) or by an agent at session start (with `--auto` to generate a unique name).

**Usage:**

```bash
scripts/spawn-agent.sh <agent-name> [--branch <branch-name>]
scripts/spawn-agent.sh --auto [--branch <branch-name>]

# Operator-provisioned
scripts/spawn-agent.sh cursor-a
scripts/spawn-agent.sh cursor-b --branch cursor/02-xss-fix

# Agent self-registration
scripts/spawn-agent.sh --auto
```

**Steps performed:**

1. If `--auto` is passed, generate a unique name: `agent-<8-hex-chars>` (from `/dev/urandom`). Otherwise validate the provided agent name (alphanumeric + hyphens, no spaces, not empty)
2. Verify current directory is the main repo root: a git repo with `.beads/` present and no `.bd-agent-identity` (prevents spawning from inside another agent's worktree)
3. Determine worktree path: `../<repo-basename>-<agent-name>` (sibling directory)
4. Fail if worktree path already exists (no silent overwrites)
5. If `--branch` is omitted, default to `<agent-name>/work` (e.g., `cursor-a/work`)
6. Run `bd worktree create <path> --branch <branch>` — creates worktree with `.beads` redirect so all agents share one beads database
7. Enable `extensions.worktreeConfig` in the repo at local scope (idempotent: `git config set extensions.worktreeConfig true` — defaults to `--local`, which writes to the repo's `.git/config`)
8. Set per-worktree git identity: `git config --worktree set user.name <agent-name>` (run inside the new worktree). Since `bd` falls back to `git user.name` when `BD_ACTOR` is unset, this transparently gives each agent a distinct identity for all `bd` commands — no env vars or wrappers needed, works across subprocess boundaries.
9. Write `.bd-agent-identity` into the worktree root (contains agent name, one line) — used by the session start guard to verify the workspace was properly provisioned
10. Print summary: worktree path, agent identity, instruction to open in editor. Also print `git worktree list` output so the operator can see all active agent workspaces

### 2. Teardown Script (`scripts/teardown-agent.sh`)

Cleans up when an agent session is done. Must be run from the main repo root (same as spawn).

**Usage:**

```bash
scripts/teardown-agent.sh <agent-name> [--force]
```

**Steps performed:**

1. Validate agent name is not empty
2. Verify current directory is the main repo root (same check as spawn)
3. Determine worktree path: `../<repo-basename>-<agent-name>`
4. Fail if worktree directory does not exist
5. Check for uncommitted changes in the worktree; fail unless `--force` is passed
6. Remove `.bd-agent-identity` from the worktree
7. Run `bd worktree remove <path>`

### 3. Identity Enforcement (Session Start Guard)

All workflow entry points (`.cursorrules`, `CLAUDE.md`, `AGENTS.md`, `START HERE.md`) get a new **Step 0** at the top of the session-start checklist:

> **Step 0: Verify or create agent identity.** Check that `.bd-agent-identity` exists in the current working directory. If found, read the agent name from it and verify that `git config get user.name` returns the same value. If `.bd-agent-identity` is **not** found, self-register: run `scripts/spawn-agent.sh --auto` from the repo root, then use the new worktree path as the working directory for all subsequent commands.

**Why this works without env vars:** The spawn script sets `git config --worktree user.name <agent-name>` in each worktree. Since `bd` resolves actor identity as `--actor` flag > `BD_ACTOR` env > `git user.name` > `$USER`, and `git user.name` is now per-worktree, every `bd` command automatically uses the correct identity. No wrappers, no PATH manipulation — it works transparently across subprocess boundaries because git config is file-based.

The main repo checkout intentionally does not have `.bd-agent-identity`. It is the "base camp" — agents self-register from it but then work in their worktree. Operators can also pre-provision named workspaces with `scripts/spawn-agent.sh <name>`.

### 4. Claim Isolation

With distinct actor identities per worktree (via `git config --worktree user.name`), beads' existing atomic claim logic handles the rest:

1. Agent `cursor-a` runs `bd update bd-xyz --claim`. Beads records assignee = `cursor-a`.
2. Agent `cursor-b` runs `bd update bd-xyz --claim`. Beads sees assignee = `cursor-a`, which is not `cursor-b`. Claim fails.
3. Agent `cursor-b` picks another task.

No changes to `bd` are needed. The fix is entirely in giving agents distinct identities.

**Defensive check:** After claiming, agents should verify: `bd show <id> --json` and confirm `assignee` matches the agent name from `.bd-agent-identity` (or equivalently, `git config get user.name`).

### 5. Files Changed

| File | Change |
|------|--------|
| `scripts/spawn-agent.sh` | New: agent workspace provisioning script |
| `scripts/teardown-agent.sh` | New: agent workspace cleanup script |
| `.cursorrules` | Add Step 0 (verify `.bd-agent-identity`) |
| `CLAUDE.md` | Add Step 0 (verify `.bd-agent-identity`) |
| `AGENTS.md` | Add "Agent Identity" section; update "Workflow for AI Agents" |
| `.workflow/START HERE.md` | Add Step 0 to session start; update parallel agents section |
| `.workflow/onboarding.md` | Replace manual worktree instructions with `spawn-agent.sh` |
| `.workflow/beads-coordination.md` | Update parallel agents and claiming sections |
| `.workflow/Tips & Lessons.md` | Add identity collision lesson learned |
| `.gitignore` | Add `.bd-agent-identity` |

### 6. What Does NOT Change

- `bd` tool itself — no modifications
- Application code — purely workflow infrastructure
- `STATUS.md` — updated at task completion, not in design

## Error Handling

**`spawn-agent.sh` fails fast if:**
- Agent name is empty or contains invalid characters
- Current directory is not the main repo root (not a git repo, `.beads/` missing, or `.bd-agent-identity` present — indicating this is already an agent worktree)
- Worktree directory already exists at the target path
- `bd worktree create` exits non-zero
- `git config --worktree set user.name` fails

**`teardown-agent.sh` fails fast if:**
- Agent name is empty
- Current directory is not the main repo root
- Worktree directory does not exist
- Worktree has uncommitted changes (overridable with `--force`)
- `bd worktree remove` exits non-zero

## Testing

- Spawn two agents (`agent-a`, `agent-b`), verify distinct worktree paths, distinct `.bd-agent-identity` contents, and distinct `git config get user.name` values per worktree
- From `agent-a` worktree, verify identity resolution: `git config get user.name` should return `agent-a`, and claiming a test task should record assignee = `agent-a`
- From `agent-a` worktree, claim a task; from `agent-b` worktree, attempt to claim the same task — verify failure
- Start an agent session in the main repo (no `.bd-agent-identity`) — verify the agent refuses to proceed
- Teardown one agent while the other continues working — verify no impact
- Spawn an agent with a name that already exists — verify failure with clear message
- Attempt to spawn from inside an existing agent worktree — verify failure with clear message
- Verify main repo `git config get user.name` is unchanged after spawn (identity is worktree-scoped)

## Alternatives Considered

**Operator-only provisioning (original v1):** Agents could not self-register; the operator had to run `spawn-agent.sh` before each agent session. Revised because agents can safely self-register — each creates a differently-named worktree, so there is no filesystem race. The `--auto` flag was added to support this.

**Pre-provisioned slots:** One-time setup creates N permanent worktree directories. Rejected because the fixed slot count adds friction and wastes disk space for unused slots.
