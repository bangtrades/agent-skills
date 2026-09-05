---
name: backtest-run
description: Use when executing a reproducible strategy backtest or reviewing its outputs. Pair with backtest-expert for research validity and nq-eob for historical replay markup capture.
required: false
version: 0.1.1
---

# Backtest execution and handoff

Obtain strategy rules, instrument/session, sample window, data source, execution model, costs, risk constraints, and intended comparison. Read `backtest-expert` for methodology instead of duplicating it here.

1. Validate data through `data-fetch`; freeze data hash, code revision, parameters, seed, dependency versions, and test windows.
2. Separate training, validation, and untouched test data. Account for lookahead, leakage, survivor bias, selection effects, and the number of parameter/strategy trials.
3. Run the existing project engine. Model fees, slippage, fills, overnight/session boundaries, and realistic sizing. Do not claim an engine or helper exists until verified.
4. Save config, trade ledger, equity series, metrics with definitions, and execution logs. Compare baseline, held-out performance, sensitivity, uncertainty, and regime dependence.
5. Use `pso-optimizer` only within the training/validation process. Route marked TradingView replay capture to `nq-eob`; it has a distinct model-ID and manual-field preservation contract.
6. Return a qualified research assessment to `strategy-report`, with unresolved implementation and data limits. A research result does not authorize live trading.

## Runtime and maintenance

Read the current project hub and applicable local instructions. Discover available tools and verify their input schema; skill names do not prove an API exists. Record what was executed, what was checked, and what remains unverified. Stage skill improvements in Cortana’s inbox; never rewrite the installed registry.
