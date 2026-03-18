# How We Work — Multi-Model Collaboration

## Team Structure

### Human Operators
- **Operator A** — uses Claude Code (CLI)
- **Operator B** — uses Cursor

Both operators:
- Assign tasks to their respective AI models
- Review and merge PRs (AI models never merge)
- Make product and priority decisions
- Coordinate via their own communication channels

### AI Models
- **Claude Code** — works via CLI, creates branches and PRs
- **Cursor** — works via IDE, creates branches and PRs

Both models:
- Read the workflow docs at session start
- Check for conflicts before starting work
- Claim tasks via the issue tracker set in `.workflow/issue-tracker.md` before working on them
- Create PRs for all code changes
- Work only on a feature branch; push only that branch. Never merge, never push directly to main

## Coordination Protocol

### Issue Tracker Is Set Once per Project

The project’s issue tracker is chosen at setup and recorded in **`.workflow/issue-tracker.md`**. All agents and operators use that same tracker so coordination is consistent. Read that file, then follow the **coordination guide** it links to (GitHub, Jira, or Beads) for how to find work, claim tasks, and avoid conflicts.

One-time setup (e.g. when creating or changing the choice) is in `.workflow/bootstrap.md`.

### Before Starting a Task

1. Read `.workflow/issue-tracker.md` to see which tracker this project uses.
2. Open the coordination guide linked there.
3. Use that guide to find available work and check for in-progress work from the other model (and its "Files to edit"). **Beads:** `bd update <id> --claim` must **succeed** before any branch or file edits for that task.
4. Create or switch to a feature branch (see Branch Naming) only **after** a successful claim.

### Branch Naming

Use a consistent pattern so it's clear who's working on what:
- Claude Code: `claude/{##}-{task-slug}`
- Cursor: `cursor/{##}-{task-slug}`

Example: `claude/03-add-xss-scenario`, `cursor/04-update-auth-tests`

### Parallel agents on one machine

Each agent should use its **own git worktree or clone** (see [.workflow/onboarding.md](onboarding.md)). Two agents in one directory will corrupt each other’s checkouts. Beads claims should run against **one** shared Beads database (primary clone or shared Dolt).

### Handling Conflicts

If both models accidentally start tasks that touch the same files:
1. The model that started **second** (later claiming timestamp on the issue) yields
2. That model stashes or shelves its work
3. Wait for the first model's PR to merge
4. Rebase and continue

If a merge conflict arises in a PR, the model that created the PR resolves it.

## Workflow

1. Operator describes what they want
2. AI model asks clarifying questions if needed
3. AI model checks the issue tracker (see `.workflow/issue-tracker.md`) for conflicts
4. AI model creates a task (if one doesn't exist) and **successfully** claims it per the coordination guide (Beads: `bd update <id> --claim` before any branch or edits)
5. AI model works on a feature branch (only after claim succeeds)
6. AI model creates a PR
7. **Human merges** the PR
8. When the PR is merged, the tracker issue is closed or completed per the coordination guide. The person who merges unblocks downstream work and updates STATUS.md / tracking docs as needed.

## Communication Style

### Keep It Quiet
- **DO:** Report outcomes ("PR created, ready to merge")
- **DO:** Surface blockers and decisions that need input
- **DON'T:** Narrate intermediate steps
- **DON'T:** Describe what you're about to do before doing it

## Code Review

### Every PR Gets Reviewed Before Merge
The creating model should review its own diff before flagging the PR as ready. Check for:
- No unintended file changes
- No hardcoded secrets or credentials
- Existing functionality isn't broken
- Changes match the task description

### Review Priority

| Change Type | Review Level |
|-------------|-------------|
| Config, docs, templates | Quick scan — low risk |
| Single-file changes | Read the diff — medium risk |
| Multi-file features | Careful review — higher risk |
| Security-related changes | Extra scrutiny — this is a security project |

## Decision Tracking

Every significant decision gets logged in `decisions.md`. This creates a record of how the project evolved, useful for both models and both operators.

## Metrics & Session Tracking

### Split Metrics Files

To avoid merge conflicts on shared metrics, each model writes to its own file in `.metrics/`:

| File | Owner | Purpose |
|------|-------|---------|
| `.metrics/metrics-claude.md` | Claude Code | Claude Code's session logs |
| `.metrics/metrics-cursor.md` | Cursor | Cursor's session logs |
| `.metrics/metrics.md` | Claude Code (merger) | Merged master — do not edit directly |

Both per-model files use identical fields that match the Meta Tracker data model. This ensures reliable sync to the dashboard.

**Before every push,** update your model's file and include that update in the commit you push.

### Who Merges

**Claude Code is always the merger.** It combines both model files into `.metrics/metrics.md` and pushes to Meta Tracker. This happens opportunistically — at session start if there's unsynced Cursor data, or at session close-out.

Neither model should edit `.metrics/metrics.md` directly. If you need to correct a past entry, edit it in your own metrics file and let the merge process update the master.

## Workflow Doc Changes

Changes to `.cursorrules`, `CLAUDE.md`, or any file in `.workflow/` are **always single-model, serialized operations**. Never run two tasks that modify workflow docs in parallel. These files are read by both models at session start — concurrent edits create unpredictable behavior and guaranteed merge conflicts.

If your task needs to update workflow docs and another model has an `in-progress` issue that also touches workflow docs, wait for theirs to merge first.

## Iteration Patterns

1. **Small, targeted PRs** — one concern per PR
2. **Branch isolation** — each model on its own branch
3. **Task ownership** — claimed via the issue tracker (per the coordination guide), no ambiguity
4. **File-level conflict detection** — "Files to edit" in issue bodies is the mechanism
5. **Sequential within chains, parallel across chains** — dependency chains are respected; independent tasks run simultaneously
6. **Research before building** — don't default to the first approach; find the best one

---

*Last updated: March 9, 2026*
