# Setup Taxonomy — T1, T2, R1, R2, R3 with Trigger Criteria

The five named playbook setups bang trades. Every snapshot must identify which (if any) are LIVE / IMMINENT / NOT APPLICABLE.

> Source authorities:
> - T1, T2: `~/Cortana/cortana-vault/research/topics/trend-pullback-playbook.md`
> - R1, R2, R3: `~/Cortana/cortana-vault/research/topics/range-day-playbook.md`

## Setup Status Categories

For each candidate setup, output one of:

- **LIVE** — All trigger conditions currently met. Trade is actionable right now (subject to R5).
- **IMMINENT** — 2 of 3 trigger conditions met, third is one bar away. Trade is forming.
- **NOT APPLICABLE (NA)** — Required pre-conditions not present (e.g., 1h bias doesn't match).
- **INVALIDATED** — Setup zone was tested and broken, no further trade on this side.

## T1 — Failed Lower-K Breakout + Orderflow + IFVG (Long)

| Field | Spec |
|---|---|
| **Pre-condition** | 1h bias bullish — price in upper portion of 1h K channel |
| **Trigger zone** | Price tests **lower** 5m K channel OR lower 15m K channel |
| **Confirmations (all 3 required)** | (a) Failed breakout — wick below lower K, then close back inside K; (b) BT Deep Trades Lite shows buy-side aggression at the test; (c) BT CVD Divergence shows positive divergence OR delta_pct >> 70% buy on the rejection bar |
| **Entry trigger** | 1m or 2m IFVG forming at or near the failed-breakout zone |
| **Stop** | Opposite side of the IFVG (typically 4–8 NQ pts) |
| **Target 1** | 5m or 15m mid-K (anchor MA) — scale 50% |
| **Target 2** | 5m or 15m upper K — scale remaining |
| **Swing target** | 1h opposite K boundary (held only on highest-conviction setups) |
| **Position size** | 2 micros MNQ ($4/pt) — R1 cap |
| **Time-out** | If T1 not hit in 20 min, scratch |

**LIVE detection (output as LIVE):**
- 1h bullish ✓
- Price at or below 5m/15m lower K
- Latest 5m bar delta_pct > 70% buy AND buy/sell ratio > 3:1
- AND price reclaim of the lower K (close above K on current or just-closed bar)

**IMMINENT detection:**
- 1h bullish ✓
- Price within 15 pts of 5m/15m lower K
- Order flow building (delta_pct rising, CVD positive divergence forming)

## T1 inverse — Failed Upper-K Breakout + Orderflow + IFVG (Short)

Mirror of T1. All conditions inverted: 1h bearish, upper K test, failed breakout above, sell delta dominance, IFVG short.

## T2 — EMA Backtest (Consolation Long Entry)

| Field | Spec |
|---|---|
| **Pre-condition** | 1h bias clear; price already in trend (missed T1, looking for re-entry) |
| **Trigger zone** | Pullback to one of: 2m 20, 2m 89, 5m 20, 15m 20, 1h 20 EMA |
| **Confirmations (min 2 of 3)** | (a) EMA holds; (b) Deep Trades / CVD shows trend-side commitment; (c) candle pattern confirms (engulfing, hammer) |
| **Entry** | On bounce confirmation candle close |
| **Stop** | Below EMA + ATR buffer (6–12 pts) |
| **Target 1** | Prior swing high in trend direction |
| **Target 2** | 5m/15m upper K |
| **Position size** | 2 micros MNQ ($4/pt) |
| **Conviction tier** | 1h 20 EMA > 15m 20 EMA > 5m 20 EMA > 2m 20/89 EMA |

**LIVE detection:**
- 1h bullish + 5m/15m bullish (stack expanding direction)
- Price testing one of the named EMAs from above
- Confirmation candle closed
- Deep Trades / CVD shows buy commitment

**IMMINENT detection:**
- Price within 8 pts of one of the named EMAs, descending into it
- Trend bias intact

## R1 — VWAP / K-Mid Mean Reversion (Range Day)

| Field | Spec |
|---|---|
| **Pre-condition** | Archetype 1 confirmed (Range / Rebalancing) |
| **Trigger zone** | Price ≥ upper K-band OR ≤ lower K-band on 1m / 5m |
| **Confirmations (min 2 of 3)** | (a) CDCΔ flat or divergent at the extreme; (b) aggression spike with absorption (no follow-through); (c) prior bar wick rejecting the band |
| **Entry** | Limit at K-band edge OR market on bar-close reclaim back inside the band |
| **Stop** | 1 K-span width past the band (6–10 NQ pts) |
| **Target 1** | VWAP / K-mid — scale 50% |
| **Target 2** | Opposite K-band (rare; only on confirmed double distribution) |
| **Position size** | 1 micro (range-day cap, tightened from default R1) |
| **Time-out** | If T1 not hit in 30 min, scratch |

**LIVE detection:**
- Archetype 1 verdict ✓
- Price at or just past 5m K Upper or Lower
- delta_pct shows absorption (high % AGAINST the prior direction)
- Aggression spike present but ratio fading

## R2 — IB Extreme Fade (Range Day)

| Field | Spec |
|---|---|
| **Pre-condition** | Archetype 1 confirmed; time after 10:30 ET (IB complete) |
| **Trigger zone** | Price at IB high or IB low |
| **Confirmations (min 2 of 3)** | (a) Failed extension — poke ≤ 4 NQ pts past IB then reject; (b) aggression spike absorbed; (c) volume on the poke < avg extension bar volume |
| **Entry** | On bar close back inside IB |
| **Stop** | 1.5× the rejection-bar range past IB extreme |
| **Target 1** | VWAP — scale 50% |
| **Target 2** | Opposite IB extreme |
| **Anti-rule** | If price accepts outside IB for ≥3 bars with EMA stack forming, this is no longer Archetype 1 — exit and stop trading the playbook |

## R3 — Value-Area Edge Fade (Range Day)

| Field | Spec |
|---|---|
| **Pre-condition** | Archetype 1 confirmed |
| **Trigger zone** | Price at VAH or VAL of composite profile |
| **Confirmations (min 2 of 3)** | (a) P-shape or b-shape pattern at the edge; (b) CDCΔ divergence; (c) no follow-through on the poke |
| **Entry** | On bar close back inside VA |
| **Stop** | Past prior bar wick by 2 NQ pts |
| **Target 1** | POC |
| **Target 2** | Opposite VA edge |
| **Anti-rule** | If POC migrates toward the edge being faded, stop trading R3 for the day |

## How to Output Setup Status

In the snapshot file, include a table like:

```markdown
| Setup | Status | Trigger Zone | Stop | T1 | T2 | Notes |
|---|---|---|---|---|---|---|
| T1 long | LIVE | 29,141 | 29,118 | 29,222 | 29,326 | 1m IFVG forming, 5m delta_pct +95.95% |
| T1 short | NA | — | — | — | — | 1h bias is bullish |
| T2 long (5m 20 EMA) | IMMINENT | 29,150 (pullback target) | 29,138 | 29,200 | 29,250 | Wait if T1 fires |
| R1 long | NA | — | — | — | — | Not Archetype 1 |
| R2 long | NA | — | — | — | — | Not Archetype 1 |
| R3 long | NA | — | — | — | — | Not Archetype 1 |
```

For Archetype 1 days, T1/T2 will be NA and R1/R2/R3 take over. For trend days, R1/R2/R3 are NA.

## Critical: Setup Status Is Not Optional

Every snapshot must include this table — even when no setup is currently live. The user needs to know:
1. What's live right now (if anything)
2. What's the closest IMMINENT setup
3. What levels matter for the next push

A snapshot that produces a bias verdict but omits setup zones is incomplete.
