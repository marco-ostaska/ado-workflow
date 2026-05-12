#!/usr/bin/env bash
# init-skills.sh — Initialize local project skills for Claude Code, Codex, and/or OpenCode
# Usage:
#   ./init-skills.sh --all       # Create in .claude/, .codex/, and .opencode/
#   ./init-skills.sh --claude    # Create in .claude/ only
#   ./init-skills.sh --codex     # Create in .codex/ only
#   ./init-skills.sh --opencode  # Create in .opencode/ only

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ADO_WORKFLOWS_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

REPO_ROOT=$(git -C "${PWD}" rev-parse --show-toplevel 2>/dev/null || pwd)

SKILLS_DIR="$ADO_WORKFLOWS_ROOT/skills"
SKILL_NAMES=("ado-story-intake" "ado-story-refinement" "ado-progress-sync" "ado-completion-closeout" "ado-to-prd")

# Check if skills directory exists
if [ ! -d "$SKILLS_DIR" ]; then
  echo "Error: skills directory not found at $SKILLS_DIR"
  exit 1
fi

# Default to --all if no argument provided
MODE="${1:---all}"

setup_platform() {
  local platform="$1"
  local target_dir="$REPO_ROOT/$2"

  echo "Setting up $platform skills in $target_dir..."

  mkdir -p "$target_dir/skills"

  for skill_name in "${SKILL_NAMES[@]}"; do
    if [ ! -d "$SKILLS_DIR/$skill_name" ]; then
      echo "  Warning: $skill_name not found, skipping"
      continue
    fi

    link_path="$target_dir/skills/$skill_name"

    # Remove existing link if present
    if [ -L "$link_path" ] || [ -e "$link_path" ]; then
      echo "  Removing existing $skill_name link/directory"
      rm -rf "$link_path"
    fi

    # Create relative symlink
    # Calculate relative path from link location to skill
    relative_path=$(python3 -c "
import os
link = '$link_path'
target = os.path.abspath('$SKILLS_DIR/$skill_name')
link_dir = os.path.dirname(link)
rel = os.path.relpath(target, link_dir)
print(rel)
")

    ln -s "$relative_path" "$link_path"
    echo "  ✓ Linked $skill_name"
  done

  echo "✓ $platform setup complete at $target_dir/skills/"
}

case "$MODE" in
  --all)
    setup_platform "Claude Code" ".claude"
    setup_platform "Codex" ".codex"
    setup_platform "OpenCode" ".opencode"
    echo ""
    echo "✓ All platforms initialized!"
    echo "  .claude/skills/     (Claude Code)"
    echo "  .codex/skills/      (Codex)"
    echo "  .opencode/skills/   (OpenCode)"
    ;;
  --claude)
    setup_platform "Claude Code" ".claude"
    echo ""
    echo "✓ Claude Code initialized!"
    echo "  .claude/skills/"
    ;;
  --codex)
    setup_platform "Codex" ".codex"
    echo ""
    echo "✓ Codex initialized!"
    echo "  .codex/skills/"
    ;;
  --opencode)
    setup_platform "OpenCode" ".opencode"
    echo ""
    echo "✓ OpenCode initialized!"
    echo "  .opencode/skills/"
    ;;
  *)
    echo "Usage: $0 [--all|--claude|--codex|--opencode]"
    echo ""
    echo "Options:"
    echo "  --all       Initialize for Claude Code, Codex, and OpenCode"
    echo "  --claude    Initialize for Claude Code only"
    echo "  --codex     Initialize for Codex only"
    echo "  --opencode  Initialize for OpenCode only"
    exit 1
    ;;
esac
