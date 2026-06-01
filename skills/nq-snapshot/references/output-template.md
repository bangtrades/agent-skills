# Output Template — Snapshot File Structure

The exact markdown skeleton to write for every snapshot. Adapt section contents to the actual data but keep the structure consistent so the chart library and Dataview queries work.

## Filename

```
~/Cortana/cortana-vault/projects/nq-trading/journal/snapshots/YYYY-MM-DD/HHMM-<context>.md
```

For morning reviews:

```
~/Cortana/cortana-vault/projects/nq-trading/journal/morning-reviews/YYYY-MM-DD.md
```

## Template

```markdown
---
title: "Snapshot — YYYY-MM-DD HH:MM ET — [Brief Description]"
type: snapshot
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [🎯, nq-trading, snapshot, tradingview, mnq, <context>]
status: captured
context: <context-slug>
symbol: "CME_MINI:MNQ1!"
timeframes: ["5m", "15m", "60m"]
captured_et: "HH:MM"
session_window: "<session label>"
# === Chart Library tagging (Layer 2 backlink) ===
archetype: "1" | "2" | "3" | "4" | "unclear"
demonstrates_concept: [...]
demonstrates_strategy: [...]
demonstrates_setup: [...]
outcome: "in-progress" | "win" | "loss" | "scratch" | "didnt-trigger" | "calibration-only"
key_observation: "Single sentence summarizing the tape state."
# === End library tagging ===
playbook: "[[research/topics/<active-playbook>|Active Playbook]]"
related:
  - "[[projects/nq-trading/journal/_index|NQ Trading Journal]]"
  - "[[research/topics/<active-playbook>|<Playbook Name>]]"
  - "[[projects/nq-trading/tv-data/chart-layouts/mnq-mtf-2x2|MNQ MTF 2x2]]"
  - "[[projects/nq-trading/tv-data/chart-library/setups/<setup>|<Setup> Library]]"
  - "[[projects/nq-trading/tv-data/chart-library/concepts/<concept>|<Concept> Library]]"
  - "[[projects/nq-trading/tv-data/chart-library/archetypes/archetype-<N>-<name>|Archetype <N> Library]]"
---

# Snapshot — YYYY-MM-DD HH:MM ET — [Brief Description]

> Anchor: <e.g., Globex re-open at 18:00 ET (~N hours ago)>
> Review time: **HH:MM ET / HH:MM PT**
> Symbol: CME_MINI:MNQ1!
> Trigger: <user phrase or auto-trigger reason>

## Headline

[2-3 sentence summary of what the tape shows and why this snapshot matters.]

**Bias verdict: [LONG / SHORT / RANGE / UNCLEAR]** with **[STRONG / MODERATE / WEAK]** confidence.

**Archetype: [N — Name]**

**Live setup(s): [T1 / T2 / R1 / R2 / R3 / None]**

## 1h Pane — Multi-Day Bias

![[raw/assets/journal/YYYY-MM-DD/<context>-1h.png]]

### Session Snapshot

| Metric | Value |
|---|---|
| 100-bar window | open X → close Y = +/- Z pts / N% over ~T duration |
| Window high / low | X / Y |
| Window range | Z pts |
| Avg volume | N |
| Last bar (HH:MM ET) | open / high / low / close / volume |

### 1h Key Levels

| Level | Value | Distance from <last> |
|---|---|---|
| BT VWAP | X | ±N pts |
| BT MA Bands Upper | X | ±N pts |
| BT MA Bands Anchor | X | ±N pts |
| BT MA Bands Lower | X | ±N pts |
| BT Volatility Envelope tight Top | X | ±N pts |
| BT Volatility Envelope tight Bottom | X | ±N pts |
| BT Volatility Envelope wide Top | X | ±N pts |
| BT Volatility Envelope wide Bottom | X | ±N pts |

[Add cursor-position warning here if values look stale.]

### 1h Order Flow (latest bar)

- Delta: ±N (XX.XX% buy/sell)
- Buy vol N vs Sell vol N — ratio X:Y
- CVD: N
- Flip signal: 0 or 1.00

**Reading:** [1-3 sentences on what the 1h vectors are saying.]

## 15m Pane — Setup Trigger Timeframe

![[raw/assets/journal/YYYY-MM-DD/<context>-15m.png]]

### Session Snapshot

| Metric | Value |
|---|---|
| ... (same structure as 1h) |

### 15m Key Levels

[Same table structure as 1h.]

### 15m Channel Position

```
position = (last - lower_band) / (upper_band - lower_band)
         = ...
         = NN.N%
```

**[Where price is in the channel and what that implies for setup status.]**

### 15m Order Flow

[Same structure.]

## 5m Pane — Execution Timeframe

![[raw/assets/journal/YYYY-MM-DD/<context>-5m.png]]

### Session Snapshot

[Same structure.]

### 5m Key Levels

[Same structure.]

### 5m Order Flow — THE KEY READ

[5m delta is usually the moment-of-truth read. Highlight if absorption, flip, or extreme one-sided action is present.]

## 9-Vector Check (Cross-TF Synthesis)

| Vector | 1h Read | 15m Read | 5m Read | Verdict |
|---|---|---|---|---|
| Opening context | ... | ... | ... | ... |
| Price action structure | ... | ... | ... | ... |
| VWAP behavior | ... | ... | ... | ... |
| MA Bands stack | ... | ... | ... | ... |
| Volume profile | ... | ... | ... | ... |
| CDCΔ | ... | ... | ... | ... |
| Aggression / flow | ... | ... | ... | ... |
| BBWP / K-span regime | ... | ... | ... | ... |
| IB range | ... | ... | ... | ... |

**Score: <N> vectors favoring LONG / SHORT / NEUTRAL.**

## Archetype Verdict

[Per archetype-rubric.md format.]

## Setup Status

| Setup | Status | Trigger Zone | Stop | T1 | T2 | Notes |
|---|---|---|---|---|---|---|
| T1 long | LIVE / IMMINENT / NA | X | Y | Z | W | ... |
| T1 short | NA / ... | — | — | — | — | <reason> |
| T2 long (5m 20 EMA) | ... | ... | ... | ... | ... | ... |
| ... (one row per relevant setup) | | | | | | |

## R5 / R3 / R1 Discipline Check

### R5 — Time-of-Day Verdict

Current time: HH:MM ET

Status: [NO TRADE / CAUTION / TRADE / REDUCED / SWEET SPOT / PRIMARY]

[Window-specific verdict.]

### R1 — Position Size Cap

Today's cap given the archetype: $4/point = 2 micros MNQ (default provisional).
Anti-doubling: next trade's $/pt cannot exceed prior losing trade's $/pt.

### R3 — Daily Loss Limit

Intraday cap: −$200 (or −$80 if Archetype 1).
[State if user is near the cap based on context if known.]

## Net Verdict

**[TRADE PERMITTED — <setup ID> with <size> cap <risk> / WAIT — no LIVE setup / STAND ASIDE — R5 (<reason>)]**

## Notes / Thesis

[1-2 paragraphs of free-form reasoning on what's happening, what to watch, and what the next decision point is.]

## Linked Trade

[None for live snapshot; populate after trade resolves.]

## See Also

- [[research/topics/<active-playbook>|<Playbook>]] — methodology this snapshot exercises
- [[projects/nq-trading/tv-data/chart-library/setups/<setup>|<Setup> Library Page]]
- [[projects/nq-trading/tv-data/chart-library/concepts/<concept>|<Concept> Library Page]]
- [[projects/nq-trading/tv-data/chart-library/archetypes/archetype-<N>|Archetype <N> Library]]
- [[projects/nq-trading/tv-data/chart-layouts/mnq-mtf-2x2|MTF Chart Layout]]
- [[projects/nq-trading/tv-data/data-fidelity-reference|TV Data Fidelity Reference]]
```

## Section Order Is Important

The order matters because users skim:

1. **Headline** — bias + archetype + live setup, in 3 lines max
2. **1h / 15m / 5m TF analyses** — in that order, top-down from macro to execution
3. **9-vector check** — the synthesis
4. **Archetype verdict** — the classification
5. **Setup status** — what's actionable
6. **R5 / R3 / R1 discipline check** — the gate
7. **Net verdict** — the one-line bottom-line
8. **Notes / Thesis** — the discretionary reasoning
9. **Linked Trade** — populated post-hoc
10. **See Also** — graph navigation

A snapshot that buries the net verdict is harder to act on.

## Length

A typical snapshot is 200-400 lines. Morning reviews can be 400-600. Anything over 700 is too much — trim the verbose reasoning and let the tables do the work.

## Tone

Direct, technical, no hedging. State what the data shows. Use "Reading:" / "Verdict:" / "Action:" headers to separate observation from interpretation from prescription.
