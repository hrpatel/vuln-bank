# Beads + Jira Dual-Tracker Design

**Date:** 2026-03-13  
**Status:** Design approved  
**Summary:** Use Beads for local, dependency-aware implementation work and sync to Jira for reporting, auditability, and visibility. No Jira sub-tasks; all synced work appears as standalone Jira issues with epic placement and optional story links.

---

## 1. Roles and high-level flow

### Jira

- **Owned by PM:** Epics, stories, Gherkin (in story description or linked Confluence).
- **Read by agents:** Source of “what to build” (epic → stories → Gherkin steps).
- **Written by sync (Beads → Jira):** Implementation tickets created in Beads appear in Jira as **standalone issues** (no sub-tasks). Placement: same epic as the source story, or ad-hoc epic. Traceability via issue links to the originating story where applicable.

### Beads

- **Owned by agents (and optionally devs):** Implementation tasks created from Jira stories/Gherkin; dependencies between tasks; claiming and progress (`bd ready`, `bd update --claim`, `bd close`).
- **Source of truth for implementation:** Task graph, status, and assignees live in Beads; Jira is updated by a one-way sync.

### Flow

PM defines work in Jira → agents read Jira, create implementation tasks in Beads (with deps), work in Beads → sync pushes Beads implementation tasks to Jira as standalone issues (epic + link to story when applicable) so they are visible and auditable.

**Out of scope:** Replacing or duplicating GitHub Issues for PR/merge workflow (e.g. “Fixes #N”). Beads + Jira is for planning and implementation tracking; PR coordination can remain on GitHub as today.

---

## 2. Data flow

### Jira → agents (read)

- Agents use Jira API (acli, MCP, or REST) to read epics, child stories, and story fields (title, description, Gherkin).
- Optional: a script or MCP tool that “lists Jira stories ready for implementation” (by status/label/sprint) as a single entry point for agents.

### Agents → Beads (create)

- **From Jira:** For a chosen story, the agent creates Beads implementation tasks, adds dependencies with `bd dep`, and sets `--external-ref jira-PROJ-<story-id>` (or equivalent) so sync can place the issue in the same epic and link to the story.
- **Local / ad-hoc:** During implementation, agents or humans create tasks in Beads with no Jira story ref (bugs, enhancements, chores). Optionally set a “related story” ref so the task is placed in that story’s epic (see placement rules below).

### Beads → Jira (sync)

- **Tasks with a Jira story external ref:** Sync creates/updates a **standalone Jira issue** (no sub-tasks). Issue is placed in the **same epic** as that story. An **issue link** is created from the new issue to the Jira story (e.g. “Relates to”, “Implements”—link type TBD per project).
- **Tasks with “related story” ref (ad-hoc found during work):** Same: standalone issue in the **same epic** as the story; optionally link to the story.
- **Tasks with no Jira ref (standalone ad-hoc):** Sync creates/updates a standalone issue under the **placeholder / ad-hoc epic**.

All synced work is standalone Jira issues only; no sub-tasks are used.

---

## 3. Placement rules (summary)


| Beads task type           | External ref in Beads   | Jira result                                                               |
| ------------------------- | ----------------------- | ------------------------------------------------------------------------- |
| Implementation of a story | Story ID                | Standalone issue in **same epic** as story; **link** to that story        |
| Ad-hoc, found during work | Story ID (related epic) | Standalone issue in **same epic** as that story; optionally link to story |
| Ad-hoc, no related epic   | None or “adhoc”         | Standalone issue in **placeholder / ad-hoc epic**                         |


Convention for “sub-task vs same-epic” is unnecessary: we never create sub-tasks. “Story ref” always means: same epic + link to story.

---

## 4. Agent workflow

### Discovering work

- **From Jira:** Agent lists “stories ready for implementation” (status/label/sprint). For each chosen story, reads title, description, Gherkin.
- **From Beads:** Agent runs `bd ready`, claims with `bd update <id> --claim`. Tasks may be story-derived or local.

### Creating implementation tasks from a Jira story

1. Agent fetches story (and Gherkin) from Jira.
2. Agent creates one or more Beads tasks with `--external-ref jira-PROJ-<story-id>`.
3. Agent adds dependencies with `bd dep` where order matters.
4. Optionally claims the first task and starts work.

### Creating local tasks (bug, enhancement, chore)

- **Found during implementation of a story:** Create Beads task with external ref to that story (so sync places issue in same epic and can link to story).
- **No related epic:** Create with no ref (or “adhoc”); sync places in placeholder/ad-hoc epic.

### During and after work

- All execution state in Beads: claim, update, close. Sync (on schedule or on-demand) creates/updates Jira issues so Jira reflects current state for reporting and audit.

---

## 5. Sync design (Beads → Jira)

### Direction and scope

- One-way: Beads is source of truth; sync only writes to Jira (create/update). No read-back from Jira into Beads for implementation state.
- Sync all Beads tasks that should be visible (story-derived and ad-hoc). Optional filter by Beads type/label if needed.

### When sync runs

- **On-demand:** Script or `bd sync` (or equivalent) after agent/human work.
- **Scheduled (optional):** Cron or CI job so Jira stays near real-time.
- Design supports both; minimum is on-demand.

### Field mapping (Beads → Jira)


| Beads               | Jira                                                                      |
| ------------------- | ------------------------------------------------------------------------- |
| Task ID (e.g. bd-x) | Stored in Jira (custom field or parseable in description) for idempotency |
| Title               | Summary                                                                   |
| Description         | Description                                                               |
| Status              | Map to Jira status (To Do, In Progress, Done)                             |
| Assignee            | Assignee if Jira user exists; else unassigned or default                  |
| External ref        | Drives placement (same epic + link, or ad-hoc epic)                       |


### Placement (no sub-tasks)

- **Story ref present:** Create/update **standalone issue**; set epic = story’s epic; create **issue link** to the Jira story (link type per project).
- **No ref (or ad-hoc):** Create/update **standalone issue** under **placeholder / ad-hoc epic**. Epic key/ID is configured (env or config).

### Idempotency

- **Match key:** Beads task ID stored in Jira. Each run: lookup by Beads ID; if found, update; if not, create and store Beads ID in Jira. No duplicate Jira issues per Beads task.

### Ad-hoc epic

- Single Jira epic for “no related epic” work (e.g. “Vuln Bank – Ad-hoc”). Epic key/ID configured once. Prefer operator-created epic; sync only references it.

### Failure and safety

- Sync is retryable; no delete of Jira issues by sync. Closing a Beads task only updates Jira status to Done (or equivalent).

---

## 6. Operational and edge cases

### issue-tracker.md and primary tracker

- Set **Beads** as the coordination source for agents: “This project uses: **Beads**” with link to `beads-coordination.md`.
- Add note: “Implementation work is tracked in Beads and synced to Jira for reporting and visibility; see dual-tracker design (docs/specs/2026-03-13-beads-jira-dual-tracker-design.md).”
- **GitHub Issues:** Continue using for PR workflow; no requirement to migrate existing Issues into Beads or Jira.

### Multi-agent

- Beads atomic claiming and `bd ready` unchanged. Both agents use same Beads DB (team mode). When creating tasks (from story or ad-hoc), agents follow placement rules (story ref → same epic + link; no ref → ad-hoc epic).

### Onboarding

- **Required:** Git, GitHub CLI, Beads, Dolt. **Jira:** read access for agents (epics/stories/Gherkin); write access for sync (where sync runs). Document in `.workflow/onboarding.md`.
- Sync credentials only needed where sync runs (local or CI); agents need only Jira read (or MCP/acli read).

### Bootstrap and coordination guide

- **Bootstrap:** “Choose the issue tracker” → Beads (with Jira sync). Ensure `issue-tracker.md` and coordination guide reference this design.
- **beads-coordination.md:** Add (or extend with) Beads + Jira: (1) create implementation tasks in Beads from Jira stories; (2) ad-hoc → same epic or ad-hoc epic; (3) sync is one-way Beads → Jira; (4) no sub-tasks; (5) link to this spec.

### Tools and automation

- **Jira read:** acli, Jira MCP, or REST; optional “stories ready for implementation” helper.
- **Sync:** Script or `bd jira` (if it supports this mapping). Config: Jira project, ad-hoc epic key, credentials; optional schedule.

---

## Document history


| Date       | Change                                                                             |
| ---------- | ---------------------------------------------------------------------------------- |
| 2026-03-13 | Initial design: Beads + Jira dual-tracker, no sub-tasks, placement and sync rules. |


