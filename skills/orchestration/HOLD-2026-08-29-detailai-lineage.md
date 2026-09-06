---
title: "HOLD — orchestration: do not publish until the six DetailAI retros are merged back"
type: reference
created: 2026-08-29
updated: 2026-08-29
tags: [🔧, orchestration, skill-publish, hold, detailai, lineage, operator-action]
status: active
related:
  - "[[projects/cortana-platform/cortana-platform--registry-relocation-runbook-2026-08-29|Registry Relocation Runbook]]"
  - "[[research/brand-recon/detail-ai/dossier|DetailAI dossier]]"
  - "[[log|Activity Log]]"
---

# HOLD — `orchestration` is not publishable as staged

**Operator decision, 2026-08-29: hold. Recover the DetailAI retros first, then publish the union.**

## The finding

Counted directly in this directory and in the loaded skill surface:

| File | DetailAI mentions | ShipCo mentions | Bytes |
|---|---|---|---|
| `SKILL.md` (staged, this dir) | **0** | 5 | 54,788 |
| `SKILL-pre-2026-08-28-fork-backup.md` | 0 | 5 | 40,859 |
| `SUPERSEDED-2026-08-08-fork.md` | 0 | 0 | 15,818 |
| `PARTIAL-2026-08-24-shipco-lineage-MERGED-IN.md` | 0 | 2 | 32,313 |
| **Loaded account-store copy** | **0** | 5 | 40,859 |

Per the 2026-08-29 projects review, `origin/main` of the agent-skills mirror carries **5 DetailAI
mentions** and the six dated wave retros — 2026-07-28 (WAI-253 wiring pass), 2026-08-12
(overnight waves 6–7), 2026-08-13 / 08-13b / 08-13c (MVCC + advisory-lock, NaN-severity), and
2026-08-17. `grep -rl "DetailAI S1 wave"` finds them **nowhere on disk**.

This is a **lineage substitution, not a redaction**: the fork preserved the football and ShipCo
branches and never carried the DetailAI branch across. Publishing the staged copy — to the
registry or the account store — makes the loss permanent everywhere except git history.

**DetailAI launches the week of 2026-08-31.** These are the orchestration lessons from the most
adversarially-gated build in the estate, and they would stop being loadable during launch week.

## Recovery — three commands on the host

```bash
cd ~/Projects/agency/WaiveLabs/agent-skills

# The origin lineage, with the six DetailAI retros intact.
git --no-optional-locks show origin/main:skills/orchestration/SKILL.md > /tmp/orch-origin.md

# Sanity: expect DetailAI >= 5, ShipCo 0.
grep -ci detailai /tmp/orch-origin.md ; grep -ci shipco /tmp/orch-origin.md

# Put it somewhere a session can read.
cp /tmp/orch-origin.md ~/Cortana/cortana-vault/_inbox/skills/orchestration/ORIGIN-2026-08-17-lineage.md
```

Then the merge is a union, not a choice: keep every changelog entry from **both** lineages,
ordered by date. Nothing is dropped; the fork's error was treating two branches as alternatives.

## Two traps to avoid on the way

1. **Never `git add -A` in this mirror.** Eight untracked files sit in `skills/orchestration/`,
   two of them (`SKILL.md.bak-2026-08-26`, `SKILL-pre-2026-08-28-fork-backup.md`) near-verbatim
   copies carrying the ShipCo material. A blanket add publishes it three times over and commits
   scratch backups. Stage `skills/orchestration/SKILL.md` and `.gitignore` **explicitly**.
2. **Clear the locks first, and read state without making new ones.**
   `rm .git/index.lock .git/HEAD.lock` before any commit. On this FUSE mount any index-touching
   git command — *including `git status`* — leaves an undeletable lock; use
   `git --no-optional-locks`, or `find`/`ls`/`diff`.
