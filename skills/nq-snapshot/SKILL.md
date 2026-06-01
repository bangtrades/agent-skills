---
name: nq-snapshot
description: Capture an MTF deep-analysis snapshot of MNQ/NQ futures from live TradingView via the tradingview MCP, applying bang's framework — 9-vector NY Session check, Day-Type Classifier, T1/T2 trend-pullback + R1/R2/R3 range-day setups, R1–R6 discipline rules, BT indicator stack — and write a snapshot file into the Cortana chart library with bidirectional tagging. Use aggressively for "nq snapshot", "snap", "snap mtf", "morning review", "deep analysis", or any prompt implying live MNQ/NQ context. Also trigger on setup scouting, post-stop forensics, regime checks, EOD wraps, and mentions of Keltner channels, K-bands, VWAP, EMA stack, CVD divergence, BT Aggression, IFVG, MA Bands, or Volatility Envelope. Cycles 5m/15m/1h via chart_set_timeframe, pulls study values + OHLCV + screenshots, runs 9-vector synthesis, identifies live/imminent setups, runs R3/R5/R1 checks, and tags frontmatter so snapshots auto-surface in library queries. Do NOT trigger for non-MNQ/NQ instruments or backtesting.
---

# NQ Snapshot — MTF Deep-Analysis Capture Skill

> Captures bang's full intraday MTF read from the live TradingView chart and produces a Cortana-vault-routed snapshot file with chart-library tagging. The skill is the executable version of [the BT Morning Review Process](file:///Users/nolan/Cortana/cortana-vault/projects/nq-trading/tv-data/routines/bt-morning-review.md).

## When To Run This

| Situation | Use this skill |
|---|---|
| User says "snap", "snapshot", "snap mtf" | ✓ |
| User says "morning review" or "deep analysis" | ✓ |
| User asks "where is price" / "what's the tape doing" | ✓ |
| User wants to scout a setup zone before entering | ✓ |
| User just hit a stop and wants forensic context | ✓ |
| User mentions any of: Keltner / K-band / VWAP / EMA stack / CVD divergence / BT Aggression / BT Deep Trades / IFVG / FVG / volatility envelope | ✓ |
| User asks about non-MNQ/NQ instruments (ES, equities, crypto) | ✗ — different framework |
| User asks for a pure backtest or historical analysis | ✗ — different skill |
| User wants conceptual discussion only, no live read | ✗ |

## High-Level Workflow

The skill executes a 7-step capture-and-synthesize routine:

1. **Verify TV MCP connection** — `tv_health_check`. If down, instruct user to launch `TV Debug.app`.
2. **Cycle the displayed chart** through 5m → 15m → 1h using `chart_set_timeframe`.
3. **Per timeframe**, capture: `data_get_study_values`, `data_get_ohlcv count=100-200 summary=true`, `capture_screenshot region=full`.
4. **Apply the 9-vector framework** to synthesize per-TF reads.
5. **Output bias hypothesis** + archetype verdict + live/imminent setups.
6. **Run R3/R5/R1 sanity checks** against current state.
7. **Write the snapshot file** with chart-library frontmatter tagging.

Detailed step-by-step protocol with exact MCP tool calls: see [references/workflow.md](references/workflow.md).

## Reference Files (Progressive Disclosure)

Load these as needed:

| File | When to read |
|---|---|
| [`references/workflow.md`](references/workflow.md) | Always — the exact 7-step protocol with MCP tool calls |
| [`references/nine-vector-framework.md`](references/nine-vector-framework.md) | When synthesizing the per-TF reads into a bias verdict |
| [`references/setup-taxonomy.md`](references/setup-taxonomy.md) | When identifying live or imminent setups (T1, T2, R1, R2, R3) |
| [`references/archetype-rubric.md`](references/archetype-rubric.md) | When classifying the day type (1, 2, 3, 4, unclear) |
| [`references/discipline-checks.md`](references/discipline-checks.md) | When running R3/R5/R1 pre-trade sanity checks |
| [`references/concept-tagging.md`](references/concept-tagging.md) | When populating `demonstrates_concept/strategy/setup` frontmatter |
| [`references/data-fidelity-notes.md`](references/data-fidelity-notes.md) | When `data_get_study_values` returns stale values or screenshot region errors |
| [`references/output-template.md`](references/output-template.md) | When writing the final snapshot file |

For the chart-library frontmatter contract specifically and the full list of tag values, read [`references/concept-tagging.md`](references/concept-tagging.md).

## Output Routing

Snapshot files land at:
```
/Users/nolan/Cortana/cortana-vault/projects/nq-trading/journal/snapshots/YYYY-MM-DD/HHMM-<context>.md
```

Screenshots route to:
```
/Users/nolan/Cortana/cortana-vault/raw/assets/journal/YYYY-MM-DD/<context>-<tf>.png
```

The `<context>` slug encodes the trigger type — common values:

| User intent | Filename context |
|---|---|
| Generic baseline / "snap mtf" | `baseline` |
| Morning review | `morning-review` |
| Pre-trade context | `pre-r1` / `pre-r2` / `pre-r3` / `pre-t1` / `pre-t2` |
| Post-stop forensic | `post-stop` |
| Regime check | `classifier` / `regime-shift` |
| End of day | `eod` |
| Setup-zone scouting | `setup-scout` |

## Trigger Phrase Quick Reference

The skill accepts modifier-style trigger phrases. Parse the user's input for these:

| Phrase | Behavior |
|---|---|
| `snapshot` (alone) | Default capture — currently-focused pane or active TF, no MTF cycle |
| `snap mtf` | Full 5m/15m/1h MTF capture |
| `snap 5m` / `snap 15m` / `snap 1h` | Single-TF capture on the named TF |
| `morning review` | Full MTF capture anchored at the prior 18:00 ET Globex open, formatted as `morning-reviews/YYYY-MM-DD.md` |
| `snap classifier` | Lighter capture — 9-vector check only, no full screenshot dump |
| `snap levels` | Focus on extracting key levels (VWAP, IB, VAH/VAL/POC) |
| `snap pre-<setup>` | Pre-trade context capture, tagged with setup name |
| `snap eod` | End-of-day session wrap |

## Critical Conventions

**Bidirectional tagging is non-negotiable.** Every snapshot's frontmatter MUST include:

```yaml
archetype: "1" | "2" | "3" | "4" | "unclear"
demonstrates_concept: [...]     # see references/concept-tagging.md
demonstrates_strategy: [...]
demonstrates_setup: [...]
outcome: "in-progress" | "win" | "loss" | "scratch" | "didnt-trigger" | "calibration-only"
key_observation: "Single sentence summarizing the tape state."
```

Without these, the snapshot won't auto-surface in chart-library Dataview queries — and the whole bidirectional linking system breaks.

**R5 time-of-day check is mandatory output.** Every snapshot ends with an explicit R3/R5/R1 verdict on whether trading is sanctioned right now or whether the user should stand aside. The verdict is just as important as the bias hypothesis.

**Honor the cursor-position artifact.** `data_get_study_values` returns values at the user's chart cursor position, NOT necessarily the latest bar. When the BT MA Bands values look stale (e.g., K Upper/Lower nowhere near current price), flag this and compute manually from OHLCV. See [`references/data-fidelity-notes.md`](references/data-fidelity-notes.md).

**The OHLCV pull reads from the displayed chart**, not the focused pane. To get OHLCV per timeframe, use `chart_set_timeframe` to cycle the displayed chart's TF rather than `pane_focus`. Restore to user's original TF when done.

## Helper Script

For arithmetic-heavy operations (channel position %, distance from key levels, R-multiple stop math), use the bundled Python helper:

```bash
python3 /Users/nolan/Projects/Trading/skills/nq-snapshot/scripts/compute_levels.py
```

It reads JSON from stdin and emits computed levels + distances + R-multiples. See the script's header for input/output schema. This keeps Claude's inline arithmetic clean and avoids drift.

## Output Quality Bar

A good snapshot:

1. **Identifies one of the four archetypes** with explicit confidence (Strong / Moderate / Weak)
2. **Names live or imminent setups** by ID (T1, T2, R1, R2, R3) with concrete trigger zones and stop/target levels
3. **Closes with R3/R5/R1 verdict** — sanctioned to trade, stand aside, or reduced-size exception
4. **Cross-links** to the playbook page, archetype library page, and any specific setup library page
5. **Tags frontmatter** so the snapshot auto-flows into the chart library

A snapshot that produces a bias verdict but skips setup-zone identification is incomplete. A snapshot that identifies setups but skips R5 sanity is dangerous.

## See Also (Cortana Vault)

- BT Morning Review Process — the human-facing routine this skill executes
- Trend-Pullback Playbook — Archetype 2/3 SOP (T1, T2 setups)
- Range-Day Playbook — Archetype 1 SOP (R1, R2, R3 setups)
- Discipline Rules — NQ/MNQ — R1-R6 cap definitions
- Day-Type × Session Classifier — the framework this skill applies
- Chart Library Index — where snapshots auto-flow via frontmatter tagging
- MNQ MTF 2x2 Chart Layout — canonical chart configuration
- TV MCP Data Fidelity Reference — known data quirks and workarounds
