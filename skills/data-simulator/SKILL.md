---
name: data-simulator
description: Analyze any company, map every data source it generates or relies on, and manufacture 2 years of calibrated, vendor-exact simulated data ready to wire into a Growth Desk demo. Trigger aggressively whenever bang asks to "simulate data for X," "build demo data," "run the data-simulator," "synthetic/mock data for a prospect," "what data does X generate," "map X's data sources," or names any brand with intent to build a demo or Growth Desk instance. Also trigger for partial runs — "extract the Shopify schema," "add Klaviyo to the schema library," "recalibrate the ledger," "export the Growth Desk contract," "load the sim into DuckDB/Supabase." Dispatches Opus agents to vendor developer docs for schema extraction; maintains a self-improving vendor-schema library in the Cortana vault. Requires (and will trigger) brand-recon for discovery. Not for pure research with no data deliverable (brand-recon) or full client onboarding (client-build-package calls this skill).
---

# data-simulator — Brand → Data Sources → 2-Year Simulated Dataset → Growth Desk

You are running bang's standardized data-simulation pipeline. The purpose: take any prospect brand and produce a complete, internally consistent, 24-month simulated data estate — shaped exactly like the real exports of the real systems that brand runs — then stage it for a Growth Desk demo that WaiveLabs uses to pitch and close the client.

**This skill is client-agnostic.** It carries mechanism, not client facts. Every brand-specific number, channel, product, competitor, and system comes from the *active client's* dossier and config — never from this skill's examples, never from a previous client's run. The reusable essence:

> **recon the target's real stack → confirm one financial calibration ladder → generate from one canonical ledger with realistic per-vendor transforms and intentional dirt → emit vendor-exact files → load a database → export the demo contract.**

Everything reconciles to one source of truth. That is the whole game: a prospect's operators will smell fake data instantly if Shopify, GA4, and the exec dashboard disagree in impossible ways — and they'll smell it just as fast if they agree *perfectly*, because real stacks never do. The simulator produces the *right kind* of disagreement.

---

## What you MUST read before starting

1. `references/pipeline.md` — the 9 ordered phases with exact steps, agent dispatch templates, and human gates
2. `references/schema-library.md` — the vault vendor-schema library: YAML format, lookup-before-research rule, Opus extraction protocol
3. `references/generation-architecture.md` — ledger design, calibration ladder, cross-source distortion model, dirt injection, determinism rules
4. `references/outputs-and-contracts.md` — the four output layers (vendor files, bronze CSVs, DuckDB/Supabase, Growth Desk contract) and their exact shapes
5. `references/source-taxonomy.md` — the checklist of data-source categories by business model, so nothing gets missed

Also check the current state of the library at `~/Cortana/cortana-vault/research/data-sim/` (`_index.md`, `_playbook.md`). Schemas already in the library are settled — do not re-research them.

## Hard dependencies

- **brand-recon dossier.** Discovery is delegated to the `brand-recon` skill — one source of truth for stack/channel research. If `~/Cortana/cortana-vault/research/brand-recon/{slug}/dossier.md` (or a project-local copy) doesn't exist, run brand-recon first, then return here. data-simulator adds only a *data-source verification pass* on top of the dossier; it never duplicates general brand research.
- **Firecrawl** for doc verification; **Agent tool with `model: "opus"`** for schema-extraction subagents (bang's explicit requirement — schema fidelity is the product, don't economize here).
- Python 3 with numpy + openpyxl + duckdb in the sandbox (`pip install --break-system-packages` as needed).

## Outputs (per run)

All run outputs land in the **active project folder** at `<project>/data-sim/{slug}/`:

```
data-sim/{slug}/
├── simulation.config.yaml      # the single source of truth: window, seed, ladder, mix, sources
├── sources.yaml                # verified data-source inventory w/ evidence + schema status
├── generators/                 # generate_ledger.py, generate_bronze.py, generate_vendor_exports.py, generate_docs.py, run_all.py
├── data/
│   ├── bronze/                 # idealized medallion CSVs (9 domains)
│   ├── sources/<vendor>/       # vendor-exact exports (CSV/TXT/XLSX)
│   └── {slug}.duckdb           # bronze/silver/gold loaded
├── contract/                   # growth-desk-data.js, agent-context/*.json
├── RECONCILIATION.md           # tie-out report — the proof the estate is coherent
└── DATA_DICTIONARY.md          # schemas, grains, quirks, truth model, Tier-2 backlog
```

Persistent artifacts land in the vault: new/updated vendor schemas in `research/data-sim/schemas/`, a run entry in `_runs.md`, lessons in `_playbook.md`.

---

## The pipeline, at a glance

Full detail in `references/pipeline.md`. TaskCreate the phases at the start so bang can watch progress.

### Phase 0 — Scope & config
Confirm brand, slug, business model, demo target (default: Growth Desk). Locate or trigger brand-recon. Create the run directory and a draft `simulation.config.yaml` from `assets/simulation-config.template.yaml`.

### Phase 1 — Data-source inventory & verification
From the dossier's tech-stack section plus the `references/source-taxonomy.md` checklist, build `sources.yaml`: every system the brand runs (commerce, ESP/SMS, analytics, retail portals, marketplaces, paid media, affiliate/creator, panels, support, internal docs), each with **evidence** (dossier citation, firecrawl check, job posting, agents.md/UCP probe) and a verification status. Unverified-but-probable sources stay in with `assumed: true` — demos need plausibility, not subpoena-grade proof, but mark the difference.

### Phase 2 — Schema resolution (library first, then Opus agents)
For each source: library hit → use it. Library miss → dispatch an **Opus agent per vendor, in parallel**, to that vendor's developer documentation (API reference, export-format docs, sample payloads) to extract the export schema into the YAML format in `references/schema-library.md`. Write every new schema to the vault library so no vendor is ever researched twice. Agents can't call authenticated vendor APIs — the docs *are* the extraction surface; the seed library was built this way and verified HIGH fidelity for most vendors.

### Phase 3 — Calibration ladder (human gate)
Auto-estimate the brand's monthly net-revenue ladder, channel mix, YoY growth, AOV, and category split from the dossier and public signals (press, panels, funding, category benchmarks). **Present the ladder to bang for approval before generating** — this is the one number set that reaches a pitch deck, and it must survive contact with people who know the brand. Never proceed on unconfirmed anchors.

### Phase 4 — Generator build
Write the config-driven generator package (ledger → bronze → vendor exports → internal docs). Architecture rules in `references/generation-architecture.md`: deterministic seeds, one canonical daily-net ledger, per-month exact rescale (±0.1% tie-out), event/launch/weekday shaping, the distortion model (attribution inflation, panel error, consent loss), and intentional bronze dirt.

### Phase 5 — Generate & reconcile
`run_all.py` executes the full sequence and prints the reconciliation report. Fix until every tie-out passes. Write `RECONCILIATION.md` and `DATA_DICTIONARY.md`.

### Phase 6 — Database load
Load bronze → silver (cleaned/conformed) → gold (star schema) into `{slug}.duckdb`. If the demo needs a hosted backend, `--supabase` pushes gold tables to a Supabase project (business data in its own schema — never mix with the `vail_*` access-gating schema).

### Phase 7 — Growth Desk contract export
Derive the demo-ready artifacts **from gold, programmatically** — never hand-type: `growth-desk-data.js` (months[], channels[], products[], creators[], competitors[], weekly retailer series) and per-capability `agent-context/*.json` matching the broker tool schemas. Exact shapes in `references/outputs-and-contracts.md`. The config ladder is the single source of truth and everything else is derived — generator targets and demo anchors can never drift apart.

### Phase 8 — Verify, log, hand off
Programmatic verification (identity checks, tie-outs, cross-source ratios, DuckDB spot queries, contract JSON validation). Update `_runs.md` and `_playbook.md`. If invoked from `client-build-package`, return the run directory path and contract location; otherwise present `RECONCILIATION.md` + the contract to bang.

---

## Client isolation — the firewall rule

Each client is a sealed namespace. What crosses client boundaries and what never does:

**Shareable (vendor/mechanism knowledge):** the vendor-schema library (Shopify's export columns are Shopify facts, not client facts), distortion-model defaults, generation architecture, `_playbook.md` mechanism lessons.

**Sealed per client (never crosses):** calibration ladders and every revenue/mix/AOV number, `sources.yaml` inventories, dossier content, product/SKU catalogs, competitor sets, creator rosters, contract exports, and any lesson phrased in terms of a specific client. All of it lives only in that client's `<project>/data-sim/{slug}/` and that client's vault research folder.

Operating consequences:
- Never open another client's `data-sim/` run, config, or contract while working a client — not even "for reference." The reference is this skill and the library.
- Numbers in this skill's references are **shape illustrations only**. If a generated output contains a value you didn't derive from the active client's config, that's contamination — trace and remove it.
- Vault bookkeeping (`_runs.md`, `_playbook.md`) records slugs, source counts, doc-yield and mechanism lessons — **no client financials, no client-specific calibration**. Client numbers stay in the client namespace.
- When a run teaches a genuinely general lesson, generalize it before writing it to `_playbook.md` (strip the client, keep the mechanism).

## Non-negotiables

- **One ledger.** Every number in every file derives from `build_daily_ledger()`. If two outputs need to disagree (and they do — see distortion model), the disagreement is a *computed transform of the ledger*, never an independent random draw.
- **Determinism.** Seeded RNG throughout; same config → identical bytes. The seed lives in `simulation.config.yaml`.
- **Declarative schemas.** Vendor schemas come from the library YAML, never hard-coded in generator functions. Generators read the YAML.
- **24-month trailing window** ending at the most recent complete month, unless the config overrides it.
- **The calibration gate is mandatory.** Auto-estimate, then confirm with bang. Implausible numbers in a pitch are worse than no demo.
- **Never copy secrets.** Env-injected only (`WL_SUPA_*`, API keys). If you find keys in reference projects, do not propagate them into run outputs.
- **Brand voice/visuals** are out of scope here — pair with the entity's `{slug}-brand` skill (emitted by brand-recon) for any styled deliverable built on this data.

## Partial runs

Each phase is independently invocable when bang asks for a slice: "add Yotpo to the schema library" → Phase 2 only for one vendor; "recalibrate to $40M" → edit config, rerun Phases 5–8; "export the contract for the new demo tab" → Phase 7. State lives in `simulation.config.yaml` + the vault library, so partial runs are cheap and safe.
