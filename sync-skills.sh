#!/usr/bin/env bash
# Link every registered local harness to this registry. No publication or push.
# Existing edits are immediately visible; new/retired IDs need sync.
# Usage: ./sync-skills.sh [check|plan|sync|add NAME SKILLS_DIR]
# Configuration: ~/.config/cortana/skill-harnesses.json
# Legacy CANONICAL and <HARNESS>_SKILLS path overrides remain supported.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CANONICAL="${CANONICAL:-$ROOT}"
if [ "$#" -eq 0 ]; then set -- sync; fi
exec python3 "$ROOT/bin/sync-harnesses.py" --registry "$CANONICAL" "$@"
