# Nine-Vector Framework — Reading Guide

The 9-vector synthesis is bang's session-archetype classifier. Each vector is read independently per timeframe; the cross-TF aggregate determines the bias verdict.

> Originated in `~/Cortana/cortana-vault/research/topics/ny-session-frameworks.md`. Refer there for the source authority.

## The 9 Vectors

| # | Vector | What you read | Bullish signal | Bearish signal | Neutral / unclear signal |
|---|---|---|---|---|---|
| 1 | **Opening context** | Where price opened relative to prior day VA, ON inventory | Inside VA or near composite POC = range-like; gap up from VA → trend up | Gap down or open below VA | Mid-VA, no clear edge |
| 2 | **Price action structure** | Recent N-bar shape — pushes, pullbacks, single prints | Higher highs + higher lows; initiative pushes | Lower highs + lower lows; cascade structure | Overlapping candles, two-sided rotation |
| 3 | **VWAP behavior** | Distance and direction to VWAP, reclaim attempts | Price above VWAP with sustained hold | Price below VWAP with rejection | Multiple crosses, no sustained hold |
| 4 | **EMA / MA Bands stack** | BT MA Bands — order of MA2 / Anchor / MA3 / MA5 / MA6 / MA7 | Short MAs above long MAs, expanding | Short MAs below long MAs, descending | Braided / flat / converging |
| 5 | **Volume profile shape** | BT Session VP Heat (when on chart) or visual approximation | P-shape (top-heavy) confirming bull or D-shape with rising POC | b-shape (bottom-heavy) confirming bear | D-shape with centered POC = range |
| 6 | **CDCΔ** | BT Smart CVD slope + BT CVD Divergence | Positive slope OR positive divergence at lows | Negative slope OR negative divergence at highs | Flat / oscillatory |
| 7 | **Aggression / flow** | BT Volatility Envelope + Delta `delta_pct` and buy/sell vol ratio | delta_pct > 50% buy with rising volume | delta_pct < −50% sell with rising volume | Spikes that fade quickly = range; |delta_pct| < 30% = neutral |
| 8 | **BBWP / K-span regime** | BT State, Structure & Energy components OR visual K-band width | Expanding (BBWP rising, K-span widening) in trend direction | Expanding against existing trend = potential reversal | Compressed (BBWP < 40, K-span narrow) = range / pre-breakout |
| 9 | **IB range vs 20-day avg** | Key Levels Suite IB high/low (post-10:30 ET) vs 20-day avg | Strong IB break with acceptance | IB containment with multiple boundary tests = range | n/a outside RTH |

## How to Read Each Vector (Decision Logic)

### Vector 1 — Opening Context

- Source: visual from screenshot + Key Levels Suite for prior VA
- Threshold:
  - Gap >0.5 ADR with acceptance → trend candidate
  - Gap inside prior VA → range / mean reversion likely
  - Outside VA but rejected back inside → reversal candidate (Archetype 4)

### Vector 2 — Price Action Structure

- Source: OHLCV last 20-50 bars + visual
- Look for:
  - Stair-stepping higher highs / lows → trend (bullish)
  - Stair-stepping lower highs / lows → trend (bearish)
  - Equal highs / lows with overlap → range
  - Sharp displacement single bars → momentum ignition

### Vector 3 — VWAP Behavior

- Source: BT VWAP value vs current price
- Compute: distance in points, sign
- Threshold rules:
  - >0.5 ATR above VWAP with no recent reclaim attempt → bullish
  - <0.5 ATR below VWAP with no recent reclaim attempt → bearish
  - Multiple crosses within 30 min → range

### Vector 4 — MA Bands Stack

- Source: BT MA Bands plots — MA2, Anchor, MA3, MA5, MA6, MA7, Upper, Lower
- Bullish stack: MA2 > Anchor > MA3 > MA5 > MA6 > MA7 (short above long)
- Bearish stack: reverse order
- Braided: MAs within 0.5 ATR of each other, no clear order

### Vector 5 — Volume Profile Shape

- Source: BT Session VP Heat (if on chart, visual read from screenshot)
- Shapes:
  - **D-shape**: centered POC, normal distribution → range / balance
  - **P-shape**: top-heavy POC → buyers exhausted at top OR accumulation
  - **b-shape**: bottom-heavy POC → sellers exhausted at bottom OR distribution
  - **Double distribution**: two POCs → regime transition / Archetype 4 candidate

### Vector 6 — CDCΔ

- Source: BT Smart CVD value + BT CVD Divergence
- Bullish:
  - Smart CVD slope rising
  - OR Divergence indicator showing positive divergence at lows
- Bearish: inverse
- Neutral: oscillatory / flat slope

### Vector 7 — Aggression / Flow

- Source: BT Volatility Envelope + Delta — `delta_pct`, `buy_vol`, `sell_vol`
- Compute: buy_vol / sell_vol ratio
- Thresholds:
  - delta_pct > 70% with ratio > 3:1 = strong commitment to direction
  - delta_pct ∈ [30%, 70%] = directional but not extreme
  - |delta_pct| < 30% = neutral, no clear flow
- Special case — **absorption signature**: delta_pct >> 70% buy at a major support level → bullish reversal candidate (and vice versa for resistance + sell delta = bearish reversal)

### Vector 8 — BBWP / K-span Regime

- Source: BT State, Structure & Energy (BBWP component) + BT Volatility Envelope width
- Thresholds (from BBWP):
  - BBWP > 70 = expanded / trend regime
  - BBWP 40-70 = mid-range
  - BBWP < 40 = compressed / range regime
- Cross-reference with K-span width visually — narrow K = compression, wide K = expansion

### Vector 9 — IB Range vs 20-day Average

- Source: Key Levels Suite IB markers (post-10:30 ET only)
- Compute: today's IB range / 20-day avg IB range
- Thresholds:
  - < 70% = compressed IB → range day signature
  - 70-130% = normal
  - > 130% = expanded IB → trend day signature
- N/A outside RTH or before 10:30 ET

## Aggregating Across Timeframes

For each vector, score it on each TF (5m, 15m, 1h):
- bullish = +1
- bearish = −1
- neutral / unclear = 0

Per-vector aggregate: sum across 3 TFs.
Total score = sum of 9 vector aggregates.

Verdict:
- Total > +12 → STRONG LONG
- Total +6 to +12 → MODERATE LONG
- Total +3 to +5 → WEAK LONG (caution)
- Total −2 to +2 → UNCLEAR / stand aside
- Total −3 to −5 → WEAK SHORT (caution)
- Total −6 to −12 → MODERATE SHORT
- Total < −12 → STRONG SHORT

## Cross-TF Contradiction Handling

When 1h disagrees with 5m/15m:
- **1h dominates for daily bias.** If 1h is bullish, the day's bias is long even if 5m is currently bearish (just means a pullback is forming).
- **5m/15m alignment with 1h direction = setup ready to trigger.** If 1h bullish + 15m bullish + 5m showing buy absorption at lower K = T1 setup is live.
- **5m/15m disagreement with 1h = wait for resolution.** Stand aside or reduced size.

## Special Patterns to Recognize

### Absorption signature (vector 7 + 8 combined)

- BBWP expanded (>70) AND price at a structural extreme (lower K, lower envelope) AND delta_pct >> 90% buy AND flip_signal = 1.00

→ **Textbook absorption** at support. T1 setup is live.

Inverse for resistance + sell delta.

### Cascade signature (vector 2 + 6 + 8 combined)

- Lower highs + lower lows on 5m AND CVD trending hard down AND BBWP expanding → Archetype 3 cascade DOWN

Inverse for cascade UP.

### Range signature (vector 1 + 5 + 8 combined)

- Opening inside VA AND D-shape profile AND BBWP < 40 → Archetype 1 range. Range-Day Playbook applies.

### False-break signature (vector 1 + 2 + 5 combined)

- Open outside VA → break extension → sharp reclaim → double distribution profile forms → Archetype 4 reversal. Fade the failed break.
