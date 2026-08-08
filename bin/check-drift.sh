#!/usr/bin/env bash
# check-drift.sh — detect divergence between the on-disk registry and the
# skills actually loaded into Claude sessions (account/cloud store).
#
# Runs on BOTH macOS (operator side) and Linux (agent side, in-session).
#
# Usage:
#   check-drift.sh export [<skills-dir>] [<out.tsv>]
#       Hash every skill's SKILL.md into a manifest.
#       Defaults: <skills-dir> = ~/Cortana/cortana-skill-registry/skills
#                 <out.tsv>    = <manifest-dir>/registry-manifest.tsv
#   check-drift.sh compare <a.tsv> <b.tsv>
#       Diff two manifests. Exit 1 if any drift.
#   check-drift.sh   (no args, operator side)
#       Export the registry manifest into the vault manifest dir, then compare
#       against session-manifest.tsv there if an agent has dropped one.
#
# Manifest format (TSV): name  body_sha  desc_sha  bytes
#   body_sha = sha256 of SKILL.md content BELOW the frontmatter (leading blank
#              lines and trailing whitespace stripped)
#   desc_sha = sha256 of the normalized description (quotes stripped, escaped
#              quotes unescaped, whitespace collapsed)
# Cosmetic frontmatter re-quoting (the cloud store quotes values) therefore
# does NOT count as drift; real wording/body changes do.
set -euo pipefail

MANIFEST_DIR="${SKILL_MANIFESTS:-$HOME/Cortana/cortana-vault/_inbox/skills/_manifests}"
DEFAULT_SKILLS="$HOME/Cortana/cortana-skill-registry/skills"

sha() { if command -v sha256sum >/dev/null 2>&1; then sha256sum | cut -c1-12; else shasum -a 256 | cut -c1-12; fi; }

hash_skill() {  # hash_skill <SKILL.md>  -> "body_sha<TAB>desc_sha<TAB>bytes"
  local f="$1" fm_end body_sha desc desc_sha bytes
  fm_end="$(awk 'NR==1 && !/^---[[:space:]]*$/ {print 0; exit} NR>1 && /^---[[:space:]]*$/ {print NR; exit}' "$f")"
  [ -z "$fm_end" ] && fm_end=0
  if [ "$fm_end" -gt 0 ]; then
    body_sha="$(awk -v s="$fm_end" 'NR>s' "$f" | sed -e 's/[[:space:]]*$//' \
      | awk '{ if (!started && $0=="") next; started=1; l[n++]=$0 }
             END { while (n>0 && l[n-1]=="") n--; for (i=0;i<n;i++) print l[i] }' | sha)"
    desc="$(sed -n "2,$((fm_end-1))p" "$f" | awk '
      !found && /^description:/ { found=1; sub(/^description:[[:space:]]*/,""); val=$0; next }
      found && /^[[:space:]]+[^[:space:]]/ { line=$0; sub(/^[[:space:]]+/,"",line); val=val " " line; next }
      found { exit }
      END { if (found) print val }' \
      | sed -e 's/^[>|][+-]\{0,1\}[[:space:]]*//' -e 's/^"//' -e 's/"[[:space:]]*$//' -e "s/^'//" -e "s/'[[:space:]]*\$//" -e 's/\\"/"/g' \
      | tr -s '[:space:]' ' ' | sed -e 's/^ //' -e 's/ $//')"
    desc_sha="$(printf '%s' "$desc" | sha)"
  else
    body_sha="$(cat "$f" | sha)"; desc_sha="noheader"
  fi
  bytes="$(wc -c < "$f" | xargs)"
  printf '%s\t%s\t%s' "$body_sha" "$desc_sha" "$bytes"
}

do_export() {
  local dir="${1:-$DEFAULT_SKILLS}" out="${2:-$MANIFEST_DIR/registry-manifest.tsv}"
  [ -d "$dir" ] || { echo "error: skills dir $dir not found" >&2; exit 1; }
  mkdir -p "$(dirname "$out")"
  : > "$out.tmp"
  local n=0
  for d in "$dir"/*/; do
    [ -f "$d/SKILL.md" ] || continue
    name="$(basename "$d")"
    case "$name" in _*|.*) continue ;; esac
    printf '%s\t%s\n' "$name" "$(hash_skill "$d/SKILL.md")" >> "$out.tmp"
    n=$((n+1))
  done
  sort "$out.tmp" > "$out" && rm -f "$out.tmp"
  echo "exported $n skills -> $out"
}

do_compare() {
  local a="$1" b="$2"
  [ -f "$a" ] && [ -f "$b" ] || { echo "error: manifest missing ($a / $b)" >&2; exit 1; }
  la="$(basename "$a" .tsv)"; lb="$(basename "$b" .tsv)"
  awk -F'\t' -v la="$la" -v lb="$lb" '
    NR==FNR { A[$1]=$2 FS $3; next }
    { B[$1]=$2 FS $3 }
    END {
      same=0; diffs=0; onlya=0; onlyb=0
      for (k in A) if (!(k in B)) { onlya++; oa=oa "  " k "\n" }
      for (k in B) if (!(k in A)) { onlyb++; ob=ob "  " k "\n" }
      for (k in A) if (k in B) {
        if (A[k]==B[k]) same++
        else {
          diffs++
          split(A[k],x,FS); split(B[k],y,FS)
          what=""
          if (x[1]!=y[1]) what="body"
          if (x[2]!=y[2]) what=(what=="" ? "description" : what "+description")
          dl=dl "  " k " (" what ")\n"
        }
      }
      printf "in sync: %d\n", same
      if (diffs)  printf "DIFFERS (%d):\n%s", diffs, dl
      if (onlya)  printf "only in %s (%d):\n%s", la, onlya, oa
      if (onlyb)  printf "only in %s (%d):\n%s", lb, onlyb, ob
      exit (diffs>0 ? 1 : 0)
    }' "$a" "$b"
}

cmd="${1:-auto}"
case "$cmd" in
  export)  shift; do_export "$@" ;;
  compare) shift; do_compare "$@" ;;
  auto)
    do_export
    if [ -f "$MANIFEST_DIR/session-manifest.tsv" ]; then
      echo ""
      echo "comparing registry vs session (account store):"
      do_compare "$MANIFEST_DIR/registry-manifest.tsv" "$MANIFEST_DIR/session-manifest.tsv"
    else
      echo "no session-manifest.tsv yet — ask the agent to run its half"
      echo "(skill-publish skill, 'Drift check' section) and re-run."
    fi
    ;;
  *) echo "usage: check-drift.sh [export|compare|<no args>]" >&2; exit 1 ;;
esac
