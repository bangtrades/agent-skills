---
name: risk-rules
description: Use when sizing a position, checking risk before a trade, or enforcing drawdown / exposure limits — position sizing, stop placement, portfolio risk checks, and kill-switch logic. Trigger on "size this position", "what's my risk", "check drawdown", "enforce risk limits", or pre-trade risk gating.
required: false
version: 0.1.0
---

# Risk Rules

> **Stub skill.** The owning agent fills in `scripts/` and expands the workflow
> as it masters the skill. The frontmatter above is the Paperclip-discoverable
> manifest. This skill complements — does not replace — the platform-enforced
> trading capability ladder (CO-1); registry skills advise, capability markers
> enforce.

Position sizing, drawdown control, and pre-trade risk checks.

## When to use this skill

- Sizing a position from account risk and stop distance.
- Checking a proposed trade against exposure and drawdown limits.
- Defining or applying kill-switch / cooldown rules.

## Usage

1. **Inputs** — account equity, per-trade risk %, entry, stop, and current open
   exposure.
2. **Size** — compute position size so loss-at-stop equals the risk budget.
   Never size from upside.
3. **Check limits** — per-position, per-instrument, and portfolio drawdown
   caps. Refuse trades that breach them.
4. **Escalate** — when a kill-switch or cooldown condition triggers, surface it;
   the platform capability ladder (CO-1) is the hard enforcement layer.

## Scripts

`scripts/` is a placeholder. Intended helpers (filled in later): position-size
calculator, drawdown monitor, limit checker.

## Mastery notes

This agent's accumulated preferences live in its vault at
`skill-mastery/risk-rules.md` (STEP-49 §2.1), not in this file.
