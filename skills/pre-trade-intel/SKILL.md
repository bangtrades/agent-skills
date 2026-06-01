---
name: pre-trade-intel
description: >-
  Query bang's structured trade history before entering a new NQ/MNQ trade and
  return a pre-trade intelligence brief: historical precedent for this setup ×
  archetype × session × mental-state combination, pattern matches against known
  weaknesses, R1–R6 rule check, market-context match, and a verdict (in or out
  of historical edge, what would raise conviction). Trigger BEFORE any new entry
  when the user says "thinking about a long here", "should I take this?", "pre-trade
  check", "intel this", "is this in my edge?", "what's my history with this setup?",
  or describes a contemplated trade without having entered. Reads
  `projects/nq-trading/system/CLAUDE.md` and queries `projects/nq-trading/trades/closed/`
  plus `projects/nq-trading/analysis/patterns/`. Writes a brief to
  `projects/nq-trading/analysis/pre-trade-intel/`. Do NOT use after entry (that's
  the trade-capture skill) and do NOT use for general market commentary (use a
  snapshot skill instead).
---

# pre-trade-intel — Historical edge check before entry

> The highest-ROI feature of the CyrilXBT architecture: query your own history
> before you trade, so you trade with historical wisdom instead of nothing but
> the current moment's information.

---

## Before You Begin

1. **Read** `projects/nq-trading/system/CLAUDE.md` — current edge hypothesis, known weaknesses, performance benchmarks. The brief judges the contemplated trade against this anchor.
2. **Read** `projects/nq-trading/trades/_index.md` for the frontmatter schema (so you know what fields to slice on).
3. **List** `projects/nq-trading/analysis/patterns/` — known patterns the contemplated trade may match.

---

## Inputs

The user gives a description of a **contemplated** (not yet entered) trade. Required fields:

- `direction` (long / short)
- `setup_type` (R1 / R2 / R3 / T1 / T2 / OB-FVG / MM-model / other-discretionary)
- `archetype` (1 / 2 / 3 / 4 / Unclear)
- `session` (asia / london / ny-am / ny-pm / ny-late)
- `mental_state_pre_label` (one of: calm / charged / anxious / revenge / FOMO / steady / numb / focused)
- `market_condition` (range / trend-up / trend-down / false-break / news-vol / other)

Ask for any missing field ONE at a time. Do not stall on `mental_state_pre_label` — the brief is still useful without it; the emotional-correlation section just gets skipped.

Optional but helpful:
- Contemplated `entry_price`, `stop_price`, `target_price` — lets you compute R:R and check R3
- Current day's running P&L — lets you check R3 budget remaining
- Any recent stop-outs in this session — feeds R2 cooldown check

---

## Workflow

### Step 1 — Slice the trade dataset

Find all files in `projects/nq-trading/trades/closed/` whose frontmatter matches on:

- `setup_type` (exact match)
- `archetype` (exact match)
- `direction` (exact match)
- `session` (exact match if N ≥ 10 after exact slice; otherwise relax to "any NY session" then "any session")

This produces the **historical-precedent cohort**.

Useful tool: ripgrep on the closed/ folder, or read all files and filter in Python. For small datasets (<200 trades) reading-and-filtering is faster than indexing.

### Step 2 — Compute precedent statistics

For the precedent cohort:

- N (sample size)
- Win rate ± 95% Wilson CI
- Avg R, expectancy (R)
- Net P&L ($)
- Distribution of `exit_reason` (target / stop / manual / time / regime / discipline)
- Distribution of `execution_quality` grades

If N < 5: state "**insufficient precedent — N=X**" and recommend treating as a low-conviction exploration. Do not compute CI for N<5.

### Step 3 — Pattern match against known patterns

For each pattern file in `projects/nq-trading/analysis/patterns/`:

- Compare its `trigger_conditions:` block against the contemplated trade's fields
- If all conditions match → **PATTERN MATCH**: surface the pattern's `classification` (weakness / strength / neutral), `observed_outcome`, and `recommended_response`

A pattern marked `weakness` with the contemplated trade matching is the loudest signal in the brief.

### Step 4 — R1–R6 rule check

Same logic as the trade-capture skill's rule check (see [[skills/trade-capture/SKILL|trade-capture]]). Surface any rule that would be violated by entering this trade right now.

### Step 5 — Market context match

Read the most recent file in `projects/nq-trading/intelligence/market-conditions/` (if any). Compare today's documented context to the conditions historically associated with winners in the precedent cohort. If today's context is materially different from the historical winners' context, flag it.

If no market-conditions file exists for today, note that this section is data-limited.

### Step 6 — Emotional state consideration

If `mental_state_pre_label` was provided and the precedent cohort has ≥ 20 trades with non-null `mental_state_pre_label`:

- Compute avg R for the precedent cohort broken down by `mental_state_pre_label`
- Is the user's current label in a historically winning bucket or a losing bucket?

If precedent N < 20 with emotional data: skip this section, note "insufficient emotional data yet".

### Step 7 — Verdict

Synthesize into one of:

- **IN EDGE** — precedent strongly positive, no pattern weakness match, all rules OK, market context consistent. State the precedent stats and proceed.
- **MARGINAL** — precedent positive but small N, OR one moderate concern (rule violation, pattern weakness, emotional mismatch). State the trade-off; let the user decide.
- **OUT OF EDGE** — precedent negative OR pattern-weakness match OR rule violation OR multiple yellow flags stacking. Recommend standing down. State what would raise conviction (e.g., "if archetype is reclassified to 2 instead of Unclear, R1 win rate jumps from 38% to 67% — wait for the classifier to confirm").

The verdict is **a recommendation, not a gate.** The user always decides. The brief's job is to make sure the user decides with the historical data in view.

### Step 8 — Write the brief

Output goes to `projects/nq-trading/analysis/pre-trade-intel/YYYY-MM-DD-HHMM-shortlabel.md` with frontmatter and the sections above. Format:

```markdown
---
title: "Pre-Trade Intel — YYYY-MM-DD HH:MM TICKER DIR SETUP"
type: pre-trade-intel
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [🎯, nq-trading, pre-trade-intel]
contemplated:
  direction: ...
  setup_type: ...
  archetype: ...
  session: ...
  market_condition: ...
  mental_state_pre_label: ...
precedent:
  n: 0
  win_rate: 0
  avg_r: 0
  expectancy: 0
verdict: ""    # IN-EDGE | MARGINAL | OUT-OF-EDGE
project: "[[projects/nq-trading/nq-trading|NQ Trading]]"
related:
  - "[[projects/nq-trading/analysis/pre-trade-intel/_index|Pre-Trade Intel Index]]"
---

# Pre-Trade Intel — {{label}}

## Contemplated Trade
- ...

## Historical Precedent (N=...)
- ...

## Pattern Matches
- ...

## Rule Check (R1–R6)
- ...

## Market Context Match
- ...

## Emotional State Consideration
- ...

## Verdict — {{IN-EDGE | MARGINAL | OUT-OF-EDGE}}

> ...

## What Would Raise Conviction
- ...
```

### Step 9 — Inline response

Always echo the verdict + the top 2 facts driving it to the user in chat, with a wikilink to the full brief. Don't make the user open the file to know the answer.

---

## Quality Bar

- **No false confidence.** N=4 precedent is "insufficient precedent." Do not extrapolate.
- **Cite specific trade files.** "Avg R of +1.4 across N=8" must link to the 8 trade files so the user can verify.
- **No moralizing.** If precedent says the contemplated trade is OUT of edge, say so plainly with the data. Don't lecture about discipline.
- **Don't repeat work.** If the same combination was queried in the last 30 minutes, link to the prior brief and only update the rule-check section (which may have changed if a new trade closed in between).

## See Also

- [[projects/nq-trading/system/CLAUDE|system/CLAUDE.md]] — strategy anchor
- [[skills/trade-capture/SKILL|trade-capture]] — sibling skill, runs AFTER entry
- [[projects/nq-trading/analysis/patterns/_index|Pattern Library]] — what we know about ourselves
- [[research/topics/obsidian-trading-brain-cyrilxbt|CyrilXBT source]] — origin of this design
