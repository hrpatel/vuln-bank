# Vuln Bank — Current Status

**Last updated:** March 10, 2026
**Repo:** https://github.com/hrpatel/vuln-bank
**Live site:** N/A (runs locally via Docker)
**Current phase:** Build
**Current state:** Workflow cleanup complete. Obsolete workflow artifacts moved to `.archive/`; live docs updated to reference GitHub Issues and `.archive` paths.

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

- **Cursor session (Mar 10):** Picked 5 SDE countermeasure issues (#100 T38, #80 T36, #97 T338, #99 T2139, #83 T1144). Implemented T38 (parameterized SQL in auth.py and app.py). Verified T36 (XSS), T338 (auth/authz), T1144 (SSTI); left T2139 incomplete by design with SDE rationale note. Updated all 5 in SDE to Complete or Incomplete with note. PR #103.
- **Cursor session (Mar 10):** Security champion: created SDElements project **vuln-bank** via sde-mcp-demo; modeled project with survey answers (Web application, Web service, Uses passwords); created GitHub issue #54 from SDE task CT1 with labels `security`, `phase:requirements`, `available`, `created-by:cursor`.
- **Cursor session (Mar 10):** Created `.archive/` and moved obsolete workflow artifacts — `tasks/`, `workflow-suggestions-cursor.md`, `REVIEW-REQUEST.md`. Added `.archive/README.md` and `.archive/tasks/done/`. Updated `.workflow/` docs and `STATUS.md` to use `.archive` paths and GitHub Issues as coordination layer.
- **Session 8 (Mar 10):** Fixed 4 bugs (#21, #22, #26, #36) in PR #53. Added session close-out workflow with split metrics files (PR #56). Meta Tracker synced with all sessions including Cursor's.
- **Session 34:** GitHub Issues POC validated — sub-issues, dependencies, labels, claiming, signaling all work. Coordination guide written (`.workflow/github-issues-coordination.md`). All workflow docs updated to reference Issues instead of task index. (PR #11)
- **Session 33:** Designed GitHub Issues coordination system to replace file-based task index (decisions.md updated)
- Cursor reviewed workflow and identified 9 improvement areas (see `.archive/workflow-suggestions-cursor.md`)
- Repo migrated: removed fork association with Commando-X/vuln-bank, recreated as standalone
- Aligned workflow docs with Meta Tracker data model (PR #3, 9 files)
- Task #01 done — vuln-bank added to Meta Tracker dashboard (PR #77 in meta-tracker repo)

## Known Issues

(None logged yet — initial setup)

## Team

- **Two AI models working in parallel:**
  - Claude Code (CLI) — operated by Michael
  - Cursor — operated by coworker
- Coordination via GitHub Issues (see `.workflow/github-issues-coordination.md`)
- Metrics: split files per model (`metrics-claude.md`, `metrics-cursor.md`), Claude Code merges into `metrics.md`

---

*This file is updated in place. It always reflects the current project state.*
