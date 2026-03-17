# Beads + Jira Dual-Tracker Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enable Beads as the primary task tracker with one-way sync to Jira for reporting and visibility, per [docs/specs/2026-03-13-beads-jira-dual-tracker-design.md](../specs/2026-03-13-beads-jira-dual-tracker-design.md).

**Architecture:** Update workflow docs and issue-tracker choice so agents use Beads for backlog and execution; document Jira read (for agents) and write (for sync) and placement rules (same epic + link, or ad-hoc epic). No sync implementation in this plan—only documentation and configuration so the workflow is defined and bootstrap is correct.

**Tech Stack:** Markdown docs, Beads (`bd`), Dolt, Jira (API/acli/MCP for read; sync TBD).

---

## File structure

| File | Action | Responsibility |
|------|--------|----------------|
| `.workflow/issue-tracker.md` | Modify | Set "This project uses: Beads"; add dual-tracker note and link to design spec. |
| `.workflow/bootstrap.md` | Modify | In "Choose the issue tracker", add one line that Beads can be used with Jira sync; reference dual-tracker design. |
| `.workflow/beads-coordination.md` | Modify | Add "Beads + Jira" subsection: create from Jira stories, ad-hoc placement, one-way sync, no sub-tasks, link to spec. |
| `.workflow/onboarding.md` | Modify | In "If the project uses Beads", add Jira: read for agents, write for sync; keep gh for PRs. |
| `docs/specs/2026-03-13-beads-jira-dual-tracker-design.md` | Exists | Design spec (no code changes). |
| `STATUS.md` | Modify | Note dual-tracker design and that Beads is primary; Jira for reporting. |

Sync implementation (script or `bd jira` config) is out of scope for this plan; the design doc and coordination guide define the behavior for a future implementation.

---

## Chunk 1: Issue tracker and bootstrap

### Task 1: Set Beads as primary tracker and add dual-tracker note

**Files:**
- Modify: `.workflow/issue-tracker.md`

- [ ] **Step 1: Update "This project uses" and follow-up line**

In `.workflow/issue-tracker.md`, change:

```markdown
**This project uses: GitHub Issues**

→ Follow **[github-issues-coordination.md](github-issues-coordination.md)** to find work, claim tasks, track dependencies, and complete work.
```

to:

```markdown
**This project uses: Beads**

→ Follow **[beads-coordination.md](beads-coordination.md)** to find work, claim tasks, and track dependencies. Implementation work is synced to Jira for reporting and visibility; see [Beads + Jira dual-tracker design](../docs/specs/2026-03-13-beads-jira-dual-tracker-design.md).
```

- [ ] **Step 2: Verify links**

Ensure the relative path to the design spec is correct from `.workflow/` (e.g. `../docs/specs/2026-03-13-beads-jira-dual-tracker-design.md` if docs is at repo root). Adjust if your repo layout differs.

- [ ] **Step 3: Commit**

```bash
git add .workflow/issue-tracker.md
git commit -m "chore: set Beads as primary tracker, add dual-tracker design link"
```

---

### Task 2: Update bootstrap for Beads + Jira option

**Files:**
- Modify: `.workflow/bootstrap.md`

- [ ] **Step 1: Add Beads + Jira sync to the tracker table**

In `.workflow/bootstrap.md`, in section "1. Choose the issue tracker", update the Beads row so it’s explicit that Beads can be used with Jira sync. Change the table row for Beads from:

```markdown
|| **Beads** | Local, dependency-aware task graph; optional Jira sync; good for agents and branching. |
```

to (no table change needed; ensure the description is clear). Add one sentence after the table:

```markdown
When using Beads with Jira sync (Beads for execution, Jira for reporting), see [Beads + Jira dual-tracker design](../docs/specs/2026-03-13-beads-jira-dual-tracker-design.md) and ensure the coordination guide and onboarding reflect Jira read/write.
```

- [ ] **Step 2: Commit**

```bash
git add .workflow/bootstrap.md
git commit -m "docs: bootstrap note for Beads + Jira dual-tracker"
```

---

## Chunk 2: Beads coordination and onboarding

### Task 3: Add Beads + Jira subsection to beads-coordination.md

**Files:**
- Modify: `.workflow/beads-coordination.md`

- [ ] **Step 1: Insert subsection after "How It Works" (or after "Beads Is the Local Task Layer")**

Add a new subsection **"Beads + Jira (this project)"** (or **"Beads + Jira sync"**) that covers:

1. Agents create implementation tasks in Beads from Jira stories (external ref to story).
2. Ad-hoc tasks: if found during work on a story, use that story’s epic; otherwise use the configured ad-hoc epic.
3. Sync is one-way Beads → Jira; no sub-tasks—all synced work is standalone Jira issues (same epic + link to story, or ad-hoc epic).
4. Link to the full design: `docs/specs/2026-03-13-beads-jira-dual-tracker-design.md`.

Suggested text (insert after the "Beads Is the Local Task Layer" block, before "Modes"):

```markdown
### Beads + Jira (this project)

This project uses Beads as the primary backlog with one-way sync to Jira for reporting and visibility.

- **From Jira:** Agents read epics/stories/Gherkin from Jira and create implementation tasks in Beads with `--external-ref jira-PROJ-<story-id>`.
- **Ad-hoc tasks:** Created during implementation go in the same epic as the story you’re working on; standalone ad-hoc tasks go in the configured ad-hoc epic.
- **Sync (Beads → Jira):** One-way only. All synced work appears as **standalone Jira issues** (no sub-tasks): same epic as the story + issue link to the story, or ad-hoc epic.

Full design: [Beads + Jira dual-tracker design](../docs/specs/2026-03-13-beads-jira-dual-tracker-design.md).
```

- [ ] **Step 2: Fix relative path if needed**

From `.workflow/beads-coordination.md`, the path to the spec is `../docs/specs/2026-03-13-beads-jira-dual-tracker-design.md` (one level up from `.workflow/` to repo root, then into docs/specs/).

- [ ] **Step 3: Commit**

```bash
git add .workflow/beads-coordination.md
git commit -m "docs: add Beads + Jira subsection to beads-coordination"
```

---

### Task 4: Onboarding — Jira read/write and Beads

**Files:**
- Modify: `.workflow/onboarding.md`

- [ ] **Step 1: Add Jira requirements under "If the project uses Beads"**

In `.workflow/onboarding.md`, in the "If the project uses Beads" section, after the Beads/Dolt install and verify steps, add:

- **Jira (when using Beads + Jira sync):** Agents need **Jira read** access (to fetch epics, stories, Gherkin). The sync process (run locally or in CI) needs **Jira write** access to create/update issues. Use acli (`acli auth`) or Jira API tokens as appropriate. GitHub CLI (`gh`) is still required for PRs.

Suggested insertion (after "**Verify:** `bd --version`...", before "### If the project uses Jira"):

```markdown
When this project uses **Beads with Jira sync** (see [dual-tracker design](../docs/specs/2026-03-13-beads-jira-dual-tracker-design.md)):
- **Jira read:** Required for agents (epics, stories, Gherkin). Use acli (`acli auth`), Jira MCP, or REST with credentials.
- **Jira write:** Required only where sync runs (local or CI) to create/update Jira issues from Beads. GitHub CLI (`gh`) remains required for PRs.
```

Path from `.workflow/onboarding.md` to spec: `../docs/specs/2026-03-13-beads-jira-dual-tracker-design.md`. If the repo root is one level up from `.workflow/`, use that; if docs lives elsewhere, adjust.

- [ ] **Step 2: Commit**

```bash
git add .workflow/onboarding.md
git commit -m "docs: onboarding Jira read/write for Beads + Jira"
```

---

## Chunk 3: STATUS and handoff

### Task 5: Update STATUS.md

**Files:**
- Modify: `STATUS.md`

- [ ] **Step 1: Add a short "Workflow" or "Tracker" note**

In `STATUS.md`, add a line or two under the existing "Team" or "Recent Work" context that the project uses Beads as the primary tracker with Jira sync for reporting, and link to the design spec. Example (adjust to fit existing structure):

```markdown
**Tracker:** Beads (primary); implementation work is synced to Jira for reporting and visibility. See [Beads + Jira dual-tracker design](docs/specs/2026-03-13-beads-jira-dual-tracker-design.md).
```

- [ ] **Step 2: Commit**

```bash
git add STATUS.md
git commit -m "docs: STATUS note Beads + Jira dual-tracker"
```

---

## Execution handoff

When all tasks are done:

1. Rebase on main if needed; push branch.
2. Open a PR that summarizes the doc and workflow updates (no code; no sync implementation yet).
3. After merge, operators can run `bd init` (or `bd init --stealth`) and configure Jira read/write per onboarding. Sync implementation can follow in a later plan.

---

**Plan complete and saved to `docs/plans/2026-03-13-beads-jira-dual-tracker.md`. Ready to execute?**
