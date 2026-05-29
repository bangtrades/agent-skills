---
name: indicator-build
description: Use when building, porting, or debugging a trading indicator or charting study — Pine Script (TradingView), or indicator logic in Python/JS. Trigger on "build an indicator", "write a Pine Script", "port this study", "add an alert condition", or "debug my indicator".
required: false
version: 0.1.0
---

# Indicator Build

> **Stub skill.** The owning agent fills in `scripts/` and expands the workflow
> as it masters the skill. The frontmatter above is the Paperclip-discoverable
> manifest.

Build and validate trading indicators / charting studies.

## When to use this skill

- Authoring a new Pine Script indicator or strategy study.
- Porting an indicator between Pine Script, Python, and JS.
- Adding or debugging alert conditions and plot logic.

## Usage

1. **Specify** — the indicator's inputs, outputs (plots/signals), and timeframe
   behavior. Note repainting risk explicitly.
2. **Implement** — write the study; keep parameters as inputs, not hardcoded.
3. **Validate** — confirm no lookahead/repainting, check edge cases (gaps, low
   volume, session boundaries).
4. **Hand off** — a signal-emitting indicator should produce series the
   `backtest-run` skill can consume.

## Scripts

`scripts/` is a placeholder. Intended helpers (filled in later): Pine templates,
repaint checks, indicator-to-signal exporters.

## Mastery notes

This agent's accumulated preferences live in its vault at
`skill-mastery/indicator-build.md` (STEP-49 §2.1), not in this file.
