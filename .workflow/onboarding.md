# Workflow Onboarding — Local Environment Setup

This doc gets your machine ready to **participate in the workflow**: clone the repo, use the issue tracker, and open/update PRs. It does not cover running the vuln-bank app locally (see the repo **README** for that).

Supported environments: **macOS** and **WSL** (Windows Subsystem for Linux, Ubuntu/Debian).

---

## Required (everyone)

### Git

- **macOS:** Usually pre-installed. If not: `xcode-select --install` or `brew install git`.
- **WSL:**  
  `sudo apt update && sudo apt install -y git`

**Verify:** `git --version`

### GitHub CLI (`gh`)

Used for PRs and (when the project uses GitHub Issues) for the issue tracker. Authenticate so you can push and create PRs.

- **macOS:**  
  `brew install gh`  
  Then: `gh auth login` (choose GitHub.com, HTTPS or SSH, authenticate in browser).

- **WSL:** Add GitHub’s APT repo and install:
  ```bash
  (type -p wget >/dev/null || (sudo apt update && sudo apt install wget -y)) \
    && sudo mkdir -p -m 755 /etc/apt/keyrings \
    && out=$(mktemp) && wget -nv -O$out https://cli.github.com/packages/githubcli-archive-keyring.gpg \
    && cat $out | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
    && sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && sudo apt update && sudo apt install gh -y
  ```
  Then: `gh auth login` (same as macOS).

**Verify:** `gh auth status`

---

## Optional (by issue tracker)

Read [.workflow/issue-tracker.md](issue-tracker.md) to see which tracker this project uses. Install only the tools for that tracker.

### If the project uses Beads

You need **Beads (`bd`)** and **Dolt** (Beads’ storage backend).

- **macOS:**  
  `brew install beads dolt`  
  Or install script (installs both):  
  `curl -fsSL https://raw.githubusercontent.com/steveyegge/beads/main/scripts/install.sh | bash`

- **WSL:**  
  `curl -fsSL https://raw.githubusercontent.com/steveyegge/beads/main/scripts/install.sh | bash`  
  (Script detects Linux and installs; ensure Dolt is installed if the script doesn’t pull it — see [Beads installation docs](https://steveyegge.github.io/beads/getting-started/installation).)

**Verify:** `bd --version`. Then in the repo: `bd init` or `bd init --stealth` (see [beads-coordination.md](beads-coordination.md)).

When this project uses **Beads with Jira sync** (see [dual-tracker design](../docs/specs/2026-03-13-beads-jira-dual-tracker-design.md)):
- **Jira read:** Required for agents (epics, stories, Gherkin). Use acli (`acli auth`), Jira MCP, or REST with credentials.
- **Jira write:** Required only where sync runs (local or CI) to create/update Jira issues from Beads. GitHub CLI (`gh`) remains required for PRs.

### If the project uses Jira

You need **Atlassian CLI (`acli`)**.

- **macOS:**  
  `brew tap atlassian/homebrew-acli && brew install acli`  
  Then: `acli auth`

- **WSL:** Debian/Ubuntu:
  ```bash
  sudo apt-get install -y wget gnupg2
  sudo mkdir -p -m 755 /etc/apt/keyrings
  wget -nv -O- https://acli.atlassian.com/gpg/public-key.asc | sudo gpg --dearmor -o /etc/apt/keyrings/acli-archive-keyring.gpg
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/acli-archive-keyring.gpg] https://acli.atlassian.com/linux/deb stable main" | sudo tee /etc/apt/sources.list.d/acli.list > /dev/null
  sudo apt update && sudo apt install -y acli
  ```
  Then: `acli auth`

**Verify:** `acli --version` and `acli auth` (log in to your Atlassian Cloud site). See [jira-coordination.md](jira-coordination.md).

---

## Checklist

1. **Clone the repo** (if you haven’t): `git clone <repo-url>` and `cd` into it.
2. **Install required tools:** Git and GitHub CLI (see above). Run `gh auth login` if needed.
3. **Check the issue tracker:** Read [.workflow/issue-tracker.md](issue-tracker.md). If the project uses Beads or Jira, install and verify those tools.
4. **Running two agents on one machine?** Add a **git worktree** or second clone (see *Parallel agents* below).
5. **Confirm:** `git --version`, `gh auth status`, and (if applicable) `bd --version` or `acli --version`.

After this, follow [.workflow/START HERE.md](START%20HERE.md) and the coordination guide linked in issue-tracker.md. For one-time project setup (e.g. choosing the tracker), see [.workflow/bootstrap.md](bootstrap.md).

---

## Parallel agents on one machine (filesystem isolation)

**Problem:** Two AI agents (e.g. Cursor + Claude Code) pointed at the **same directory** will fight over the working tree: each checks out its own branch and overwrites the same files, causing lost work and merge chaos.

**Fix — pick one:**

### Option 1: Git worktrees (recommended)

One clone stays the “primary” repo; additional agents use a **sibling directory** that shares `.git` but has its own checkout.

From your primary clone (e.g. `~/code/vuln-bank`):

```bash
cd ~/code/vuln-bank
git fetch origin
# New branch for the second agent (create if needed):
git worktree add ../vuln-bank-claude -b claude/01-my-task
# Or attach to an existing branch:
# git worktree add ../vuln-bank-claude claude/01-my-task
```

Point the **second** agent’s workspace at `~/code/vuln-bank-claude`. It edits and commits there; the first agent stays in `~/code/vuln-bank`. Push from either tree with `git push -u origin <branch>`.

List / remove worktrees:

```bash
git worktree list
git worktree remove ../vuln-bank-claude   # after branch is merged or abandoned
```

### Option 2: Second full clone

```bash
git clone <repo-url> vuln-bank-agent2
cd vuln-bank-agent2 && git checkout claude/01-my-task
```

More disk use; mentally simple. Same **Beads** guidance as below.

### Beads with multiple directories

Beads/Dolt data (`.beads/`) is tied to the directory where `bd init` ran. **Do not** run unrelated `bd` commands from two different trees unless both use the **same** Beads database (e.g. shared Dolt server — see [Beads docs](https://steveyegge.github.io/beads/)).

**Practical pattern:**

1. Designate **one** directory as the Beads source of truth (usually the primary clone).
2. Run **`bd ready`**, **`bd update <id> --claim`**, **`bd close`** only from that directory (or ensure all worktrees share the same Dolt backend).
3. Implement code in whichever worktree/clone holds your feature branch.

If each tree has its own isolated `.beads`, claims in one tree are invisible to the other — **avoid** that for multi-agent coordination.

See [.workflow/beads-coordination.md](beads-coordination.md) — *Parallel agents and directories*.

---

*Last updated: March 2026*
