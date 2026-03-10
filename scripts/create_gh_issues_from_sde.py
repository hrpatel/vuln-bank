#!/usr/bin/env python3
"""Create GitHub issues from vuln-bank SDE countermeasures JSON. Uses gh api."""
import json
import re
import subprocess
import sys

REPO = "hrpatel/vuln-bank"
JSON_PATH = ".tmp/sde-countermeasures.json"


def escape_body(s: str) -> str:
    if not s:
        return ""
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\r", "").replace("\n", "\\n")


def main():
    with open(JSON_PATH, "r") as f:
        data = json.load(f)
    results = data.get("results", [])
    created = 0
    for r in results:
        task_id = r.get("task_id", "")
        sid = r.get("id", "")
        title = r.get("title", "Untitled")
        phase = r.get("phase") or {}
        phase_name = phase.get("name", "")
        phase_slug = phase.get("slug", "requirements")
        problem = r.get("problem") or {}
        problem_title = problem.get("title", "")
        text = r.get("text") or {}
        desc = (text.get("description") or "").strip()
        url = r.get("url", "")

        gh_title = f"[Security] {phase_name}: {title} (SDE {task_id})"
        if len(gh_title) > 256:
            gh_title = gh_title[:253] + "..."

        body_parts = [
            "## Source",
            f"- **SDElements:** vuln-bank (31763) · [task]({url})",
            f"- **Task ID:** {task_id} ({sid})",
            f"- **Phase:** {phase_name}",
            f"- **Problem:** {problem_title}",
            "",
            "## Description",
            desc or "(No description.)",
            "",
            "## Acceptance criteria",
            "- [ ] Implement/verify per SDE guidance",
        ]
        body = "\n".join(body_parts)

        labels = ["security", f"phase:{phase_slug}", "available", "created-by:cursor"]
        label_args = [f for L in labels for f in ("-f", f"labels[]={L}")]

        cmd = [
            "gh", "api", f"repos/{REPO}/issues", "-X", "POST",
            "-f", f"title={gh_title}",
            "-f", f"body={body}",
        ] + label_args

        try:
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if out.returncode != 0:
                print(f"Failed {task_id}: {out.stderr or out.stdout}", file=sys.stderr)
                continue
            created += 1
            num = json.loads(out.stdout).get("number", "?")
            print(f"  #{num} {task_id}: {title[:50]}...")
        except Exception as e:
            print(f"Error {task_id}: {e}", file=sys.stderr)
    print(f"Created {created}/{len(results)} issues.")


if __name__ == "__main__":
    main()
