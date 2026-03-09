# Workflow Review — Cursor Agent Analysis

**Date:** March 9, 2026
**Reviewer:** Cursor (operated by coworker)
**Scope:** Full review of workflow docs, tracking files, and coordination protocol after Meta Tracker alignment updates

---

## Summary

The workflow is well-structured and the Meta Tracker alignment adds useful rigor to session and decision tracking. The coordination protocol is clear in intent. However, there are structural issues — some critical — that will cause problems once both models are actively working in parallel. This document covers what works, what doesn't, and concrete suggestions.

---

## What Works Well

- **Separate entry points** (`.cursorrules`, `CLAUDE.md`) funneling into shared docs in `.workflow/` is a clean design. Each model knows where to start without reading the other's file.
- **Branch naming convention** (`cursor/` vs `claude/` prefixes) provides instant visibility into ownership. No ambiguity about which model created which branch.
- **Task template** with "Files to Edit" as a declared conflict surface is pragmatic. File-level granularity is the right abstraction — line-level would be overengineering.
- **"Humans merge" rule** is a sensible safety net that prevents models from creating irreversible state.
- **Decision log structure** (Type, Category, Chosen path, Alternatives) is well-designed. The entry type taxonomy (decision, event, dead-end, discovery, pivot) covers real scenarios.
- **Session metrics field definitions** (Phase, Driver, Operator, Work Category, Tool) are standardized enough to be useful without being so rigid they become a burden.
- **Dependency chain documentation** in the task index gives both models visibility into sequencing requirements at a glance.

---

## Critical Issues

### 1. The task index lives on branches — coordination has a visibility gap

**The problem:** The workflow says both models should read and write `tasks/index.md` to signal active work. It also says "all changes go through PRs — no direct pushes to main." These two rules are incompatible.

If I claim task #5 by updating `tasks/index.md` on branch `cursor/05-something`, Claude Code working from `main` or its own branch will never see that claim. The index only works as a real-time coordination mechanism if both models are reading and writing the *same copy*. Branch isolation guarantees they aren't.

This means the entire file-level conflict detection system — the centerpiece of the coordination protocol — has a visibility gap. Both models could check the index, both see a task as `Queued`, and both start working on it.

**Severity:** High. This undermines the core coordination mechanism.

**Suggested fix:** Either (a) exempt `tasks/index.md` status updates from the "no direct pushes to main" rule — a quick commit to main that only touches the status column is low-risk, or (b) use GitHub Issues as the coordination layer — they're branch-independent and have built-in timestamps, or (c) require models to push their branch and open a draft PR immediately after claiming, so the other model can check open PRs/branches as a secondary signal.

### 2. Race condition on task claiming — no atomicity

**The problem:** Even if the index visibility issue were solved, two models can read the index at the same moment, both see a task as `Queued`, and both claim it. The "later timestamp yields" conflict resolution rule in `How We Work.md` is unenforceable — timestamps in a markdown file are imprecise (date-level, not time-level), and there's no guarantee both models record the same format.

**Severity:** Medium-high. Rare in practice if human operators coordinate verbally, but the workflow should not depend on out-of-band communication to function.

**Suggested fix:** Add a "Claimed at" column in the index with ISO timestamps. Define a tie-breaking rule that doesn't depend on timestamps (e.g., Claude Code yields to Cursor on even-numbered tasks, Cursor yields on odd — arbitrary but deterministic). Or, more practically: require the human operator to assign tasks explicitly rather than having models self-serve from the queue.

### 3. No staleness detection for abandoned claims

**The problem:** If Claude Code claims a task and then the session crashes, the operator walks away, or the work is abandoned, that task stays `In Progress (Claude Code)` indefinitely. There's no timeout, no heartbeat, and no protocol for reclaiming stale work. I would perpetually avoid those files even though nobody is actually working on them.

**Severity:** Medium. Will cause unnecessary blocking as the project grows.

**Suggested fix:** Add a convention: if a task has been `In Progress` for more than 48 hours with no corresponding PR or branch activity, it can be reclaimed. Include a "Claimed at" timestamp in the index to make staleness detectable. Either model can flag a stale task; the human operator makes the call.

### 4. "Files to Edit" is a static declaration but scope expands dynamically

**The problem:** A task might declare it will touch `app.py`, but during implementation discover it also needs `database.py`. The conflict detection only works if the file list is accurate and complete at task creation time. There's no protocol for what happens when a task's file footprint grows mid-work.

**Severity:** Medium. Will cause silent conflicts when tasks are more complex than initially estimated.

**Suggested fix:** Add to the workflow: "If your task needs to modify files not listed in its 'Files to Edit' section, update the task file and re-check the index for conflicts before proceeding. If a new overlap is discovered, pause and notify your operator."

---

## Moderate Issues

### 5. Content duplication across entry points

`.cursorrules`, `CLAUDE.md`, `START HERE.md`, and `How We Work.md` all restate the same core rules (check the index, claim tasks, no direct pushes, humans merge). The new "Tracking" section was added to both `.cursorrules` and `CLAUDE.md`, creating another copy. If these diverge — and with two models editing them over time, they will — the models will follow different rules.

**Suggested fix:** Make `.cursorrules` and `CLAUDE.md` thin entry points (5-10 lines) that say "read `.workflow/START HERE.md`" and contain only model-specific instructions (e.g., "your branch prefix is `cursor/`"). Move all shared rules into `.workflow/` as the single source of truth.

### 6. Bookkeeping overhead is uniform regardless of task size

The task completion checklist requires updating: the task file, the index, `metrics.md`, `decisions.md`, and `STATUS.md`. The metrics now have 5 structured fields per session (Phase, Driver, Operator, Work Category, Tool). For a 10-minute documentation fix, the tracking overhead may exceed the actual work.

Notably, task #04 (data model alignment) was completed without a separate task file — it exists only as a row in the index. This suggests the workflow is already being bent for small tasks, which validates the need for a formal lightweight path.

**Suggested fix:** Define task tiers. "Quick fix" scope tasks require only an index update and a PR. "Moderate" and "Substantial" tasks get the full checklist. This is already implied by the "Scope" field in the task template — make it explicit by tying scope to required bookkeeping.

### 7. No cross-model communication channel

If I discover during my work that a function signature changed, or that a dependency was added, there's no way to signal that to Claude Code. The index tracks status but not messages. The `Tips & Lessons.md` file is close, but it's for general learnings, not task-specific signals.

**Suggested fix:** Add a "Signals" or "Notes" section to the bottom of `tasks/index.md` where either model can leave short, timestamped messages for the other. Example: "Mar 9 (Cursor): Refactored auth.py — check function signatures if your task imports from it."

### 8. Workflow docs are themselves a conflict surface

Task #03 lists `CLAUDE.md` and `.cursorrules` as files to edit. Both models read these files at the start of every session. If one model is updating the workflow while the other is following it, behavior becomes unpredictable. There's no guidance that workflow infrastructure changes should be serialized.

**Suggested fix:** Add to `How We Work.md`: "Changes to `.cursorrules`, `CLAUDE.md`, or `.workflow/` files are always single-model, serialized operations. Never run two tasks that modify workflow docs in parallel."

### 9. Stale dependency declarations in task files

Tasks #02 and #03 both list `Depends on: 01` with the note "workflow setup must be merged first." Task #01 is now marked Done. The dependency chain section in the index was updated (`#01 ✓`), but the individual task files still reference the old dependency. This is minor now but will cause confusion as the task count grows — a model reading the task file sees a dependency; the index says it's resolved.

**Suggested fix:** When a dependency is satisfied, update the individual task file to reflect it (e.g., `Depends on: ~~01~~ None — resolved Mar 9`). Or accept that the index is the source of truth for dependency status and note that convention explicitly.

---

## Observations on the Meta Tracker Integration

The structured fields in `metrics.md` and `decisions.md` are a good addition. A few notes:

- **The field definitions are clear and I can use them.** Phase, Driver, Operator, Work Category, Tool — these are unambiguous enough that I can fill them in without guessing.
- **The decision entry types are practical.** The distinction between decision, dead-end, discovery, and pivot covers real scenarios I'd encounter during development.
- **Both models logging to the same file will cause merge conflicts.** If Claude Code and I both complete tasks in the same period and both update `metrics.md`, the PRs will conflict. This circles back to the branch-visibility issue above.

---

## Recommended Actions (Priority Order)

| # | Action | Severity | Effort |
|---|--------|----------|--------|
| 1 | Solve index visibility: exempt `tasks/index.md` from the no-direct-push rule, or use GitHub Issues as the coordination layer | Critical | Low |
| 2 | Add a scope-expansion protocol for "Files to Edit" | High | Low |
| 3 | Add staleness detection (Claimed-at timestamp + 48hr reclaim convention) | Medium | Low |
| 4 | Add a cross-model signals/notes section to the index | Medium | Low |
| 5 | DRY up entry points — thin `.cursorrules`/`CLAUDE.md`, canonical rules in `.workflow/` | Medium | Medium |
| 6 | Define lightweight bookkeeping for "Quick fix" scope tasks | Medium | Low |
| 7 | Serialize workflow doc changes (add explicit rule) | Medium | Low |
| 8 | Add a tie-breaking rule for simultaneous task claims | Low | Low |
| 9 | Establish convention for updating resolved dependencies in task files | Low | Low |

---

## Answers to Specific Review Questions

**Does the coordination protocol in `How We Work.md` make sense?**
Yes, the intent is clear. The gap is execution — the protocol assumes both models can see the same index state in real time, but branch isolation prevents that.

**Are the `.cursorrules` instructions sufficient?**
Sufficient to understand what to do. The tracking section is a good addition. I'd prefer a thinner file that delegates to `.workflow/` for shared rules, to reduce drift risk.

**Is the task index format practical?**
The format works. I can read, claim, and update it. The wide table is harder to edit without introducing formatting errors, but manageable. The "Active Work" summary section at the bottom is a helpful quick-reference.

**Can I log sessions and decisions using the structured formats?**
Yes. The field definitions in `metrics.md` and the entry type guide in `decisions.md` are clear enough to use without ambiguity.

**Branch naming convention?**
`cursor/{##}-{task-slug}` works. No issues.

**Anything missing for parallel work?**
The cross-model signals channel (item #4 above) and the scope-expansion protocol (item #2) are the main gaps.

---

*This file is for human and AI review. It can be deleted or archived after the feedback is addressed.*
