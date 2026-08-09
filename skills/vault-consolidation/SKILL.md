---
name: vault-consolidation
description: Weekly sleep-time consolidation run for the Cortana vault — the scheduled background maintenance agent that owns memory hygiene on a clock (Letta sleep-time-compute / auto-consolidation pattern). Trigger on "weekly consolidation", "vault maintenance run", "sleep-time run", "consolidate the vault", "run vault hygiene", or any scheduled weekly vault-maintenance invocation. Runs preflight gate + checkpoint, updated-field sync, lint with mechanical fixes, staleness sweep, orphan/index drift sweep, log month rollover, action-items triage, contradiction scan, dashboard refresh, and files an ops report to handoffs/. Deterministic where possible, report-don't-guess everywhere else. Do NOT trigger for on-demand deep vault reviews (obsidian-review) or content ingest (obsidian).
---

# Vault Consolidation — weekly sleep-time run

Scheduled maintenance agent for `~/Cortana`. A SEPARATE background run owns memory
hygiene on a clock — the session agents never have to hand-run this.

**Schedule:** designed for weekly automated runs (Sunday). Safe to run manually
anytime. Idempotent — a second run on a clean vault is a no-op plus a short report.

**Working dir:** `~/Cortana` (vault root; `.obsidian/` lives here, wikilinks resolve
from here). Read `cortana-vault/SCHEMA.md` sections you touch before editing anything.

## HARD RULES

- NEVER edit `cortana-vault/raw/` — immutable archive.
- NEVER edit exporter-regenerated files: `projects/nq-trading/backtests/*/sample-days/*.md`
  and backtest rules pages — the exporter clobbers hand edits. Flag drift in the report instead.
- Trash, never delete. Moves only; every move has a conservation postcondition
  (counts before == counts after, verified against the preflight sidecar).
- Sweeps touch the `status:` line ONLY — never rewrite `updated:` in the same pass
  (the apply in step 2 already set honest dates; a sweep must not clobber them).
- Judgment findings go in the report, never auto-resolved. Mechanical = deterministic
  fix with one right answer; everything else = judgment.
- Commits go through the fail-closed pre-commit hook. Never `--no-verify`.
  `SKIP_GITLEAKS=1` only if gitleaks is not installed.
- Own lane only: no SCHEMA.md, CLAUDE.md, or skill-registry edits from this run.

## Sequence

Run steps in order. Abort the run (and file a partial report) if preflight fails.

### 1. Preflight + checkpoint

```bash
python3 cortana-vault/scripts/consolidation-preflight.py --checkpoint
```

Gates: vault root resolves (`.obsidian` + SCHEMA present), git tree clean or
checkpoint-committed, log.md + action-items.md parse. Writes baseline counts to
`/tmp/consolidation-preflight.json` — the conservation reference for steps 6–7.
Nonzero exit = stop; do not consolidate.

### 2. Sync `updated:` fields — FIRST, before any sweep

```bash
python3 cortana-vault/scripts/sync-updated-field.py --apply
```

Runs FIRST by design: it rewrites `updated:` from mtime (>7d divergent), so every
later staleness judgment works from honest dates — and no later status-only sweep
ever runs in the same pass as an apply that could clobber its dates. Record the
applied count for the report.

### 3. Lint — fix mechanical, report judgment

```bash
python3 cortana-vault/scripts/vault-lint.py
```

- **Fix now (mechanical):** broken links from known renames (update the link),
  missing required frontmatter fields (add per SCHEMA), missing/duplicate emoji
  category tag, `archive`→`archived` typos.
- **Report only (judgment):** contradictions, ambiguous link targets, thin-content
  calls, anything where the fix requires deciding what bang meant.
- Re-run lint after fixes; the report cites before/after finding counts.

Also run the seam check — findings are judgment, report only:

```bash
python3 cortana-vault/scripts/projects-review.py --quiet
```

### 4. Staleness sweep (status line only)

```bash
python3 cortana-vault/scripts/vault-lint.py --check staleness --stale-days 30
```

For each `status: active` page with `updated:` >30d, per SCHEMA semantics:

| Page reality | New status |
|---|---|
| Evergreen knowledge (topics, frameworks, specs, model/rules pages that are simply *finished*) | `reference` |
| Real work intentionally on hold | `paused` |
| Work that is actually done | `completed` |
| Genuinely unclear | leave `active`, list in report |

Edit the `status:` line ONLY. Note: `research/papers/` (78 files) crosses the 30-day
line ~2026-08-15 — clean batch to `reference` when it shows up.

### 5. Orphan + index-drift sweep

Scope: `projects/` and `research/` (exclude `research/brand-recon/*/references/`,
`raw/`, and all SCHEMA audit-excluded dirs).

- Notes with zero inbound links: add a real link from the nearest `_index.md` /
  hub / MOC if membership is unambiguous; otherwise flag in report.
- Drift-detect: for each `_index.md` with a static list/table, diff the list against
  the folder's actual `.md` files. Append rows for missing files using only facts
  read from the file's own frontmatter — never fabricate metadata for a row.
  Files listed but absent on disk → report (possible unrecorded rename).

### 6. Log month rollover (conservation-checked)

If preflight reported `prior_month_entries > 0` in `log.md`:

1. For each prior month, create or append `cortana-vault/log/YYYY-MM.md` with SCHEMA
   frontmatter (`type: log`, `status: archived`, tags `[🔧, log, meta, archive]`,
   archive-shard callout linking `[[log]]` — copy the pattern from `log/2026-07.md`).
2. Move entries VERBATIM, preserving reverse-chronological order. Current month
   stays in `log.md`.
3. **Postcondition:** moved + remaining == preflight `log_md.entries`. Mismatch =
   restore from git checkpoint and report; do not improvise.

### 7. Action-items triage (conservation-checked)

In `cortana-vault/action-items.md` (sections Active / Parked / Done):

- Recount Active open boxes; if >50, warn in the report (lint threshold).
- For each Active item, check its linked source pages: if all went
  `completed`/`archived`, move the item VERBATIM to Parked under its original
  section heading. Never delete, never reword, never auto-check boxes.
- **Postcondition:** total checkbox count unchanged vs sidecar. Verify:

```bash
python3 cortana-vault/scripts/consolidation-preflight.py --postcheck
```

(Exits 1 if the action-items total shrank. Log-entry conservation from step 6 is
asserted manually against the printed before/after.)

### 8. Memory hygiene — contradiction scan (report only)

- Grep vault notes for `supersedes:` frontmatter; walk each chain; flag chains whose
  superseded note still has `status: active`.
- Find duplicate `title:` values across notes (excluding audit-excluded dirs).
- NEVER auto-resolve either — list pairs in the report for bang to adjudicate.

### 9. Dashboard refresh

```bash
python3 cortana-vault/scripts/update-dashboard-reports.py
```

### 10. Ops report → handoffs/

Write `cortana-vault/handoffs/YYYY-MM-DD-consolidation.md`:

```yaml
---
title: "Vault Consolidation — Weekly Run (YYYY-MM-DD)"
type: session
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [🔧, consolidation, maintenance, sleep-time]
status: completed
related: ["[[log]]", "[[SCHEMA]]", "[[dashboard]]"]
---
```

Body sections, in order:
- **What ran** — each step, pass/skip, duration if notable.
- **Counts** — files touched per step; conservation numbers (sidecar before/after
  for log entries and action-items; sync-applied count; statuses changed by value).
- **Judgment items for bang** — lint judgment findings, ambiguous stale pages,
  orphans without an obvious home, contradiction pairs, projects-review findings.
- **Retrieval observability** — queries this run made that returned empty; notes
  written in the last week that nothing links to (written-never-linked).

### 11. Log entry + final commit

1. Append a `log.md` entry per SCHEMA Log Format (`type: lint`), linking the
   handoff report and pages touched.
2. Commit everything through the hook:

```bash
git add -A && git commit -m "Weekly consolidation run YYYY-MM-DD"
```

If the hook blocks, fix the offending file — never bypass. `SKIP_GITLEAKS=1`
prefix only when `command -v gitleaks` is empty.

## Failure posture

Any step that errors: stop, leave the tree as-is (the step-1 checkpoint makes the
run revertible), file the partial report with the failure verbatim, still write the
log entry. A half-run that reports honestly beats a full run that guesses.
