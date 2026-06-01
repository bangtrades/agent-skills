# Concept Tagging — Chart Library Frontmatter Contract

Every snapshot's frontmatter must tag what it demonstrates. Without proper tagging, the snapshot doesn't auto-surface in the Cortana chart-library Dataview queries — and the bidirectional linking breaks.

> Source authority: `~/Cortana/cortana-vault/projects/nq-trading/tv-data/chart-library/_index.md`

## Required Frontmatter Fields

```yaml
archetype: "1" | "2" | "3" | "4" | "unclear"
demonstrates_concept: [list of concept slugs]
demonstrates_strategy: [list of strategy slugs]
demonstrates_setup: [list of setup slugs]
outcome: "in-progress" | "win" | "loss" | "scratch" | "didnt-trigger" | "calibration-only"
key_observation: "Single sentence: what does this snapshot teach?"
```

## Concept Slugs (for `demonstrates_concept`)

Pick the concepts the snapshot demonstrates. Each maps to a chart-library page at `cortana-vault/projects/nq-trading/tv-data/chart-library/concepts/<slug>.md`:

| Slug | When to tag |
|---|---|
| `absorption` | Latest bar shows extreme one-sided delta (>70%) at a structural level — buyers absorbing offers (or vice versa). Signature: high buy_vol, low sell_vol, price holds despite prior selling. |
| `cvd-divergence` | Price made a new low (or high) but CVD did not — Smart CVD / CVD Divergence shows positive divergence (or negative at highs). |
| `failed-auction` | Aggressive orders cannot push through a structural level → rejection back to value. Most common at IB extremes or VAH/VAL. |
| `poc-failure` | Price approaches the POC but fails to accept there → entry trigger in Vacuum Method. |
| `lvn-pullback` | Pullback into a Low Volume Node in a trending move → trend re-entry zone. |
| `reload-pattern` | Large passive order appears on the DOM → high probability of price reaching that level. |
| `value-area-edge-fade` | Price tags VAH or VAL and rejects → mean-reversion back to POC. |
| `momentum-ignition` | Large aggressive orders flood one side triggering stops and algos — self-reinforcing move. |
| `keltner-traversal` | Price is moving between K channel boundaries with the trend direction as bias. The foundation of T1 setups. |
| `ifvg` | An Inverse Fair Value Gap is forming or providing entry — a 3-bar pattern where a prior FVG zone has been violated and now acts as opposite-direction support/resistance. |

## Strategy Slugs (for `demonstrates_strategy`)

Pick from documented strategies (external methodologies) that the current setup resembles. Often empty for live snapshots; useful for replay drills:

| Slug | When to tag |
|---|---|
| `yush-model-1` | Range fade — VA edge + big-trade + delta confirmation. |
| `yush-model-2` | Trend LVN pullback — entry on pullback into LVN with big-trade + delta. |
| `cimi-failed-auction` | Composite VP level + absorption on footprint → mean reversion to POC. |
| `okala-8020` | Mean reversion at x80/x20 NQ round-number levels. |
| `spc-strategy` | Sweep level + LVN tag + 5-min candle closure + CVD agreement. |
| `first-candle-value` | Enter on closure outside 15-min VP, stop at POC. |
| `vacuum-method` | P/b-shape trapped profile → POC failure entry, target LVN end. |
| `kc-breakout` | Keltner channel expansion breakout with regime filter (BT internal strategy). |

## Setup Slugs (for `demonstrates_setup`)

The five BT internal playbook setups:

| Slug | When to tag |
|---|---|
| `t1-failed-lower-k` | T1 long setup (or T1 short, same slug — direction inferred from context). |
| `t2-ema-backtest` | T2 EMA backtest consolation entry. |
| `r1-vwap-revert` | R1 VWAP / K-mid mean reversion. |
| `r2-ib-fade` | R2 IB extreme fade. |
| `r3-va-edge-fade` | R3 value-area edge fade. |

## Archetype Values

```yaml
archetype: "1"    # Range / Rebalancing
archetype: "2"    # Rebalance → Trend Acceptance
archetype: "3"    # Trend Acceptance → Cascade
archetype: "4"    # False Break / Exhaustion Reversal
archetype: "unclear"
```

## Outcome Values

For live snapshots (no trade taken yet):
- `outcome: "in-progress"` — capture during an active session, trade may follow
- `outcome: "calibration-only"` — capture for reference, no trade intended

For post-trade snapshots:
- `outcome: "win"` — linked trade hit target
- `outcome: "loss"` — linked trade hit stop
- `outcome: "scratch"` — linked trade exited at breakeven
- `outcome: "didnt-trigger"` — setup zone was identified but conditions never converged

For after-hours / R5-blocked snapshots:
- `outcome: "calibration-only"` — almost always the right tag

## Tagging Decision Tree

For each snapshot, ask:

1. **What's the archetype?** → set `archetype`
2. **What setups are LIVE or IMMINENT?** → add their slugs to `demonstrates_setup`
3. **What concepts is the live tape showing?**
   - Strong one-sided delta at a key level → `absorption`
   - CVD positive divergence at lows (or negative at highs) → `cvd-divergence`
   - Failed extension past IB → `failed-auction`
   - K channel test in trend direction → `keltner-traversal`
   - 1m/2m IFVG forming → `ifvg`
   - Large passive order visible on DOM (manual observation) → `reload-pattern`
   - VAH/VAL test → `value-area-edge-fade`
   - Strong directional aggression → `momentum-ignition`
4. **Does this look like a published methodology?** → add to `demonstrates_strategy`
5. **Did the user already trade it / will they?** → set `outcome` accordingly

## Multi-Tag Examples

### Example 1 — Pre-T1 setup snapshot

```yaml
archetype: "3"
demonstrates_concept: ["keltner-traversal", "absorption"]
demonstrates_strategy: []
demonstrates_setup: ["t1-failed-lower-k"]
outcome: "in-progress"
key_observation: "5m bar shows 95.95% buy delta at lower K — T1 setup live."
```

### Example 2 — Range-day R1 trade taken and won

```yaml
archetype: "1"
demonstrates_concept: ["value-area-edge-fade", "failed-auction"]
demonstrates_strategy: ["yush-model-1"]
demonstrates_setup: ["r1-vwap-revert"]
outcome: "win"
key_observation: "Faded upper K at VAH; absorbed sell delta; reverted to VWAP for +12 pts."
```

### Example 3 — After-hours baseline (no trade)

```yaml
archetype: "unclear"
demonstrates_concept: ["keltner-traversal"]
demonstrates_strategy: []
demonstrates_setup: []
outcome: "calibration-only"
key_observation: "Post-RTH consolidation; R5 blocks; baseline reference for next session."
```

### Example 4 — Archetype 4 reversal trade

```yaml
archetype: "4"
demonstrates_concept: ["failed-auction", "absorption", "cvd-divergence"]
demonstrates_strategy: ["cimi-failed-auction"]
demonstrates_setup: []
outcome: "in-progress"
key_observation: "Aggressive extension above prior day VAH absorbed; CVD divergence; double-distribution forming."
```

## Where Snapshots Auto-Surface

Once tagged, the snapshot auto-appears in the Dataview queries on:

- `chart-library/concepts/<slug>.md` for each concept tagged
- `chart-library/strategies/<slug>.md` for each strategy tagged
- `chart-library/setups/<slug>.md` for each setup tagged
- `chart-library/archetypes/archetype-<N>-<...>.md` for the archetype

Each library page's Dataview block pulls every snapshot with the matching `demonstrates_*` value, so populating frontmatter correctly is the entire mechanism.

## When to Create a New Concept

If the snapshot demonstrates a concept that's not in the slug list, two paths:

1. **Tag with the closest existing slug** + flag in `key_observation` that a new concept is implied. Mention it to the user.
2. **Don't tag it.** A missing tag is better than a wrong tag.

Do NOT silently invent new slugs without updating the chart-library structure.
