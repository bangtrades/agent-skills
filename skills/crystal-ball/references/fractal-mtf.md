# The Fractal Multi-Timeframe Framework

The CB tool's real power is not a single ladder — it is the way ladders **nest across
timeframes**. This is bang's core discovery (2026, refined since): NQ/MNQ price is fractal,
and CB expansions nest fractally inside one another. This file is the framework for reading
and trading that nesting.

> Status: framework v1. It is refined as the sample library grows across timeframes — see
> `research/topics/crystal-ball-cb-tool.md`.

---

## 1 — The fractal principle

- A **higher-timeframe (HTF) CB activates on the HTF breakout** — when price breaks the HTF
  trend (the HTF CISD), an HTF expansion begins and an HTF CB measures it.
- Inside that one HTF expansion, price prints **many lower-timeframe (LTF) CBs** — each LTF
  leg up (or down) is its own complete CB cycle (anchor → ladder → T5 → terminal sequence).
- So an HTF CB is a *container*; the LTF CBs are the steps that fill it. The HTF T1–T5 are
  reached by a *succession* of LTF CB cycles, not one smooth move.

This is why the same expansion looks different per timeframe (see the timeframe-calibration
note in `cb-construction.md`): each timeframe is measuring a different layer of the same
fractal.

**Reading implication.** When you decode a CB, always ask: *which layer is this?* A 2m CB is
one step inside a 15m CB, which is one step inside a 1h CB, inside a 4h CB. Name the layer,
and name the CB above and below it if you can see them.

---

## 2 — The escalation read: 2m → 5m → 15m → 1h → 4h

When a low-timeframe CB starts to play out, escalate to see if the move is going to extend
into higher-timeframe projections:

1. **A 2m CB starts to play out** — price is walking a 2m ladder.
2. **Check the 5m.** Is there a 5m CB whose levels the 2m move is feeding? Is the 2m
   expansion an early step of a 5m expansion?
3. **Then the 15m.** Same question one layer up.
4. **Then 1h / 4h.** Does the move look set to print *higher-timeframe* CB projections — i.e.
   is this the start of an HTF expansion, not just an LTF pop?

The escalation answers the only question that matters for sizing and targets: **is this a
contained LTF move that will exhaust at its LTF T5, or the first leg of an HTF expansion that
will run through HTF T1–T5?** If the LTF T5 lines up with an HTF level being freshly broken,
the move extends. If the LTF T5 sits in open air with no HTF structure behind it, expect the
LTF terminal sequence (range / manipulate / retrace) and nothing more.

---

## 3 — OB reversal zones — where the LTF CB is born

A new expansion needs a launch point. bang's launch point for LTF trades is a
**higher-timeframe order block (OB)** — a 1h or 4h OB is often a high-quality reversal zone.

The process:

1. **Wait for price to reach a 1h or 4h OB.** That OB is the candidate reversal zone — where
   the prior move is likely to exhaust and a new expansion is likely to start.
2. **Let the reversal confirm** — the CISD breakout of the prior LTF trend, inside/at the OB.
   That CISD is what the new LTF CB's 0.618 calibrates to.
3. **Anchor the LTF CB** on the new expansion out of the OB and read its ladder.
4. **Escalate** (Section 2) — does this LTF CB feed a 5m/15m/1h CB?

The OB gives the *where* (the reversal zone), the CISD gives the *when* (confirmation), and
the CB gives the *how far* (the ladder). The 1h/4h OB is the anchor of confidence: an LTF CB
launching from an HTF OB has HTF structure behind it and is far more likely to extend.

Order-block identification is its own methodology — see the EOB / Enhanced Order Block work
in the vault (`research/topics/eob-enhanced-orderblock.md`).

---

## 4 — Trading the CB

bang's CB usage rules, to be expanded as samples teach more:

- **Fade T5.** When price reaches T5 the expansion is exhausted — bang fades it,
  counter-trading the exhaustion into the expected range / manipulation / retrace. The fade
  is the tradeable event of a *completed* CB.
- **Breakout above T5 → look for new longs.** If, instead of the terminal sequence, price
  **breaks cleanly above T5**, that is a fresh expansion starting — hunt new longs and draw a
  new CB. T5 is the pivot between *reversal* (fade) and *continuation* (new expansion).
- **No breakout → measure the opposite expansion.** If price fails at T5, flip the tool —
  anchor the new (opposite-direction) expansion and measure its CB.
- **Time entries against the 1h/4h OB.** An LTF reversal entry is highest-quality when it
  happens *at* a 1h/4h OB (Section 3). Entering an LTF CB fade or launch without HTF OB
  context is lower-conviction.
- **Use the higher-TF T5 as the exhaustion marker** when timeframes disagree — the LTF T5
  can be tagged and blown through while the HTF T5 marks the true exhaustion zone.

---

## 5 — The synthesis question

Every CB analysis should end by answering, in one paragraph: **where is this CB in the
fractal stack, and what does the stack imply?**

- If the CB is an LTF CB nested early inside a freshly-activated HTF CB → the move extends;
  LTF T5 is a waypoint, not the destination; targets are the HTF ladder.
- If the CB is an LTF CB with no HTF expansion behind it → the move is contained; play the
  LTF terminal sequence (fade T5).
- If the CB *is* the HTF CB → its T1–T5 will be filled by a succession of LTF CB cycles;
  expect chop and pauses (especially T3–T4) as each LTF cycle resolves.

That synthesis — not the single ladder — is the deliverable.
