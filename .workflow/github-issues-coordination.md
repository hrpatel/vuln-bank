# GitHub Issues Coordination Guide

**This is the coordination system for multi-model work on vuln-bank.** Both Claude Code and Cursor use GitHub Issues as the real-time layer for task claiming, dependency tracking, and cross-model signaling.

> **Why Issues instead of the task index?** The old `tasks/index.md` had a visibility gap — both models edit it on branches, so neither could see the other's claims until a PR merged. Issues are branch-independent by design.

---

## How It Works

### Issues Are the Live Layer

Every task is a GitHub Issue. The issue body contains the spec (acceptance criteria, files to edit, context). Labels, assignments, and comments provide real-time status that both models can see from any branch.

### Task Files Are Archival

When an issue closes, a snapshot can be saved to `tasks/done/` for offline/portfolio reference. Task files are no longer the coordination mechanism — Issues are.

---

## Labels

| Label | Color | Meaning |
|-------|-------|---------|
| `available` | Green | Ready for either model to pick up |
| `in-progress` | Yellow | Claimed and being worked on |
| `blocked` | Red | Has unresolved dependencies |
| `claude-code` | Purple | Owned by Claude Code |
| `cursor` | Blue | Owned by Cursor |

---

## Workflow

### Starting a Session

1. Check open issues: `gh issue list --repo hrpatel/vuln-bank`
2. Look for issues labeled `available` — these are ready to claim
3. Check for issues labeled `blocked` — these have unresolved dependencies
4. If your operator gives you new work, create an issue (see "Creating Issues" below)

### Claiming a Task

```bash
# 1. Assign yourself and update labels
gh api repos/hrpatel/vuln-bank/issues/{N} -X PATCH \
  -f "labels[]=in-progress" \
  -f "labels[]=claude-code" \
  -f "assignees[]=hrpatel"

# 2. Leave a claiming comment (visible to the other model)
gh api repos/hrpatel/vuln-bank/issues/{N}/comments -X POST \
  -f body="**[Claude Code]** Claiming this task. Starting work now."
```

For Cursor, use `cursor` instead of `claude-code` in the label.

### Completing a Task

```bash
# 1. Close the issue
gh api repos/hrpatel/vuln-bank/issues/{N} -X PATCH -f state=closed

# 2. Check what this issue was blocking
gh api repos/hrpatel/vuln-bank/issues/{N}/dependencies/blocking \
  --jq '.[] | {number: .number, title: .title}'

# 3. For each downstream issue, check if ALL its blockers are now closed
gh api repos/hrpatel/vuln-bank/issues/{DOWNSTREAM}/dependencies/blocked_by \
  --jq '[.[] | select(.state == "open")] | length'
# If the result is 0, all blockers are resolved — flip it to available:
gh api repos/hrpatel/vuln-bank/issues/{DOWNSTREAM} -X PATCH \
  -f "labels[]=available"

# 4. Leave a completion comment
gh api repos/hrpatel/vuln-bank/issues/{N}/comments -X POST \
  -f body="**[Claude Code]** Done. PR #__ ready for merge. Unblocked #__."
```

> **Important:** Closing a blocker does NOT auto-update downstream labels. The completing model must check and flip `blocked` to `available` on any issue that is now unblocked. This is typically 2-3 API calls.

### Cross-Model Signaling

Use issue comments for anything the other model or operator needs to see:
- Scope changes: "This is bigger than expected — splitting into two issues"
- Blockers: "Need operator input on X before continuing"
- Handoffs: "Finished the backend piece, frontend is ready for the other model"

Comments are timestamped and branch-independent — no merge required to see them.

---

## Dependency Chains

### Creating a Chain

A chain is a parent issue with sub-issues linked by dependencies.

```bash
# 1. Create parent issue
gh api repos/hrpatel/vuln-bank/issues -X POST \
  -f title="Feature: SQL injection module" \
  -f body="Parent issue for the SQLi chain..."

# 2. Create sub-issues (note the returned issue ID from the response)
gh api repos/hrpatel/vuln-bank/issues -X POST \
  -f title="Research SQLi patterns" \
  -f body="..."

# 3. Link sub-issues to parent (use the issue ID, not the number)
#    -F (not -f) sends the value as an integer, which the API requires.
gh api repos/hrpatel/vuln-bank/issues/{PARENT}/sub_issues -X POST \
  -F sub_issue_id={CHILD_ISSUE_ID}

# 4. Add dependency: child blocked by another child
#    Use the issue ID (from the API response), not the issue number.
gh api repos/hrpatel/vuln-bank/issues/{BLOCKED}/dependencies/blocked_by -X POST \
  -F issue_id={BLOCKER_ISSUE_ID}
```

### Reading Dependencies

```bash
# What blocks issue N?
gh api repos/hrpatel/vuln-bank/issues/{N}/dependencies/blocked_by \
  --jq '.[] | {number: .number, state: .state, title: .title}'

# What does issue N block?
gh api repos/hrpatel/vuln-bank/issues/{N}/dependencies/blocking \
  --jq '.[] | {number: .number, title: .title}'

# Parent progress roll-up
gh api repos/hrpatel/vuln-bank/issues/{PARENT} \
  --jq '.sub_issues_summary'
```

### Issue ID vs Issue Number

The API uses two different identifiers:
- **Issue number** (`#8`) — used in URL paths: `/issues/8`
- **Issue ID** (`4047868731`) — used in request bodies for sub-issues and dependencies

To get an issue ID: `gh api repos/hrpatel/vuln-bank/issues/{N} --jq '.id'`

---

## API Quick Reference

| Action | Method | Endpoint | Body |
|--------|--------|----------|------|
| List issues | GET | `/repos/{owner}/{repo}/issues` | — |
| Create issue | POST | `/repos/{owner}/{repo}/issues` | `-f title=... -f body=...` |
| Update labels/assignees | PATCH | `/repos/{owner}/{repo}/issues/{N}` | `-f "labels[]=..."` |
| Close issue | PATCH | `/repos/{owner}/{repo}/issues/{N}` | `-f state=closed` |
| Add comment | POST | `/repos/{owner}/{repo}/issues/{N}/comments` | `-f body=...` |
| Add sub-issue | POST | `/repos/{owner}/{repo}/issues/{N}/sub_issues` | `-F sub_issue_id={ID}` |
| Add dependency | POST | `/repos/{owner}/{repo}/issues/{N}/dependencies/blocked_by` | `-F issue_id={ID}` |
| List blockers | GET | `/repos/{owner}/{repo}/issues/{N}/dependencies/blocked_by` | — |
| List blocking | GET | `/repos/{owner}/{repo}/issues/{N}/dependencies/blocking` | — |

All commands use `gh api` with the repo prefix `repos/hrpatel/vuln-bank`.

---

## Solving Hard Problems

### Race Conditions on Claiming

GitHub assignment is atomic — if two models try to assign themselves simultaneously, the second write wins. To make claiming safe:

1. Before claiming, re-read the issue to confirm it is still `available` and unassigned
2. Assign + relabel in a single PATCH call (reduces the window)
3. If you see an issue is already assigned or labeled `in-progress`, do not claim it — pick another

This is not a perfect lock, but the race window is small (seconds) and operators can resolve the rare conflict verbally.

### Staleness Detection

If a task has been `in-progress` for unusually long with no comments or PR activity, it may be abandoned. Either model can check:

```bash
# When was the last update on issue N?
gh api repos/hrpatel/vuln-bank/issues/{N} --jq '.updated_at'

# Any recent comments?
gh api repos/hrpatel/vuln-bank/issues/{N}/comments --jq '.[-1].created_at'
```

Convention: if an `in-progress` issue has no activity for 48+ hours, either operator can reassign it. The model should leave a comment before reclaiming: "No activity in 48h — reclaiming for [model name]."

### Scope Expansion

When a task grows beyond its original spec:
1. Leave a comment on the issue explaining the scope change
2. If it should split, create new sub-issues under the same parent
3. Update the issue body with the revised scope
4. Do not silently expand — the other model and operators need to see the change

### Label Consistency

Labels must be kept in sync manually. The key transitions:

| Event | Label Change | Who Does It |
|-------|-------------|-------------|
| Task created | Set `available` (or `blocked` if it has open dependencies) | Creator |
| Task claimed | `available` -> `in-progress` + model label | Claiming model |
| Task completed | Issue closed | Completing model |
| Blocker resolved | `blocked` -> `available` on downstream issues | Completing model |
| Task abandoned | `in-progress` -> `available`, remove assignment | Either operator |

---

## Migration Notes

The old `tasks/index.md` file remains in the repo as a historical reference but is **no longer the coordination mechanism**. Both `CLAUDE.md` and `.cursorrules` now direct models to check GitHub Issues first.

Existing task files in `tasks/` are kept for reference. New work should be created as GitHub Issues, not task files.

---

*Last updated: March 9, 2026 — POC validated in Session 34*
