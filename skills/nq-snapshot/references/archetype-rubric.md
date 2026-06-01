# Archetype Rubric — Four Day Types with Diagnostic Patterns

Bang's 4-archetype session classification. Every snapshot outputs an archetype verdict.

> Source authority: `~/Cortana/cortana-vault/research/topics/ny-session-frameworks.md`

## Archetype 1 — Range / Rebalancing

> Bias: **Fade extremes → target VWAP / K-mid.**

| Vector | Reading |
|---|---|
| Opening context | Opens inside prior VA or near composite POC |
| Price action structure | Overlapping candles, two-sided rotation, equal highs/lows |
| VWAP behavior | Multiple VWAP crosses; no sustained hold; mean reversion to VWAP |
| EMA 9/21/55 (BT MA Bands) | EMAs braided/flat; frequent crossovers |
| Volume profile | D-shaped; centered POC; minimal migration |
| CDCΔ | Flat / oscillatory; frequent signal crosses |
| Aggression / flow | Aggression spikes fade quickly |
| Regime / volatility | BBWP mid/compressed (< 50); K-span narrow |
| IB range | Compressed (< 70% of 20-day avg) |

**Playbook to use**: Range-Day Playbook (R1, R2, R3 setups).

**Counter-confirms** (if these are present, NOT Archetype 1):
- Strong EMA stack (long stack ascending or descending)
- Single prints / displacement bars
- BBWP > 70 (expansion territory)
- Sustained one-sided delta (>70% in same direction across 5+ bars)

## Archetype 2 — Rebalance → Trend Acceptance

> Bias: **Trade in direction of acceptance; pullback entries.**

| Vector | Reading |
|---|---|
| Opening context | Opens in value; initial rotation fails one side |
| Price action structure | Early rotation → initiative push → acceptance outside IB |
| VWAP behavior | Initial chop across VWAP → decisive reclaim or rejection; then VWAP acts as dynamic S/R |
| EMA stack | EMAs initially braided → stack and expand; short MAs lead, long MAs follow |
| Volume profile | POC migrates; value shifts |
| CDCΔ | Slope builds after balance; sustained directional bias |
| Aggression / flow | Flow crosses signal and holds |
| Regime / volatility | K-span expanding; BBWP rising |
| IB range | Normal to expanding |

**Playbook to use**: Trend-Pullback Playbook (T1, T2 setups).

**Signature pattern**: Morning has tight initial 30-min IB → after 10:30 ET, IB extension holds in one direction → trend day with pullback entries.

## Archetype 3 — Trend Acceptance → Cascade

> Bias: **Pullbacks only; no fades.**

| Vector | Reading |
|---|---|
| Opening context | Opens outside value or gap beyond prior range |
| Price action structure | Immediate displacement; shallow pullbacks; single prints |
| VWAP behavior | VWAP rarely reclaimed; price holds one side entire session |
| EMA stack | Strong EMA alignment early; clean stack; widening separation; no re-cross |
| Volume profile | Elongated; thin behind move |
| CDCΔ | Strong unidirectional CDCΔ; minimal pullback |
| Aggression / flow | Persistent aggression in trend direction; little opposing delta |
| Regime / volatility | High BBWP (> 70); wide K-span; expansion day |
| IB range | Expanded (> 130% of 20-day avg) |

**Playbook to use**: Trend-Pullback Playbook with emphasis on T2 EMA-backtest entries (T1 setups rare because pullbacks are shallow).

**Anti-pattern**: Fading a cascade is the highest-cost mistake. If aggression and CVD are both pushing hard, don't fight it.

## Archetype 4 — False Break / Exhaustion Reversal

> Bias: **Fade failed breakout; target opposite VA.**

| Vector | Reading |
|---|---|
| Opening context | Opens outside value but stalls |
| Price action structure | Breakout attempt → sharp reclaim → reversal structure |
| VWAP behavior | Early extension away from VWAP → sharp reclaim → VWAP flips sides |
| EMA stack | EMAs initially stack → short MAs cross back through long MAs; possible mid-MA reclaim |
| Volume profile | Double distribution; P or b-shape reversal |
| CDCΔ | Delta divergence; slope stalls before price reversal |
| Aggression / flow | Aggression spike followed by absorption |
| Regime / volatility | BBWP expanding then compressing |
| IB range | Often starts expanded then narrows |

**Playbook to use**: Special — Archetype 4 reversal trades are similar to T1 but at extreme levels (not the K channel). Fade the failed break, target the opposite VA or VWAP.

**Signature pattern**: Strong move in one direction → sudden volume spike absorbed → reversal candle → price closes back inside the prior range. The absorption bar is the key — if delta_pct is extreme (>90%) AGAINST the prior move at the extension, that's the signal.

## Unclear

When ≤2 of the 9 vectors agree on either direction, or vectors are split across TFs without resolution:

- **Verdict**: Unclear
- **Action**: Stand aside
- **Next check**: Re-evaluate in 1-2 hours OR after a structural event (IB completion, lunch close, etc.)

## How to Output the Archetype Verdict

In the snapshot:

```markdown
**Archetype Verdict: [ARCHETYPE NAME]**
**Confidence: STRONG / MODERATE / WEAK / UNCLEAR**

Reasoning:
- 9-vector score: +X (long) / −X (short)
- Key contributing vectors: [list 3-5 strongest]
- Vectors against: [list any contradicting]
- Cross-TF agreement: [1h ✓ / 15m ✓ / 5m ✓ — or note disagreement]
```

The verdict drives playbook selection:

| Archetype | Playbook |
|---|---|
| 1 — Range | Range-Day Playbook (R1/R2/R3) |
| 2 — Rebalance→Trend | Trend-Pullback Playbook (T1/T2) |
| 3 — Trend→Cascade | Trend-Pullback Playbook, emphasis on T2 |
| 4 — False-Break Reversal | Special Archetype-4 reversal trade |
| Unclear | Stand aside |

## Cross-Confirmation Heuristics

When an archetype call is ambiguous, these heuristics break ties:

| Heuristic | If TRUE → leans toward |
|---|---|
| BBWP < 40 across all TFs | Archetype 1 |
| BBWP > 70 across all TFs + clean EMA stack | Archetype 2 or 3 |
| Single prints / displacement bars visible on 5m | Archetype 3 |
| Sharp reclaim after extension in last 5-10 bars | Archetype 4 |
| Multiple VWAP crosses in last 30 min | Archetype 1 |
| Price holding one side of VWAP > 1 hour | Archetype 2 or 3 |
| IB completed but no extension | Archetype 1 |
| IB completed with extension that held | Archetype 2 |
| Extension reversed back through IB | Archetype 4 |

## Mid-Day Re-Evaluation

The archetype can flip mid-day. Re-run the classifier at:

- 10:30 ET (IB completion)
- 11:00 ET (post-IB confirmation)
- 14:00 ET (post-lunch directional resolution)
- Whenever a structural break occurs (BOS / MSS marker)

If ≥3 vectors change category, exit any open positions and re-classify.
