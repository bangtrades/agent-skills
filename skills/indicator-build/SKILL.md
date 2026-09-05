---
name: indicator-build
description: Use when specifying or porting a trading indicator across Pine, Python, or JavaScript. Use pine-script for Pine language implementation and pine-develop for a requested live compile loop.
required: false
version: 0.1.1
---

# Indicator specification and portability

Define inputs, outputs, units, warmup behavior, session/timeframe semantics, alert timing, and repaint policy. Reuse `pine-script` for Pine implementation rather than loading a second language guide.

1. Identify the authoritative source and destination. Preserve an editable source snapshot before changes.
2. Implement parameters as inputs and make confirmed-bar versus intrabar behavior explicit.
3. Compare known examples across warmup, gaps, session boundaries, missing volume, and timeframe changes. Verify lookahead and repaint behavior with evidence.
4. Use `pine-develop` only when a live TradingView edit/compile is requested and the runtime exposes the required tools.
5. Return source, input/output contract, checked examples, compile status, and any unverified chart behavior. Feed signal series to `backtest-run` when requested.

This small contract is a future merge candidate into indicator-development references; retain it until cross-language callers are migrated.

## Runtime and maintenance

Read the current project hub and applicable local instructions. Discover available tools and verify their input schema; skill names do not prove an API exists. Record what was executed, what was checked, and what remains unverified. Stage skill improvements in Cortana’s inbox; never rewrite the installed registry.
