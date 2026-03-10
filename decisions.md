# Vuln Bank — Decision Log

## Project Metadata

| Field | Value |
|-------|-------|
| **Project Name** | Vuln Bank |
| **Repository** | https://github.com/hrpatel/vuln-bank |
| **Live URL** | N/A (local Docker) |
| **Tech Stack** | Python, Flask, PostgreSQL, HTML/CSS/JS |
| **Started** | March 2026 |
| **Status** | Active |
| **Primary AI Tools** | Claude Code, Cursor |

---

## How to Log Decisions

Each entry uses a structured format that feeds into Meta Tracker's decision tree. The key fields:

| Field | Values | When to Use |
|-------|--------|-------------|
| **Type** | decision · event · dead-end · discovery · pivot | What kind of entry this is |
| **Category** | technical · functional · ux-design · process | What domain it belongs to |
| **Chosen path** | Free text | What we actually did (decisions/pivots only) |
| **Alternatives** | List | What else we considered (decisions/pivots only) |
| **Failure reason** | Free text | Why it didn't work (dead-ends only) |

Both models should log decisions — not just the model that made them. If Cursor discovers something important, log it here.

---

## Entries

### Getting Organized

**Summary:** Setting up workflow and coordination for multi-model collaboration
**Sessions:** 1
**Phase:** Spec
**AI Tools:** Claude Code

---

#### Multi-Model Coordination Protocol
- **Type:** decision
- **Category:** process
- **Context:** Two AI models (Claude Code and Cursor) need to work on the same repo in parallel without stepping on each other.
- **Chosen path:** Task index coordination with branch prefixes and file-level conflict detection
- **Alternatives:** (1) Domain separation (backend vs frontend ownership) — too rigid. (2) Sequential turns — too slow, kills parallelism. (3) Forking the repo per model — too much overhead to sync.
- **Why this path:** Uses existing task tracking infrastructure. File-level conflict detection is simple and sufficient. Branch prefixes make ownership visible. The task index is the single coordination point.
- **Outcome:** Implemented in PR #1

#### Workflow Documentation in Repo
- **Type:** decision
- **Category:** process
- **Context:** Both models need access to the workflow system. Cursor reads from the repo; Claude Code reads from CLAUDE.md and repo files.
- **Chosen path:** Shared .workflow/ docs with model-specific entry points (.cursorrules, CLAUDE.md)
- **Alternatives:** (1) External docs only. (2) Single shared config file.
- **Why this path:** Each model has its own entry point (`.cursorrules` vs `CLAUDE.md`) but shares the same workflow docs. No duplication of process rules.
- **Outcome:** Implemented in PR #1

---

#### Repo Migration — Remove Fork Association
- **Type:** decision
- **Category:** process
- **Context:** hrpatel/vuln-bank was a fork of Commando-X/vuln-bank. Git tooling (gh) auto-created PRs against the upstream repo, leaking work to a public project.
- **Chosen path:** Delete the fork, recreate as a standalone repo, re-push all content
- **Alternatives:** (1) Remove upstream remote only — doesn't fix the GitHub fork association. (2) Keep the fork and be careful — too error-prone.
- **Why this path:** Clean break eliminates the risk entirely. All content was backed up locally before deletion.
- **Outcome:** New standalone repo at same URL, PR #3 re-created successfully, no data lost

---

### Solving Coordination Gaps

**Summary:** Replacing file-based task coordination with GitHub Issues after Cursor identified critical visibility gap
**Sessions:** 33, 34
**Phase:** Spec
**AI Tools:** Claude Code

---

#### GitHub Issues Replace Task Index as Coordination Layer
- **Type:** decision
- **Category:** process
- **Context:** Cursor's workflow review (March 9) identified that the task index (`tasks/index.md`) is broken as a coordination mechanism. Both models update it on their own branches, so neither can see the other's claims. The file-level conflict detection system — the centerpiece of the coordination protocol — has a visibility gap. Additionally: no atomicity on task claiming (race condition), no staleness detection for abandoned claims, no cross-model communication channel, and scope expansion is not signaled.
- **Chosen path:** GitHub Issues as the full coordination system. Issues are the live, real-time layer. Task files become archival snapshots saved to `tasks/done/` when issues close (for portfolio/offline reference).
- **Alternatives:** (1) Exempt `tasks/index.md` from no-direct-push rule — still has race conditions on concurrent pushes, creates precedent hole. (2) Draft PR on claim as secondary signal — weak, does not solve race condition, clutters PR list. (3) Hybrid: Issues for status, task files for specs — splits source of truth across two systems. (4) Keep current system and rely on verbal operator coordination — fragile, does not scale.
- **Why this path:** GitHub Issues are branch-independent by design, eliminating the visibility gap entirely. GitHub's native dependency tracking (GA August 2025) and sub-issues (GA 2025) provide exactly the chain/blocking semantics needed. Assignment is atomic (no race condition). Comments provide cross-model signaling. Timestamps provide staleness detection. One source of truth, not two.

#### POC Validation Results (Session 34)
- **Type:** event
- **Category:** process
- **Context:** Built a test chain (parent issue #7 with 3 sub-issues #8-#10) to validate every feature of the design.
- **Results:**
  - Labels: create, assign, swap — all work via PATCH
  - Sub-issues: link via POST with `-F sub_issue_id={id}` (must be integer). Parent shows automatic progress roll-up (e.g., 1/3 = 33%)
  - Dependencies: link via `POST /issues/{N}/dependencies/blocked_by` with `-F issue_id={id}`. Dependency data includes blocker state (open/closed)
  - Assignment (claiming): atomic, visible immediately
  - Cross-model signaling: comments are timestamped and branch-independent
  - **Key finding:** Closing a blocker does NOT auto-update downstream labels. Label flipping (blocked -> available) is a manual step for the completing model. Typically 2-3 API calls.
  - **Key finding:** Issue ID (large integer from API response) vs issue number (#8) — sub-issue and dependency APIs require the ID, not the number
  - **Key finding:** Fine-grained PATs need explicit "Issues: Read and write" permission for label and assignment updates
- **Outcome:** All design assumptions validated. Guide written to `.workflow/github-issues-coordination.md`. Workflow docs updated. Ready for Cursor and operators to review.

### Workflow Refinements

**Summary:** DRY up workflow docs, add issue attribution, codebase audit
**Sessions:** 5
**Phase:** Spec
**AI Tools:** Claude Code

---

#### DRY Up Entry Points (Cursor Suggestion #5)
- **Type:** decision
- **Category:** process
- **Context:** Cursor's workflow review identified that `CLAUDE.md` and `.cursorrules` both restated the same rules (coordination, conflict avoidance, tracking, code changes), creating drift risk as both models edit them over time.
- **Chosen path:** Slim both entry points to model-specific settings only (~32 lines each, down from ~60). All shared rules live in `.workflow/` as the single source of truth.
- **Alternatives:** (1) Keep duplication and manually sync — error-prone and unsustainable. (2) Single shared config — doesn't work because each model needs its own entry point file.
- **Why this path:** Eliminates duplication entirely. Each model still has its own entry point with model-specific info (name, operator, branch prefix, label) but reads shared rules from one place.
- **Outcome:** Implemented in PR #13

#### Serialize Workflow Doc Changes (Cursor Suggestion #8)
- **Type:** decision
- **Category:** process
- **Context:** Cursor flagged that workflow docs (`.cursorrules`, `CLAUDE.md`, `.workflow/` files) are themselves a conflict surface. If one model updates workflow while the other follows it, behavior becomes unpredictable.
- **Chosen path:** Explicit rule in `How We Work.md`: changes to entry points or `.workflow/` files are always single-model, serialized operations. Never parallel.
- **Alternatives:** (1) No rule, rely on operators to coordinate verbally — fragile. (2) Lock workflow files to one model — too restrictive.
- **Why this path:** Simple, low-overhead rule that prevents the specific problem without over-constraining.
- **Outcome:** Implemented in PR #13

#### Created-By Labels for Issue Attribution
- **Type:** decision
- **Category:** process
- **Context:** Needed a way to track which AI model created each GitHub Issue, separate from which model works on it. The existing `claude-code` and `cursor` labels track ownership/assignment.
- **Chosen path:** New `created-by:claude-code` and `created-by:cursor` labels, applied at issue creation time. Documented in coordination guide.
- **Alternatives:** (1) Use issue body text to note creator — not filterable. (2) Use assignee — conflicts with "who's working on it."
- **Why this path:** Labels are filterable, visible at a glance, and don't conflict with the existing ownership labels.
- **Outcome:** Labels created, coordination guide updated, applied to all 26 issues from codebase audit.

---

## Appendix: Entry Types

| Type | Use When |
|------|----------|
| **decision** | A deliberate choice between alternatives |
| **event** | Something noteworthy happened (milestone, external change) |
| **dead-end** | An approach was tried and abandoned |
| **discovery** | Something was learned that changed understanding |
| **pivot** | Direction changed mid-task |

## Appendix: Glossary

| Term | Meaning |
|------|---------|
| Vuln Bank | The deliberately vulnerable banking app |
| Claude Code | AI model operated via CLI by Michael |
| Cursor | AI model operated via IDE by coworker |
| Task Index | `tasks/index.md` — the coordination point for parallel work |
| Meta Tracker | Dashboard that visualizes project decisions and metrics (meta.jynaxxapps.com) |

---

*For use with the Meta Tracker app (meta.jynaxxapps.com)*
