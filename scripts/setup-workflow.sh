#!/usr/bin/env bash
set -euo pipefail

# scripts/setup-workflow.sh
# Purpose: Initialize the local issue-tracker configuration from a template.

TEMPLATE=".workflow/issue-tracker.md.template"
TARGET=".workflow/issue-tracker.md"

usage() {
    echo "Usage: $0 [--tracker <beads|github|jira>] [--force]"
    echo ""
    echo "Options:"
    echo "  --tracker <choice>  Pre-select tracker: beads, github, or jira"
    echo "  --force             Overwrite existing $TARGET"
    echo ""
    exit 1
}

die() { echo "ERROR: $1" >&2; exit 1; }

TRACKER_CHOICE=""
FORCE=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --tracker)
            [[ $# -lt 2 ]] && die "--tracker requires a value"
            TRACKER_CHOICE=$(echo "$2" | tr '[:upper:]' '[:lower:]')
            shift 2 ;;
        --force)
            FORCE=true; shift ;;
        -h|--help)
            usage ;;
        *)
            die "Unknown option: $1" ;;
    esac
done

[[ -f "$TEMPLATE" ]] || die "Template not found: $TEMPLATE"

if [[ -f "$TARGET" ]] && [[ "$FORCE" == "false" ]]; then
    echo "$TARGET already exists. Use --force to overwrite."
    exit 0
fi

# Prompt if no tracker choice provided
if [[ -z "$TRACKER_CHOICE" ]]; then
    echo "Which issue tracker will this clone use for task coordination?"
    echo "1) Beads (Local + Optional Jira sync)"
    echo "2) GitHub Issues (Real-time cloud sync)"
    echo "3) Jira (Direct Atlassian sync)"
    read -rp "Select [1-3]: " CHOICE
    case "$CHOICE" in
        1) TRACKER_CHOICE="beads" ;;
        2) TRACKER_CHOICE="github" ;;
        3) TRACKER_CHOICE="jira" ;;
        *) die "Invalid selection" ;;
    esac
fi

case "$TRACKER_CHOICE" in
    beads)
        DISPLAY_NAME="Beads"
        GUIDE_LINK='→ Follow **[beads-coordination.md](beads-coordination.md)** to find work, claim tasks, and track dependencies. Implementation work is synced to Jira for reporting and visibility; see [Beads + Jira dual-tracker design](../docs/specs/2026-03-13-beads-jira-dual-tracker-design.md).'
        ;;
    github)
        DISPLAY_NAME="GitHub Issues"
        GUIDE_LINK='→ Follow **[github-issues-coordination.md](github-issues-coordination.md)** to find work, claim tasks, and track dependencies.'
        ;;
    jira)
        DISPLAY_NAME="Jira"
        GUIDE_LINK='→ Follow **[jira-coordination.md](jira-coordination.md)** to find work, claim tasks, and track dependencies.'
        ;;
    *)
        die "Invalid tracker choice: $TRACKER_CHOICE. Use 'beads', 'github', or 'jira'."
        ;;
esac

echo "Initializing $TARGET for $DISPLAY_NAME..."

export TRACKER_CHOICE_VAL="$DISPLAY_NAME"
export GUIDE_LINK_VAL="$GUIDE_LINK"

# Use perl -pe with environment variables to safely handle special characters in the replacement string
perl -pe 's/\[TRACKER_CHOICE\]/$ENV{TRACKER_CHOICE_VAL}/g; s/\[DYNAMIC_GUIDE_LINK\]/$ENV{GUIDE_LINK_VAL}/g' "$TEMPLATE" > "$TARGET"

echo "Done. Issue tracker set to $DISPLAY_NAME."
