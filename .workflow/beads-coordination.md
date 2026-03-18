# Beads Coordination Guide

**Beads (`bd`) is the local, git-backed task graph for this project.** It gives agents and humans a dependency-aware issue tracker with hash-based IDs (no merge collisions), JSON output for tooling, and optional sync with Jira (see `.workflow/jira-coordination.md` for Jira-only usage).

> **Why Beads?** Tasks are stored in a Dolt database under `.beads/` with first-class dependency support. Use `bd ready` to see work that has no open blockers. Beads can run in stealth mode (local only, not committed) or team mode (shared in repo).

---

## How It Works

### Beads Is the Local Task Layer

- **Storage:** Dolt database in `.beads/` (or shared server at `~/.beads/shared-server/`).
- **Issue IDs:** Hash-based (e.g. `bd-a1b2`) so multiple agents/branches don’t collide.
- **Dependencies:** `blocks` / `blocked-by`; `bd ready` lists open issues with no active blockers.
- **Types:** task, bug, feature, epic, chore, decision (and custom via config).

### Beads + Jira (this project)

This project uses Beads as the primary backlog with one-way sync to Jira for reporting and visibility.

- **From Jira:** Agents read epics/stories/Gherkin from Jira and create implementation tasks in Beads with `--external-ref jira-PROJ-<story-id>`.
- **Ad-hoc tasks:** Created during implementation go in the same epic as the story you're working on; standalone ad-hoc tasks go in the configured ad-hoc epic.
- **Sync (Beads → Jira):** One-way only. All synced work appears as **standalone Jira issues** (no sub-tasks): same epic as the story + issue link to the story, or ad-hoc epic.

Full design: [Beads + Jira dual-tracker design](../docs/specs/2026-03-13-beads-jira-dual-tracker-design.md).

### Modes

| Mode | Use case |
|------|----------|
| **Default** | Team: `.beads/` in repo, everyone uses same DB. |
| **`bd init --stealth`** | Personal: beads data excluded from git (`.git/info/exclude`), invisible to collaborators. |
| **`bd init --contributor`** | OSS contributor: planning issues in a separate location (e.g. `~/.beads-planning`). |

---

## Setup

### First-Time Init (this repo)

```bash
# Team workflow (beads in repo)
bd init

# Or personal / invisible to others
bd init --stealth
```

Beads requires a running Dolt server (default port 3307 or 3306). If you use a shared server or different host/port, set `--server-host`, `--server-port`, and `BEADS_DOLT_PASSWORD` as needed.

### Tell Agents

After init, add to `AGENTS.md` (or equivalent):

```
Use 'bd' for task tracking. See .workflow/beads-coordination.md.
```

---

## Workflow

### Claim before branch or edits (mandatory)

**Order for every implementation session:** (1) `bd ready --unassigned` (or equivalent) → (2) pick **one** task ID → (3) `bd update <id> --claim` → (4) **only if claim succeeds**, create your git feature branch and edit files.

If claim fails, another agent holds that task—pick a different ID from `bd ready --unassigned`. **Do not** create a branch or modify the repo for a Beads task until your claim succeeds. Skipping this step causes duplicate work when multiple agents run in parallel.

### Starting a Session

1. See ready unclaimed work: `bd ready --unassigned` (add `-n 5` to cap the list). For JSON: `bd ready --unassigned --json`
2. Optionally also run `bd ready` to see your own in-progress items.

### Claiming a Task

```bash
# Atomically claim: sets assignee to you and status to in_progress
bd update <id> --claim
```

Fails if the issue is already claimed. Use `BD_ACTOR` or `--actor` to set the assignee name (defaults to `git user.name` or `$USER`). **Claim must succeed before any git branch or file changes for that task.**

### Creating a Task

```bash
# Minimal
bd create "Title of the task"

# With description, priority, type
bd create "Add login rate limit" -d "Limit to 5 attempts per minute." -p 1 -t feature

# With acceptance criteria and parent (epic)
bd create "Implement rate limit middleware" --acceptance "Returns 429 when exceeded" --parent bd-a3f8
```

Use `--external-ref jira-PROJ-123` to link to a Jira issue. Use `--silent` to output only the new issue ID for scripting.

### Adding Dependencies

```bash
# bd-abc is blocked by bd-xyz (bd-xyz must be done first)
bd dep add bd-abc bd-xyz

# Or shorthand: “this blocks that”
bd dep bd-xyz --blocks bd-abc
```

Dependency types (optional `-t`): blocks, tracks, related, parent-child, discovered-from, until, caused-by, validates, relates-to, supersedes.

### Completing a Task

```bash
bd update <id> --status closed
```

Or use `bd close <id>`.

### Viewing Details

```bash
bd show <id>
bd show <id> --long    # Extended metadata
bd show --current      # Last touched / in-progress issue
```

---

## Commands Quick Reference

| Action | Command |
|--------|---------|
| List ready work | `bd ready` |
| List with filters | `bd list --status open`, `bd list -t feature`, `bd list --assignee @me` |
| Create issue | `bd create "Title"` (+ `-d`, `-p`, `-t`, `--parent`, `--acceptance`) |
| Claim | `bd update <id> --claim` |
| Update fields | `bd update <id> --title "..."`, `--status`, `--assignee`, etc. |
| Add dependency | `bd dep add <blocked> <blocker>` or `bd dep <blocker> --blocks <blocked>` |
| Show issue | `bd show <id>` |
| Close | `bd close <id>` or `bd update <id> --status closed` |
| JSON output | Append `--json` to any command |

---

## Dependency and Hierarchy

- **Parent/child:** Use `--parent <id>` on `bd create` for sub-tasks under an epic.
- **Blocking:** `bd dep add <blocked-id> <blocker-id>` — blocker must be done before blocked appears in `bd ready`.
- **List blockers:** `bd dep list <id>` (or see `bd show <id>`).
- **Dependency tree:** `bd dep tree <id>`.

---

## Solving Hard Problems

### Parallel agents and directories

Two agents in the **same directory** overwrite each other's checkouts and share the same `git user.name`, making `bd` claims indistinguishable. **Use `scripts/spawn-agent.sh`** to create an isolated worktree per agent (see [.workflow/onboarding.md](onboarding.md)).

Each agent's worktree has a distinct `git config --worktree user.name`, so `bd` automatically uses the correct identity for claims, updates, and closes. No `BD_ACTOR` env var is needed.

### Multi-Agent Claiming

`bd update <id> --claim` is atomic. The claim records the agent's `git user.name` as the assignee. When agents have distinct identities (set by `spawn-agent.sh`), a second agent's claim on the same task will fail because the assignee doesn't match.

If a claim fails, the agent must pick another task — never proceed with implementation. Re-run `bd ready --unassigned` after a failed claim.

**Defensive check:** After claiming, verify the assignee matches your identity:

```bash
bd show <id> --json | jq -r '.assignee'
# Should match: git config get user.name
```

### Staleness

Use `bd stale` to see issues not updated recently. If something has been in progress too long, operators can reassign or unclaim (e.g. clear assignee and set status back to open) and document in a comment or external process.

### JSON for Agents

Use `--json` on any command for machine-readable output. Example:

```bash
bd ready --json -n 5
bd show bd-a1b2 --json
```

### Stealth vs Team

- **Stealth:** Your beads data is not committed; no conflict with other people’s tasks. Good for personal backlogs or experiments.
- **Team:** Beads DB is in the repo (or on a shared Dolt server); everyone sees the same graph. Use for shared coordination; avoid editing the same issue from two branches without syncing.

---

## Jira Sync (Optional)

Beads can sync with Jira via `bd jira`. Configuration and sync behavior are documented in the Beads docs; this guide focuses on local `bd` usage. For Jira-only workflows (acli, MCP, etc.), see `.workflow/jira-coordination.md`.

---

*Last updated: March 2026 — based on `bd` and acli installed locally*
