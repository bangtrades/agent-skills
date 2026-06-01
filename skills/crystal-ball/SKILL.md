---
name: crystal-ball
description: >-
  Capture and analyze bang's Crystal Ball (CB) fib-expansion tool on a TradingView
  NQ/MNQ chart — decode the T1–T5 target ladder, trace price through it, apply the
  fractal multi-timeframe framework, and write a CB analysis into the Cortana vault.
  Use this skill aggressively whenever the user mentions the "CB tool", "crystal ball",
  a "CB example", a fib expansion, expansion targets / T1–T5, or asks to snapshot or
  analyze a chart that has a CB drawing on it. Also trigger for multi-timeframe
  expansion reads (2m/5m/15m/1h/4h CB nesting), "where is this expansion going",
  fade-the-T5 setups, OB-reversal-zone entries timed against a CB, and adding a new CB
  sample to the library. Do NOT trigger for the 2m K-Span model, generic indicator
  snapshots, or non-NQ/MNQ instruments.
---

# Crystal Ball (CB) — Fib-Expansion Framework

> The Crystal Ball is bang's original price-projection tool: a calibrated Fibonacci
> expansion that forecasts **where** a move travels and **how** it gets there. This skill
> captures a CB drawing off the live TradingView chart, traces price against its ladder,
> applies the fractal multi-timeframe framework, and routes a CB analysis into the vault.
>
> The framework is built from a growing sample library. The authoritative methodology
> page — with every numbered sample — is `research/topics/crystal-ball-cb-tool.md` in the
> Cortana vault. **This skill executes the framework; that page is the evidence base.**
> Refine both as the sample size grows across timeframes.

---

## What the CB tool is (one screen)

A fib drawn on a confirmed expansion. Two construction inputs:

1. **Anchor `0`** — the start of the expansion (the low for a bullish CB, the high for a bearish one), set right after the prior trend's exhaustion flush.
2. **0.618 = the CISD breakout** — the tool is sized so its 0.618 gridline lands on the [[research/topics/cisd|CISD]] that confirmed the trend broke.

With those two inputs fixed, the **T1–T5 ladder** falls out:

| Level | Coeff | Role |
|---|---|---|
| `0` | 0 | expansion start (anchor) |
| `0.618` | 0.618 | CISD breakout — calibration handle |
| `0.877` | 0.877 | minor waypoint |
| **T1** | 1.000 | measured move |
| **T2** | 1.236 | target 2 |
| **T3** | 1.618 | target 3 — start of the chop zone |
| **T4** | 1.902 | target 4 — end of the chop zone |
| **T5** | 2.380 | terminal / exhaustion |

Price walks the ladder in sequence, pausing at each level. It **often chops in the T3–T4
band** (a tendency, not a rule — it can also cascade through). At **T5 the move is exhausted**:
it ranges, manipulates (sweeps) the extreme, then retraces back into the range. Full
construction + behavior detail: **`references/cb-construction.md`**.

The tool is regime-agnostic — it works on **all timeframes** and **both directions**.

---

## When to run this

Run when the user wants a CB read: they point at a chart with a CB drawing, share a "CB
example", ask where an expansion is headed, ask for a fade-T5 or OB-reversal read, or want
a new sample added to the library. The chart is a live or replay-mode **TradingView NQ/MNQ**
chart driven through the `tradingview` MCP.

This skill is the CB cousin of `nq-snapshot`: nq-snapshot reads the live tape via the
9-vector framework; crystal-ball reads a *drawn CB expansion* and its fractal context.

---

## Workflow

### 1 — Locate the CB drawing
Confirm the chart symbol/timeframe (`chart_get_state`) and replay state (`replay_status`).
Extract drawings with `ui_evaluate` over the chart's `dataSources()` — the CB is a
`LineToolFibRetracement` carrying **T1–T5 level labels** (coefficients 1 / 1.236 / 1.618 /
1.902 / 2.38). Capture its two anchor points (`idx`, `price`, and `indexToTimePoint(idx)`)
and the `reverse` flag. See `references/cb-construction.md` for the exact `ui_evaluate`
expression.

### 2 — Decode the ladder
Anchor point[0] = the `0` level (expansion start). The second anchor sets the unit.
**Direction:** anchor low + second anchor above → **bullish** (ladder projects up); anchor
high + second anchor below → **bearish** (ladder projects down). Compute every level.
`cb_trace.py` does this — don't hand-compute.

### 3 — Pull OHLCV
`data_get_ohlcv` for the displayed timeframe, enough bars to span from the anchor to the
frontier (plus a little lead-in). Save to a CSV (`time_unix,open,high,low,close,volume`).
Also `capture_screenshot region=full`.

### 4 — Trace price through the ladder
Run the bundled script — it computes the ladder and the first-touch trace deterministically:

```bash
python3 scripts/cb_trace.py --ohlcv <bars.csv> --anchor-price <P0> \
    --unit-price <P_T1> --direction bull|bear --anchor-unix <U0>
```

It prints: every level's price, the first bar to touch it, bars-from-anchor, the T5
overshoot, and where the last bar sits. This is the repeated arithmetic from every prior
sample — always use the script so the numbers don't drift.

### 5 — Apply the fractal multi-timeframe read
This is the heart of the framework. A CB is **fractal**: a higher-timeframe CB activates on
the HTF breakout and **contains many lower-timeframe CBs** nested inside it. Determine where
*this* CB sits in the nesting, and whether the move is set to extend into higher-TF
projections. Full process — the 2m→5m→15m→1h→4h escalation, OB reversal zones, the entry
logic — is in **`references/fractal-mtf.md`**. Read it for this step.

### 6 — Build the trading read
Apply bang's CB rules: **fade T5** (the exhaustion); a **breakout above T5** → hunt new
longs (fresh expansion); no breakout → measure the opposite-direction CB. Time entries
against **1h / 4h order blocks** as reversal zones. Detail in `references/fractal-mtf.md`.

### 7 — Write the CB snapshot + log the sample
Write the analysis using `references/output-template.md`, to
`cortana-vault/projects/nq-trading/journal/snapshots/YYYY-MM-DD/HHMM-cb-<context>.md`.
Archive the OHLCV CSV to `cortana-vault/research/topics/data/cb-tool-samples/`. Then
**add the capture as the next numbered sample** in `research/topics/crystal-ball-cb-tool.md`
(sample-log row + a detail block) and append a `log.md` entry. The growing sample log is how
the framework gets refined — never skip it.

### 8 — Report
Give the user: the decoded ladder, where price is on it, the phase, the fractal-MTF read,
the trading read, and links to the snapshot + methodology page. Keep chat output tight; the
full analysis is in the file.

---

## Quality bar

A good CB analysis:

1. **Decodes the ladder exactly** — anchors, 0.618/CISD, T1–T5 — verified by `cb_trace.py`, not eyeballed.
2. **Traces price honestly** — which levels were touched, in what sequence, where it chopped vs cascaded, the T5 overshoot. Report what the tape did, including where it diverged from the textbook.
3. **Places the CB in the fractal nesting** — names the HTF CB it sits inside and/or the LTF CBs inside it; says whether the move looks set to print higher-TF projections.
4. **Gives a trading read** — phase (expanding / chop zone / T5 exhaustion / terminal), the fade-T5 / breakout / OB-zone implication. Scenario framing, never a directive "buy here".
5. **Logs the sample** — the capture becomes sample N in the methodology page, so the dataset compounds.

Honest divergence reporting matters more than a clean story. If price cascaded through the
chop zone, or overshot T5 oddly, or the fractal read is ambiguous — say so. Those are the
observations that sharpen the framework.

---

## Reference files

| File | Read it when |
|---|---|
| `references/cb-construction.md` | Step 1–2 / 4 — the `ui_evaluate` extraction, ladder math, and how price moves through the tool |
| `references/fractal-mtf.md` | Step 5–6 — the fractal nesting, the 2m→4h escalation, OB reversal zones, the trading process |
| `references/output-template.md` | Step 7 — the CB snapshot file template + frontmatter |
| `scripts/cb_trace.py` | Step 4 — ladder computation + first-touch trace (always use it) |

---

## See also (Cortana vault)

- `research/topics/crystal-ball-cb-tool.md` — the methodology page + numbered sample library (the evidence base)
- `research/topics/cisd.md` — the CISD breakout the 0.618 anchors to
- `research/topics/2m-kspan-model.md` — bang's intraday K-boundary model (separate; also CISD-based)
- The `nq-snapshot` skill — the live-tape 9-vector counterpart to this skill
