#!/usr/bin/env bash
# unload-skills.sh — Remove local project skills from Claude Code, Codex, and/or OpenCode
# Usage:
#   ./unload-skills.sh --all       # Remove from .claude/, .codex/, and .opencode/
#   ./unload-skills.sh --claude    # Remove from .claude/ only
#   ./unload-skills.sh --codex     # Remove from .codex/ only
#   ./unload-skills.sh --opencode  # Remove from .opencode/ only

set -e

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
cd "$REPO_ROOT"

# Default to --all if no argument provided
MODE="${1:---all}"

unload_platform() {
  local platform="$1"
  local target_dir="$2"

  if [ ! -d "$target_dir/ado-workflow" ]; then
    echo "  $platform skills not found at $target_dir/ado-workflow/"
    return
  fi

  echo "Removing $platform skills from $target_dir..."
  rm -rf "$target_dir/ado-workflow"
  echo "✓ $platform skills removed"

  # Clean up empty parent directory if it exists and is empty
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
  *)
    echo "Usage: $0 [--all|--claude|--codex|--opencode]"
    echo ""
    echo "Options:"
    echo "  --all       Remove from Claude Code, Codex, and OpenCode"
    echo "  --claude    Remove from Claude Code only"
    echo "  --codex     Remove from Codex only"
    echo "  --opencode  Remove from OpenCode only"
    exit 1
    ;;
esac
