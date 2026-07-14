# Installing sprint-runner

Two install paths depending on where you want this skill available.

## Option A — Global (available in every Claude Code session)

```bash
mkdir -p ~/.claude/skills
cp -r sprint-runner-skill ~/.claude/skills/sprint-runner
```

Then in a new Claude Code session, verify with:

```bash
claude --list-skills | grep sprint-runner
# expect: sprint-runner listed with its description
```

## Option B — Project-local (only available in Novai)

```bash
mkdir -p ~/Projects/Novai/.claude/skills
cp -r sprint-runner-skill ~/Projects/Novai/.claude/skills/sprint-runner
```

Project-local skills take precedence over global ones with the same name.

## Trying it out

Once installed, any of these phrases should trigger the skill:

- "scaffold a tracker for Sprint 11"
- "write up the run summary for S10-12"
- "regenerate the sprint-runs index"
- "what shipped in commits f5f304e..HEAD"

## Operations summary

| Operation | Trigger phrase | Script |
|-----------|---------------|--------|
| `new-sprint` | "start Sprint N", "scaffold tracker" | `scripts/new_sprint.py` |
| `update-sprint` | "add a decision", "scope changed" | (Edit tool, in-place) |
| `finish-sprint` | "write up this run", "what shipped" | `scripts/run_summary.py` + Claude fills placeholders |
| `sprint-index` | "update the index" | `scripts/sprint_index.py` |

## Customizing for your repo

The skill assumes:

- Repo root contains `.git/` and `docs/` directories.
- `docs/SPRINT-N-tracker.md` is the tracker pattern.
- `docs/sprint-runs/SN-XX-<slug>.md` is the run-summary pattern.
- `docs/sprint-runs/index.md` is the rolling ledger.

If you ever want a different layout, edit `SKILL.md` section "Operations" and the scripts' target path logic — everything else is layout-agnostic.

## Uninstalling

```bash
rm -rf ~/.claude/skills/sprint-runner   # or the project-local path
```

## File layout

```
sprint-runner/
├── SKILL.md                              # Main skill prompt with operation contracts
├── INSTALL.md                            # This file
├── scripts/
│   ├── new_sprint.py                     # Scaffold docs/SPRINT-N-tracker.md
│   ├── run_summary.py                    # Generate run-summary draft from git log
│   └── sprint_index.py                   # Regenerate docs/sprint-runs/index.md
├── templates/
│   ├── tracker.md.hbs                    # Sprint tracker template
│   ├── run-summary.md.hbs                # Per-story run summary template
│   └── index.md.hbs                      # Rolling ledger template
└── references/
    ├── bang-style-guide.md               # Voice conventions — read before writing prose
    ├── tracker-shape.md                  # Annotated tracker template
    └── run-summary-shape.md              # Annotated run-summary template
```
