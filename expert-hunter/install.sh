#!/bin/bash
# Install /expert-hunter skill into Claude Code (directory-based layout)
# Source of truth: this repo (egor-project/expert-hunter/SKILL.md)
# Target: ~/.claude/skills/expert-hunter/SKILL.md

set -euo pipefail

REPO_SKILL="$(cd "$(dirname "$0")" && pwd)/SKILL.md"
TARGET_DIR="$HOME/.claude/skills/expert-hunter"
TARGET="$TARGET_DIR/SKILL.md"

if [ ! -f "$REPO_SKILL" ]; then
    echo "ERROR: SKILL.md not found at $REPO_SKILL"
    exit 1
fi

# Remove old single-file layout if exists
[ -f "$HOME/.claude/skills/expert-hunter.md" ] && rm "$HOME/.claude/skills/expert-hunter.md"

mkdir -p "$TARGET_DIR"
cp "$REPO_SKILL" "$TARGET"
echo "Installed: $TARGET (from $REPO_SKILL)"
