# Vuln Bank — Current Status

**Last updated:** March 9, 2026
**Repo:** https://github.com/hrpatel/vuln-bank
**Live site:** N/A (runs locally via Docker)
**Current phase:** Spec
**Current state:** Cursor review complete; coordination gap identified as next priority (task #05)

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

- Cursor reviewed workflow and identified 9 improvement areas (workflow-suggestions-cursor.md)
- Repo migrated: removed fork association with Commando-X/vuln-bank, recreated as standalone
- Aligned workflow docs with Meta Tracker data model (PR #3, 9 files)
- Task #01 done — vuln-bank added to Meta Tracker dashboard (PR #77 in meta-tracker repo)
- Workflow setup: added multi-model coordination docs, task tracking, project metrics structure

## Known Issues

(None logged yet — initial setup)

## Team

- **Two AI models working in parallel:**
  - Claude Code (CLI) — operated by Michael
  - Cursor — operated by coworker
- Coordination via task index with file-level conflict detection

---

*This file is updated in place. It always reflects the current project state.*
