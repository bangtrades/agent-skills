# Generation Architecture — ledger, calibration, distortion, dirt

This is the proven generator design (battle-tested on a live client engagement). Follow it structurally; swap the config, not the architecture. All values below are defaults or shape illustrations — every real number comes from the active client's `simulation.config.yaml`.

## 1. Determinism

- `numpy.random.default_rng(seed)` + `random.seed(seed)`; seed lives in `simulation.config.yaml`.
- Same config → byte-identical outputs. This matters: demos get regenerated, decks quote numbers, and drift between regenerations destroys trust in the artifact.
- One seed for bronze, a derived seed (`seed + 1`) for vendor exports, `seed + 2` for docs — so layers can regenerate independently without reshuffling each other.

## 2. The canonical ledger

`build_daily_ledger(config)` produces the single truth: a `date × channel → net_revenue` frame for the full window, plus shared dims (products, channels, events). Construction:

1. **Channel-month targets.** For each month, split `monthly_net_m` by `channel_share`; prior-year shares derived as `share / (1 + channel_yoy)` per channel, renormalized.
2. **Daily shaping (multiplicative):** `weekday_factor × event_lift × noise`, where noise = `rng.normal(1.0, σ)` (σ ≈ 0.06–0.10). Event lifts come from the config's events calendar (retailer sale windows, launches, gifting, holiday).
3. **Exact rescale.** After shaping, rescale each channel-month so it ties to target *exactly*. Tie-out is then structural, not statistical.

SKU-level detail is drawn *inside* a day's channel total: `sku_weight × category-affinity(channel) × launch-gating` (SKUs contribute zero before `launch_date` — realistic launch effects for free). Unit economics from dims: `gross = units × list_price`, `discount = gross × channel_discount_rate × jitter`, `returns` likewise, and enforce the identity `net = gross − discount − returns` by solving for units/discount, never by fudging net (net is ledger-fixed).

Useful distributions: `rng.dirichlet` for spend/platform splits, `rng.uniform` for rates, Zipf-ish `1/rank^k` for store/creator/SKU long tails.

## 3. The cross-source distortion model

**The core insight: every vendor file is a *transform of the ledger*, and the transforms disagree the way real systems disagree.** Defaults (override per brand in config):

| source view | transform of ledger | why |
|---|---|---|
| Commerce platform (Shopify) net sales | = ledger DTC exactly | it IS the ledger for DTC |
| Retail portal (Sephora et al.) net | = ledger retail channel exactly | sell-through truth |
| Amazon Ordered Product Sales | ledger / (1 − ~12%) | OPS is gross of returns/discounts |
| TikTok Shop GMV vs Gross Revenue | GMV = ledger / (1 − refund_rate) | GMV ≠ revenue |
| GA4 revenue | 0.90 × commerce platform | consent + attribution loss |
| Meta-attributed revenue | ×1.45 vs its true contribution | 7d-click/1d-view over-attribution |
| TikTok Ads-attributed | ×1.35 | same disease |
| Google-attributed | ×1.15 | brand-search harvesting |
| Pinterest | engaged-view-inflated ROAS | platform-reported optimism |
| ESP+SMS lifecycle revenue | together = 16% of total net | lifecycle attribution overlaps paid |
| Panel estimates (Stackline-class) | ledger ± 10% noise | third-party modeling error |
| Scraper estimates (FastMoss-class) | ledger ± 25% noise | worse modeling error |

The *sum of platform-attributed revenue deliberately exceeds actual revenue*. That's not a bug — attribution-vs-incrementality reconciliation is the flagship silver-layer lesson and a devastating pitch moment ("your platforms claim 1.6× your actual revenue — here's what's really incremental").

Panel/scraper error must be *modeled* noise (seeded, smooth-ish, occasionally directionally wrong), not white noise per row.

## 4. Intentional dirt (bronze only)

Inject into the idealized bronze layer, in configured quantities, and report exact counts in RECONCILIATION.md:
- inconsistent key casing/whitespace (lowercased ids, padded `" ID "` variants) — ~2% of rows
- null-able numeric columns (discount) — ~0.5%
- exact duplicate rows — a couple dozen
- vendor exports carry their *structural* quirks instead (comment blocks, total rows, currency strings, blank continuation rows) — from the schema YAML quirks lists. Do not add random dirt to vendor files; their realism comes from structure, not typos.

## 5. Config is the API

Everything above is driven by `simulation.config.yaml` (template in `assets/`). Generators contain *mechanism*; the config contains *facts about the brand*. When real client data eventually replaces a simulated source, the swap is config + one generator function — not a rebuild. Design every function with that swap in mind.

## 6. Reconciliation report

`run_all.py` ends by printing and writing:
- monthly net vs ladder (24 rows, delta %, must be ≤0.1%)
- channel mix vs target (≤0.5pt)
- identity check pass count + intentional-dirt counts
- every distortion ratio measured vs designed band (e.g., "Meta attributed / true contribution = 1.44 (target 1.45 ±0.05) ✓")
- row counts per file

If any check fails, the run fails. No silent clamping.
