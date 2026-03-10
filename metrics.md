# Vuln Bank — Project Metrics

## Project Metadata

| Field | Value |
|-------|-------|
| **Project Name** | Vuln Bank |
| **Repository** | https://github.com/hrpatel/vuln-bank |
| **Tracking Since** | March 6, 2026 |
| **Last Updated** | March 10, 2026 (Session 9) |


> **This is the merged master.** Do not edit directly. Each model writes to `metrics-claude.md` or `metrics-cursor.md`. Claude Code merges both into this file and syncs to Meta Tracker.

---

## 1. Code Volume

| Session | Date | Model | Lines Added | Lines Deleted | Net Change | Key Files Changed |
|---------|------|-------|-------------|---------------|------------|-------------------|
| 1 | Mar 6 | Claude Code | 629 | 0 | +629 | Workflow setup (non-code) |
| 4 | Mar 9 | Claude Code | 323 | 58 | +265 | .workflow/github-issues-coordination.md, CLAUDE.md, .cursorrules, How We Work.md, START HERE.md, decisions.md |
| 5 | Mar 10 | Cursor | 39 | 88 | -49 | CLAUDE.md, .cursorrules, How We Work.md, START HERE.md, github-issues-coordination.md |
| 7 | Mar 10 | Cursor | ~50 | ~10 | +40 | .workflow/START HERE.md, github-issues-coordination.md, How We Work.md |
| 8 | Mar 10 | Claude Code | 159 | 41 | +118 | README.md, app.py, auth.py, Dockerfile, openapi.json, index.html |
| 8 | Mar 10 | Cursor | ~46 | 0 | +46 | STATUS.md, docs/sdelements-profile-and-assumptions.md |
| 9 | Mar 10 | Claude Code | 24 | 18 | +6 | app.py, How We Work.md, Dockerfile, docker-compose.yml, README.md |

---

## 2. PR & Commit Activity

| Session | Date | PRs Created | PRs Merged | Commits | Model | Notes |
|---------|------|-------------|------------|---------|-------|-------|
| 1 | Mar 6 | 1 | -- | 3 | Claude Code | PR #1: Workflow setup |
| 1 | Mar 6 | 1 | -- | 1 | Claude Code | PR #2: Review request |
| 3 | Mar 9 | 1 | 1 | 2 | Claude Code | PR #3: Workflow alignment (9 files) |
| 4 | Mar 9 | 1 | -- | 1 | Claude Code | PR #11: GitHub Issues coordination guide (6 files) |
| 5 | Mar 10 | 1 | -- | 2 | Claude Code | PR #13: DRY entry points + serialize workflow changes |
| 7 | Mar 10 | 1 | -- | 2 | Cursor | PR #50: Rebase-on-main checklist step |
| 8 | Mar 10 | 2 | 2 | 3 | Claude Code | PR #53: Fix 4 bugs. PR #56: Session close-out workflow |
| 8 | Mar 10 | 1 | 1 | 1 | Cursor | PR #59: SDElements profile + assumptions doc |
| 9 | Mar 10 | 2 | 2 | 2 | Claude Code | PR #102: Bare exceptions + stale refs. PR #104: Docker modernization |

---

## 3. Bug Tracking

| # | Date Found | Summary | Severity | Source | Resolution | Session Fixed | Model |
|---|-----------|---------|----------|--------|------------|---------------|-------|
| #21 | Mar 10 | Commando-X repo references throughout codebase | Medium | Codebase audit | Fixed (PR #53) | 8 | Claude Code |
| #22 | Mar 10 | Dead SQLite code in auth.py — 3 endpoints crash | High | Codebase audit | Fixed (PR #53) | 8 | Claude Code |
| #26 | Mar 10 | Overly permissive uploads directory (chmod 777) | Low | Codebase audit | Fixed (PR #53) | 8 | Claude Code |
| #36 | Mar 10 | Debug prints exposing usernames, SQL queries, JWT tokens | Medium | Codebase audit | Fixed (PR #53) | 8 | Claude Code |
| #37 | Mar 10 | Bare exception handlers masking errors in app.py | Low | Codebase audit | Fixed (PR #102) | 9 | Claude Code |

---

## 4. Stack Profile

| Dependency | Version | Category | Notes |
|-----------|---------|----------|-------|
| Python | 3.12 | Core | Flask application (upgraded Session 9, PR #104) |
| Flask | 2.0.1 | Core | Web framework |
| PostgreSQL | 16 | Core | Database via Docker (upgraded Session 9, PR #104) |
| Docker Compose | V2 | Build | Modernized Session 9, PR #104 |

---

## 5. Session Metrics

| Session | Date | Duration (approx) | PRs | Decisions | Focus Area | Phase | Driver | Operator | Work Category | Tool |
|---------|------|--------------------|-----|-----------|------------|-------|--------|----------|---------------|------|
| 1 | Mar 6 | ~45 min | 2 | 2 | Workflow setup, multi-model coordination | Spec | ai | michael | Planning | Claude Code |
| 2 | Mar 9 | ~20 min | 0 | 0 | Align workflow docs with Meta Tracker data model | Spec | collaborative | michael | Planning | Claude Code |
| 3 | Mar 9 | ~1.5 hr | 1 | 1 | Repo migration, workflow alignment PR, Cursor review intake | Spec | collaborative | michael | Planning | Claude Code |
| 4 | Mar 9 | ~1 hr | 1 | 2 | GitHub Issues POC, coordination guide, workflow doc updates | Spec | collaborative | michael | Planning | Claude Code |
| 5 | Mar 10 | -- | 0 | 0 | .archive/ created, moved obsolete workflow artifacts | Spec | ai | coworker | Planning | Cursor |
| 6 | Mar 10 | -- | 1 | 2 | DRY entry points, created-by labels, codebase audit, 26 issues | Spec | collaborative | michael | Planning | Claude Code |
| 7 | Mar 10 | -- | 1 | 0 | Rebase-on-main in checklist; close issue only when PR merged | Spec | ai | coworker | Planning | Cursor |
| 8 | Mar 10 | -- | 3 | 1 | Fixed 4 bugs, session close-out workflow | Build | collaborative | michael | Bug | Claude Code |
| 8 | Mar 10 | -- | 1 | 0 | SDElements Django profile, survey bias, profile doc | Spec | ai | coworker | Planning | Cursor |
| 9 | Mar 10 | ~30 min | 2 | 1 | Bare exceptions, stale refs, Docker modernization | Build | ai | michael | Bug, Tooling | Claude Code |

### Field Definitions

| Field | Values | Meaning |
|-------|--------|---------|
| **Phase** | Research \u00b7 Spec \u00b7 Build \u00b7 Review \u00b7 Shipped | What project lifecycle phase this session contributed to |
| **Driver** | human \u00b7 ai \u00b7 collaborative | Who steered the work |
| **Operator** | michael \u00b7 hrpatel \u00b7 joint | Which human operator was involved |
| **Work Category** | Feature \u00b7 Refactor \u00b7 Bug \u00b7 Tooling \u00b7 Scripting \u00b7 Data \u00b7 Local-Tooling \u00b7 Planning | Type of work done |
| **Tool** | Claude Code \u00b7 Cursor \u00b7 Mixed | Which AI model did the work |

---

## 6. Multi-Model Activity

| Issue(s) | Model | PR | Lines Changed | Notes |
|----------|-------|----|--------------|-------|
| -- | Claude Code | #1 | +578 | Workflow setup, all docs |
| -- | Claude Code | #2 | +51 | Review request for Cursor |
| #04 | Claude Code | #3 | +111 | Workflow docs alignment (repo migration) |
| -- | Cursor | #5 | +151 | Workflow review and suggestions |
| #05 | Claude Code | #11 | +265 | GitHub Issues coordination guide, POC validation |
| -- | Cursor | -- | -49 | .archive/ created; moved obsolete artifacts |
| -- | Claude Code | #13 | -49 | DRY entry points, serialize workflow changes |
| #49 | Cursor | #50 | +40 | Rebase-on-main step, close-issue-on-merge rule |
| #21,#22,#26,#36 | Claude Code | #53 | +118 | Fix 4 bugs (Commando-X refs, dead SQLite, perms, debug prints) |
| #55 | Claude Code | #56 | -- | Session close-out workflow + split metrics |
| -- | Cursor | #59 | +46 | SDElements profile + assumptions doc |
| #37,#15 | Claude Code | #102 | +6/-6 | Bare exceptions fix, stale index refs |
| #23,#25,#39 | Claude Code | #104 | +18/-12 | Docker modernization (Python 3.12, Compose V2, health checks) |

---

*For use with the Meta Tracker app (meta.jynaxxapps.com)*
