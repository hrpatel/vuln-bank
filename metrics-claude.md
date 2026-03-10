# Vuln Bank — Claude Code Session Metrics

**Owner:** Claude Code
**Purpose:** Per-session metrics log. Claude Code updates this file at session close-out. Claude Code merges this + `metrics-cursor.md` into `metrics.md` (master) and syncs to Meta Tracker.

---

## Sessions

| Session | Date | Duration (approx) | PRs | Decisions | Focus Area | Phase | Driver | Operator | Work Category | Tool | Bugs Fixed |
|---------|------|--------------------|-----|-----------|------------|-------|--------|----------|---------------|------|------------|

## Code Volume

| Session | Date | Lines Added | Lines Deleted | Net Change | Key Files Changed |
|---------|------|-------------|---------------|------------|-------------------|

## PR Activity

| Session | Date | PRs Created | PRs Merged | Commits | Notes |
|---------|------|-------------|------------|---------|-------|

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
| **Tool** | Claude Code | Always "Claude Code" in this file |
| **Bugs Fixed** | Count or issue numbers | Issues closed as bugs in this session |

---

*Updated at each session close-out. Do not edit `metrics.md` directly — Claude Code merges both model files into the master.*
