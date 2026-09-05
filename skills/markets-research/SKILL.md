---
name: markets-research
description: Use when building a sourced market, sector, macro, or trading-signal brief. Use bt-equity for a full single-company investment dossier and nq-snapshot for live NQ chart analysis.
required: false
version: 0.1.1
---

# Markets research

Frame the instrument, horizon, as-of time, question, and decision. Retrieve existing relevant evidence before expanding research.

1. Request data through `data-fetch` or an available provider. Record source, retrieval time, observation time, units, and limitations.
2. Use current primary evidence for prices, economic releases, filings, calendars, and company statements. Keep facts, estimates, inference, and scenarios distinct.
3. Build bull and bear cases, catalysts, disconfirming evidence, and explicit unknowns. Do not substitute sentiment for verified financial data.
4. Route a company dossier to `bt-equity`, live NQ chart work to `nq-snapshot`, historical edge checks to `pre-trade-intel`, and sizing to `risk-rules`.
5. Return the thesis, evidence table, invalidation conditions, horizon, and unanswered questions. A brief provides decision support, not an order.

Hand off reproducible hypotheses to `backtest-run`. Cite every material factual claim. If a feed is unavailable, qualify the answer rather than inventing observations.

## Runtime and maintenance

Read the current project hub and applicable local instructions. Discover available tools and verify their input schema; skill names do not prove an API exists. Record what was executed, what was checked, and what remains unverified. Stage skill improvements in Cortana’s inbox; never rewrite the installed registry.
