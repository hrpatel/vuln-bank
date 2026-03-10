# Task: Solve multi-model coordination gaps

**Status:** Done
**Created:** March 9, 2026
**Priority:** High
**Scope:** Substantial
**Depends on:** None
**Parallel safe with:** Any non-overlapping
**Executed by:** Claude Code
**Completed:** March 10, 2026
**PR:** #11, #13

---

## What

Address the coordination gaps identified in Cursor's workflow review (`workflow-suggestions-cursor.md`). The primary focus is solving the task index visibility problem — both models work on branches, but the coordination mechanism (`tasks/index.md`) requires real-time shared state that branch isolation prevents.

## Why

The current workflow assumes both models can see the same index state, but they can't. This undermines the entire conflict detection system. Solving this foundational issue will cascade into fixing several other reported problems.

## Primary Problem: Index Visibility

Both models read/write `tasks/index.md` to coordinate, but the "all changes through PRs" rule means index updates are invisible to the other model until merged. Two models can both see a task as Queued and both claim it.

### Options to Evaluate

**Option A — Direct-push exception for index updates**
- Allow `tasks/index.md` status-only commits directly to main
- Pros: Simplest, lowest friction, index becomes real-time
- Cons: Breaks the "everything through PRs" rule; risk of push conflicts
- Cascade: Also solves staleness detection (#3) if we add a Claimed-at column

**Option B — GitHub Issues as coordination layer**
- Use Issues for task claiming/status instead of a markdown file
- Pros: Branch-independent, timestamped, has built-in assignment
- Cons: Duplicates the task index, adds friction, both models need API access
- Cascade: Solves race conditions (#2) via GitHub's atomic assignment; solves cross-model signals (#4) via issue comments

**Option C — Draft PR as claim signal**
- Require models to push branch and open a draft PR immediately after claiming
- Pros: Visible to both models via `gh pr list`; no rule changes needed
- Cons: Doesn't update the index itself; requires checking two sources of truth
- Cascade: Partially solves staleness (#3) — PRs have timestamps

**Option D — Hybrid: index on main + Issues for signals**
- Direct-push index updates for real-time coordination
- GitHub Issues for cross-model notes and async communication
- Pros: Best of both — index stays simple, Issues handle what markdown can't
- Cascade: Solves #1, #3, #4, and #7 from Cursor's list

### Research needed
- How do other multi-agent repos handle shared mutable state?
- Is there a GitHub Actions approach (auto-merge index-only PRs)?
- Would a lightweight locking mechanism (e.g., a `LOCK` file) work?

## Secondary Issues (may be solved by primary fix)

These were identified in Cursor's review. Evaluate which ones are addressed by the chosen coordination solution:

| # | Issue | Likely solved by primary fix? |
|---|-------|-------------------------------|
| 2 | Race condition on task claiming | Partially (A), Yes (B), No (C) |
| 3 | Staleness detection | Yes if Claimed-at column added |
| 4 | Cross-model signals | Yes (B, D), No (A, C) |
| 5 | DRY up entry points | Independent — separate task |
| 6 | Lightweight bookkeeping tiers | Independent — separate task |
| 7 | Serialize workflow doc changes | Yes (D), Partially (A) |
| 8 | Tie-breaking for simultaneous claims | Yes (B), Needs rule (A, C, D) |
| 9 | Update resolved dependencies | Independent — cosmetic |

## Acceptance Criteria

- [ ] Primary coordination mechanism chosen and documented in decisions.md
- [ ] Index visibility gap is resolved — both models can see real-time task status
- [ ] At least 3 secondary issues addressed or explicitly deferred with rationale
- [ ] Workflow docs updated to reflect the new coordination approach
- [ ] Both model entry points (.cursorrules, CLAUDE.md) updated if needed

## Files to Edit

`tasks/index.md`, `.workflow/How We Work.md`, `.workflow/START HERE.md`, `decisions.md`, `CLAUDE.md`, `.cursorrules`, possibly `metrics.md`

## Notes

- Cursor's full review is in `workflow-suggestions-cursor.md` (repo root)
- This is the first task requiring both models to agree on a solution — consider having both models propose independently, then the operators pick
- The solution should be simple enough that both models can follow it without special tooling
