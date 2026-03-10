# Vuln Bank — Claude Code Instructions

**Read this file, then `.workflow/START HERE.md`. Every session. No exceptions.**

## Model-Specific Settings

- **You are:** Claude Code (CLI)
- **Your operator:** Michael
- **Your branch prefix:** `claude/{##}-{task-slug}`
- **Your label:** `claude-code`
- **Other model's label to watch:** `cursor`

## Quick Start

1. Read `.workflow/START HERE.md` for session rules, task workflow, and coordination protocol
2. Read `STATUS.md` for current project state
3. Check GitHub Issues for available work: `gh issue list --repo hrpatel/vuln-bank --label available`
4. Check for issues labeled `in-progress` + `cursor` — avoid file conflicts with those
5. Pick an available issue or ask Michael what to work on

## Workflow Reference

All shared rules live in `.workflow/` — that is the single source of truth:
- `START HERE.md` — session rules and task workflow
- `How We Work.md` — roles, coordination protocol, review process
- `github-issues-coordination.md` — Issues coordination guide, API reference, and hard-problem solutions
- `Tips & Lessons.md` — practical knowledge from AI-assisted development
- `task-template.md` — standard format for archival task snapshots

## Project Context

This is a deliberately vulnerable banking application for security testing practice. Work involves updating and extending the vulnerability bank — adding new vulnerability scenarios, improving existing ones, and maintaining the application.
