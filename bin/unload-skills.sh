#!/usr/bin/env bash
# unload-skills.sh — Remove local project skills from Claude Code, Codex, OpenCode, and/or Pi
# Usage:
#   ./unload-skills.sh --all       # Remove from .claude/, .codex/, .opencode/, and .agents/
#   ./unload-skills.sh --claude    # Remove from .claude/ only
#   ./unload-skills.sh --codex     # Remove from .codex/ only
#   ./unload-skills.sh --opencode  # Remove from .opencode/ only
#   ./unload-skills.sh --pi        # Remove from .agents/ only

set -e

REPO_ROOT=$(git -C "${PWD}" rev-parse --show-toplevel 2>/dev/null || pwd)
SKILL_NAMES=("ado-story-intake" "ado-story-refinement" "ado-progress-sync" "ado-completion-closeout" "ado-to-prd")

# Default to --all if no argument provided
MODE="${1:---all}"

unload_platform() {
  local platform="$1"
  local target_dir="$REPO_ROOT/$2"
  local skills_dir="$target_dir/skills"
  local removed=false

  for skill_name in "${SKILL_NAMES[@]}"; do
    local skill_path="$skills_dir/$skill_name"

    if [ -L "$skill_path" ] || [ -e "$skill_path" ]; then
      rm -rf "$skill_path"
      echo "  ✓ Removed $skill_name"
      removed=true
    fi
  done

  if [ "$removed" = false ]; then
    echo "  $platform skills not found at $skills_dir/"
    return
  fi

  echo "✓ $platform skills removed"

  if [ -d "$skills_dir" ] && [ -z "$(ls -A "$skills_dir")" ]; then
    rmdir "$skills_dir"
    echo "  Cleaned up empty $skills_dir/"
  fi

  if [ -d "$target_dir" ] && [ -z "$(ls -A "$target_dir")" ]; then
    rmdir "$target_dir"
    echo "  Cleaned up empty $target_dir/"
  fi
}

case "$MODE" in
  --all)
    unload_platform "Claude Code" ".claude"
    unload_platform "Codex" ".codex"
    unload_platform "OpenCode" ".opencode"
    unload_platform "Pi" ".agents"
    echo ""
    echo "✓ All platforms unloaded!"
    ;;
  --claude)
    unload_platform "Claude Code" ".claude"
    echo ""
    echo "✓ Claude Code unloaded!"
    ;;
  --codex)
    unload_platform "Codex" ".codex"
    echo ""
    echo "✓ Codex unloaded!"
    ;;
  --opencode)
    unload_platform "OpenCode" ".opencode"
    echo ""
    echo "✓ OpenCode unloaded!"
    ;;
  --pi)
    unload_platform "Pi" ".agents"
    echo ""
    echo "✓ Pi unloaded!"
    ;;
  *)
    echo "Usage: $0 [--all|--claude|--codex|--opencode|--pi]"
    echo ""
    echo "Options:"
    echo "  --all       Remove from Claude Code, Codex, OpenCode, and Pi"
    echo "  --claude    Remove from Claude Code only"
    echo "  --codex     Remove from Codex only"
    echo "  --opencode  Remove from OpenCode only"
    echo "  --pi        Remove from Pi only (.agents/skills)"
    exit 1
    ;;
esac
