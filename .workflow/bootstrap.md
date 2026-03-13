# Workflow Bootstrap — One-Time Project Setup

Use this checklist **once** when setting up multi-model AI collaboration on a new repo (or when changing how the project tracks work). After this, agents and operators follow the workflow in START HERE and the coordination guide chosen below.

**New to this repo?** Complete [onboarding.md](onboarding.md) first (git, GitHub CLI, and any tracker-specific tools for macOS or WSL). Then return here for project-level setup.

---

## 1. Choose the issue tracker

Decide where tasks will live so **all** agents and operators look in the same place:

| Option | Use when |
|--------|----------|
| **GitHub Issues** | Work is coordinated in this repo; labels, assignees, and PR linking matter. |
| **Jira** | Work is driven by an existing Jira project (epics, stories); team already uses Jira. |
| **Beads** | Local, dependency-aware task graph; optional Jira sync; good for agents and branching. |

**Set the choice:** Edit [.workflow/issue-tracker.md](issue-tracker.md). Set the line “This project uses:” to **GitHub Issues**, **Jira**, or **Beads**, and leave the rest of the file as-is (it already links to the right coordination guide).

---

## 2. Ensure the coordination guide exists

- **GitHub Issues:** [github-issues-coordination.md](github-issues-coordination.md) — repo-specific (e.g. `hrpatel/vuln-bank`); update repo references if you copy to another project.
- **Jira:** [jira-coordination.md](jira-coordination.md) — set project key and any Jira-specific conventions.
- **Beads:** [beads-coordination.md](beads-coordination.md) — run `bd init` (or `bd init --stealth`) in the repo; add “Use 'bd' for task tracking” to AGENTS.md if you use it.

---

## 3. Entry points

Ensure each agent has an entry point that points at the workflow:

- **CLI agents:** [CLAUDE.md](../CLAUDE.md) (or equivalent) — “Read this file, then .workflow/START HERE.md.”
- **Cursor:** [.cursorrules](../.cursorrules) — same.

START HERE and the entry points tell agents to read **issue-tracker.md** first, then follow the linked coordination guide. No further bootstrap steps needed per session.

---

## 4. Optional: Gherkin and Jira/Beads

If requirements will be written in Gherkin or you use Jira/Beads:

- See [gherkin-requirements.md](gherkin-requirements.md) for where to put feature files and how agents should generate them.
- Jira and Beads coordination docs describe multi-model claiming and signaling; no extra bootstrap step beyond choosing the tracker in step 1.

---

*After bootstrap, session start is: read entry point → read START HERE → read issue-tracker.md → follow the linked coordination guide.*
