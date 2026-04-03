# Vuln Bank — Agent Instructions

This is a deliberately vulnerable banking application for security testing practice. Work involves adding new vulnerability scenarios, improving existing ones, and maintaining the application.

---

## Step 0 — Verify or Create Agent Identity

Do this **before anything else**. Check that `.bd-agent-identity` exists in your working directory.

**Found:** Read the agent name and confirm `git config get user.name` matches.

**Not found — self-register:**
```bash
# From the repo root:
scripts/spawn-agent.sh --auto
# Read the "Worktree:" path from the output, then cd into it:
cd <worktree-path>
```
After `cd`, confirm `.bd-agent-identity` exists. Use this worktree as your working directory for **all** subsequent commands. Do not proceed without a valid identity.

**Operator-provisioned (alternative):** Operators can pre-create named workspaces before starting agents:
```bash
scripts/spawn-agent.sh my-agent-name    # creates isolated worktree
scripts/teardown-agent.sh my-agent-name # when done
```

Each worktree has `git config --worktree user.name` set to the agent name. A dedicated worktree is required for all agents regardless of the chosen issue tracker, ensuring filesystem isolation and correct attribution of work.

---

## Session Start

1. Read `STATUS.md` — current project state.
2. Find ready work: `bd ready --unassigned --json`
3. Claim one task: `bd update <id> --claim` — **must succeed before creating a branch or editing any file.** If it fails (already claimed by another agent), pick a different task.
4. Create a feature branch: `git checkout -b <your-prefix>/<id>-<slug>` — never commit directly to `main`.
5. If no unclaimed work is available, ask your operator what to do next.

---

## Core Rules

1. **Work quietly.** Don't narrate intermediate steps — surface results, blockers, and decisions only.
2. **Humans merge.** Never merge PRs yourself — create them and flag as ready for review.
3. **Claim before you touch.** `bd update <id> --claim` must succeed before any branch or file change for that task.
4. **Tasks are sequential unless marked parallel-safe.** Parallel tasks touching the same files will revert each other.
5. **Ask before acting on anything destructive or ambiguous.**
6. **Never push to `main`.** Feature branches only.

---

## Before You Build

Don't default to the first obvious solution. Before writing code, ask:

- Is there a better pattern for this problem type?
- Are there libraries already in the stack that handle this well?
- What do leading products do for this same problem?
- Is there a simpler solution with less code?

A few minutes of research before implementing saves multiple iteration cycles after.

---

## Non-Interactive Shell Commands

Shell commands like `cp`, `mv`, and `rm` may be aliased to interactive (`-i`) mode on some systems, causing agents to hang indefinitely on y/n prompts. **Always use non-interactive flags:**

```bash
cp -f source dest       # NOT: cp source dest
mv -f source dest       # NOT: mv source dest
rm -f file              # NOT: rm file
rm -rf directory        # NOT: rm -r directory
cp -rf source dest      # NOT: cp -r source dest
```

Other commands that may prompt:
- `scp` / `ssh` — add `-o BatchMode=yes`
- `apt-get` — add `-y`
- `brew` — set `HOMEBREW_NO_AUTO_UPDATE=1`

---

## Issue Tracking (Beads)

Use `bd` for **all** task tracking. Do not create markdown TODO lists or use other tracking systems.

### Essential Commands

```bash
bd ready --unassigned --json          # Find available work
bd show <id>                          # View issue details
bd update <id> --claim                # Claim work atomically (always first)
bd create "Title" -d "Desc" -t task|bug|feature|chore -p 0-4
bd close <id>                         # Complete work
bd dolt push                          # Push beads data to remote
```

Append `--json` to any command for machine-readable output.

### Priorities

| Value | Meaning |
|-------|---------|
| `0` | Critical — security, data loss, broken builds |
| `1` | High — major features, important bugs |
| `2` | Medium (default) |
| `3` | Low — polish, optimization |
| `4` | Backlog |

### Discovered Work

When you find additional work while implementing, create a linked issue:
```bash
bd create "Found issue" -d "Details" -p 1 --deps discovered-from:<parent-id>
```

### Rules

- ✅ Claim before branching or editing files
- ✅ Use `--json` for programmatic use
- ✅ Link discovered work with `discovered-from`
- ✅ Check `bd ready` before asking "what should I work on?"
- ❌ No markdown TODO lists
- ❌ No duplicate tracking systems

Full reference: `.workflow/beads-coordination.md`

---

## Session Completion

Work is **not complete** until `git push` succeeds. Complete all steps before ending a session:

1. **File issues for remaining work** — create Beads issues for anything unfinished or discovered.
2. **Run quality gates** — tests, linters, builds (if code changed).
3. **Update issue status** — `bd close <id>` for completed tasks; release any claimed-but-unfinished tasks back to open.
4. **Update docs** — `STATUS.md` (project state), `decisions.md` (significant decisions), `.metrics/metrics-<your-model>.md` (session row — include in the commit you push).
5. **Push:**
   ```bash
   git pull --rebase
   bd dolt push
   git push
   git status   # must show "up to date with origin"
   ```
6. **Open a PR** to `main` and flag it as ready for review.

Never say "ready to push when you are" — you must push. If push fails, resolve and retry.

---

## Key References

| Doc | When to read |
|-----|-------------|
| `STATUS.md` | Every session — current project state |
| `decisions.md` | When you need project history; log decisions here |
| `.metrics/` | Before every push — include updated session row in commit |
| `.workflow/beads-coordination.md` | Full `bd` command and dependency reference |
| `.workflow/Tips & Lessons.md` | When you hit a technical snag |
| `.workflow/onboarding.md` | First-time setup; parallel agent details |
