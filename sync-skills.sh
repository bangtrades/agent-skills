#!/usr/bin/env bash
# Cortana skill sync — keep Codex, Claude, and Hermes harnesses pointed at the
# single canonical registry. Idempotent and safe to re-run.
#
#   Codex  & Claude : MIRROR  — every registry skill becomes a per-skill symlink
#                     (real dirs backed up; harness-internal siblings preserved).
#   Hermes          : FILL    — only adds top-level symlinks for registry skills
#                     Hermes doesn't already have (anywhere, nested included), so
#                     its own curator-managed library and categories are untouched.
#
# Editing an existing shared skill propagates instantly (symlinks resolve to the
# clone). New skills appear on the next `git pull`/`commit` via the installed
# git hooks (this script wires them up).
set -euo pipefail

CANONICAL="${CANONICAL:-$HOME/Cortana/cortana-skill-registry}"
SRC="$CANONICAL/skills"

# Harness skills dirs — override via env if yours differ. Empty = skip.
CODEX_SKILLS="${CODEX_SKILLS:-$HOME/.codex/skills}"
CLAUDE_SKILLS="${CLAUDE_SKILLS:-$HOME/.claude/skills}"
# Hermes lives on the symba volume by default; fall back to ~/.hermes.
if [ -z "${HERMES_SKILLS:-}" ]; then
  if [ -d /Volumes/symba/.hermes/skills ]; then HERMES_SKILLS=/Volumes/symba/.hermes/skills
  else HERMES_SKILLS="$HOME/.hermes/skills"; fi
fi

ts() { date +%Y%m%d-%H%M%S; }
[ -d "$SRC" ] || { echo "FATAL: registry skills not found at $SRC" >&2; exit 1; }

# MIRROR: every registry skill -> per-skill symlink in target (back up real dirs).
mirror() {
  local T="$1" L="$2"; [ -z "$T" ] && return 0
  mkdir -p "$T"; local bk="$T/.pre-consolidation-backup-$(ts)" n=0 b=0
  for d in "$SRC"/*/; do
    local id; id=$(basename "$d"); local tgt="$T/$id"
    if [ -L "$tgt" ]; then rm -f "$tgt"
    elif [ -e "$tgt" ]; then mkdir -p "$bk"; mv "$tgt" "$bk/$id"; b=$((b+1)); fi
    ln -s "$SRC/$id" "$tgt"; n=$((n+1))
  done
  echo "[$L] mirror: $n linked, $b backed up -> $T"
}

# FILL: add top-level symlinks only for registry skills Hermes lacks anywhere.
fill() {
  local T="$1" L="$2"; [ -z "$T" ] && return 0
  [ -d "$T" ] || { echo "[$L] skip (no dir $T)"; return 0; }
  # set of skill ids Hermes already has (top-level + nested)
  local have; have=$(find "$T" -name SKILL.md 2>/dev/null \
                     | grep -v '\.curator_backups' \
                     | sed 's#/SKILL.md$##' | xargs -n1 basename 2>/dev/null | sort -u)
  local n=0
  for d in "$SRC"/*/; do
    local id; id=$(basename "$d")
    if printf '%s\n' "$have" | grep -qx "$id"; then continue; fi      # keep native
    local tgt="$T/$id"
    [ -L "$tgt" ] && rm -f "$tgt"
    [ -e "$tgt" ] && continue
    ln -s "$SRC/$id" "$tgt"; n=$((n+1))
  done
  echo "[$L] fill: $n new top-level symlinks -> $T (native/curator skills untouched)"
}

# Wire git hooks so pulls/commits re-sync automatically (per-clone local config).
install_hooks() {
  local hd="$CANONICAL/hooks"
  if [ -d "$hd" ]; then
    git -C "$CANONICAL" config core.hooksPath hooks
    chmod +x "$hd"/* 2>/dev/null || true
    echo "[hooks] core.hooksPath -> hooks (auto-resync on merge/checkout/commit)"
  fi
}

echo "== Cortana skill sync =="
echo "registry: $SRC ($(ls "$SRC" | wc -l | tr -d ' ') skills)"
mirror "$CODEX_SKILLS"  codex
mirror "$CLAUDE_SKILLS" claude
fill   "$HERMES_SKILLS" hermes
install_hooks
echo "done."
