# Design: Metrics directory and capture-before-push

**Date:** 2026-03-10  
**Status:** Approved (design)  
**Summary:** Move all session/workflow metrics files into `.metrics/`, add a README with pre-push checklist, and require metrics to be updated and included in the commit before every push.

---

## 1. Goals

- **Centralize metrics** — All metrics-related files live under `.metrics/` at repo root.
- **Capture as work happens** — Before every push, the agent updates the relevant metrics file and includes that update in the same commit, so each push carries up-to-date metrics.

---

## 2. Directory layout and file moves

### New layout

- **`.metrics/`** (new directory at repo root)
  - **`metrics.md`** — Merged master. Claude Code merges here; no one else edits directly.
  - **`metrics-claude.md`** — Claude Code’s session log.
  - **`metrics-cursor.md`** — Cursor’s session log.
  - **`README.md`** — Purpose of the directory, file roles, pre-push checklist, pointer to workflow docs.

### Moves

| From (root)        | To                  |
|--------------------|---------------------|
| `metrics.md`       | `.metrics/metrics.md` |
| `metrics-claude.md` | `.metrics/metrics-claude.md` |
| `metrics-cursor.md` | `.metrics/metrics-cursor.md` |

### Unchanged

- File names stay the same.
- Split-model ownership and merge process (Claude = merger) unchanged.
- Meta Tracker continues to consume the merged file; any path config (e.g. for sync) must point at `.metrics/metrics.md`.

---

## 3. `.metrics/README.md` content

- **Purpose** — `.metrics/` holds session and workflow metrics for project tracking and Meta Tracker. Each push should include up-to-date metrics so the repo stays current.
- **Files**
  - **`metrics.md`** — Merged master. Do not edit directly. Claude Code merges from the two model files and syncs to Meta Tracker.
  - **`metrics-claude.md`** — Claude Code only.
  - **`metrics-cursor.md`** — Cursor only.
- **Pre-push checklist**
  - Before every push: update your model’s metrics file (session row, code volume, PR activity as applicable).
  - Include that metrics update in the same commit you push (or in a dedicated metrics commit on the same branch before pushing).
  - If you have done no work this session, no metrics change is required.
- **Full rules** — See `.workflow/START HERE.md` and `.workflow/How We Work.md` for when to update, merge process, and field definitions.
- Keep the README to one short, scannable page.

---

## 4. “Update metrics before every push” in workflow docs

### START HERE.md

- **Task Completion Checklist**
  - Retain existing “Metrics updated — on session close…” item.
  - Add new checklist item (e.g. after rebase): **“Before every push: update your model’s metrics file and include it in the commit you’re pushing (so each push carries up-to-date metrics).”** Optionally add: if there’s no new work this session, no metrics change is required.
- **Session Close-Out**
  - Keep “Update your metrics file” but use paths: `.metrics/metrics-claude.md`, `.metrics/metrics-cursor.md`.
  - Add one sentence: this is the same update done before any push; on close-out we also do it as part of the final PR.
- **All metrics paths** — Replace every reference to `metrics.md` / `metrics-claude.md` / `metrics-cursor.md` with `.metrics/` versions (e.g. `.metrics/metrics.md`).
- **Metrics Merge (Claude Code only)** — Update the three merge steps to: “Pull latest `.metrics/metrics-cursor.md`”, “Pull latest `.metrics/metrics-claude.md`”, “Merge both into `.metrics/metrics.md`”.
- **Key References table** — Change the metrics row to: **`.metrics/`** (or **`.metrics/README.md`** and **`.metrics/metrics.md`**), location **`.metrics/`**, when **“When updating tracking data; before every push (include in commit).”**

### How We Work.md

- **Metrics & Session Tracking — Split Metrics Files**
  - Update the table so all three files are under `.metrics/` (e.g. `.metrics/metrics-claude.md`, `.metrics/metrics-cursor.md`, `.metrics/metrics.md`).
  - Add one sentence: **“Before every push, update your model’s file and include that update in the commit you push.”**
  - Keep “Who merges” and “do not edit metrics.md directly”; only paths change to `.metrics/...`.

---

## 5. Complete list of files to change

### Moves (no content change)

- `metrics.md` → `.metrics/metrics.md`
- `metrics-claude.md` → `.metrics/metrics-claude.md`
- `metrics-cursor.md` → `.metrics/metrics-cursor.md`

### New

- `.metrics/README.md` — Content from section 3 above.

### Workflow docs (paths + new rule)

- `.workflow/START HERE.md` — All metrics paths → `.metrics/...`; add “before every push” checklist item; update Session Close-Out and Metrics Merge paths; update Key References table.
- `.workflow/How We Work.md` — Table paths → `.metrics/...`; add “before every push” sentence in Metrics & Session Tracking.

### Other references

- `.workflow/Tips & Lessons.md` — Change “log it in `metrics.md`” to “log it in `.metrics/metrics.md`” (or “in the metrics master file under `.metrics/`”).
- `STATUS.md` — Update the line that describes split metrics to: “`.metrics/metrics-claude.md`, `.metrics/metrics-cursor.md`, Claude Code merges into `.metrics/metrics.md`”.

### Internal refs inside metrics files

- **`.metrics/metrics.md`** — In the “do not edit” note, leave references as `metrics-claude.md` and `metrics-cursor.md` (same directory).
- **`.metrics/metrics-claude.md`** and **`.metrics/metrics-cursor.md`** — In the footer, change “Do not edit `metrics.md`” to “Do not edit the master file in this directory (`metrics.md`)” so it’s clear without adding paths.

### No change

- **CLAUDE.md / .cursorrules** — Update only if they mention metrics file names; otherwise leave as “see START HERE”.
- **.workflow/github-issues-coordination.md** — Update only if it explicitly references metrics files.
- **.archive/** — Leave as-is (historical).

---

## 6. Next step

After user approval of this spec: create an implementation plan (e.g. ordered tasks for moves, new README, and doc edits) and then implement.
