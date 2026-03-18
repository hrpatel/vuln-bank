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

**Problem:** Two AI agents using the **same directory** will fight over the working tree when each checks out a different branch. They also share the same `git user.name`, which makes `bd` claims indistinguishable.

**Fix: `spawn-agent.sh`.** Run it once per agent from the main repo root. It creates a sibling worktree with a distinct agent identity.

```bash
cd ~/code/vuln-bank                                # main repo (base camp)
scripts/spawn-agent.sh cursor-a                    # creates ../vuln-bank-cursor-a
scripts/spawn-agent.sh cursor-b --branch cursor/02-fix  # creates ../vuln-bank-cursor-b
```

Point each agent at its own folder. The main repo is the "base camp" — no agent should work directly in it.

**What the script does:**
1. Creates a git worktree via `bd worktree create` (shares `.beads` database)
2. Sets `git config --worktree user.name <agent-name>` so `bd` commands use a distinct identity
3. Writes `.bd-agent-identity` so agents can verify their workspace at session start

**Teardown:**

```bash
scripts/teardown-agent.sh cursor-a            # removes ../vuln-bank-cursor-a
scripts/teardown-agent.sh cursor-b --force    # force-remove even with uncommitted changes
```

**Listing active workspaces:**

```bash
git worktree list
```

### Beads with multiple worktrees

All worktrees share the same Beads database (the spawn script sets up the `.beads` redirect). Run `bd ready`, `bd update <id> --claim`, and `bd close` from **any** worktree — claims are globally visible because the database is shared.

Each worktree has a distinct `git user.name`, so `bd` records a different assignee per agent. This prevents the cross-claim confusion that occurs when all agents share one identity.

---

*Last updated: March 2026*
