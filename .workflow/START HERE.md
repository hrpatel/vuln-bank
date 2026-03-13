# START HERE

**Read this file first. Every session. No exceptions.**

---

## The Rules

1. **Work quietly.** Don't narrate intermediate steps. Surface results, blockers, and decisions only.
2. **Humans merge.** AI models never merge PRs. They create them, review them, flag them as ready.
3. **Tasks are sequential unless marked parallel-safe.** Parallel tasks touching the same files can revert each other.
4. **Ask before acting on anything destructive or ambiguous.** When in doubt, ask.
5. **Check for conflicts before starting.** Use the coordination guide (see `.workflow/issue-tracker.md`) to see in-progress work and verify no task from the other model touches your files.
6. **Claim your work.** Claim a task in the project’s issue tracker when you start (via the coordination guide). Create a PR when you finish; the tracker issue is closed or completed per the guide (e.g. when the PR is merged).

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
3. **Read `.workflow/issue-tracker.md`** to see which issue tracker this project uses. Follow the **coordination guide linked there** to find available work and claim a task (and to check for in-progress work from the other model).
4. If no work is available, ask your operator what to do next.

## Task Workflow

- **Tasks are tracked in the system set in `.workflow/issue-tracker.md`.** The coordination guide for that tracker describes the spec format, files to edit, and acceptance criteria.
- When you finish a task, follow the coordination guide (e.g. PR, completion comment, status update). Do not close or complete the issue in the tracker until the guide says so (e.g. after PR merge).
- Update `STATUS.md`, `decisions.md`, and `.metrics/` (your model's file) as part of completing any task that warrants it.

## Task Dependencies & Parallel Work

Your coordination guide (see `.workflow/issue-tracker.md`) describes how dependencies and sub-tasks work. In all cases:

- **Files to edit:** Always list files that the task will modify — this enables conflict detection between models.

**How to assess parallel safety:** Two tasks conflict if they modify the same file. Check in-progress work (via the coordination guide) before starting yours.

## Creating New Tasks

Follow the coordination guide linked in `.workflow/issue-tracker.md` to create tasks. In general: include a clear title, spec, acceptance criteria, and "Files to edit"; set status/labels so others can see it's available or blocked; link dependencies if the tracker supports it.

## Task Completion Checklist

1. **Rebase on main before closing** — when closing a session: fetch and rebase (`git fetch origin main && git rebase origin/main`), resolve any conflicts, then commit and push; use `git push --force-with-lease origin <branch>` if the branch was already pushed. Verify the PR shows no conflicts.
2. **Before every push** — update your model's metrics file (`.metrics/metrics-claude.md` or `.metrics/metrics-cursor.md`) and include it in the commit you're pushing, so each push carries up-to-date metrics. If there's no new work this session, no metrics change is required.
3. **PR created or updated** — open or update the PR. Follow the coordination guide (`.workflow/issue-tracker.md`) for when to close or complete the tracker issue (e.g. when the PR is merged).
4. **Downstream unblocked** — when the PR is merged, follow the coordination guide to flip any newly-unblocked work to available (or document in the PR comment).
5. **Completion comment** — per the coordination guide, leave a comment or update in the tracker noting the PR and that it’s ready for review/merge.
6. **Metrics updated** — on session close, update your model's file in `.metrics/` (session row, PR/commits, and code volume if applicable).
7. **Decisions updated** — if a significant decision was made, update `decisions.md`.
8. **STATUS.md updated** — reflect the current project state.

## Session Close-Out

When your operator says "close this session" (or equivalent), follow these steps:

1. **Finish or pause current work** — commit, push, and create/update PRs for any in-progress tasks.
2. **Update your metrics file** — add a session row to your model's file (same update you do before any push; on close-out we also do it as part of the final PR):
   - Claude Code → `.metrics/metrics-claude.md`
   - Cursor → `.metrics/metrics-cursor.md`
   - Include: session number, date, duration, PRs, decisions, focus area, phase, driver, operator, work category, bugs fixed.
   - Add code volume and PR activity rows as applicable.
3. **Update `decisions.md`** — if any significant decisions were made this session.
4. **Update `STATUS.md`** — reflect the current project state.
5. **Release claimed issues** — any tasks you claimed but didn’t finish should be released back to available (per the coordination guide) so the other model can pick them up.
6. **Commit and PR** — push your metrics/docs update as part of your final PR, or as a separate close-out PR.

> **Do not edit `.metrics/metrics.md` directly.** Each model writes to its own file. Claude Code is the merger — it combines both files into `.metrics/metrics.md` (master) and syncs to Meta Tracker.

### Metrics Merge (Claude Code only)

At session start or close-out, Claude Code checks for unsynced data:
1. Pull latest `.metrics/metrics-cursor.md` — if Cursor added sessions since last merge, incorporate them.
2. Pull latest `.metrics/metrics-claude.md` — include own session data.
3. Merge both into `.metrics/metrics.md` (the master file).
4. Push updated data to Meta Tracker (`vulnBankMetrics.ts` + `vulnBankProject.ts`).

This can happen at any natural breakpoint — no need to wait for the other model.

## Review Cadence

**After every 2-3 merges**, do a quick review pass:

1. **Build check** — verify the application runs correctly.
2. **Data integrity** — check for mismatched references or broken functionality.
3. **Bug logging** — any issues found get logged in `.metrics/metrics.md` (via your model's file and merge).
4. **Flag for review** — note anything for the human operators to check.

## Key References

| Doc | Location | When to Read |
|-----|----------|-------------|
| **STATUS.md** | Repo root | Every session |
| **How We Work** | `.workflow/` | When you need process details |
| **Tips & Lessons** | `.workflow/` | When you hit a technical snag |
| **decisions.md** | Repo root | When you need project history; log decisions using the structured format |
| **.metrics/** | `.metrics/` | When updating tracking data; before every push (include in commit). See `.metrics/README.md` and field definitions in the metrics files. |
| **Onboarding** | `.workflow/onboarding.md` | First-time local setup (git, gh, optional bd/acli) — macOS & WSL |
| **Issue tracker** | `.workflow/issue-tracker.md` | Which tracker this project uses; read first, then follow its coordination guide |
| **Bootstrap** | `.workflow/bootstrap.md` | One-time setup when choosing or changing the issue tracker |
| **GitHub Coordination** | `.workflow/github-issues-coordination.md` | If tracker is GitHub Issues |
| **Beads Coordination** | `.workflow/beads-coordination.md` | If tracker is Beads |
| **Jira Coordination** | `.workflow/jira-coordination.md` | If tracker is Jira |
| **Gherkin Requirements** | `.workflow/gherkin-requirements.md` | Writing requirements as Gherkin feature files |

---

*Adapt these guidelines to your workflow. Last updated: March 10, 2026.*
