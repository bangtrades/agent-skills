#!/bin/bash
# Publish committed registry content to origin and the company mirror.
# Dirty mirror work is never overwritten. Replaced files go to external trash.
# CORTANA_DEFER_DOWNSTREAM=1 defers the post-commit invocation during a batch;
# this script itself always performs the explicitly requested synchronization.
set -euo pipefail
REG="$(cd "$(dirname "$0")/.." && pwd)"
STATE="$REG/.sync-state"
MIRROR="${SKILL_MIRROR:-}"
if [ -z "$MIRROR" ]; then
  MIRROR="$(git -C "$REG" config --get cortana.skillMirror || true)"
fi
if [ -z "$MIRROR" ]; then
  for c in "$HOME/Projects/agency/WaiveLabs/agent-skills" \
           "/sessions"/*/mnt/Projects/agency/WaiveLabs/agent-skills; do
    [ -d "$c/.git" ] && MIRROR="$c" && break
  done
  MIRROR="${MIRROR:-$HOME/Projects/agency/WaiveLabs/agent-skills}"
fi
ts() { date "+%Y-%m-%d %H:%M:%S"; }
note() { echo "[sync-downstream] $*"; echo "$(ts) $*" >> "$STATE"; }
fail() { note "FAILED: $*"; exit 1; }

[ "$(git -C "$REG" branch --show-current)" = main ] || fail "registry must be on main"
SHA="$(git -C "$REG" rev-parse HEAD)"
if git -C "$REG" push origin HEAD:refs/heads/main; then
  note "origin push OK ($SHA)"
else
  fail "origin push failed; company mirror was not changed"
fi

[ -d "$MIRROR/.git" ] || fail "mirror clone missing at $MIRROR; set SKILL_MIRROR"
[ "$(git -C "$MIRROR" branch --show-current)" = main ] || fail "mirror must be on main"
[ -z "$(git -C "$MIRROR" status --porcelain)" ] || fail "mirror has existing changes; preserve/reconcile them or use a clean SKILL_MIRROR clone"
command -v rsync >/dev/null 2>&1 || fail "rsync unavailable; mirror untouched"

# Archive HEAD, never the working tree: untracked and unpublished skill edits
# must not leak into the organization mirror. Keep the snapshot for inspection.
SNAPSHOT="$(mktemp -d "${TMPDIR:-/tmp}/cortana-skills-downstream.XXXXXX")"
if ! git -C "$REG" archive "$SHA" skills | tar -xf - -C "$SNAPSHOT"; then
  fail "could not export committed skills; mirror untouched"
fi
[ -d "$SNAPSHOT/skills" ] || fail "committed skills unavailable; mirror untouched"
MIRROR_PARENT="$(cd "$MIRROR/.." && pwd)"
BACKUP="$MIRROR_PARENT/.trash/cortana-skill-sync/$(date +%Y%m%d-%H%M%S)-$$"
mkdir -p "$BACKUP"
note "snapshot=$SNAPSHOT restore_backup=$BACKUP"
# Preserve stale and changed paths by renaming them before the overlay copy.
# In particular, do not rely on platform-specific rsync deletion backups.
python3 - "$SNAPSHOT/skills" "$MIRROR/skills" "$BACKUP" <<'PY'
import filecmp
import json
import os
from pathlib import Path
import sys

source, target, backup = map(Path, sys.argv[1:])
receipt = {'state': 'running', 'moves': []}
record = backup/'moves.json'
def save():
    record.write_text(json.dumps(receipt, indent=2)+'\n')
save()
for current, dirs, files in os.walk(target, followlinks=False):
    for name in list(dirs)+files:
        path = Path(current)/name
        wanted = source/path.relative_to(target)
        if not path.is_symlink() and path.is_file() and name.endswith(('.zip', '.bak')):
            continue
        if path.is_symlink():
            same = wanted.is_symlink() and os.readlink(path) == os.readlink(wanted)
        elif path.is_dir():
            same = wanted.is_dir() and not wanted.is_symlink()
        else:
            if any('documents' in [part.lower() for part in p.resolve().parts] for p in (path, wanted)):
                raise ValueError('prohibited path target')
            same = wanted.is_file() and not wanted.is_symlink() and filecmp.cmp(path, wanted, shallow=False)
        if same:
            continue
        destination = backup/path.relative_to(target)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists() or destination.is_symlink():
            raise ValueError('backup collision')
        entry = {'path': str(path), 'restore_from': str(destination), 'state': 'pending'}
        receipt['moves'].append(entry);save()
        path.rename(destination)
        entry['state'] = 'done';save()
        if name in dirs:
            dirs.remove(name)
receipt['state'] = 'complete';save()
PY
if ! rsync -a --backup --backup-dir="$BACKUP" \
    --exclude "*.zip" --exclude "*.bak" "$SNAPSHOT/skills/" "$MIRROR/skills/"; then
  fail "mirror copy failed; no mirror commit or push; inspect snapshot and backup"
fi
if ! git -C "$MIRROR" diff --quiet -- skills || [ -n "$(git -C "$MIRROR" ls-files --others --exclude-standard -- skills)" ]; then
  git -C "$MIRROR" add -A -- skills
  # Preserve the existing fail-closed behavior: never push after failed commit.
  if cmsg=$(git -C "$MIRROR" commit -m "sync: registry $SHA" -- skills 2>&1); then
    note "mirror commit OK ($(git -C "$MIRROR" rev-parse --short HEAD))"
  else
    printf '%s\n' "$cmsg" >&2
    printf '%s\n' "$cmsg" >> "$STATE"
    fail "mirror commit failed; content remains staged; mirror push skipped"
  fi
else
  note "mirror already current"
fi
if git -C "$MIRROR" push origin HEAD:refs/heads/main; then
  note "mirror push OK ($(git -C "$MIRROR" rev-parse HEAD))"
else
  fail "mirror push failed; local mirror commit and backups retained"
fi
