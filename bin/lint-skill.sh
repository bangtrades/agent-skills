#!/usr/bin/env bash
# lint-skill.sh — pre-publish lint for a staged skill directory.
#
# Usage: lint-skill.sh <skill-dir> [--strict]
#   FAIL (exit 1): missing/invalid frontmatter, name mismatch, no trigger cues
#                  in description, secret-shaped strings, symlinks
#   WARN (exit 0): machine-absolute paths, oversize description/files,
#                  .DS_Store, self-improving skill without a Changelog
#   --strict: warnings also fail.
#
# Compatible with macOS /bin/bash 3.2.
set -euo pipefail

DIR="${1:-}"; STRICT="${2:-}"
[ -n "$DIR" ] && [ -d "$DIR" ] || { echo "usage: lint-skill.sh <skill-dir> [--strict]" >&2; exit 1; }
DIR="$(cd "$DIR" && pwd)"
SK="$DIR/SKILL.md"
base="$(basename "$DIR")"

fails=0; warns=0
fail() { echo "  LINT FAIL: $1"; fails=$((fails+1)); }
warn() { echo "  lint warn: $1"; warns=$((warns+1)); }

[ -f "$SK" ] || { echo "  LINT FAIL: SKILL.md missing"; echo "  LINT: FAIL"; exit 1; }

# --- frontmatter -------------------------------------------------------------
if [ "$(head -1 "$SK" | tr -d '[:space:]')" != "---" ]; then
  fail "SKILL.md must start with '---' frontmatter"
fi
fm_end="$(awk 'NR>1 && /^---[[:space:]]*$/ {print NR; exit}' "$SK")"
if [ -z "$fm_end" ]; then
  fail "frontmatter has no closing '---'"
  fm=""
else
  fm="$(sed -n "2,$((fm_end-1))p" "$SK")"
fi

fm_get() {  # fm_get <key> -> value; strips quotes/block markers, joins continuations
  echo "$fm" | awk -v key="$1" '
    !found && $0 ~ "^"key":" { found=1; sub("^"key":[[:space:]]*",""); val=$0; next }
    found && /^[[:space:]]+[^[:space:]]/ { line=$0; sub(/^[[:space:]]+/,"",line); val=val " " line; next }
    found { exit }
    END { if (found) print val }' \
  | sed -e 's/^[>|][+-]\{0,1\}[[:space:]]*//' \
        -e 's/^"//' -e 's/"[[:space:]]*$//' \
        -e "s/^'//" -e "s/'[[:space:]]*\$//" \
        -e 's/\\"/"/g'
}

name="$(fm_get name)"
desc="$(fm_get description)"

if [ -z "$name" ]; then fail "frontmatter 'name' missing"; fi
if [ -n "$name" ] && [ "$name" != "$base" ]; then fail "name '$name' != directory '$base'"; fi
if [ -n "$name" ] && ! echo "$name" | grep -Eq '^[a-z0-9][a-z0-9-]*$'; then
  fail "name '$name' not kebab-case ([a-z0-9-])"
fi

if [ -z "$desc" ]; then
  fail "frontmatter 'description' missing"
else
  if ! echo "$desc" | grep -Eiq 'use (when|this|whenever|if|for|after)|trigger'; then
    fail "description has no trigger cues (add 'Use when ...' / 'Trigger on ...')"
  fi
  dlen="$(printf '%s' "$desc" | wc -c | xargs)"
  if [ "$dlen" -gt 1024 ]; then warn "description is $dlen chars (>1024 — may truncate in pickers)"; fi
fi

# --- secrets -----------------------------------------------------------------
# Patterns use [ ]/[-]/[_]/[.] classes so this file never matches itself.
SECRET_PATS='[-]{5}BEGIN[ ].*PRIVATE[ ]KEY
sk[-]ant[-][A-Za-z0-9_-]{12,}
sk[-][A-Za-z0-9]{24,}
AKIA[0-9A-Z]{16}
ghp[_][A-Za-z0-9]{30,}
github[_]pat[_][A-Za-z0-9_]{22,}
xox[baprs][-][A-Za-z0-9-]{12,}
AIza[0-9A-Za-z_-]{30,}
eyJ[A-Za-z0-9_-]{20,}[.]eyJ'
WARN_PATS='(password|passwd|secret|api[_-]?key)[[:space:]]*[:=][[:space:]]*.\{0,1\}[A-Za-z0-9+/_-]{16,}
Bearer[ ][A-Za-z0-9._~+/-]{25,}'

scan() {  # scan "<patterns>" <TAG>  -> prints "TAG<tab>pattern" + indented hits
  echo "$1" | while IFS= read -r p; do
    [ -n "$p" ] || continue
    hits="$(grep -RInE -I --exclude-dir=.git -e "$p" "$DIR" 2>/dev/null | head -3 || true)"
    if [ -n "$hits" ]; then
      printf '%s\t%s\n' "$2" "$p"
      echo "$hits" | sed 's/^/      /'
    fi
  done
}

TAB="$(printf '\t')"
sec_out="$(scan "$SECRET_PATS" SECRET)"
if [ -n "$sec_out" ]; then
  echo "$sec_out" | sed "s/^SECRET${TAB}/  LINT FAIL: secret-shaped string matches /"
  fails=$((fails + $(printf '%s\n' "$sec_out" | grep -c "^SECRET") ))
fi
warn_out="$(scan "$WARN_PATS" CRED)"
if [ -n "$warn_out" ]; then
  echo "$warn_out" | sed "s/^CRED${TAB}/  lint warn: credential-shaped string matches /"
  warns=$((warns + $(printf '%s\n' "$warn_out" | grep -c "^CRED") ))
fi

# --- machine-absolute paths (warn) ------------------------------------------
path_hits="$(grep -RInE -I --exclude-dir=.git \
  -e '/(Users|home)/[A-Za-z][A-Za-z0-9_-]*/' -e '/Volumes/[A-Za-z]' \
  "$DIR" 2>/dev/null | head -5 || true)"
if [ -n "$path_hits" ]; then
  warn "machine-absolute path(s) — prefer ~ or \$HOME:"
  echo "$path_hits" | sed 's/^/      /'
fi

# --- file hygiene ------------------------------------------------------------
links="$(find "$DIR" -type l | head -5 || true)"
if [ -n "$links" ]; then fail "symlinks present (skill bundles need real files): $(echo $links)"; fi
if find "$DIR" -name '.DS_Store' | grep -q .; then
  warn ".DS_Store files present (excluded at publish)"
fi
big="$(find "$DIR" -type f -size +512k | head -3 || true)"
if [ -n "$big" ]; then warn "file(s) >512KB: $(echo $big)"; fi

# --- self-improving skills need a changelog ---------------------------------
if echo "$desc" | grep -qi 'self-improving' && ! grep -q '^## Changelog' "$SK"; then
  warn "self-improving skill without a '## Changelog' section in SKILL.md"
fi

# --- verdict -----------------------------------------------------------------
if [ "$fails" -gt 0 ]; then
  echo "  LINT: FAIL ($fails failure(s), $warns warning(s))"; exit 1
fi
if [ "$STRICT" = "--strict" ] && [ "$warns" -gt 0 ]; then
  echo "  LINT: FAIL (strict — $warns warning(s))"; exit 1
fi
echo "  LINT: PASS ($warns warning(s))"
