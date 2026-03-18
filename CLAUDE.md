# Vuln Bank — CLI Agent Instructions

**Entry point for CLI-based AI agents.** (Used by Claude Code and other CLI agents. Filename is historical.)

**Read this file, then `.workflow/START HERE.md`. Every session. No exceptions.**

## Model-Specific Settings

Set these for your agent (example values shown for Claude Code):

- **You are:** [e.g. Claude Code (CLI)]
- **Your operator:** [e.g. Michael]
- **Your branch prefix:** [e.g. `claude/{##}-{task-slug}`]
- **Your label:** [e.g. `claude-code`]
- **Other model's label to watch:** [e.g. `cursor`]

## Quick Start

1. Read `.workflow/START HERE.md` for session rules and task workflow
2. Read `STATUS.md` for current project state
3. Read `.workflow/issue-tracker.md` to see which issue tracker this project uses, then follow the coordination guide linked there to find and claim work (and to avoid file conflicts with the other model’s in-progress work)
4. If no work is available, ask your operator what to work on

**Beads — claim first:** Run `bd update <id> --claim` and succeed *before* creating a branch or editing files for that task. If claim fails, pick another task.

**Parallel agents:** Use a **git worktree** per agent on the same machine (see `.workflow/onboarding.md`).

Work on a feature branch only; never push to main.

## Workflow Reference

All shared rules live in `.workflow/` — that is the single source of truth:
- `START HERE.md` — session rules and task workflow
- `issue-tracker.md` — which tracker this project uses; read first, then follow its coordination guide
- `bootstrap.md` — one-time setup when choosing or changing the issue tracker
- `github-issues-coordination.md`, `beads-coordination.md`, `jira-coordination.md` — per-tracker guides (use the one linked in issue-tracker.md)
- `gherkin-requirements.md` — writing requirements as Gherkin feature files
- `Tips & Lessons.md` — practical knowledge from AI-assisted development

## Project Context

This is a deliberately vulnerable banking application for security testing practice. Work involves updating and extending the vulnerability bank — adding new vulnerability scenarios, improving existing ones, and maintaining the application.
