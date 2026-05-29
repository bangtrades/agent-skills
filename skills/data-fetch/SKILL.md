---
name: data-fetch
description: Use when retrieving market data — OHLCV bars, quotes, fundamentals, or on-chain data from an exchange or data provider. Trigger on "fetch price data", "pull OHLCV", "get historical bars", "download market data", or when another skill needs clean data as input.
required: false
version: 0.1.0
---

# Data Fetch

> **Stub skill.** The owning agent fills in `scripts/` and expands the workflow
> as it masters the skill. The frontmatter above is the Paperclip-discoverable
> manifest.

Retrieve and normalize market data for downstream skills.

## When to use this skill

- Pulling OHLCV bars, quotes, or fundamentals for a symbol.
- Fetching historical data for a backtest window.
- Providing clean, normalized data to `markets-research` / `backtest-run`.

## Usage

1. **Specify** — symbol(s), interval, date range, and source.
2. **Fetch** — call the provider; handle pagination, rate limits, and retries.
3. **Normalize** — consistent schema (timestamp, OHLCV), UTC timestamps, gap
   handling documented.
4. **Validate** — check for missing bars, duplicates, and obvious bad ticks
   before handing data on.

> **Secrets:** API keys for data providers are supplied at runtime via the
> agent's environment / capability markers — never commit credentials to this
> registry.

## Scripts

`scripts/` is a placeholder. Intended helpers (filled in later): provider
clients, OHLCV normalizer, data-quality checks.

## Mastery notes

This agent's accumulated preferences live in its vault at
`skill-mastery/data-fetch.md` (STEP-49 §2.1), not in this file.
