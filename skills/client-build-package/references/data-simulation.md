# Data Simulation — synthetic, calibrated, deliberately imperfect

No real client data before contract — ever. But fake-looking data kills demos. The method
(proven in `~/Projects/Summer Fridays/Fabric_Simulation/`) is **synthetic-but-calibrated**:
seeded generators that reproduce the client's public reality closely enough that their own
team nods at the numbers.

## Calibration truth model

Before generating anything, write down the targets in a truth block at the top of the
generator (SF hit ±0.1% of these):

- **Top line:** annual revenue / run rate from the dossier (public statements, press,
  credible estimates).
- **Mix:** channel/segment split (SF: Sephora 56% / Intl 15% / Shopify 12% / Amazon 11% /
  TikTok Shop 5% / Affiliate 1.5%).
- **Shape:** seasonality, launch spikes, day-of-week patterns, promo calendar (build an
  events_calendar reference table and let it drive the curves).
- **Entities:** real product names/lines from the dossier, real channel names, plausible
  SKU counts.

## Generator discipline

- **Deterministic:** fix the RNG seed (SF: `numpy seed 20260630`). Regeneration must be
  reproducible; the demo, the deck, and the lab all cite the same numbers.
- **One script per layer:** `generate_data.py` (clean-ish analytical layer) and, if the
  engagement warrants it, `generate_sources_tier1.py` (vendor-exact raw exports).
- **Reconciliation targets:** compute and record the expected aggregates (monthly revenue by
  channel, etc.) — they double as the correctness check for any downstream pipeline work.
- **Data dictionary:** ship `DATA_DICTIONARY.md` — schema, grain, calibration notes,
  intentional-dirtiness inventory. It reads as professionalism in front of client IT.

## Deliberate dirtiness

If the engagement includes any data-platform story (medallion lakehouse, ETL, warehouse),
make the bronze layer **realistically dirty**: mixed-case IDs, null discounts, duplicate
rows (SF: ~1,170 bad casings, ~197 nulls, 25 dups across ~70K rows). Clean data makes the
silver-layer demo a lie; dirty data makes the cleaning story real.

## Two tiers of realism

- **Tier 1 — analytical tables:** the CSVs the app/dashboards read. Enough for the demo.
- **Tier 2 — source-system-shaped exports:** files shaped exactly like the client's actual
  vendor exports (SF simulated 16 systems: Shopify, Amazon Seller Central + Ads, Sephora
  brand portal, Klaviyo, Attentive, GA4, Meta/Google/TikTok/Pinterest paid media, LTK,
  Stackline, TikTok Shop, internal xlsx trackers). Build Tier 2 when the pitch includes an
  ingestion/integration story — walking an exec through *their own vendors'* file formats is
  disproportionately convincing.

## Domain checklist

Cover every domain a surface will show (SF: sales, marketing spend, web traffic, email/SMS,
inventory, retention, creators, campaigns, launch scorecard, AI-visibility share-of-voice,
reference dims + events calendar). A surface with no backing table is where demos 404.

## Hands-on lab (optional, high-leverage)

If the client's required platform differs from the demo stack, build a **copy-paste lab**
(SF: 15-module Fabric/OneLake HTML lab: workspace → lakehouse → bronze/silver/gold PySpark →
SQL endpoint → semantic model → Power BI → wire to app → orchestration → governance →
teardown). It proves the migration path is real before contract, and becomes Week-1 delivery
material after signature. Note real-world access constraints in the lab (SF lesson: fresh
tenants can't create free Fabric trial capacity — the unblock was paid Azure F2 at ~$0.36/hr,
an operator-gated step).

## Honesty lines (use verbatim when relevant)

- "All data shown is synthetic, calibrated to your public footprint — no client data was
  used."
- On data leaving a governed platform: never claim "nothing leaves." The honest line is
  "a minimized, aggregated slice; no-train / zero-retention posture on all model calls."


## The contract needs "extras" by default

Surface agents always need soft datasets beyond the exec numbers: review corpus with text,
share-of-voice trend series, pipeline/funnel slices, support-contact themes, top-account
lists. Derive them programmatically from the simulation's gold layer at contract-export time
and ship them inside the same data module — if they're missing, surface agents will be forced
to invent numbers, which violates the one-ledger rule.
