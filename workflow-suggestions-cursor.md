# Workflow Review — Cursor Agent Analysis

**Date:** March 9, 2026 (updated)
**Reviewer:** Cursor (operated by coworker)
**Scope:** Second review after Claude Code addressed feedback via task #05 (GitHub Issues coordination)

---

## Summary

Claude Code responded to the original feedback by replacing the markdown-based task index with GitHub Issues as the coordination layer. This is the right call — it directly solves the critical visibility gap (issue #1), race conditions (#2), staleness detection (#3), scope signaling (#4), and cross-model communication (#7). The POC validation was thorough, with real dependency chains tested.

However, there is a hard blocker for this side: **`gh` CLI is not installed on this machine.** The entire new workflow depends on `gh api` commands. Until that's resolved, I cannot participate in the Issues-based coordination system at all.

This review covers: what the changes solve, new concerns, remaining gaps, and a practical usability assessment for the Cursor operator.

---

## Status of Original Feedback Items

| # | Original Issue | Status | How It Was Addressed |
|---|---------------|--------|---------------------|
| 1 | Index visibility gap (critical) | **Resolved** | GitHub Issues are branch-independent — no merge required to see claims |
| 2 | Race condition on claiming | **Mostly resolved** | GitHub assignment is atomic. Small race window remains but acceptable |
| 3 | Staleness detection | **Resolved** | `updated_at` timestamps + 48-hour reclaim convention documented |
| 4 | Scope expansion protocol | **Resolved** | Issue comments + sub-issue splitting documented in coordination guide |
| 5 | DRY up entry points | **Not addressed** | `.cursorrules` and `CLAUDE.md` still duplicate shared rules |
| 6 | Lightweight bookkeeping tiers | **Partially addressed** | Issue close is lighter than old checklist, but metrics/decisions/STATUS updates remain universal |
| 7 | Cross-model signals | **Resolved** | Issue comments are timestamped and branch-independent |
| 8 | Serialize workflow doc changes | **Not addressed** | No explicit rule added |
| 9 | Stale dependencies in task files | **Obsoleted** | Task files are now archival; GitHub's native dependency system tracks this |

**Score: 6 of 9 addressed, 1 obsoleted, 2 remaining.** That's a strong response to the feedback.

---

## Hard Blocker: `gh` CLI Not Installed

`gh` (GitHub CLI) is not installed on this machine. Every step in the new coordination workflow — checking for work, claiming tasks, leaving comments, closing issues, managing dependencies — requires `gh api` commands.

**Impact:** Until `gh` is installed and authenticated with a PAT that has "Issues: Read and write" permissions, I cannot:
- Check what tasks are available
- Claim work
- Signal status to Claude Code
- Leave cross-model comments
- Close issues or unblock downstream work

**Fix:** `brew install gh` (or equivalent), then `gh auth login` with a PAT that has the required permissions. This is a one-time setup.

**Workaround (partial):** The human operator can use the GitHub web UI to manage issues, and relay the state to me verbally. But this defeats the purpose of the automated coordination system.

---

## New Concerns with the GitHub Issues Approach

### 1. API call complexity

The coordination guide has 20+ distinct `gh api` calls with specific payload formats, field types (`-f` for strings, `-F` for integers), and multi-step sequences. Each claim-and-start flow is ~3 API calls. Each complete-and-unblock flow is ~4-5 API calls. A typo or wrong flag can misconfigure labels or silently fail.

**Suggestion:** Create a small set of shell scripts or aliases (e.g., `./scripts/claim-issue.sh 8 cursor`, `./scripts/close-issue.sh 8`) that wrap the common multi-step sequences. This reduces the error surface and makes the workflow repeatable. Both models can call these scripts instead of composing raw API calls each time.

### 2. Issue ID vs Issue number is a footgun

The guide documents this well, but it's still the most likely error source. Sub-issue and dependency APIs require the internal ID (a large integer like `4047868731`), not the human-visible number (`#8`). Every time a model links dependencies or sub-issues, it must first look up the ID with an extra API call.

**Suggestion:** If wrapper scripts are created (see above), they should handle ID lookup internally — accept the human-readable number, resolve to ID, then call the API.

### 3. Manual label flipping on unblock

Closing a blocker does NOT auto-update downstream issue labels. The completing model must:
1. Check what the closed issue was blocking
2. For each downstream issue, check if all its blockers are now resolved
3. Flip `blocked` to `available` on any fully-unblocked issue

This is a 2-3 step process that's easy to forget, leaving blocked issues in limbo with no one noticing.

**Suggestion:** At minimum, add this to the task completion checklist prominently. Ideally, a GitHub Action could automate this: when an issue closes, check its "blocking" list and auto-relabel downstream issues if all their blockers are resolved.

### 4. No fallback if GitHub API is unavailable

If the API is down, rate-limited, or the PAT expires, coordination halts entirely. The old markdown system at least allowed local editing.

**Suggestion:** Keep `tasks/index.md` as a degraded-mode fallback, not just historical reference. Add a note to the coordination guide: "If `gh` commands fail, fall back to `tasks/index.md` on main and notify your operator."

### 5. Transition state of existing tasks

Tasks #02, #03, and #05 exist as markdown files in `tasks/` but the new system says "new work should be created as GitHub Issues." It's unclear whether these tasks should be migrated to Issues or left as-is.

**Suggestion:** Migrate the queued tasks (#02, #03, #05) to GitHub Issues as part of the rollout. Close the loop by noting in each task file "Migrated to Issue #N" or delete them.

---

## Remaining Gaps (Unchanged from Original Review)

### DRY up entry points (original item #5)

`.cursorrules` and `CLAUDE.md` were both updated for the Issues workflow, but they still duplicate the same rules. The risk of drift increases with each update — this round is a case in point, as the same changes had to be applied to both files.

**Recommendation:** Make both files thin pointers (~10 lines) that say "read `.workflow/START HERE.md` for all rules." Keep only model-specific info in each (branch prefix, operator name, model identifier for labels).

### Serialize workflow doc changes (original item #8)

Task #05 itself touches `.cursorrules`, `CLAUDE.md`, and `.workflow/` files — exactly the conflict surface flagged in the original review. No explicit rule was added about serializing changes to workflow infrastructure.

**Recommendation:** Add to `How We Work.md`: "Changes to `.cursorrules`, `CLAUDE.md`, or `.workflow/` files must be done by one model at a time. Never run two tasks that modify workflow docs in parallel."

---

## Usability Assessment for the Cursor Operator

This section addresses the practical question: **can you use this workflow effectively with your current tooling?**

### Current State

| Capability | Available? | Notes |
|-----------|-----------|-------|
| Git (branch, commit, push) | Yes | SSH remote configured, works |
| `gh` CLI | **No** | Not installed — hard blocker for Issues workflow |
| GitHub web UI | Yes | Manual fallback for issue management |
| Cursor agent (me) | Yes | Can read/write files, run shell commands, create PRs (once `gh` is available) |
| Network access to GitHub API | Needs testing | Sandbox may restrict; may need `full_network` permission per command |

### What You Can Do Today

- **Read and follow the workflow docs** — all the process documentation works as-is
- **Branch, code, commit, push** — git operations work fine
- **Manage issues via GitHub web UI** — you can view, create, label, and comment on issues in a browser
- **Relay coordination state to me verbally** — tell me what issues are available and I'll work accordingly
- **Review PRs from Claude Code** — viewable on GitHub or via `git diff`

### What's Blocked Until `gh` Is Installed

- **Automated issue management** — the core claim/signal/unblock workflow
- **Creating PRs from the command line** — I can't run `gh pr create`
- **Checking issue status programmatically** — I'd have to ask you to look at GitHub

### Setup Checklist

To fully participate in the workflow:

1. **Install `gh`:** `brew install gh`
2. **Authenticate:** `gh auth login` — use a PAT with these scopes:
   - `repo` (full access) or at minimum:
   - `Issues: Read and write`
   - `Pull requests: Read and write`
   - `Contents: Read and write`
3. **Test:** `gh issue list --repo hrpatel/vuln-bank` — should return open issues
4. **Test labels:** `gh api repos/hrpatel/vuln-bank/labels --jq '.[].name'` — should show `available`, `in-progress`, `blocked`, `claude-code`, `cursor`

Once this is done, I can run the full coordination workflow autonomously.

### Practical Workflow for You (the Human)

Even with `gh` installed, your day-to-day interaction with the workflow should be lightweight:

1. **Start of session:** Tell me what to work on, or say "check for available issues"
2. **During work:** I handle branching, coding, claiming issues, leaving comments
3. **When I'm done:** I create a PR and flag it. You review and merge on GitHub
4. **Between sessions:** Check GitHub Issues in your browser for status — it's always current

The operator role is primarily: assign work, review PRs, merge. The coordination overhead falls on the AI models, not on you.

---

## Recommendation on the Pending PR

The branch `claude/05-issues-coordination-guide` is well-constructed and addresses the most critical problems. My recommendation:

1. **Install `gh` first** — without it, merging the new workflow creates a system I can't use
2. **Create the GitHub labels** (`available`, `in-progress`, `blocked`, `claude-code`, `cursor`) before or immediately after merging
3. **Migrate tasks #02, #03, #05 to Issues** — close the transition cleanly
4. **Merge the PR** — the Issues-based coordination is a clear improvement over the markdown index
5. **Add wrapper scripts later** — not a blocker, but reduces API call errors over time

---

*This file is for human and AI review. Delete or archive after the feedback cycle is complete.*
