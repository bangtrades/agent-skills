# Workflow — Step-by-Step Capture Protocol

The exact MCP tool calls and decision logic for executing an nq-snapshot. Follow these in order.

## Step 0 — Parse the trigger phrase

Identify the user's intent from the trigger phrase. This determines the `context` slug used in the output filename and the scope of capture:

| Trigger phrase pattern | Context slug | Scope |
|---|---|---|
| "snap mtf" / "snapshot mtf" | `baseline` | Full 5m/15m/1h cycle |
| "morning review" / "morning analysis" | `morning-review` | Full MTF + output goes to `morning-reviews/YYYY-MM-DD.md` instead of `snapshots/` |
| "snap pre-r1" / "pre-t1" etc | `pre-<setup>` | Full MTF, pre-trade focus |
| "snap classifier" | `classifier` | Lighter — values only, no screenshot |
| "snap levels" | `levels` | Focus on extracting key levels |
| "snap post-stop" | `post-stop` | Full MTF, post-trade forensic |
| "snap eod" | `eod` | Full MTF, EOD wrap |
| "snap" / "snapshot" (alone) | `baseline` | Default — depends on what's displayed; if grid layout cycle MTF, if single-pane just current TF |
| "snap 5m" / "snap 15m" / "snap 1h" | `<tf>-focus` | Single-TF only |

## Step 1 — Verify TV MCP connection

```
mcp__tradingview__tv_health_check
```

**If `success: false`:** stop and tell the user:
> "TradingView Desktop isn't running with the debug port. Launch **TV Debug.app** from your Desktop, wait for "DEBUG PORT IS LIVE", then say ready."

Do NOT attempt to run `tv_launch` automatically — the user may have unsaved chart state.

**If `success: true`:** continue.

## Step 2 — Capture the layout context

```
mcp__tradingview__pane_list
```

Record:
- `chart_count` (1 = single chart, 4 = 2x2 grid)
- Active pane's `resolution` (the user's current TF)
- All pane resolutions (for later restoration)

This is the "before" state. Restore to it at end.

## Step 3 — Cycle the chart through 5m / 15m / 1h

**Important mechanic:** `data_get_ohlcv` reads from the currently-displayed chart, NOT the focused pane in a grid layout. So use `chart_set_timeframe` to cycle the chart's TF, not `pane_focus`.

For each TF in sequence (5m → 15m → 1h):

```
mcp__tradingview__chart_set_timeframe timeframe="5"   # or "15", "60"

mcp__tradingview__data_get_study_values
  # Returns BT MA Bands, BT Volatility Envelope, BT VWAP, BT Volatility Envelope + Delta (with order flow)

mcp__tradingview__data_get_ohlcv count=100 summary=true
  # Or count=200 for 5m to span Globex open in morning review

mcp__tradingview__capture_screenshot region="full" filename="<context>-<tf>-YYYY-MM-DD"
  # NOT region="chart" — that errors in multi-pane mode
```

After all three TFs: `chart_set_timeframe` back to the user's original TF (from Step 2).

## Step 4 — Save screenshots to vault

The TV MCP saves screenshots to `~/Projects/Trading/tradingview-mcp/screenshots/<filename>.png`. Copy them to the vault asset path:

```bash
cp ~/Projects/Trading/tradingview-mcp/screenshots/<filename>.png \
   ~/Cortana/cortana-vault/raw/assets/journal/YYYY-MM-DD/<context>-<tf>.png
```

Use `mkdir -p` first to ensure the date folder exists.

## Step 5 — Per-TF synthesis

For each TF's data, extract and record:

**Quote / session window:**
- Current price (last close from OHLCV)
- Window OHLC + range + % change over the window
- Average volume
- Latest bar OHLC + volume

**Key levels** (from `data_get_study_values`):
- BT VWAP value + distance from current price
- BT MA Bands: Upper, Lower, Anchor + distances
- BT Volatility Envelope (tight): Top / Bottom + distances
- BT Volatility Envelope (wide): Top Min / Top Max / Bottom Min / Bottom Max + distances

**Channel position** (compute):
```
position = (last - lower_band) / (upper_band - lower_band)
```
Express as percent. <0 = below channel, >100 = above channel.

**Order flow** (from BT Volatility Envelope + Delta on the latest bar):
- delta + delta_pct
- buy_vol / sell_vol ratio
- CVD (cumulative)
- flip_threshold + flip_signal (0 or 1)

**Per-vector tag** for the 9-vector synthesis (see [nine-vector-framework.md](nine-vector-framework.md)):
- bullish / bearish / neutral / unclear per vector

## Step 6 — Apply the 9-Vector Framework

See [nine-vector-framework.md](nine-vector-framework.md) for the full reading guide.

Score each of the 9 vectors across all 3 TFs. Total bullish vs bearish vectors determines bias verdict:

- 7-9 vectors agreeing on one side → **STRONG** confidence
- 5-6 vectors agreeing → **MODERATE** confidence
- 3-4 vectors agreeing → **WEAK** confidence
- ≤2 vectors agreeing on either side → **UNCLEAR** — stand aside

## Step 7 — Classify the archetype

See [archetype-rubric.md](archetype-rubric.md) for the diagnostic patterns.

Output one of:
- Archetype 1 — Range / Rebalancing
- Archetype 2 — Rebalance → Trend Acceptance
- Archetype 3 — Trend Acceptance → Cascade
- Archetype 4 — False Break / Exhaustion Reversal
- Unclear

## Step 8 — Identify live or imminent setups

See [setup-taxonomy.md](setup-taxonomy.md) for trigger criteria per setup.

For each candidate setup (T1, T2, R1, R2, R3, plus their inverses):
- Determine whether it's LIVE (triggering right now), IMMINENT (within reach), or NOT APPLICABLE
- For LIVE/IMMINENT setups: write the trigger zone, stop, T1, T2 targets in concrete points

A snapshot is incomplete without explicit setup zones — even if no setup is currently live, the answer "no live setup, watching X level for Y" is the valid output.

## Step 9 — R3 / R5 / R1 sanity check

See [discipline-checks.md](discipline-checks.md) for the current rule values.

Explicitly state:
- **R5**: is the current time in a sanctioned trade window? If not, snapshot ends with "STAND ASIDE — R5".
- **R3**: what's the daily-loss cap today? (Default $200.) If user is approaching it, flag.
- **R1**: what's the max position size? ($4/pt = 2 micros default.)

## Step 10 — Write the snapshot file

See [output-template.md](output-template.md) for the full template.

File path:
- Standard snapshot: `~/Cortana/cortana-vault/projects/nq-trading/journal/snapshots/YYYY-MM-DD/HHMM-<context>.md`
- Morning review: `~/Cortana/cortana-vault/projects/nq-trading/journal/morning-reviews/YYYY-MM-DD.md`

Use `mkdir -p` to create date folders as needed.

## Step 11 — Tag the frontmatter

See [concept-tagging.md](concept-tagging.md) for the full taxonomy.

The frontmatter MUST include:
```yaml
archetype: "1" | "2" | "3" | "4" | "unclear"
demonstrates_concept: [...]
demonstrates_strategy: [...]
demonstrates_setup: [...]
outcome: "in-progress" | "win" | "loss" | "scratch" | "didnt-trigger" | "calibration-only"
key_observation: "Single sentence."
```

For most live snapshots, `outcome: "in-progress"` or `"calibration-only"` is appropriate. Use `"win"` / `"loss"` only after the linked trade resolves.

## Step 12 — Cross-link

The snapshot's `related:` frontmatter list should include:
- The active playbook page ([Trend-Pullback Playbook] or [Range-Day Playbook])
- Each demonstrated concept's chart-library page
- Each demonstrated setup's chart-library page
- The matching archetype's library page
- Today's daily log if it exists
- The prior snapshot if one exists for the day

## Step 13 — Append to log.md and report

Append a log entry to `~/Cortana/cortana-vault/log.md` with type `snapshot`, source `nq-snapshot skill`, pages-touched list, and key-observation.

Then report to the user in chat:
1. The snapshot file path (as a computer:// or obsidian-launcher link)
2. The 1-sentence bias verdict
3. Live setup status (or stand-aside reason)
4. The single most important next action (wait for X, watch Y, etc.)

Keep the in-chat output tight. The full analysis is in the file.

## Restoration

Before exiting:
```
mcp__tradingview__chart_set_timeframe timeframe="<original-tf-from-step-2>"
```

If the user's original layout was a grid and you used `pane_focus` anywhere, restore the original active_index too.

## Failure Modes

| Symptom | Likely cause | Workaround |
|---|---|---|
| `tv_health_check` fails | TV not in debug mode | Tell user to launch TV Debug.app |
| `data_get_study_values` returns values far from current price | Cursor-position artifact | Compute K channel manually from OHLCV + indicator parameters |
| `capture_screenshot region="chart"` errors | Multi-pane layout | Use `region="full"` always |
| `chart_get_visible_range` errors | Not implemented | Skip; use OHLCV period.from/to instead |
| `data_get_ohlcv` returns wrong timeframe | Reads from displayed chart, not focused pane | Always `chart_set_timeframe` first |
| OHLCV count limit | 500-bar hard cap | For longer windows, multi-call + stitch |

See [data-fidelity-notes.md](data-fidelity-notes.md) for the full known-issues log.
