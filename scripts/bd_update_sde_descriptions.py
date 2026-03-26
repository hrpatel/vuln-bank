#!/usr/bin/env python3
"""Update Beads issues that have sde-* external refs with SDE countermeasure text."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SDE_JSON = Path(sys.argv[1]) if len(sys.argv) > 1 else None


def main():
    if not SDE_JSON or not SDE_JSON.is_file():
        print("Usage: bd_update_sde_descriptions.py <path-to-sde-tasks.json>", file=sys.stderr)
        sys.exit(1)

    data = json.loads(SDE_JSON.read_text())
    id_to_text = {r["id"]: r.get("text") or "" for r in data["results"]}

    out = subprocess.run(
        ["bd", "list", "--json"],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        check=True,
    )
    issues = json.loads(out.stdout)

    updated = 0
    for issue in issues:
        ref = issue.get("external_ref") or ""
        if not ref.startswith("sde-"):
            continue
        sde_id = ref.removeprefix("sde-")  # e.g. 31763-T2
        text = id_to_text.get(sde_id)
        if text is None:
            print(f"Skip {issue['id']}: no SDE text for {sde_id}", file=sys.stderr)
            continue
        bead_id = issue["id"]
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(text)
            path = f.name
        try:
            subprocess.run(
                ["bd", "update", bead_id, "--body-file", path],
                cwd=Path(__file__).resolve().parents[1],
                check=True,
            )
            print(f"Updated {bead_id} ({sde_id})")
            updated += 1
        finally:
            Path(path).unlink(missing_ok=True)

    print(f"Done: {updated} issues updated.", file=sys.stderr)


if __name__ == "__main__":
    main()
