#!/usr/bin/env bash
# Link all agent harnesses to ONE canonical clone of the consolidated skill registry.
# Pattern: single source of truth + per-harness symlink (edit once, every harness sees it;
# `git pull` in the canonical clone updates them all). Idempotent & safe — backs up any
# existing skills dir to <dir>.bak-<timestamp> before symlinking.
set -euo pipefail

# ---- EDIT THESE if your paths differ -------------------------------------
CANONICAL="${CANONICAL:-$HOME/Cortana/cortana-skill-registry}"     # the git clone
REPO_URL="${REPO_URL:-}"                                            # set to GitHub URL to clone if CANONICAL missing
# Each harness's skills directory. Comment out any you don't use.
CODEX_SKILLS="${CODEX_SKILLS:-$HOME/.codex/skills}"
CLAUDE_SKILLS="${CLAUDE_SKILLS:-$HOME/.claude/skills}"
# Hermes/Paperclip consume via read-only mount of CANONICAL/skills — see HARNESS-LINKING.md.
# --------------------------------------------------------------------------

ts() { date +%Y%m%d-%H%M%S; }

# 1) Ensure the canonical clone exists
if [ ! -d "$CANONICAL/.git" ]; then
  if [ -n "$REPO_URL" ]; then
    echo "==> Cloning $REPO_URL -> $CANONICAL"
    git clone "$REPO_URL" "$CANONICAL"
  else
    echo "ERROR: $CANONICAL is not a git clone and REPO_URL is unset." >&2
    echo "       Set REPO_URL=git@github.com:<you>/cortana-skill-registry.git and re-run." >&2
    exit 1
  fi
fi
SRC="$CANONICAL/skills"
[ -d "$SRC" ] || { echo "ERROR: $SRC not found"; exit 1; }

link_one() {
  local target="$1" label="$2"
  [ -z "$target" ] && return 0
  mkdir -p "$(dirname "$target")"
  if [ -L "$target" ]; then
    echo "==> $label: replacing existing symlink $target"
    rm "$target"
  elif [ -e "$target" ]; then
    local bak="$target.bak-$(ts)"
    echo "==> $label: backing up $target -> $bak"
    mv "$target" "$bak"
  fi
  ln -s "$SRC" "$target"
  echo "    linked $target -> $SRC"
}

link_one "$CODEX_SKILLS"  "codex"
link_one "$CLAUDE_SKILLS" "claude"

echo
echo "==> Linked harness skill dirs to $SRC"
echo "    Update everything later with:  git -C \"$CANONICAL\" pull"
echo "    Hermes/Paperclip: mount $SRC read-only into the container (see HARNESS-LINKING.md)."
