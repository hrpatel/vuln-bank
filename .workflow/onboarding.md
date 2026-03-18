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
4. **Running two agents on one machine?** Add a **git worktree** (see *Parallel agents* below).
5. **Confirm:** `git --version`, `gh auth status`, and (if applicable) `bd --version` or `acli --version`.

After this, follow [.workflow/START HERE.md](START%20HERE.md) and the coordination guide linked in issue-tracker.md. For one-time project setup (e.g. choosing the tracker), see [.workflow/bootstrap.md](bootstrap.md).

---

## Parallel agents on one machine (filesystem isolation)

**Problem:** Two AI agents (e.g. Cursor + Claude Code) using the **same directory** will fight over the working tree when each checks out a different branch.

**Fix: git worktree.** Keep one main checkout; add a **sibling directory** per extra agent (same repo, separate working tree).

From your main repo (e.g. `~/code/vuln-bank`):

```bash
cd ~/code/vuln-bank
git fetch origin
# New branch for the second agent:
git worktree add ../vuln-bank-claude -b claude/01-my-task
# Or attach to an existing branch:
# git worktree add ../vuln-bank-claude claude/01-my-task
```

Point the second agent at `~/code/vuln-bank-claude`. The first agent stays in `~/code/vuln-bank`. Push from either path: `git push -u origin <branch>`.

```bash
git worktree list
git worktree remove ../vuln-bank-claude   # after merge or abandon
```

### Beads with multiple worktrees

Beads (`.beads/`) is tied to where `bd init` ran. **Practical pattern:**

1. Use **one** directory for Beads (usually the **main** worktree).
2. Run **`bd ready`**, **`bd update <id> --claim`**, **`bd close`** only from that directory (or use a shared Dolt server per [Beads docs](https://steveyegge.github.io/beads/)).
3. Edit code in the worktree that has your feature branch.

Do not rely on separate `.beads` per worktree for coordination—claims would not be shared.

See [.workflow/beads-coordination.md](beads-coordination.md) — *Parallel agents and directories*.

---

*Last updated: March 2026*
