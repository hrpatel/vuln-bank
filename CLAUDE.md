# Vuln Bank — Claude Code Instructions

**Read this file first. Every session. No exceptions.**

## Quick Start

1. Read this file (you're doing it now)
2. Read `STATUS.md` for current project state
3. **Check GitHub Issues** for available work: `gh issue list --repo hrpatel/vuln-bank --label available`
4. Check for any issues labeled `in-progress` + `cursor` — avoid file conflicts with those
5. Pick an available issue or ask Michael what to work on

## Multi-Model Coordination

This repo is worked on by **two AI models in parallel**:
- **Claude Code** (CLI) — operated by Michael
- **Cursor** — operated by a coworker

**Coordination happens through GitHub Issues**, not `tasks/index.md`. See `.workflow/github-issues-coordination.md` for the full guide, API reference, and examples.

### The Rules

1. **Check before you start.** Check GitHub Issues for `in-progress` tasks from the other model. If one touches the same files as yours, pick a different task.
2. **Claim your task.** Assign yourself and label the issue `in-progress` + `claude-code` in a single PATCH call.
3. **Branch per task.** Always work on a feature branch, never directly on main.
4. **PRs are the merge point.** Create PRs; humans merge.
5. **Unblock downstream.** When you close an issue, check what it was blocking and flip newly-unblocked issues from `blocked` to `available`.

### Conflict Avoidance

Each issue body lists the files it will edit. This is the conflict-detection mechanism:
- If your task touches `app.py` and a Cursor issue labeled `in-progress` also touches `app.py`, **don't start yours yet**.
- If there's no file overlap, you're safe to work in parallel.
- When in doubt, ask Michael.

## Workflow Reference

Full workflow documentation is in `.workflow/`:
- `START HERE.md` — session rules and task workflow
- `How We Work.md` — roles, coordination protocol, review process
- `github-issues-coordination.md` — **GitHub Issues coordination guide, API reference, and hard-problem solutions**
- `Tips & Lessons.md` — practical knowledge from AI-assisted development
- `task-template.md` — standard format for archival task snapshots

## Project Context

This is a deliberately vulnerable banking application for security testing practice. Work involves updating and extending the vulnerability bank — adding new vulnerability scenarios, improving existing ones, and maintaining the application.

## Tracking

- Log sessions to `metrics.md` using the structured field definitions (Phase, Driver, Operator, Work Category, Tool)
- Log significant decisions to `decisions.md` using the structured entry format (Type, Category, Chosen path, Alternatives)
- Both feed into the Meta Tracker dashboard (meta.jynaxxapps.com)

## Code Changes

- All changes go through PRs — no direct pushes to main
- Michael or the coworker merges — AI models never merge
- Keep PRs focused: one concern per PR
