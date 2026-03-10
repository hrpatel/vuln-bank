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
- Claim tasks in the index before working on them
- Create PRs for all code changes
- Never merge, never push directly to main

## Coordination Protocol

### GitHub Issues Are the Source of Truth

**GitHub Issues** are the real-time coordination layer. Labels, assignments, and comments are visible to both models from any branch — no merge required. See `.workflow/github-issues-coordination.md` for the full API reference and workflow details.

| Label | Meaning |
|-------|---------|
| `available` | Ready for either model to pick up |
| `in-progress` | Claimed and being worked on |
| `blocked` | Has unresolved dependencies |
| `claude-code` | Owned by Claude Code |
| `cursor` | Owned by Cursor |

> **Historical note:** `tasks/index.md` was the original coordination mechanism but had a visibility gap — both models edited it on branches, so neither could see the other's claims. Issues solve this by being branch-independent.

### Before Starting a Task

1. Check GitHub Issues: `gh issue list --repo hrpatel/vuln-bank`
2. Find an issue labeled `available` (or create one if your operator gives you new work)
3. Check its "Files to edit" against all `in-progress` issues from the other model
4. If there's a file overlap → pick a different issue or wait
5. If no overlap → claim the issue (assign + relabel in one PATCH call), then start working

### Branch Naming

Use a consistent pattern so it's clear who's working on what:
- Claude Code: `claude/{##}-{task-slug}`
- Cursor: `cursor/{##}-{task-slug}`

Example: `claude/03-add-xss-scenario`, `cursor/04-update-auth-tests`

### Handling Conflicts

If both models accidentally start tasks that touch the same files:
1. The model that started **second** (later timestamp in the index) yields
2. That model stashes or shelves its work
3. Wait for the first model's PR to merge
4. Rebase and continue

If a merge conflict arises in a PR, the model that created the PR resolves it.

## Workflow

1. Operator describes what they want
2. AI model asks clarifying questions if needed
3. AI model checks GitHub Issues for conflicts
4. AI model creates an issue (if one doesn't exist) and claims it (assign + label)
5. AI model works on a feature branch
6. AI model creates a PR
7. **Human merges** the PR
8. When the PR is merged, the issue is closed (by automation if the PR body has "Fixes #N", or manually). The person who merges unblocks downstream issues and updates STATUS.md / tracking docs as needed.

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

To avoid merge conflicts on shared metrics, each model writes to its own file:

| File | Owner | Purpose |
|------|-------|---------|
| `metrics-claude.md` | Claude Code | Claude Code's session logs |
| `metrics-cursor.md` | Cursor | Cursor's session logs |
| `metrics.md` | Claude Code (merger) | Merged master — do not edit directly |

Both per-model files use identical fields that match the Meta Tracker data model. This ensures reliable sync to the dashboard.

### Who Merges

**Claude Code is always the merger.** It combines both model files into `metrics.md` and pushes to Meta Tracker. This happens opportunistically — at session start if there's unsynced Cursor data, or at session close-out.

Neither model should edit `metrics.md` directly. If you need to correct a past entry, edit it in your own metrics file and let the merge process update the master.

## Workflow Doc Changes

Changes to `.cursorrules`, `CLAUDE.md`, or any file in `.workflow/` are **always single-model, serialized operations**. Never run two tasks that modify workflow docs in parallel. These files are read by both models at session start — concurrent edits create unpredictable behavior and guaranteed merge conflicts.

If your task needs to update workflow docs and another model has an `in-progress` issue that also touches workflow docs, wait for theirs to merge first.

## Iteration Patterns

1. **Small, targeted PRs** — one concern per PR
2. **Branch isolation** — each model on its own branch
3. **Task ownership** — claimed via GitHub Issue assignment, no ambiguity
4. **File-level conflict detection** — "Files to edit" in issue bodies is the mechanism
5. **Sequential within chains, parallel across chains** — dependency chains are respected; independent tasks run simultaneously
6. **Research before building** — don't default to the first approach; find the best one

---

*Last updated: March 9, 2026*
