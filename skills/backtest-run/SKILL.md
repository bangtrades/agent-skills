---
name: backtest-run
description: Use when running, analyzing, or validating a trading strategy backtest — preparing data, executing a backtest, and reading the results (returns, drawdown, Sharpe, win rate). Trigger on "backtest this strategy", "run a backtest", "analyze these results", "is this overfit", or "walk-forward test".
required: false
version: 0.1.0
---

# Backtest Run

> **Stub skill.** The owning agent (Quant / Backtesting) fills in `scripts/` and
> expands the workflow as it masters the skill. The frontmatter above is the
> Paperclip-discoverable manifest.

Run and critically analyze strategy backtests.

## When to use this skill

- Executing a backtest for a strategy or signal.
- Reading backtest output and judging robustness.
- Guarding against overfitting (walk-forward, out-of-sample splits).

## Usage

1. **Prepare** — clean data (via `data-fetch`), define the strategy rules, set
   the test window, costs, and slippage. Reserve out-of-sample data.
2. **Run** — execute the backtest deterministically; record the exact config.
3. **Analyze** — returns, max drawdown, Sharpe/Sortino, win rate, exposure.
   Compare in-sample vs out-of-sample.
4. **Judge** — flag overfitting and regime dependence. A good-looking curve is
   not a pass. Feed sizing constraints from `risk-rules`.

## Scripts

`scripts/` is a placeholder. Intended helpers (filled in later): backtest
runner, metrics report, walk-forward harness.

## Mastery notes

This agent's accumulated preferences live in its vault at
`skill-mastery/backtest-run.md` (STEP-49 §2.1), not in this file.
