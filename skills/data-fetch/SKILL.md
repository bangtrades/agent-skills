---
name: data-fetch
description: Use when retrieving and validating market observations or historical datasets for research and backtests; specify source, instrument, time window, and adjustment policy.
required: false
version: 0.1.1
---

# Market data retrieval contract

Capture provider, instrument and contract ID, venue, timezone, interval, date range, and requested fields before fetching. Distinguish spot, futures contracts, continuous series, and adjusted equities.

1. Inspect the provider available in this runtime; use its documented pagination, limits, and retry behavior.
2. Preserve raw observations in an authorized new destination and produce a separate normalized dataset. Never modify Cortana’s immutable archive.
3. Record observation and retrieval timestamps, timezone/session calendar, currency, price units, corporate-action adjustments, and futures roll policy. Preserve economic-data vintages when relevant.
4. Validate ordering, duplicate timestamps, missing sessions/bars, OHLC consistency, volume units, and implausible prices. Do not silently fill gaps or mix adjusted and unadjusted data.
5. Return dataset location, source/query, schema, coverage, gap report, transformation log, and content hash. Distinguish unavailable fields from zeros.

Feed `markets-research` and `backtest-run`. Use `stock-market-pro` only when its data source and capabilities fit; credentials remain in the runtime, not notes or output.

## Runtime and maintenance

Read the current project hub and applicable local instructions. Discover available tools and verify their input schema; skill names do not prove an API exists. Record what was executed, what was checked, and what remains unverified. Stage skill improvements in Cortana’s inbox; never rewrite the installed registry.
