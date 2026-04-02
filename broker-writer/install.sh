#!/bin/bash
set -euo pipefail

SKILL_DIR="$HOME/.claude/skills/broker-writer"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ ! -f "$SCRIPT_DIR/SKILL.md" ]; then
  echo "ERROR: SKILL.md not found in $SCRIPT_DIR"
  exit 1
fi

mkdir -p "$SKILL_DIR"
cp "$SCRIPT_DIR/SKILL.md" "$SKILL_DIR/SKILL.md"

# Remove old flat-file layout if exists
if [ -f "$HOME/.claude/skills/broker-writer.md" ]; then
  rm "$HOME/.claude/skills/broker-writer.md"
  echo "Removed old flat file: ~/.claude/skills/broker-writer.md"
fi

echo "Installed /broker-writer skill to $SKILL_DIR/SKILL.md"
echo "Restart Claude Code to activate."
