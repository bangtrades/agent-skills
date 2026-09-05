---
name: risk-rules
description: Use when calculating a proposed position’s risk or checking it against supplied account and exposure limits. Requires explicit current limits and instrument specifications; does not place trades.
required: false
version: 0.1.1
---

# Position risk contract

Obtain account currency/equity, approved per-trade and portfolio limits, current exposure/drawdown, entry, stop, contract multiplier or point value, lot step, and fee/slippage assumptions. Retrieve current contract specifications and account rules from authoritative sources. Leave unknown inputs unknown; do not invent risk percentages.

1. Compute loss per unit from absolute entry-stop distance times point value, plus modeled fees/slippage. Convert currencies where needed using a dated rate.
2. Compute the permitted risk budget from supplied policy and remaining limits. Divide by loss per unit and round down to the allowed lot step. Reject zero/negative distance or missing specifications.
3. Recompute total modeled loss after rounding; compare aggregate, correlated, instrument, session, daily-loss, and drawdown exposure against actual policy.
4. Explain sensitivity to gaps, liquidity, and stop execution. Loss-at-stop is a model, not a guaranteed maximum loss.
5. Return inputs with source dates, formula, intermediate values, rounded size, limit checks, and missing inputs. Treat this as advisory evidence for an authorized decision.

Use `pre-trade-intel` for historical context. Capability controls and order permissions belong to the actual platform; this skill cannot enforce a kill switch or authorize execution.

## Runtime and maintenance

Read the current project hub and applicable local instructions. Discover available tools and verify their input schema; skill names do not prove an API exists. Record what was executed, what was checked, and what remains unverified. Stage skill improvements in Cortana’s inbox; never rewrite the installed registry.
