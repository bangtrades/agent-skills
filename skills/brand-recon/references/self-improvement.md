# Self-Improvement Closeout — Phase 14

This file documents the closing routine of every investigation. The contract is simple: every run leaves the playbook smarter than it found it. Skipping this step breaks the compounding mechanism that is the entire point of having a packaged skill.

## What gets updated

Three files at `~/Cortana/cortana-vault/research/brand-recon/`:

| File | Purpose | Update style |
|---|---|---|
| `_playbook.md` | Narrative log of lessons learned, novel techniques, blockers, surprises | Append a dated block per run |
| `_sources.md` | Per-URL quality + access ledger | Append individual lines per source touched |
| `_runs.md` | Run index (one row per investigation) | Append a row to the table |

## Why these three, in this format

- `_playbook.md` captures the **narrative** of what worked — the kind of insight that's worth reading top-to-bottom every quarter.
- `_sources.md` captures **structured per-URL data** — queryable, machine-friendly, the source that gets read at the START of each new investigation to inherit prior knowledge.
- `_runs.md` is just an **index** — what entities have been investigated, when, and where to find the dossier.

This separation keeps each file good at its job. A single combined file would either be too verbose (when read by an agent) or too sparse (when read by a human).

## The Phase 14 routine, step by step

### Step 1 — Read the current state of all three files

If any file doesn't exist (first run after install), create it from the seed template (see "Seed templates" below).

### Step 2 — Append to `_playbook.md`

Append a new block at the end of the file, NOT at the top. The file reads chronologically; oldest at top, newest at bottom. This makes diffing across runs easy.

Template:
```markdown
---

## YYYY-MM-DD — {entity-slug}

**Entity:** {Entity Name} ({primary_url})
**Run length:** ~{N} minutes
**Phases completed:** {N}/15

### What worked unusually well
- {observation 1}
- {observation 2}

### What was blocked / low-yield
- {observation 1 with the source}
- {observation 2 with the source}

### Novel techniques discovered
- {anything that should be added to the workflow for future runs}

### Updates to the source catalog
- {anything that should change in source-catalog.md based on this run}

### Updates to the dossier template
- {anything the dossier template should change to better match this entity type}

### Lessons for the next run
- {1–3 sentences of operational guidance}
```

Keep each section short. The point is to capture diff-worthy observations, not full prose.

### Step 3 — Append to `_sources.md`

For every URL the investigation touched, append one line under the auto-entries section using this format:

```
YYYY-MM-DD — {entity-slug} — {url-or-domain} — access:{firecrawl|firecrawl-flaky|chrome|search|paywall|blocked} — yield:{high|medium|low|noisy|blocked} — notes:{1-line description}
```

Examples (from the CopperJoint bootstrap):
```
2026-05-27 — copperjoint — facebook.com/copperjoint — access:firecrawl — yield:blocked — notes:firecrawl returns "we do not support this site" — escalate to Chrome MCP next time
2026-05-27 — copperjoint — openpr.com — access:firecrawl — yield:high — notes:six press releases between Sept 2025 and Jan 2026 — also surfaces sibling press in the "More Releases for X" panel — scrape ONE release and harvest the sibling panel for free
```

Don't batch — one line per URL. The catalog becomes searchable: future runs can grep `_sources.md` for a domain to instantly inherit its access strategy.

### Step 4 — Append to `_runs.md`

`_runs.md` is a single markdown table. Append one row at the end:

```markdown
| YYYY-MM-DD | {slug} | {Entity Name} | {primary_url} | [[research/brand-recon/{slug}/dossier.md\|dossier]] | [[research/brand-recon/{slug}/{slug}-brand/SKILL.md\|brand]] | {1-sentence headline finding} |
```

The table columns are: Date, Slug, Name, URL, Dossier link, Brand skill link, Headline.

### Step 5 — Update the run summary section in `_playbook.md`

At the top of `_playbook.md` there's a small summary section. Update the counter:

```markdown
**Total runs:** {N}
**Last run:** YYYY-MM-DD ({slug})
```

That's it. The skill is now smarter than it was before the run.

## Anti-patterns

- **Skipping for "obvious" runs.** Even an obvious run produces some lesson. If nothing else, document that this entity type was so standard that the playbook already covered it — that's confirmation evidence.
- **Generic platitudes.** "WebSearch was useful" is not a lesson. "Glassdoor employee bands consistently underestimate small DTC brands by 50–80% vs. press-mentioned headcount" is a lesson.
- **Dumping raw scrape data into the playbook.** The playbook is for synthesized lessons, not source material. Source material goes in `raw-scrapes/`.
- **Editing prior entries.** Once a playbook entry is written, treat it as immutable. If you discover something was wrong, write a correction in the next entry rather than rewriting history.

## Seed templates

Bootstrap any missing file with these templates on the first run.

### `_playbook.md` seed

```markdown
# brand-recon Playbook

Lessons accumulated across every investigation. Append-only.

**Total runs:** 0
**Last run:** none

---

## How to use this file

- Read top-to-bottom before each new run to inherit prior lessons
- Skim the most recent 3 entries for blocked-source updates
- Search by entity-slug or category for prior comparable runs
```

### `_sources.md` seed

```markdown
# Source Catalog — Live Ledger

Per-URL access + yield data. Appended to by Phase 14 of every run.

Format: `YYYY-MM-DD — {entity-slug} — {url-or-domain} — access:{...} — yield:{...} — notes:{...}`

The canonical category catalog (which sources to hit per phase) lives in the brand-recon skill at `references/source-catalog.md`. This file is the running ledger of actual results.

---

<!-- BEGIN AUTO-APPENDED ENTRIES -->
<!-- END AUTO-APPENDED ENTRIES -->
```

### `_runs.md` seed

```markdown
# brand-recon Run Index

| Date | Slug | Name | URL | Dossier | Brand Skill | Headline |
|---|---|---|---|---|---|---|
```

## Updating the brand-recon skill itself

The self-improvement loop updates the vault-side ledgers (`_playbook.md`, `_sources.md`, `_runs.md`). It does NOT modify the brand-recon skill files themselves.

If a lesson is generally applicable across entities and should be encoded into the skill's permanent guidance (not just the ledger), surface that to the user explicitly:

> "Two lessons from this run suggest the brand-recon skill itself should be updated: (1) the `/agents.md` probe is now successful enough often enough that it should move from 'optional' to 'mandatory' in the Phase 11 checklist; (2) the firecrawl Reddit search consistently returns empty — we should default to `WebSearch site:reddit.com` first. Want me to patch the skill?"

Don't auto-edit the skill. The vault ledger is the autonomous compounding layer; structural skill changes are a deliberate user decision.

## When the playbook gets long

After 20+ runs, the playbook will get unwieldy. At that point, archive old entries:

- Move entries older than 12 months to `_playbook-archive.md`
- Keep only the most recent year in `_playbook.md`
- Surface this proactively to the user when the file crosses ~400 lines

The point is to keep the always-loaded file lean, not to delete history.
