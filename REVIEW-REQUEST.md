# Review Request — Workflow & Coordination Setup

**Date:** March 9, 2026 (updated)
**Original PR:** #1 — Add workflow docs and multi-model coordination
**Updated in:** #3 — Align workflow docs with Meta Tracker data model
**Created by:** Claude Code (AI model, operated by Michael)

---

## For the Human Operator

This repo has a workflow system so that two AI models (Claude Code and Cursor) can work on this repo in parallel without colliding. Here's what's in it:

- **Entry points for each model:** `CLAUDE.md` (for Claude Code) and `.cursorrules` (for Cursor) — each model reads its own file at the start of every session
- **Shared process docs** in `.workflow/` — how to coordinate, claim tasks, avoid conflicts, review code
- **Task tracking** — `tasks/index.md` is the shared queue where both models signal what they're working on
- **Project tracking** — `STATUS.md`, `decisions.md`, `metrics.md` for ongoing project state
- **Meta Tracker integration** — session metrics and decisions use a structured format that feeds into the Meta Tracker dashboard (meta.jynaxxapps.com)

**What we need from you:** Point your Cursor agent at this file and ask it to review the workflow. We want to make sure the coordination protocol works from both models' perspectives.

---

## For the Cursor Agent

Welcome — we'll be collaborating on this codebase. We'd like your review to make sure the workflow works for you.

### Files to Review (in this order)

1. **`.cursorrules`** — Your session entry point. You'll read this first every session. Check that the instructions are clear and actionable.
2. **`.workflow/How We Work.md`** — The coordination protocol. Defines how we claim tasks, avoid file conflicts, name branches, and resolve collisions.
3. **`tasks/index.md`** — The shared task queue. The status column (`In Progress (Claude Code)` / `In Progress (Cursor)`) is how we signal active work to each other.
4. **`.workflow/START HERE.md`** — The universal session startup checklist.
5. **`.workflow/task-template.md`** — The format for new task files. The "Files to Edit" field is how we detect potential conflicts.
6. **`metrics.md`** — Session metrics with field definitions (Phase, Driver, Operator, Work Category, Tool). Both models should log their sessions here.
7. **`decisions.md`** — Decision log with structured entry format (Type, Category, Chosen path, Alternatives). Both models should log decisions here.

### What Changed Since Initial Setup

The workflow docs have been aligned with the Meta Tracker data model. Key additions:

- **`decisions.md`** now has a "How to Log Decisions" guide with entry types (decision, event, dead-end, discovery, pivot) and structured fields
- **`metrics.md`** now has session field definitions that feed into the dashboard — Phase, Driver, Operator, Work Category, Tool
- **`tasks/index.md`** now has an "Executed By" column so we can track which model did what
- **`.workflow/How We Work.md`** now describes the structured formats for decisions and metrics
- **`CLAUDE.md`** and **`.cursorrules`** now include metrics and decision logging as part of task completion

### Feedback We're Looking For

- Does the coordination protocol in `How We Work.md` make sense? Anything unclear or unworkable?
- Are the `.cursorrules` instructions sufficient for you to follow the workflow?
- Is the task index format practical? Can you check it, claim tasks, and update it without friction?
- Can you log sessions to `metrics.md` and decisions to `decisions.md` using the structured formats?
- Branch naming convention (`cursor/{##}-{task-slug}`) — does that work for you?
- Is there anything missing that would help you work in parallel with another AI model?

### How to Respond

Create a file called `REVIEW-RESPONSE.md` in the repo root with your feedback, or leave comments on the PR — either works. Your operator can also relay feedback verbally.

---

*This file can be deleted after the review is complete.*
