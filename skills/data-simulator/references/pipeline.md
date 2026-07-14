# Pipeline — the 9 phases in execution detail

Run phases in order on a full run. Each phase states its inputs, exact actions, outputs, and gate (if any). TaskCreate one task per phase at the start; mark in_progress/completed as you go.

---

## Phase 0 — Scope & config

**Inputs:** brand name or URL from bang; active project folder.

1. Derive `slug` (kebab-case, ≤32 chars) — match brand-recon's slug if a dossier exists.
2. Locate the dossier: `~/Cortana/cortana-vault/research/brand-recon/{slug}/dossier.md`, or a project-local `research/brand-recon/{slug}/dossier.md`. **Missing → invoke the brand-recon skill now**, then return.
3. Ask bang (AskUserQuestion, one round max) only for what the dossier can't answer: demo target if not Growth Desk, unusual window, whether a hosted (Supabase) backend is needed.
4. Create `<project>/data-sim/{slug}/` and copy `assets/simulation-config.template.yaml` → `simulation.config.yaml`; fill brand, slug, window (default: 24 trailing complete months), seed (default: `int(YYYYMMDD)` of run date).

**Output:** run directory + draft config.

---

## Phase 1 — Data-source inventory & verification

**Inputs:** dossier; `references/source-taxonomy.md`.

1. Extract every named system from the dossier (tech-stack, channels, retail partners, social sections).
2. Walk the taxonomy checklist for the brand's business model; add probable-but-unnamed sources as `assumed: true` (e.g., a Shopify DTC brand almost certainly has GA4 and at least one ESP).
3. Verify cheaply where possible, in parallel:
   - `firecrawl_scrape` `{domain}/agents.md` and `/.well-known/ucp` (AI-native tell — when live, a major pitch angle and a simulatable source of its own)
   - Homepage source hints: Klaviyo/Attentive/GA4/Meta pixel script tags (`firecrawl_scrape` with raw HTML)
   - `firecrawl_search` job postings ("{brand} klaviyo OR shopify plus OR netsuite site:linkedin.com OR site:builtin.com") — stacks leak through hiring
   - Retail-partner store locators / brand pages (Sephora, Ulta, Target, Amazon storefront)
4. Write `sources.yaml`:

```yaml
sources:
  - vendor: shopify            # library key
    category: commerce
    status: verified           # verified | assumed
    evidence: "dossier §4 — platform confirmed; ESP tag observed on homepage"
    tier: 1                    # 1 = generate now, 2 = backlog
    exports: [total_sales_over_time, orders_export]
```

**Output:** `sources.yaml`. Tier-2 backlog entries are documented, not generated — they become the DATA_DICTIONARY backlog section.

---

## Phase 2 — Schema resolution

**Inputs:** `sources.yaml`; vault library `~/Cortana/cortana-vault/research/data-sim/schemas/`.

1. For each Tier-1 source, check `schemas/{vendor}.yaml`. Hit → mark resolved. The library is settled law; do not re-research or "improve" existing entries unless bang asks.
2. For all misses, dispatch **one Opus agent per vendor, all in a single message** (parallel). Dispatch template:

```
Agent tool — subagent_type: general-purpose, model: opus
prompt: |
  You are extracting the export/report data schema for {VENDOR} so we can generate
  simulated files indistinguishable in shape from real exports.

  Sources to mine (in order): official developer docs / API reference at {DOC_URL},
  export-format help-center articles, sample payloads in docs, reputable third-party
  integration docs (Fivetran/Airbyte source schemas are excellent — they document
  vendor exports column-by-column). Use firecrawl_scrape/search and WebSearch.
  You cannot call the vendor's API; the documentation is the extraction surface.

  For EACH export/report a brand operator would actually download or a pipeline
  would ingest (not every API endpoint — the 2-5 exports that matter for
  {CATEGORY} analytics), produce a schema entry per the YAML template below,
  including: exact column names in exact order, types, grain, date/window
  conventions, filename pattern, and QUIRKS (metadata comment blocks, title/total
  rows, currency/percent string formats, blank continuation rows, casing oddities).
  Quirks are first-class — they are what makes simulated files credible and what
  silver-layer demos teach against.

  Rate each export's fidelity: HIGH (docs show exact columns), MED (reconstructed
  from partial docs/screenshots), LOW (inferred). Return ONLY the completed YAML.
  Template: {contents of assets/vendor-schema.template.yaml}
```

3. Validate returned YAML (parseable, non-empty columns, fidelity rated), then write to `schemas/{vendor}.yaml` and append to `_index.md`. Note fresh extractions in the run log.
4. Copy the resolved schema set (or references to it) into the run's `DATA_DICTIONARY.md` scaffold.

**Output:** every Tier-1 source has a schema; library grew.

---

## Phase 3 — Calibration ladder ⛔ HUMAN GATE

**Inputs:** dossier (revenue estimates, channel structure, funding/press), category benchmarks.

1. Estimate and write into `simulation.config.yaml`:
   - `monthly_net_m`: 24 monthly net-revenue targets ($M) — seasonality-shaped (category gifting/holiday/launch curves), YoY growth applied
   - `channel_share` (latest FY) + `channel_yoy` — prior year derived as `share / (1 + yoy)`, renormalized
   - `category_split`, `aov_by_channel`, `events` (retailer events, launches, holiday windows with demand-lift factors)
2. Document the reasoning: which signals produced the topline (press revenue figures, panel estimates, employee count × category revenue-per-head, retailer door counts × velocity benchmarks).
3. **Present the ladder to bang** (send_user_message with the table + reasoning, then AskUserQuestion: approve / adjust topline / adjust mix). Do not generate before approval. If bang adjusts, rescale and re-present only if the change was structural.

**Output:** approved config. This is now the *only* place these numbers live — everything downstream derives from it.

---

## Phase 4 — Generator build

**Inputs:** approved config, resolved schemas, `references/generation-architecture.md`.

Write `generators/` as a small config-driven package (not one monolith):

- `generate_ledger.py` — `build_daily_ledger(config)` → canonical `date × channel` daily-net frame + shared dims. Everything imports this.
- `generate_bronze.py` — the 9 idealized bronze domains (sales_daily w/ dirt, marketing_spend, web_traffic, email_sms, inventory, retention_cohorts, creators, campaigns, ai_visibility, launch_scorecard + dims). Adapt domains to the business model (see source-taxonomy).
- `generate_vendor_exports.py` — reads library YAML schemas + the distortion model, emits `data/sources/<vendor>/…` with exact filenames, column orders, and quirks.
- `generate_docs.py` — internal-style XLSX with live formulas (openpyxl): weekly sales summary, plan-vs-actual, budget tracker, marketing calendar.
- `run_all.py` — sequences everything, prints the reconciliation report, exits nonzero on any tie-out failure.

**Output:** generator package committed to the run dir.

## Phase 5 — Generate & reconcile

Run `run_all.py`. Required tie-outs (fail loudly, fix, rerun):
- monthly net vs `monthly_net_m` within ±0.1%
- channel mix vs target within ±0.5pt
- `net = gross − discount − returns` on all clean rows
- every cross-source ratio within its designed band (see distortion model)
- dirt counts as designed (report them — they're features)

Write `RECONCILIATION.md` (the tie-out evidence) and finalize `DATA_DICTIONARY.md` (schemas, grains, quirks, truth model, Tier-2 backlog).

## Phase 6 — Database load

`generators/load_db.py`: bronze CSVs → DuckDB `{slug}.duckdb` with three schemas — `bronze` (raw, dirt intact), `silver` (cleaned: trimmed/upper channel_ids, coalesced nulls, deduped), `gold` (star: fact_sales, fact_marketing, dim_date, dim_product, dim_channel + per-capability marts). DuckDB reads CSVs natively — keep the load script under ~100 lines of SQL.

Optional `--supabase`: push **gold only** to the WaiveLabs Supabase project into schema `sim_{slug}`. Never touch `vail_*` (access-gating). Keys from env only.

## Phase 7 — Growth Desk contract export

`generators/export_contract.py` queries **gold** and writes `contract/` — shapes specified in `references/outputs-and-contracts.md`:
- `growth-desk-data.js` — the demo data objects (months[], channels[], products[], campaigns[], socialPlatforms[], creators[], competitors[], RETAILERS[] + weekly pos/shipped series)
- `agent-context/{capability}.json` — one context blob per broker capability

Derived programmatically so demo numbers can never drift from the ledger. If the demo app clone already exists, offer to wire the files in directly.

## Phase 8 — Verify, log, hand off

1. Programmatic verification pass (re-run tie-outs from Phase 5, JSON-validate the contract, DuckDB spot queries: top SKUs, monthly totals, channel mix — eyeball for plausibility).
2. Vault bookkeeping: append run to `_runs.md` (date, slug, sources count, new schemas, output path — **no client financials**; the ladder stays in the client namespace); add lessons to `_playbook.md` (doc URLs that worked/died, quirks discovered, estimation *methods* that landed — generalized, client stripped).
3. Present to bang: RECONCILIATION.md, DATA_DICTIONARY.md, the contract, and the DuckDB path. If invoked from client-build-package, return paths and stop — the parent skill handles the demo build.
