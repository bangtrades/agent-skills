#!/usr/bin/env bash
# publish-skill.sh — the ONLY sanctioned writer of the Cortana skill registry.
# Agent proposes (stages to the vault inbox); the operator runs this to publish.
#
# Usage:
#   publish-skill.sh [options] <skill-name> [<skill-name>...]
#
# Options:
#   -y, --yes         skip the confirm prompt (still lints, still diffs)
#   --exact           mirror the staged dir exactly (DELETES registry files not
#                     present in staging — default is a safe overlay merge)
#   --push            after publishing, push (push-to-github.sh or git push)
#   --staging <dir>   override staging root (default: vault _inbox/skills)
#   -m <msg>          commit summary override (single skill only)
#
# Compatible with macOS /bin/bash 3.2. No associative arrays, no mapfile.
set -euo pipefail

BIN_DIR="$(cd "$(dirname "$0")" && pwd)"
REGISTRY="$(cd "$BIN_DIR/.." && pwd)"
STAGING="${SKILL_STAGING:-$HOME/Cortana/cortana-vault/_inbox/skills}"
LINT="$BIN_DIR/lint-skill.sh"

YES=0; EXACT=0; PUSH=0; MSG=""
NAMES=""

usage() { sed -n '2,16p' "$0"; exit 1; }

while [ $# -gt 0 ]; do
  case "$1" in
    -y|--yes) YES=1 ;;
    --exact) EXACT=1 ;;
    --push) PUSH=1 ;;
    --staging) shift; STAGING="$1" ;;
    -m) shift; MSG="$1" ;;
    -h|--help) usage ;;
    -*) echo "unknown option: $1" >&2; usage ;;
    *) NAMES="$NAMES $1" ;;
  esac
  shift
done

NAMES="$(echo "$NAMES" | xargs || true)"
[ -n "$NAMES" ] || usage
set -- $NAMES
if [ -n "$MSG" ] && [ $# -gt 1 ]; then
  echo "error: -m only valid with a single skill" >&2; exit 1
fi

# --- sanity -----------------------------------------------------------------
[ -d "$REGISTRY/.git" ] || { echo "error: $REGISTRY is not a git repo" >&2; exit 1; }
[ -d "$REGISTRY/skills" ] || { echo "error: $REGISTRY/skills missing" >&2; exit 1; }
[ -d "$STAGING" ] || { echo "error: staging root $STAGING missing" >&2; exit 1; }
[ -x "$LINT" ] || { echo "error: $LINT missing or not executable" >&2; exit 1; }

install_skill() {  # install_skill <src> <dest> <exact 0|1> — tar copy, .DS_Store excluded
  if [ "$3" = 1 ]; then rm -rf "$2"; fi
  mkdir -p "$2"
  (cd "$1" && tar -cf - --exclude '.DS_Store' .) | (cd "$2" && tar -xf -)
}

confirm() {  # confirm "<prompt>" -> 0 yes / 1 no
  [ "$YES" = 1 ] && return 0
  printf "%s [y/N] " "$1"
  if [ -t 0 ]; then read -r ans; else read -r ans </dev/tty; fi
  case "$ans" in y|Y|yes|YES) return 0 ;; *) return 1 ;; esac
}

published=""; skipped=""; failed=""
STAMP="$(date +%Y%m%d-%H%M%S)"

for name in "$@"; do
  echo ""
  echo "=============================================================="
  echo "  skill: $name"
  echo "=============================================================="
  src="$STAGING/$name"
  dest="$REGISTRY/skills/$name"

  if [ ! -f "$src/SKILL.md" ]; then
    echo "  FAIL: no staged skill at $src (need SKILL.md)"; failed="$failed $name"; continue
  fi

  # --- lint ---
  if ! "$LINT" "$src"; then
    echo "  FAIL: lint failed — fix the staged copy and re-run"; failed="$failed $name"; continue
  fi

  # --- diff ---
  verb="update"
  if [ ! -d "$dest" ]; then
    verb="add"
    echo "  NEW skill (not in registry yet). Staged contents:"
    (cd "$src" && find . -type f | sed 's/^/    /')
    echo "  ---- SKILL.md (first 40 lines) ----"
    head -40 "$src/SKILL.md" | sed 's/^/    /'
  else
    stagedf="$(cd "$src" && find . -type f ! -name '.DS_Store' | sed 's|^\./||' | sort)"
    destf="$(cd "$dest" && find . -type f ! -name '.DS_Store' | sed 's|^\./||' | sort)"
    changedf=""
    while IFS= read -r f; do
      [ -n "$f" ] || continue
      if [ ! -f "$dest/$f" ] || ! cmp -s "$dest/$f" "$src/$f"; then
        changedf="$changedf$f
"
      fi
    done <<EOF_LIST
$stagedf
EOF_LIST
    # registry files not present in staging
    onlydest="$(printf '%s\n%s\n%s\n' "$stagedf" "$stagedf" "$destf" | sort | uniq -u)"
    if [ -z "$changedf" ] && { [ "$EXACT" != 1 ] || [ -z "$onlydest" ]; }; then
      echo "  already up to date — nothing to publish"
      skipped="$skipped $name"; continue
    fi
    echo "  ---- diff: registry -> staged ----"
    while IFS= read -r f; do
      [ -n "$f" ] || continue
      if [ -f "$dest/$f" ]; then
        git -C "$REGISTRY" -c core.pager=cat diff --no-index -- "$dest/$f" "$src/$f" || true
      else
        git -C "$REGISTRY" -c core.pager=cat diff --no-index -- /dev/null "$src/$f" || true
      fi
    done <<EOF_LIST2
$changedf
EOF_LIST2
    if [ -n "$onlydest" ]; then
      if [ "$EXACT" = 1 ]; then
        echo "  --exact: these registry files are NOT in staging and WILL BE DELETED:"
      else
        echo "  note: registry files not in staging (kept — overlay mode; use --exact to mirror):"
      fi
      echo "$onlydest" | sed 's/^/    /'
    fi
  fi

  # --- confirm ---
  if ! confirm "  Publish '$name' ($verb)?"; then
    echo "  declined — staged copy left at $src"; skipped="$skipped $name"; continue
  fi

  # --- install ---
  install_skill "$src" "$dest" "$EXACT"

  # skill-publish carries the registry tooling: refresh bin/ from its scripts/
  pathspec="skills/$name"
  if [ "$name" = "skill-publish" ] && [ -d "$dest/scripts" ]; then
    mkdir -p "$REGISTRY/bin"
    cp "$dest/scripts/"*.sh "$REGISTRY/bin/" && chmod +x "$REGISTRY/bin/"*.sh
    pathspec="$pathspec bin"
    echo "  refreshed bin/ from skills/skill-publish/scripts/"
  fi

  # --- commit ---
  nfiles="$(cd "$src" && find . -type f ! -name '.DS_Store' | wc -l | xargs)"
  summary="${MSG:-$verb $nfiles file(s) via publish-skill}"
  git -C "$REGISTRY" add -A -- $pathspec
  if git -C "$REGISTRY" diff --cached --quiet -- $pathspec; then
    echo "  nothing changed after install (unexpected) — no commit"
    skipped="$skipped $name"; continue
  fi
  git -C "$REGISTRY" commit -q -m "skill($name): $summary" -- $pathspec
  sha="$(git -C "$REGISTRY" rev-parse --short HEAD)"
  echo "  committed $sha: skill($name): $summary"

  # --- archive staged copy ---
  mkdir -p "$STAGING/_published"
  mv "$src" "$STAGING/_published/$name-$STAMP"
  echo "  staged copy archived to _published/$name-$STAMP"
  published="$published $name"
done

# --- push --------------------------------------------------------------------
echo ""
echo "=============================================================="
echo "  published:${published:- none}"
echo "  skipped:  ${skipped:- none}"
echo "  failed:   ${failed:- none}"
if [ -n "$published" ]; then
  if [ "$PUSH" = 1 ]; then
    if [ -x "$REGISTRY/push-to-github.sh" ]; then
      (cd "$REGISTRY" && ./push-to-github.sh)
    else
      git -C "$REGISTRY" push
    fi
  else
    echo "  next: push when ready (./push-to-github.sh or --push next time)"
  fi
  echo "  reminder: if this change did NOT originate in a Claude session,"
  echo "  sync the account/cloud store too (save the skill in a local session"
  echo "  or from the .skill file) so sessions load the same version."
fi
[ -z "$failed" ]
