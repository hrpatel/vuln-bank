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

- `[Claude Code]` **GitHub Issues are the coordination layer, not the task index.** The old `tasks/index.md` had a visibility gap — both models edited it on branches, so neither saw the other's claims. Issues are branch-independent.
- `[Claude Code]` **Branch naming signals ownership.** Use `claude/` or `cursor/` prefixes so it's obvious who's working where.
- `[Claude Code]` **File-level granularity is enough.** You don't need line-level locking — if two tasks touch the same file, they conflict. Keep tasks scoped to avoid this.
- `[Claude Code]` **Claim your issue before you start coding.** The gap between "I decided to work on this" and "I labeled the issue" is where collisions happen.
- `[Claude Code]` **Workflow doc changes are serialized.** Never run two tasks that modify `.cursorrules`, `CLAUDE.md`, or `.workflow/` files in parallel.
- `[Cursor]` **The task index has a visibility gap.** Both models edit it on branches, so neither can see the other's claims until a PR merges. (This observation led to the GitHub Issues migration.)

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

- `[Michael]` _(check-in pending)_
- `[Hrdayesh]` _(check-in pending)_

---

## Friction Points (Unresolved)

_Log things that are slowing work down or causing confusion. When resolved, move to the relevant section above with the solution._

_(none currently)_

---

*Review cadence: both operators check in every 3-4 sessions. AI models prompt if overdue. Last reviewed: (not yet)*
