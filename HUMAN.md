# Vuln Bank — Operator Prompts

Suggested prompts for working with AI agents on this project. Copy, paste, and adapt as needed.

---

## Starting a Session

**New session, let the agent find its own work:**
```
Read AGENTS.md to get started. Register if needed, then pick up 1 task from the backlog.
```

**New session, assign a specific task:**
```
Read AGENTS.md to get started. Register if needed, then work on <task-id / description>.
```

**Resume after a break:**
```
Read AGENTS.md and STATUS.md to get context. Resume where we left off — check bd for any in-progress tasks assigned to you.
```

---

## Assigning Work

**Point to a specific Beads task:**
```
Pick up task <id>. Read AGENTS.md first if you haven't this session.
```

**Describe work without a ticket:**
```
Create a Beads task for <description>, claim it, then implement it.
```

**Unblock a task:**
```
<id> is now unblocked. Claim it and proceed.
```

---

## Checking Progress

**Status update:**
```
What are you currently working on? Show me the bd status for your claimed tasks.
```

**Review what's been done:**
```
Summarize what was completed this session and what's still open.
```

**Check for conflicts with the other agent:**
```
Before starting, check bd for any tasks the other agent has in progress that might touch the same files as your next task.
```

---

## Reviewing Work

**Review a PR before merging:**
```
Walk me through what changed in this PR and confirm the acceptance criteria were met.
```

**Request changes:**
```
Don't merge yet. Address this feedback first: <feedback>
```

**Approve and merge (you do this — agents don't merge):**
Merge via the GitHub UI or `gh pr merge <number> --squash`.

---

## Closing a Session

**Standard close-out:**
```
Close out the session: file issues for anything unfinished, update STATUS.md and your metrics file, push, and open a PR.
```

**Hard stop (agent may have in-progress work):**
```
Stop what you're doing, commit your current state to a WIP branch, release any claimed Beads tasks back to open, and push so nothing is stranded locally.
```

---

## Managing Parallel Agents

**Provision a named worktree before starting an agent:**
```bash
scripts/spawn-agent.sh cursor-a
scripts/spawn-agent.sh claude-1
```

**Tear down when done:**
```bash
scripts/teardown-agent.sh cursor-a
```

**Check which agents are active:**
```bash
git worktree list
```

---

## Troubleshooting

**Agent is stuck or not making progress:**
```
Stop and explain what's blocking you. Don't retry the same approach — describe what you've tried and what failed.
```

**Claim failed (task already taken):**
```
Your claim on <id> failed. Run bd ready --unassigned and pick a different task.
```

**Push failing:**
```
Show me the push error. Don't skip the push — resolve it and retry.
```

**Merge conflict:**
```
Don't force-push. Rebase on main, resolve the conflicts, and show me what changed before pushing.
```
