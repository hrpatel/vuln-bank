# Vuln Bank — Project Metrics

## Project Metadata

| Field | Value |
|-------|-------|
| **Project Name** | Vuln Bank |
| **Repository** | https://github.com/hrpatel/vuln-bank |
| **Tracking Since** | March 6, 2026 |
| **Last Updated** | March 9, 2026 (Session 4) |

---

## 1. Code Volume

| Session | Date | Lines Added | Lines Deleted | Net Change | Key Files Changed |
|---------|------|-------------|---------------|------------|-------------------|
| 1 | Mar 6 | 629 | 0 | +629 | Workflow setup (non-code) |
| 4 | Mar 9 | 323 | 58 | +265 | .workflow/github-issues-coordination.md, CLAUDE.md, .cursorrules, How We Work.md, START HERE.md, decisions.md |

---

## 2. PR & Commit Activity

| Session | Date | PRs Created | PRs Merged | Commits | Model | Est. Time | Actual Time | Notes |
|---------|------|-------------|------------|---------|-------|-----------|-------------|-------|
| 1 | Mar 6 | 1 | -- | 3 | Claude Code | 30 min | ~25 min | PR #1: Workflow setup |
| 1 | Mar 6 | 1 | -- | 1 | Claude Code | 10 min | ~10 min | PR #2: Review request |
| 3 | Mar 9 | 1 | 1 | 2 | Claude Code | -- | -- | PR #3: Workflow alignment (9 files) |
| 4 | Mar 9 | 1 | -- | 1 | Claude Code | -- | ~1 hr | PR #11: GitHub Issues coordination guide + workflow updates (6 files) |

---

## 3. Bug Tracking

| # | Date Found | Summary | Severity | Source | Resolution | Session Fixed |
|---|-----------|---------|----------|--------|------------|---------------|

---

## 4. Stack Profile

| Dependency | Version | Category | Notes |
|-----------|---------|----------|-------|
| Python | 3.x | Core | Flask application |
| Flask | -- | Core | Web framework |
| SQLite | -- | Core | Database |
| Docker | -- | Build | Containerization |

---

## 5. Session Metrics

| Session | Date | Duration (approx) | PRs | Decisions | Focus Area | Phase | Driver | Operator | Work Category | Tool |
|---------|------|--------------------|-----|-----------|------------|-------|--------|----------|---------------|------|
| 1 | Mar 6 | ~45 min | 2 | 2 | Workflow setup, multi-model coordination | Spec | ai | michael | Planning | Claude Code |
| 2 | Mar 9 | ~20 min | 0 | 0 | Align workflow docs with Meta Tracker data model | Spec | collaborative | michael | Planning | Claude Code |
| 3 | Mar 9 | ~1.5 hr | 1 | 1 | Repo migration, workflow alignment PR, Cursor review intake | Spec | collaborative | michael | Planning | Claude Code |
| 4 | Mar 9 | ~1 hr | 1 | 2 | GitHub Issues POC, coordination guide, workflow doc updates | Spec | collaborative | michael | Planning | Claude Code |

### Field Definitions

These fields align with the Meta Tracker data model so sessions feed directly into the dashboard.

| Field | Values | Meaning |
|-------|--------|---------|
| **Phase** | Research · Spec · Build · Review · Shipped | What project lifecycle phase this session contributed to |
| **Driver** | human · ai · collaborative | Who steered the work — the human operator, the AI model, or both actively |
| **Operator** | michael · hrpatel · joint | Which human operator was involved |
| **Work Category** | Feature · Refactor · Bug · Tooling · Scripting · Data · Local-Tooling · Planning | Type of work done |
| **Tool** | Claude Code · Cursor · Mixed | Which AI model did the work |

---

## 6. Multi-Model Activity

| Task # | Model | PR | Lines Changed | Notes |
|--------|-------|----|--------------|-------|
| -- | Claude Code | #1 | +578 | Workflow setup, all docs |
| -- | Claude Code | #2 | +51 | Review request for Cursor |
| 04 | Claude Code | (on PR #1) | +108 | Data model alignment for workflow docs |
| 04 | Claude Code | #3 | +111 | Workflow docs alignment (repo migration) |
| -- | Cursor | #5 | +151 | Workflow review and suggestions |
| 05 | Claude Code | #11 | +265 | GitHub Issues coordination guide, POC validation, workflow doc updates |

Both models should log their work here so activity across Claude Code and Cursor is visible in one place.

---

*For use with the Meta Tracker app (meta.jynaxxapps.com)*
