---
name: pine-develop
description: Use when a task explicitly needs a live TradingView Pine editor edit, compile, and chart-verification loop. Pair with pine-script; discover actual available editor tools first.
version: 0.2.0
---

# Live Pine development adapter

Read `pine-script` for language rules. Identify the target chart and script, preserve its current source, and keep a local reviewable change.

1. Discover editor read/write/compile and chart-inspection tools exposed by this runtime. Read their schemas. The registry does not ship `pine_pull.js` or `pine_push.js`; never invoke invented helpers.
2. Read the current script and implement the requested change using the project’s version and formatting conventions.
3. When live editing is authorized, write to the verified target and compile. Capture compiler errors and iterate until resolved or a concrete tool limitation is established.
4. Verify plots, inputs, alerts, timeframe behavior, and strategy results as applicable. Record the source revision and evidence of the chart examined.
5. Return source and compile/chart status separately. If editor tools are unavailable, deliver the source and explicitly mark live compilation unverified.

Do not publish a script, alter an unrelated chart, or place orders as a side effect of development.

## Runtime and maintenance

Read the current project hub and applicable local instructions. Discover available tools and verify their input schema; skill names do not prove an API exists. Record what was executed, what was checked, and what remains unverified. Stage skill improvements in Cortana’s inbox; never rewrite the installed registry.
