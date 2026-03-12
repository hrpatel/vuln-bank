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

1. Read `.workflow/START HERE.md` for session rules, task workflow, and coordination protocol
2. Read `STATUS.md` for current project state
3. Check GitHub Issues for available work: `gh issue list --repo hrpatel/vuln-bank --label available`
4. Check for issues labeled `in-progress` plus the other model's label — avoid file conflicts with those
5. Pick an available issue or ask your operator what to work on

## Workflow Reference

All shared rules live in `.workflow/` — that is the single source of truth:
- `START HERE.md` — session rules and task workflow
- `How We Work.md` — roles, coordination protocol, review process
- `github-issues-coordination.md` — Issues coordination guide, API reference
- `beads-coordination.md` — local task tracking with Beads (`bd`)
- `jira-coordination.md` — Jira workflow with Atlassian CLI (`acli`)
- `gherkin-requirements.md` — writing requirements as Gherkin feature files
- `Tips & Lessons.md` — practical knowledge from AI-assisted development

## Project Context

This is a deliberately vulnerable banking application for security testing practice. Work involves updating and extending the vulnerability bank — adding new vulnerability scenarios, improving existing ones, and maintaining the application.
