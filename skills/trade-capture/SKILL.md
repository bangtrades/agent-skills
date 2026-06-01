---
name: trade-capture
description: >-
  Convert a natural-language trade description into a fully populated structured
  trade file in `projects/nq-trading/trades/open/` using bang's setup taxonomy
  (R1/R2/R3 range, T1/T2 trend), archetype labels (1/2/3/4/Unclear), and rules
  R1–R6 check. Trigger on ANY informal trade-entry phrasing — "long NQ at 21450,
  R1 fade upper K-band, stop 21430, target 21490", "took a short T1 entry off the
  failed lower-K", "just entered MNQ long off VWAP revert" — even when the user
  doesn't say "log this" or "capture trade". Also trigger on close-side phrasings
  ("stopped out at 21430", "hit target +1.8R", "scratched at breakeven") to fill
  the close addendum and move the file from open/ to closed/. Reads
  `projects/nq-trading/system/CLAUDE.md` for context before generating any trade
  file. Do NOT use for daily journal entries (use the daily journal template) or
  for backfilled historical reconstruction (use reconstructed-trades/).
---

# trade-capture — Structured NQ trade journaling

> Convert natural-language trade descriptions into the structured per-trade files
> that power weekly performance analysis, monthly edge reports, and pre-trade
> intelligence queries. This is the **input layer** to the trade dataset.

---

## Before You Begin

1. **Read** `projects/nq-trading/system/CLAUDE.md` — the strategy anchor (edge hypothesis, known weaknesses, current performance benchmarks, rules). All trade interpretation references this context.
2. **Read** `projects/nq-trading/trades/_index.md` — the design rationale, file layout, and lifecycle.
3. **Read** `projects/nq-trading/trades/_templates/trade-open.md` and `_templates/trade-close-addendum.md` — the canonical frontmatter schema.
4. **Skim** `research/topics/range-day-playbook.md` and `research/topics/trend-pullback-playbook.md` — to know what counts as a legal R1/R2/R3/T1/T2 setup.

You do NOT need to read every prior trade. The skill operates at the level of an individual capture.

---

## Two Modes

### Mode A — Entry capture (creates a new file in `trades/open/`)

Trigger phrases (non-exhaustive):
- "long NQ at 21450, R1 fade..."
- "took a T1 entry off failed lower-K..."
- "just entered MNQ short, stop 21470, target 21420..."
- "in NQ long, conf 7, R1 setup, $10/pt"

### Mode B — Close addendum (moves a file from `trades/open/` to `trades/closed/`)

Trigger phrases (non-exhaustive):
- "stopped out at 21430"
- "hit target +1.8R"
- "scratched at breakeven"
- "exited NQ long manually at 21462, +0.4R"

If multiple open trades exist, ask which one to close. Otherwise infer.

---

## Mode A — Entry Capture Workflow

### Step 1 — Parse the natural-language description

Extract these fields from the user's prose. Ask for **missing required fields** ONE at a time, not all at once. Required minimum:

| Field | Required? | Inference rules |
|---|---|---|
| `instrument` | yes | Default NQ unless user says MNQ/ES/MES |
| `direction` | yes | "long"/"bought"→long, "short"/"sold"→short |
| `entry_price` | yes | Must be numeric |
| `stop_price` | yes | If user gives "stop X pts away", compute it |
| `target_price` | yes | Same — convert R or pts to price |
| `setup_type` | yes | Match phrase → taxonomy: see "Setup Recognition" below |
| `size_contracts` and `size_dollar_per_point` | yes | If only one given, infer the other (5 micros = $10/pt; 10 micros = $20/pt; 1 mini = $20/pt) |
| `archetype` | yes | If user didn't say, ask: "Archetype 1 (range), 2 (rebalance→trend), 3 (trend→cascade), 4 (false-break reversal), or Unclear?" |
| `session` | yes | Infer from current ET time if `entry_time` is present; else ask |
| `thesis_confidence` | yes | If user didn't say, ask 1–10 |
| `mental_state_pre` | yes | Ask 1–10 (energy/focus aggregate). If user already said "calm" / "charged" / "anxious" / "revenge" / "FOMO" / "steady" / "numb" / "focused", store that as `mental_state_pre_label` and ask numeric |
| `market_condition` | preferred | Short tag — `range`, `trend-up`, `trend-down`, `false-break`, `news-vol`. Infer from archetype if absent |
| `account` | preferred | Default to whatever was in the most recent prior trade if unspecified; else ask |
| `playbook_match` | yes | If `setup_type` is R1/R2/R3/T1/T2 → Yes. If discretionary → Partial or No (ask) |
| `entry_date` and `entry_time` | yes | Default to "now" in ET if not specified |

**One question at a time.** Don't dump a form on the user mid-trade. The capture must be under 60 seconds.

### Setup Recognition

| User phrase contains | → `setup_type` |
|---|---|
| "VWAP revert", "K-mid revert", "fade upper/lower K-band", "fade extreme" | **R1** |
| "IB extreme", "fade IB high/low", "initial balance extreme" | **R2** |
| "VA edge", "value area fade", "VAH/VAL fade" | **R3** |
| "failed breakout", "failed lower-K", "IFVG", "lower-K breakout failed" | **T1** |
| "EMA backtest", "9 EMA pullback", "21 EMA test" | **T2** |
| "order block", "OB entry", "FVG fill" | **OB-FVG** |
| "MM model", "market maker model" | **MM-model** |
| Anything else | **other-discretionary** — flag for R6 check |

### Step 2 — Run the R1–R6 rule check

For each rule, decide `OK` or `VIOLATION` based on context. If you cannot determine a rule from context, ask. Common reasoning:

- **R1 size cap:** size_dollar_per_point ≤ $10 on Range/Unclear/Reversal-day; ≤ $20 on Trend
- **R2 revenge cooldown:** check if the user just mentioned a stop-out in this session (read recent open/closed trades for today)
- **R3 daily loss limit:** if today's running P&L is already at or near –$200, this trade is borderline; flag
- **R4 min hold:** entry-time check only — verifies the user isn't planning an instant scratch (a stop within 2 pts of entry on a $20/pt setup is suspicious)
- **R5 time-of-day:** is `entry_time` inside an approved window?
- **R6 off-playbook block:** is `setup_type` ∈ {R1, R2, R3, T1, T2} or explicitly approved discretionary?

Mark each as `Rx:OK` or `Rx:VIOLATION` in the `rules_check` array. If any violations, surface them to the user before writing the file: "**R1 violation: you're sizing $20/pt on a Range-day setup. Continue anyway?**" Do not silently log a violation — the user should consciously override.

### Step 3 — Generate the filename

Pattern: `YYYY-MM-DD-HHMM-TICKER-DIR-SETUP-shortlabel.md`

Where `shortlabel` is a 2–5 word kebab-case description of the specific instance (`vwap-revert-from-upper-kband`, `failed-lowerk-breakout`, `va-low-fade-2nd-test`).

### Step 4 — Write the file

Use `_templates/trade-open.md` as the skeleton. Populate every entry-side frontmatter field. In the body:

- Fill the **one-line thesis** from the user's prose
- Fill **Setup Description** with the specific trigger conditions observed (don't just restate the setup name)
- Fill **Plan** table with entry/stop/targets/R:R
- Tick the relevant **Risk Check** checkboxes; for any violation, leave unticked and explain in a one-line note below the checklist
- Fill **Mental State at Entry**

Leave the close-side fields blank (already blank in the template) and the close addendum section as the HTML comment placeholder.

### Step 5 — Confirm

After writing, give the user a one-line confirmation showing:
- Trade file path (clickable wikilink)
- Setup × Archetype × Session × Mental-state
- R:R primary
- Any rule violations flagged

---

## Mode B — Close Addendum Workflow

### Step 1 — Identify the trade

If exactly one file exists in `trades/open/`, use it. Otherwise list open trades and ask which to close.

### Step 2 — Parse the close description

Extract: `exit_date`, `exit_time`, `exit_price`, `exit_reason`, `mental_state_post`. Compute (do not ask):

- `result_r = (exit_price - entry_price) * direction_sign / (entry_price - stop_price) * direction_sign`
   - For long: `(exit - entry) / (entry - stop)`
   - For short: `(entry - exit) / (stop - entry)`
- `result_pnl_dollars = (exit_price - entry_price) * direction_sign * size_dollar_per_point`
- `hold_duration_min` = ISO time diff in minutes

### Step 3 — Ask the qualitative fields

- **Execution quality A–F** (vs plan, not vs P&L) — explain the grading rubric only if user hasn't seen it recently
- **What I learned** — one paragraph, "specific observation → specific change" format
- **Any rule violations** that became apparent on review (e.g., R4 if held only 30 seconds when plan was for 5 min)

### Step 4 — Update the file

- Flip `status:` from `open` → `closed` (or `scratched` / `invalid`)
- Fill all close-side frontmatter fields
- Replace the close-addendum HTML-comment placeholder with the actual sections from `_templates/trade-close-addendum.md`, filled in
- Update `updated:` to today's ISO date

### Step 5 — Move the file

Move from `trades/open/` to `trades/closed/`. Preserve the filename.

### Step 6 — Side effects

- If `violations:` is non-empty: append a row to `projects/nq-trading/journal/_violations-log.md` referencing this trade
- Increment `trades_total` in the day's `projects/nq-trading/journal/YYYY-MM-DD.md` frontmatter
- If the trade matches a known pattern in `projects/nq-trading/analysis/patterns/`, append this trade to that pattern's `example_trades:` array

### Step 7 — Confirm

Give the user a one-line close summary:
- Result: +/-X.XR ($+/-YYY)
- Exit reason
- Execution quality grade
- Any violations now logged

---

## Quality Bar

- **No silent inference of violations.** If R1 is violated, the user sees it before the file is written.
- **Entry-side fields are immutable after creation.** If a correction is needed, add a `correction:` field — do not rewrite history.
- **Filename naming is deterministic.** Two runs of the skill on the same input must produce the same filename.
- **Body prose is yours, not the user's.** The user gives terse prose; you expand it to the template structure. But do not invent facts — if the user didn't tell you what confirmations they saw, leave the "Required confirmations seen" line blank with a `[ask]` marker.

## See Also

- [[projects/nq-trading/system/CLAUDE|system/CLAUDE.md]] — strategy anchor (context)
- [[projects/nq-trading/trades/_index|Trades Index]] — design rationale
- [[skills/pre-trade-intel/SKILL|pre-trade-intel skill]] — sibling skill, runs BEFORE entry
- [[research/topics/obsidian-trading-brain-cyrilxbt|CyrilXBT source]] — origin of this architecture
