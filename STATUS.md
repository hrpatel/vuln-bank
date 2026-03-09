# Vuln Bank — Current Status

**Last updated:** March 9, 2026
**Repo:** https://github.com/hrpatel/vuln-bank
**Live site:** N/A (runs locally via Docker)
**Current phase:** Spec
**Current state:** Task #05 in progress — GitHub Issues coordination system designed, POC validated, guide written. Awaiting Cursor/operator review before full switchover.

---

## What the App Is

A deliberately vulnerable banking application designed for practicing security testing of web apps, APIs, AI-integrated apps, and secure code reviews. Features common vulnerabilities found in real-world applications.

## Codebase

- **Stack:** Python (Flask), SQLite, HTML/CSS/JS templates
- **Key files:**
  - `app.py` — main Flask application
  - `auth.py` — authentication module
  - `database.py` — database operations
  - `ai_agent_deepseek.py` — AI agent integration
  - `templates/` — HTML templates
  - `static/` — CSS, JS, images

## Recent Work

- **Session 34:** GitHub Issues POC validated — sub-issues, dependencies, labels, claiming, signaling all work. Coordination guide written (`.workflow/github-issues-coordination.md`). All workflow docs updated to reference Issues instead of task index. (PR #11)
- **Session 33:** Designed GitHub Issues coordination system to replace file-based task index (decisions.md updated)
- Cursor reviewed workflow and identified 9 improvement areas (workflow-suggestions-cursor.md)
- Repo migrated: removed fork association with Commando-X/vuln-bank, recreated as standalone
- Aligned workflow docs with Meta Tracker data model (PR #3, 9 files)
- Task #01 done — vuln-bank added to Meta Tracker dashboard (PR #77 in meta-tracker repo)

## Known Issues

(None logged yet — initial setup)

## Team

- **Two AI models working in parallel:**
  - Claude Code (CLI) — operated by Michael
  - Cursor — operated by coworker
- Coordination via GitHub Issues (replacing file-based task index — see `.workflow/github-issues-coordination.md`)

---

*This file is updated in place. It always reflects the current project state.*
