#!/usr/bin/env bash
# Create the private GitHub repo for the consolidated Cortana skill registry and push.
# Run this on YOUR machine (it uses your own GitHub auth). Requires git; gh CLI optional.
set -euo pipefail

REPO_NAME="${1:-cortana-skill-registry}"
# Set OWNER to your GitHub username or org. Leave blank to use your gh default account.
OWNER="${OWNER:-}"

cd "$(dirname "$0")"

if command -v gh >/dev/null 2>&1; then
  echo "==> Using gh CLI to create private repo and push"
  TARGET="${OWNER:+$OWNER/}$REPO_NAME"
  gh repo create "$TARGET" --private --source=. --remote=origin --push
else
  echo "==> gh not found. Create an EMPTY private repo named '$REPO_NAME' on github.com first,"
  echo "    then re-run with the remote URL, e.g.:"
  echo "       REMOTE=git@github.com:<you>/$REPO_NAME.git ./push-to-github.sh"
  if [ -n "${REMOTE:-}" ]; then
    git remote remove origin 2>/dev/null || true
    git remote add origin "$REMOTE"
    git push -u origin "$(git symbolic-ref --short HEAD)"
  else
    exit 1
  fi
fi
echo "==> Done. Repo pushed."
