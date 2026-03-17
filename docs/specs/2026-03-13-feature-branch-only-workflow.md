# Feature-Branch-Only Workflow — Design Note

**Date:** 2026-03-13  
**Summary:** All changes are made on feature branches; agents and humans never push to `main`. This note records where the rule is stated so it is visible at session start and at push time.

## Rule

- Work only on a feature branch (create or checkout before making changes).
- Push only that branch (e.g. `git push --force-with-lease origin <branch>`).
- Never push to `main`. Humans merge PRs; agents do not merge.

## Where It Is Stated

| Location | Purpose |
|----------|--------|
| **START HERE.md** | "How to Start a Session": create/checkout feature branch; do not commit/push to main. Task Completion Checklist: push only to your feature branch; never to main. |
| **How We Work.md** | "Both models": work only on a feature branch; push only that branch; never push to main. Optionally "Before Starting a Task": create or switch to feature branch. |
| **.cursorrules** / **CLAUDE.md** | One line in Quick Start / Workflow Reference: work on a feature branch only; never push to main. |

## Branch Naming

Per How We Work: `claude/{##}-{task-slug}`, `cursor/{##}-{task-slug}`.

---

*Design approved 2026-03-13. Changes applied in same session.*
