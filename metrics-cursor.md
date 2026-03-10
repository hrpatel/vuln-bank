# Vuln Bank — Cursor Session Metrics

**Owner:** Cursor
**Purpose:** Per-session metrics log. Cursor updates this file at session close-out. Claude Code merges this + `metrics-claude.md` into `metrics.md` (master) and syncs to Meta Tracker.

---

## Sessions

| Session | Date | Duration (approx) | PRs | Decisions | Focus Area | Phase | Driver | Operator | Work Category | Tool | Bugs Fixed |
|---------|------|--------------------|-----|-----------|------------|-------|--------|----------|---------------|------|------------|
| 8 | Mar 10 | -- | 0 | 0 | SDElements: vuln-bank project, Django profile (P5), survey bias (auth/encryption/compliance), profile doc; branch cursor/50 | Spec | ai | coworker | Planning | Cursor | 0 |

## Code Volume

| Session | Date | Lines Added | Lines Deleted | Net Change | Key Files Changed |
|---------|------|-------------|---------------|------------|-------------------|
| 8 | Mar 10 | ~46 | 0 | +46 | STATUS.md, docs/sdelements-profile-and-assumptions.md (new) |

## PR Activity

| Session | Date | PRs Created | PRs Merged | Commits | Notes |
|---------|------|-------------|------------|---------|-------|
| 8 | Mar 10 | 0 | 0 | 1 | cursor/50-sdelements-profile-assumptions: SDE profile + doc; metrics this commit |

## Bugs Found/Fixed

| # | Date Found | Summary | Severity | Source | Resolution | Session Fixed |
|---|-----------|---------|----------|--------|------------|---------------|

---

### Field Reference

These fields must match the Meta Tracker data model for reliable sync.

| Field | Values | Meaning |
|-------|--------|---------|
| **Phase** | Research · Spec · Build · Review · Shipped | Project lifecycle phase |
| **Driver** | human · ai · collaborative | Who steered the work |
| **Operator** | michael · hrpatel · joint | Which human operator |
| **Work Category** | Feature · Refactor · Bug · Tooling · Scripting · Data · Local-Tooling · Planning | Type of work |
| **Tool** | Cursor | Always "Cursor" in this file |
| **Bugs Fixed** | Count or issue numbers | Issues closed as bugs in this session |

---

*Updated at each session close-out. Do not edit `metrics.md` directly — Claude Code merges both model files into the master.*
