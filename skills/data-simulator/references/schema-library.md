# Vendor-Schema Library — vault conventions

**Location:** `~/Cortana/cortana-vault/research/data-sim/`

```
research/data-sim/
├── _index.md        # one line per vendor: key, category, fidelity, date added, extracted-by
├── _playbook.md     # doc-source lessons: which URLs yield schemas, which are dead/paywalled
├── _runs.md         # every simulation run: date, slug, ladder topline, output path
└── schemas/
    ├── shopify.yaml
    ├── klaviyo.yaml
    └── ...
```

The library is the compounding asset. Every schema extracted once is free forever; every run makes the next one cheaper. Rules:

1. **Lookup before research.** A library hit ends the question. Re-extract only when bang says a vendor changed its export format, or when a schema's `fidelity: LOW` entry is blocking a demo that needs better.
2. **Write-through.** New extractions go to the vault the moment they validate — not at end of run. A crashed run should still have banked its schemas.
3. **Vendor schemas are vendor facts, not client facts.** A Shopify orders export has the same 79 columns for every merchant — that's why the library is shareable across clients. Anything client-specific an extraction surfaces (a client's custom fields, per-merchant column drift) gets noted as a *conditional quirk* ("column X present only when integration Y is enabled"), never as a client reference.

## Schema YAML format

One file per vendor. Format (full template in `assets/vendor-schema.template.yaml`):

```yaml
vendor: klaviyo
category: esp            # commerce|esp|sms|analytics|marketplace|retail_portal|paid_media|affiliate|panel|support|reviews|internal
display_name: Klaviyo
doc_sources:
  - url: https://developers.klaviyo.com/en/reference
    yield: high
extracted: 2026-07-10
extracted_by: opus-agent   # or: sf-corpus | manual
fidelity: HIGH             # HIGH | MED | LOW (worst of exports)
exports:
  - key: campaigns_export
    filename_pattern: "campaigns-export-{YYYY-MM-DD}.csv"
    grain: campaign
    window_convention: all-time as of export date
    format: csv
    columns:
      - {name: "Campaign Name", type: string}
      - {name: "Send Time", type: datetime, format: "YYYY-MM-DD HH:MM:SS"}
      - {name: "Total Recipients", type: int}
      # ... exact order matters — generators write columns in this order
    quirks:
      - "Rates exported as decimals (0.4123), not percent strings"
    fidelity: HIGH
notes: |
  Attribution: Klaviyo-attributed revenue is lifecycle attribution — in the
  distortion model, klaviyo + attentive revenue together = lifecycle_share of
  total net (default 16%), NOT additive with paid-media attribution.
```

**Quirks are mandatory, not decoration.** Metadata comment blocks (GA4), title lines + Total rows (Google Ads), `US$1,234.56` / `12.34%` strings (Amazon), blank continuation rows (Shopify line items), `Mobile APP` casing (Amazon), Sat–Fri weeks (Stackline), store×$-only vs SKU×units-only report gap (Sephora). These make files credible and give silver-layer demos real work. An export entry without a quirks list means the agent didn't look hard enough.

## Opus extraction protocol

- One agent per vendor, parallel dispatch, `model: "opus"` (bang's mandate — schema fidelity is the deliverable; do not downgrade to save tokens).
- Best doc surfaces, in yield order (per `_playbook.md`, which supersedes this list as it learns): official export/report help-center articles (better than API refs for *file* shape) → API reference response schemas → **Fivetran/Airbyte connector docs** (document vendor exports column-by-column; consistently high yield) → community/CSV samples and competitor migration guides.
- The agent returns YAML only. Validate: parses, ≥1 export, exact column names (not paraphrased), fidelity rated per export, quirks present. Reject and re-dispatch with feedback if sloppy.
- Record doc-URL yields in `_playbook.md` so future dispatches start from known-good surfaces.

## Bootstrapping

If `research/data-sim/` doesn't exist, create the folder set (`schemas/`, `_index.md`, `_playbook.md`, `_runs.md`) empty and let runs populate it. If a verified generator corpus exists from a prior engagement, its header lists may be banked into the library as `extracted_by: verified-corpus` — extract only the vendor schemas (vendor facts), never the engagement's calibration or brand config.
