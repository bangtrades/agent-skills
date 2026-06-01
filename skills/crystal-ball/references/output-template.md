# CB Snapshot — Output Template

The CB analysis is written to:
`cortana-vault/projects/nq-trading/journal/snapshots/YYYY-MM-DD/HHMM-cb-<context>.md`

`<context>` examples: `weekly-cb-assessment`, `cb-1h-live`, `cb-15m-bearish`,
`cb-expansion-example`.

---

## Frontmatter contract

```yaml
---
title: "NQ <TF> — Crystal Ball <bullish|bearish> Expansion (CB Sample #N)"
type: snapshot
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [🎯, nq-trading, snapshot, crystal-ball, cb-tool, fib-expansion, <tf>, <bullish|bearish>, nq]
status: active
instrument: NQ1!
session_date: YYYY-MM-DD
capture_context: cb-<context>
capture_mode: "live | replay (frontier ...)"
timeframe: <2m|5m|15m|1h|4h|1W>
archetype: "n/a-cb"
demonstrates_concept: [crystal-ball-tool, fib-expansion, cisd-range-break, exhaustion-manipulation, fractal-mtf]
demonstrates_strategy: [crystal-ball-cb-tool]
demonstrates_setup: [cb-fade-t5]            # if applicable
outcome: "in-progress | calibration-only | win | loss"
key_observation: "One sentence — the CB read."
related:
  - "[[research/topics/crystal-ball-cb-tool|Crystal Ball (CB) Tool]]"
  - "[[<prior CB sample>]]"
---
```

---

## Body structure

```markdown
# NQ <TF> — Crystal Ball <…> Expansion (CB Sample #N)

> One-paragraph intro: what chart, live or replay, why this sample matters.

## The CB drawing — decoded
[table: level | coeff | price | status vs. current price]
[note the anchor bar, the 0.618/CISD level, direction]

## The expansion trace
[table from cb_trace.py: level | price | first-touch (PT) | bars-from-anchor | gap]
[one line: did price touch all levels in sequence? skips? pace pattern?]

## Analysis
[numbered: construction confirmed; how price walked the ladder — pause/cascade,
chop-zone behavior; the T5 state — reached? overshoot? terminal sequence?]

## Fractal multi-timeframe read
[the Section-5 synthesis from references/fractal-mtf.md: which layer is this CB;
the HTF CB it nests in / the LTF CBs inside it; does the move extend into HTF
projections or exhaust at its own T5?]

## Trading read / forward assessment
[scenario framing — fade T5 / breakout-above-T5 / OB reversal zone; downside &
upside refs at the ladder levels; NOT a directive "buy here"]

## R3 / R5 / R1 — discipline check
[R5 time-of-day; calibration-only if replay/historical; the actionable CB event]

## See also
[methodology page + adjacent CB samples]
```

---

## After writing the snapshot — log the sample

The skill is only done when the sample is logged. In
`research/topics/crystal-ball-cb-tool.md`:

1. Add a row to the **Sample log** table (`# | date | instrument·TF | state | notes`).
2. Add a **Sample #N detail** block (anchor, 0.618/CISD, ladder, trace summary, the lesson).
3. Update **open questions** if the sample informs one (overshoot, chop-through, etc.).

Then append a `log.md` entry (type `snapshot`, the CB context, pages touched).

The compounding sample library *is* the framework's refinement mechanism — every capture
must land in it.

---

## Tone

Scenario analysis of bang's own tool — never a directive trade call. Report honest
divergence (cascades through the chop zone, odd T5 overshoots, ambiguous fractal nesting)
over a tidy story. Keep the in-chat summary tight; the file holds the full read.
