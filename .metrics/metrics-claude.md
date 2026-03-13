# Vuln Bank — Claude Code Session Metrics

**Owner:** Claude Code
**Purpose:** Per-session metrics log. Claude Code updates this file at session close-out. Claude Code merges this + `metrics-cursor.md` into `metrics.md` (master, in this directory) and syncs to Meta Tracker.

---

## Sessions

| Session | Date | Duration (approx) | PRs | Decisions | Focus Area | Phase | Driver | Operator | Work Category | Tool | Bugs Fixed |
|---------|------|--------------------|-----|-----------|------------|-------|--------|----------|---------------|------|------------|
| 8 | Mar 10 | -- | 3 | 1 | Fixed 4 bugs (#21, #22, #26, #36), Meta Tracker sync, session close-out workflow (#55) | Build | collaborative | michael | Bug | Claude Code | #21, #22, #26, #36 |
| 9 | Mar 10 | ~30 min | 2 | 1 | Bare exception fix (#37), stale refs (#15), Docker modernization (#23, #25, #39), closed #52 #16 | Build | ai | michael | Bug, Tooling | Claude Code | #37 |

## Code Volume

| Session | Date | Lines Added | Lines Deleted | Net Change | Key Files Changed |
|---------|------|-------------|---------------|------------|-------------------|
| 8 | Mar 10 | 159 | 41 | +118 | README.md, app.py, auth.py, Dockerfile, openapi.json, index.html, metrics-claude.md, metrics-cursor.md, START HERE.md, How We Work.md, metrics.md |
| 9 | Mar 10 | 24 | 18 | +6 | app.py, How We Work.md, Dockerfile, docker-compose.yml, README.md |

## PR Activity

| Session | Date | PRs Created | PRs Merged | Commits | Notes |
|---------|------|-------------|------------|---------|-------|
| 8 | Mar 10 | 1 | -- | 2 | PR #53: Fix 4 bugs (Commando-X refs, debug prints, dead SQLite, upload perms) |
| 8 | Mar 10 | 1 | 1 | 1 | PR #56: Session close-out workflow + split metrics files (#55) |
| 9 | Mar 10 | 2 | 2 | 2 | PR #102: Bare exceptions + stale refs (#37, #15). PR #104: Docker modernization (#23, #25, #39) |

## Bugs Found/Fixed

| # | Date Found | Summary | Severity | Source | Resolution | Session Fixed |
|---|-----------|---------|----------|--------|------------|---------------|
| #21 | Mar 10 | Commando-X repo references throughout codebase | Medium | Codebase audit | Fixed (PR #53) | 8 |
| #22 | Mar 10 | Dead SQLite code in auth.py — 3 endpoints crash at runtime | High | Codebase audit | Fixed (PR #53) | 8 |
| #26 | Mar 10 | Overly permissive uploads directory (chmod 777) | Low | Codebase audit | Fixed (PR #53) | 8 |
| #36 | Mar 10 | Debug prints exposing usernames, SQL queries, JWT tokens | Medium | Codebase audit | Fixed (PR #53) | 8 |

---

### Field Reference

These fields must match the Meta Tracker data model for reliable sync.

| Field | Values | Meaning |
|-------|--------|---------|
| **Phase** | Research · Spec · Build · Review · Shipped | Project lifecycle phase |
| **Driver** | human · ai · collaborative | Who steered the work |
| **Operator** | michael · hrpatel · joint | Which human operator |
| **Work Category** | Feature · Refactor · Bug · Tooling · Scripting · Data · Local-Tooling · Planning | Type of work |
| **Tool** | Claude Code | Always "Claude Code" in this file |
| **Bugs Fixed** | Count or issue numbers | Issues closed as bugs in this session |

---

*Updated at each session close-out. Do not edit the master file in this directory (`metrics.md`) — Claude Code merges both model files into it.*
