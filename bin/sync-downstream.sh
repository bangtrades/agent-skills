#!/bin/bash
# sync-downstream.sh — propagate the registry to all downstream surfaces.
# Called automatically by the post-commit hook; safe to run manually anytime.
# Surfaces: (1) origin push (bangtrades/agent-skills), (2) WaiveLabs org mirror
# (rsync -> commit -> push). Network failures WARN, never block — the commit
# already happened; sync state is recorded so the weekly consolidation can nag.
set -uo pipefail
REG="$(cd "$(dirname "$0")/.." && pwd)"
STATE="$REG/.sync-state"
MIRROR="${SKILL_MIRROR:-$HOME/Projects/agency/WaiveLabs/agent-skills}"
ts() { date "+%Y-%m-%d %H:%M:%S"; }
note() { echo "[sync-downstream] $*"; echo "$(ts) $*" >> "$STATE"; }

# 1. push registry to its origin
if git -C "$REG" push origin main >/dev/null 2>&1; then
  note "origin push OK ($(git -C "$REG" rev-parse --short HEAD))"
else
  note "WARN origin push FAILED (offline/no creds?) — run: git -C $REG push origin main"
fi

# 2. sync org mirror
if [ -d "$MIRROR/.git" ]; then
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --delete --exclude "*.zip" --exclude "*.bak" "$REG/skills/" "$MIRROR/skills/"
  else
    cp -R "$REG/skills/." "$MIRROR/skills/"
  fi
  if [ -n "$(git -C "$MIRROR" status --porcelain)" ]; then
    git -C "$MIRROR" add -A skills
    git -C "$MIRROR" commit -q -m "sync: registry $(git -C "$REG" rev-parse --short HEAD) ($(ls "$REG/skills" | grep -vc '\.' ) skills)" \
      && note "mirror commit OK" || note "WARN mirror commit failed"
  else
    note "mirror already current"
  fi
  if git -C "$MIRROR" push origin main >/dev/null 2>&1; then
    note "mirror push OK"
  else
    note "WARN mirror push FAILED — run: git -C $MIRROR push origin main"
  fi
else
  note "WARN mirror not found at $MIRROR — set SKILL_MIRROR or clone it"
fi
