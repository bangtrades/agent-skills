# Data Fidelity Notes — Known MCP Quirks and Workarounds

What works reliably, what doesn't, and how to compensate.

> Source authority: `~/Cortana/cortana-vault/projects/nq-trading/tv-data/data-fidelity-reference.md`

## Hard Limits

### `data_get_ohlcv` — 500-bar cap per call

| Timeframe | 500-bar coverage |
|---|---|
| 1m | ~8.3 hours |
| 2m | ~16.7 hours |
| 5m | ~41.7 hours (~5 trading days) |
| 15m | ~5.2 days |
| 1h | ~31.7 days (~1 month) |
| 4h | ~127 days |
| Daily | ~22 months |

For snapshots, count=100-200 is usually plenty. For morning reviews anchored at the prior 18:00 ET Globex open (12-15 hours ago), use count=200 on the 5m.

### `capture_screenshot` regions

| Region | Behavior |
|---|---|
| `region="full"` | ✓ Reliable. Use this. |
| `region="chart"` | ✗ Errors in multi-pane layouts ("Cannot take screenshot with 0 width"). |
| `region="strategy_tester"` | Untested. |

**Default to `region="full"` always.**

## Critical Quirks

### `data_get_study_values` — cursor-position dependency

**Symptom:** Indicator values returned correspond to wherever the user's cursor is hovering on the chart in TradingView, NOT necessarily the latest bar.

**Example failure:** On the 1h pane, BT MA Bands returned Upper 26,943 / Lower 26,565 — values that map to mid-April 2026 price levels — when current price was near 29,324.

**Detection:** If the BT MA Bands Upper/Lower values are nowhere near current price (>3 ATRs away), suspect this artifact.

**Workarounds (in order of preference):**

1. **Compute manually from OHLCV.** Most BT MA Bands settings are documented (anchor = 20 EMA, K-span = 2 × 14-period ATR). Pull 50-100 bars and compute. The script `scripts/compute_levels.py` does this.

2. **Ask the user to click on the latest bar** in TradingView before re-running the value pull. The cursor position determines what the data window shows.

3. **Read values from the screenshot.** The chart shows the current K band visually. Use vision to estimate.

4. **Use BT VWAP and BT Volatility Envelope as cross-checks.** These are computed independently and seem less prone to the cursor artifact in practice.

### `data_get_ohlcv` — reads from displayed chart, not focused pane

In a multi-pane layout, `data_get_ohlcv` always reads from whichever chart is currently RENDERED (often pane 0 by default, or whichever was last interacted with). It does NOT use the pane focused via `pane_focus`.

**Workaround:** Use `chart_set_timeframe` to cycle the DISPLAYED chart's TF, not `pane_focus`. The displayed chart is what data tools read from.

After all three TF pulls, set the displayed chart back to the user's original TF.

### `chart_get_visible_range` — not implemented

**Symptom:** Returns `{"success": false, "error": "evaluate is not defined"}`.

**Workaround:** Use `data_get_ohlcv` and read `period.from` and `period.to` as a proxy for visible range.

## Soft Quirks

### Indicators with no `plot()` output don't surface via `data_get_study_values`

Surfaced: BT MA Bands, BT VWAP, BT Volatility Envelope, BT Volatility Envelope + Delta, Volume, BT Ligma, EMA, VWAP.

Not surfaced (uses `table.new()`, `label.new()`, `line.new()`, or `box.new()`): Key Levels Suite (Leviathan), Fair Value Gap (LuxAlgo), Gann Fan, BT Session VP Heat, BT OI Strikes, BT Smart CVD (visually), BT CVD Divergence (visually).

**Workarounds:**
- Try `data_get_pine_tables` / `_labels` / `_lines` / `_boxes` for structural overlays (less tested).
- Read from the screenshot for visual indicators.
- Manually note level values the user has set if they're discoverable.

### Some indicators take a few seconds to compute after timeframe switch

If `data_get_study_values` returns empty or partial data immediately after `chart_set_timeframe`, wait 1-2 seconds and retry.

## Reliability Tier List

| Tool | Reliability | Notes |
|---|---|---|
| `tv_health_check` | A | Use as gating check at start |
| `pane_list` | A | Always returns current layout state |
| `chart_set_timeframe` | A | Reliable across all standard TFs |
| `data_get_ohlcv` | A | Returns full bar fidelity up to 500 |
| `capture_screenshot region=full` | A | Reliable |
| `quote_get` | A | Live quote, always current |
| `chart_get_state` | B | Active pane only |
| `pane_focus` | B | Works but may not always sync with what `chart_get_state` returns |
| `data_get_study_values` | C | Cursor-position artifact; needs sanity check |
| `capture_screenshot region=chart` | D | Errors in multi-pane |
| `chart_get_visible_range` | F | Not implemented |
| `data_get_pine_tables/labels/lines/boxes` | ? | Untested |

## Recommended Defaults Per Use Case

| Use case | Tool + params |
|---|---|
| Quick price check | `quote_get` |
| Indicator state on displayed chart | `data_get_study_values` + cursor-artifact sanity check |
| OHLCV summary for current state | `data_get_ohlcv count=100 summary=true` |
| OHLCV full bars | `data_get_ohlcv count=200 summary=false` (or up to 500) |
| Full chart screenshot | `capture_screenshot region=full` |
| MTF cycle (snapshot skill) | `chart_set_timeframe` 5→15→60→restore |
| 9-vector classifier | Cycle TFs + `data_get_study_values` per TF + manual visual check from screenshot |

## When Data Looks Wrong — Diagnostic Checklist

1. **Did `chart_set_timeframe` actually take effect?** Call `pane_list` to verify the active pane's resolution matches what you set.
2. **Is the cursor on the latest bar?** Cursor-position artifact suspect.
3. **Did you wait for indicator computation?** Brief delay after TF switch.
4. **Is the user's chart on a different symbol than expected?** `pane_list` shows symbol per pane.
5. **Is TV Desktop responding at all?** `tv_health_check` should still pass.

If multiple anomalies appear at once, the safest move is to capture the screenshot and rely on visual reading until the data layer recovers.

## What to Tell the User When Data Is Compromised

Flag the data quality issue explicitly in the snapshot:

```markdown
> [!warning] Data fidelity note
> [Indicator/tool] returned [observed value] which appears to be a [cursor-position artifact / cache lag / etc.]. Visual read from the screenshot is recommended for confirmation. The bias verdict below relies on cross-confirmed indicators only.
```

Never silently use values you suspect are wrong. The user needs to know what was trustworthy vs what was inferred.
