#!/bin/bash
set -euo pipefail

SKILL_DIR="$HOME/.claude/skills/broker-checker-gptzero"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ ! -f "$SCRIPT_DIR/SKILL.md" ]; then
  echo "ERROR: SKILL.md not found in $SCRIPT_DIR"
  exit 1
fi

mkdir -p "$SKILL_DIR"
cp "$SCRIPT_DIR/SKILL.md" "$SKILL_DIR/SKILL.md"

echo "Installed /broker-checker-gptzero skill to $SKILL_DIR/SKILL.md"
echo ""
echo "IMPORTANT: Set the API key before using:"
echo "  export GPTZERO_API_KEY=<key>"
echo ""
echo "Restart Claude Code to activate."
