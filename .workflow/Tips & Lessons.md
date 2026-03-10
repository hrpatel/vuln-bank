# Tips & Lessons Learned

A living document capturing what we've learned — from both AI models and both operators. Add entries as you discover them.

---

## How This Doc Works

- **Anyone can add entries:** Claude Code, Cursor, Michael, Hrdayesh
- **Format:** Each entry has an attribution tag: `[Claude Code]`, `[Cursor]`, `[Michael]`, `[Hrdayesh]`
- **Check-in cadence:** Both operators review this doc every 3-4 sessions (or ~weekly) and add their own observations. AI models should prompt for this if it's been a while.
- **Keep entries short and actionable.** This is a reference, not a journal.

---

## Multi-Model Coordination

- **GitHub Issues are the coordination layer.** Before starting any work, check `gh issue list --repo hrpatel/vuln-bank` for in-progress work. If another model has an issue that touches the same files, pick something else.
- **Branch naming signals ownership.** Use `claude/` or `cursor/` prefixes so it's obvious who's working where.
- **File-level granularity is enough.** You don't need line-level locking — if two tasks touch the same file, they conflict. Keep tasks scoped to avoid this.
- **Update the index immediately.** Claim your task before you start coding, not after. The gap between "I decided to work on this" and "I updated the index" is where collisions happen.

## AI Code Generation

- `[Claude Code]` **Be extremely specific in prompts.** Exact file paths, exact code patterns, exact replacements. Tell the tool what NOT to change.
- `[Claude Code]` **Sequential tasks within dependency chains.** Parallel tasks touching the same files can revert each other's changes.
- `[Claude Code]` **Check diffs carefully.** AI tools sometimes touch more files than asked. Always review the full diff before committing.

## Security Testing Context

- `[Claude Code]` **This is a deliberately vulnerable app.** Vulnerabilities are features, not bugs. Don't "fix" intentional vulnerabilities unless explicitly asked to.
- `[Claude Code]` **Document each vulnerability clearly.** Include: what the vulnerability is, where it lives, how to exploit it, and how a real app would fix it.
- `[Claude Code]` **Separate intentional vulns from real bugs.** If you find an actual bug (not an intentional vulnerability), log it in `metrics.md`.
- `[Claude Code]` **Mark intentional vulns in code.** Use a consistent comment pattern (e.g. `# VULN: <description>`) so models and contributors can tell what's intentional.

## Workflow & Process

- `[Claude Code]` **All changes through PRs.** No direct pushes to main.
- `[Claude Code]` **Keep PRs focused.** One task per PR makes review easier and rollback safer.
- `[Claude Code]` **Update metrics/decisions as part of the work**, not as a separate ritual. Cadence: every 3-4 completed tasks or end of session — whichever comes first.
- `[Claude Code]` **DRY up entry points.** Keep `CLAUDE.md` and `.cursorrules` thin — model-specific settings only. All shared rules in `.workflow/`.
- `[Cursor]` **Bookkeeping overhead should scale with task size.** Quick fixes shouldn't need the full task completion checklist.

## Code Review

- `[Claude Code]` **Deep review via source analysis.** For large PRs, read the full source file, not just the diff.
- `[Claude Code]` **Parity checks.** When adding a second way to do something, verify the new path matches the existing one in behavior.

## GitHub & Tooling

- `[Claude Code]` **PAT tokens:** Never hardcode tokens in committed files.
- `[Claude Code]` **`gh api` for fork-safe PR creation.** `gh pr create` defaults to upstream on forks. Use REST API instead.
- `[Claude Code]` **Issue ID vs issue number.** Sub-issue and dependency APIs require the issue ID (large integer), not the issue number (#N). Get it with `gh api repos/.../issues/{N} --jq '.id'`.

---

## Operator Observations

_This section is for Michael and Hrdayesh to add their own learnings from working with the AI models._

- `[Michael]` **Single-operator work informed multi-model, but wasn't a substitute for it.** The personal project workflow (single operator, single AI) was a valuable starting point — it gave us conventions, cadences, and a task/PR discipline to build on. But it was never going to surface multi-model problems like the visibility gap. Those only appear when two models and two operators are actually working in parallel. The lesson isn't "we should have started from scratch" — it's that the single-operator experience was a good foundation, and extending it was the right approach.

- `[Michael]` **The multi-model POC should have started earlier within the team.** The gap wasn't in the technical design — it was in timing. This kind of coordination POC should have been run sooner, ideally by someone with more technical depth (e.g. a tech lead) who could stress-test the workflow before rolling it out to less experienced operators. The process learning curve is real, and having someone navigate it first would have smoothed the path for everyone else.

- `[Michael]` **Operator skill differences change what the process needs to handle.** The AI model compensates for the operator in ways that aren't always visible — a vague instruction that Cursor figures out looks like success, but it's fragile. Process guardrails (created-by labels, serialization rules, check-in cadences) aren't overhead for experienced operators — they're safety nets for less experienced ones. The workflow needs to accommodate both without slowing anyone down.

- `[Michael]` **We need to think from others' perspectives.** When something works for one operator, it's easy to assume it works for all. The real skill is recognizing when the process needs to adjust for different experience levels, and watching for issues that come from that gap — not just technical issues, but judgment calls about what to push back on, what looks wrong in a diff, and which tasks are safe to parallelize.

- `[Hrdayesh]` _(check-in pending)_

---

## AI Model Observations

_What the AI models have learned about working in this multi-model, multi-operator setup._

- `[Claude Code]` **You can't POC multi-model coordination with one model.** The failure modes only appear under real conditions. The task index worked fine in single-operator sessions — it took Cursor's fresh perspective to expose the visibility gap.

- `[Claude Code]` **Fork association is a landmine.** `gh` tooling silently targeting upstream repos can leak work to public projects. When working with forks, always verify where PRs and pushes are going. Half-measures (removing remotes) don't fix GitHub-level fork association.

- `[Claude Code]` **DRY applies to process docs, not just code.** Same rules copy-pasted across 4 files drifted within a few sessions. Thin entry points + single source of truth works for docs the same way it works for code.

- `[Claude Code]` **Deliberately vulnerable apps are tricky to audit.** The line between "intentional vulnerability" and "actual bug" requires careful code reading. Explicit markers (like `# VULN:` comments) would save both models and new contributors significant time.

- `[Claude Code]` **Metrics discipline doesn't come naturally.** It should be automatic — part of closing out work, not a separate step triggered by a reminder.

---

## Friction Points (Unresolved)

_Log things that are slowing work down or causing confusion. When resolved, move to the relevant section above with the solution._

_(none currently)_

---

*Review cadence: both operators check in every 3-4 sessions. AI models prompt if overdue. Last reviewed: (not yet)*
