---
name: markets-research
description: Use when researching a market, ticker, sector, or trading signal — gathering news, sentiment, macro context, on-chain/order-flow signals, and synthesizing a research brief. Trigger on "research this market", "what's the signal on X", "analyze sentiment for", "build a thesis on", or pre-trade context gathering.
required: false
version: 0.1.0
---

# Markets Research

> **Stub skill.** The owning agent (Market Analyst) fills in `scripts/` and
> expands the workflow as it masters the skill. The frontmatter above is the
> Paperclip-discoverable manifest.

Research a market or signal end-to-end and produce a decision-ready brief.

## When to use this skill

- Building a thesis on a ticker, pair, or sector before a trade.
- Synthesizing news, sentiment, and macro context into one brief.
- Evaluating a candidate signal (technical, on-chain, or order-flow).

## Usage

1. **Frame the question** — instrument, timeframe, and the decision the research
   feeds (entry, sizing, hold/exit).
2. **Gather** — news, sentiment, macro calendar, and any signal feeds available
   via the `data-fetch` skill. Cite every source.
3. **Synthesize** — bull case, bear case, key levels, catalysts, and the
   confidence level. Separate fact from inference.
4. **Hand off** — output a brief that `risk-rules` and `backtest-run` can consume
   (proposed direction, invalidation level, time horizon).

## Scripts

`scripts/` is a placeholder. Intended helpers (filled in later): signal-feed
pullers, sentiment aggregation, brief templating.

## Mastery notes

This agent's accumulated preferences for this skill live in its vault at
`skill-mastery/markets-research.md` (STEP-49 §2.1), not in this file.
