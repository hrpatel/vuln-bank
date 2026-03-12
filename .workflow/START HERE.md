# START HERE

**Read this file first. Every session. No exceptions.**

---

## The Rules

1. **Work quietly.** Don't narrate intermediate steps. Surface results, blockers, and decisions only.
2. **Humans merge.** AI models never merge PRs. They create them, review them, flag them as ready.
3. **Tasks are sequential unless marked parallel-safe.** Parallel tasks touching the same files can revert each other.
4. **Ask before acting on anything destructive or ambiguous.** When in doubt, ask.
5. **Check for conflicts before starting.** Check GitHub Issues labeled `in-progress` and verify no task from the other model touches your files.
6. **Claim your work.** Assign yourself and label the issue when you start. Create a PR when you finish; the issue stays open until the PR is merged (human or automation closes it then).

## Before You Build

When approaching any implementation task, don't default to the obvious solution. Before writing code, ask:

- Is there a better pattern for this? Research best-in-class approaches for the problem type.
- Are there established libraries or utilities already in the stack that handle this well?
- What do leading products do for this same problem?
- Is there a simpler solution that achieves the same outcome with less code?

A few minutes of research before implementing saves multiple iteration cycles after.

## How to Start a Session

1. Read your entry point — `CLAUDE.md` for CLI agents (e.g. Claude Code), `.cursorrules` for Cursor — it brought you here.
2. Check `STATUS.md` for current project state.
3. **Check GitHub Issues** for available work: `gh issue list --repo hrpatel/vuln-bank --label available`. If there are available issues, pick one that doesn't conflict with any `in-progress` work.
4. If no issues are available, ask your operator what to work on.
5. For the full coordination guide, see `.workflow/github-issues-coordination.md`.

## Task Workflow

- **Tasks are GitHub Issues.** The issue body contains the spec, files to edit, and acceptance criteria.
- Labels and assignments provide real-time status visible from any branch.
- When you finish a task, create or update the PR and leave a completion comment; do not close the issue. The issue is closed when the PR is merged (by human or automation); downstream issues are unblocked at that time.
- Update `STATUS.md`, `decisions.md`, and `metrics.md` as part of completing any task that warrants it.

## Task Dependencies & Parallel Work

GitHub Issues support native dependency tracking:
- **Sub-issues:** Group related tasks under a parent issue. The parent shows automatic progress roll-up.
- **Dependencies:** Link issues with "blocked by" relationships. Check `.workflow/github-issues-coordination.md` for the API commands.
- **Files to edit:** Always list files in the issue body — this enables conflict detection between models.

**How to assess parallel safety:** Two tasks conflict if they modify the same file. Check the "Files to edit" section of all `in-progress` issues before starting yours.

## Creating New Tasks

1. **Create a GitHub Issue.** Include a clear title, spec, acceptance criteria, and "Files to edit" section in the body.
2. **Label it.** Use `available` if it's ready to start, or `blocked` if it has unresolved dependencies.
3. **Link dependencies.** If the task depends on another issue, add a "blocked by" link via the API.
4. **Link to parent.** If it's part of a chain, add it as a sub-issue of the parent.

## Task Completion Checklist

1. **Rebase on main before closing** — when closing a session: fetch and rebase (`git fetch origin main && git rebase origin/main`), resolve any conflicts, then commit and push; use `git push --force-with-lease origin <branch>` if the branch was already pushed. Verify the PR shows no conflicts.
2. **PR created or updated** — open or update the PR; do **not** close the GitHub Issue. The issue is closed when the PR is merged (by human or automation).
3. **Downstream unblocked** — when the PR is merged and the issue is closed, whoever merges flips any newly-unblocked issues from `blocked` to `available` (or document in the PR comment which issues to unblock).
4. **Completion comment** — leave a comment on the issue noting the PR number and that it is ready for review/merge.
5. **Metrics updated** — on session close, update `metrics.md` (session row, PR/commits, and code volume if applicable).
6. **Decisions updated** — if a significant decision was made, update `decisions.md`.
7. **STATUS.md updated** — reflect the current project state.

## Session Close-Out

When your operator says "close this session" (or equivalent), follow these steps:

1. **Finish or pause current work** — commit, push, and create/update PRs for any in-progress tasks.
2. **Update your metrics file** — add a session row to your model's file:
   - Claude Code → `metrics-claude.md`
   - Cursor → `metrics-cursor.md`
   - Include: session number, date, duration, PRs, decisions, focus area, phase, driver, operator, work category, bugs fixed.
   - Add code volume and PR activity rows as applicable.
3. **Update `decisions.md`** — if any significant decisions were made this session.
4. **Update `STATUS.md`** — reflect the current project state.
5. **Release claimed issues** — any `in-progress` issues you didn't finish should be relabeled `available` so the other model can pick them up.
6. **Commit and PR** — push your metrics/docs update as part of your final PR, or as a separate close-out PR.

> **Do not edit `metrics.md` directly.** Each model writes to its own file. Claude Code is the merger — it combines both files into `metrics.md` (master) and syncs to Meta Tracker.

### Metrics Merge (Claude Code only)

At session start or close-out, Claude Code checks for unsynced data:
1. Pull latest `metrics-cursor.md` — if Cursor added sessions since last merge, incorporate them.
2. Pull latest `metrics-claude.md` — include own session data.
3. Merge both into `metrics.md` (the master file).
4. Push updated data to Meta Tracker (`vulnBankMetrics.ts` + `vulnBankProject.ts`).

This can happen at any natural breakpoint — no need to wait for the other model.

## Review Cadence

**After every 2-3 merges**, do a quick review pass:

1. **Build check** — verify the application runs correctly.
2. **Data integrity** — check for mismatched references or broken functionality.
3. **Bug logging** — any issues found get logged in `metrics.md`.
4. **Flag for review** — note anything for the human operators to check.

## Key References

| Doc | Location | When to Read |
|-----|----------|-------------|
| **STATUS.md** | Repo root | Every session |
| **How We Work** | `.workflow/` | When you need process details |
| **Tips & Lessons** | `.workflow/` | When you hit a technical snag |
| **decisions.md** | Repo root | When you need project history; log decisions using the structured format |
| **metrics.md** | Repo root | When updating tracking data; log sessions using the field definitions |
| **GitHub Issues** | `gh issue list --repo hrpatel/vuln-bank` | Before starting any work |
| **Coordination Guide** | `.workflow/github-issues-coordination.md` | API reference for Issues workflow |

---

*Adapt these guidelines to your workflow. Last updated: March 10, 2026.*
