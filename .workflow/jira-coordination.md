# Jira Coordination Guide

**Jira is used for epics, stories, and tickets that originate or live in the cloud.** This guide covers how to work with Jira from the command line using the Atlassian CLI (`acli`). It does not describe Beads or Beads↔Jira sync; for local task tracking see `.workflow/beads-coordination.md`.

> **When to use Jira here:** Requirements and work items that are created in Jira (epics, stories, bugs), or that need to stay in sync with a team board. Use `acli` for search, view, create, transition, and link.

---

## How It Works

### acli (Atlassian CLI)

- **Auth:** Run `acli auth` once to authenticate to your Atlassian Cloud site.
- **Scope:** Commands are under `acli jira` (and optionally `acli confluence`). This doc focuses on Jira work items.
- **Project:** Replace `PROJ` (or your project key) in examples with your actual Jira project key.

---

## Setup

### Authenticate

```bash
acli auth
```

Follow the prompts to log in to your Atlassian Cloud instance. Credentials are stored for subsequent commands.

### Verify

```bash
acli jira project list
# or
acli jira workitem search --jql "project = PROJ" --limit 5
```

---

## Workflow

### Search for Work Items

```bash
# By JQL (replace PROJ with your project key)
acli jira workitem search --jql "project = PROJ"
acli jira workitem search --jql "project = PROJ AND status = 'To Do'" --limit 20
acli jira workitem search --jql "project = PROJ AND type = Epic" --paginate

# Count only
acli jira workitem search --jql "project = PROJ" --count

# Specific fields, JSON or CSV
acli jira workitem search --jql "project = PROJ" --fields "key,summary,status,assignee" --json
acli jira workitem search --jql "project = PROJ" --csv
```

### View a Single Work Item

```bash
acli jira workitem view PROJ-123
acli jira workitem view PROJ-123 --fields summary,description,comment
acli jira workitem view PROJ-123 --json
acli jira workitem view PROJ-123 --web   # Open in browser
```

### Create a Work Item

```bash
acli jira workitem create --help   # See required/optional fields for your instance
```

Use the help output to see the exact flags (e.g. project, type, summary, description). Create in bulk with `acli jira workitem create-bulk` if supported.

### Transition Status

```bash
acli jira workitem transition --help
```

Use the help to see how to move an issue (e.g. To Do → In Progress → Done). Transitions are workflow-dependent per project.

### Other Operations

- **Assign:** `acli jira workitem assign --help`
- **Edit:** `acli jira workitem edit --help`
- **Link:** `acli jira workitem link --help`
- **Comment:** `acli jira workitem comment --help`

Run `acli jira workitem <subcommand> --help` for each for exact usage.

---

## Commands Quick Reference

| Action | Command |
|--------|---------|
| Search | `acli jira workitem search --jql "project = PROJ"` |
| View one | `acli jira workitem view KEY-123` |
| View in browser | `acli jira workitem view KEY-123 --web` |
| Create | `acli jira workitem create` (see --help for fields) |
| Transition | `acli jira workitem transition` (see --help) |
| Assign | `acli jira workitem assign` |
| Edit | `acli jira workitem edit` |
| Comment | `acli jira workitem comment` |
| Auth | `acli auth` |

Replace `PROJ` and `KEY-123` with your project key and issue key.

---

## JQL Tips

- **Open issues:** `status != Done AND status != Closed`
- **My issues:** `assignee = currentUser()`
- **Epics:** `type = Epic` or `issuetype = Epic`
- **By label:** `labels = "your-label"`
- **Paginate:** Use `--paginate` to fetch all results across pages.

---

## Requirements and Gherkin

When requirements (from Jira or agents) are expressed in Gherkin, see `.workflow/gherkin-requirements.md` for where to store feature files and how to generate them from Jira descriptions or other sources.

---

## Solving Hard Problems

### Rate Limits

Jira Cloud has rate limits. For large bulk operations, add delays or use pagination and batch in scripts.

### Field Names and Workflows

Field IDs and transition names vary by Jira project. Use `acli jira field` and `acli jira workitem transition --help` (or your instance’s workflow) to get exact values.

### MCP vs CLI

If you use the Atlassian MCP (e.g. in Cursor), you can perform Jira operations via MCP tools as well. This doc focuses on `acli`; use whichever fits your workflow.

---

*Last updated: March 2026 — based on acli installed locally*
