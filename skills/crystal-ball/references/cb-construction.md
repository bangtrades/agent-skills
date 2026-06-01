# CB Construction & Price Behavior

How the Crystal Ball tool is built, extracted from the chart, and how price moves through it.

## Table of contents

1. Construction — the three steps
2. Extracting the CB drawing via `ui_evaluate`
3. Decoding the ladder (the math)
4. How price moves through the tool
5. The T5 terminal sequence
6. Bearish CBs (the mirror)

---

## 1 — Construction: the three steps

The CB is a Fibonacci retracement/expansion tool drawn on a confirmed expansion leg.

1. **Anchor the start of the expansion.** Mark the low (bullish) or high (bearish) where
   the expansion begins — typically the bar right after the prior trend's exhaustion flush
   (often a high-volume capitulation bar). This is the tool's `0`.
2. **Calibrate 0.618 to the CISD breakout.** Drag the far anchor until the **0.618 gridline
   lands on the CISD** — the change-in-state-of-delivery candle/level that confirmed the
   prior trend was broken. The 0.618 is the *calibration handle*; the CISD breakout is the
   known structural input. Anchor + 0.618-on-CISD fully determines the tool.
3. **Read the T1–T5 ladder.** Once calibrated, the extension levels resolve into the target
   ladder.

> **Timeframe calibration.** Each timeframe has its *own* CISD breakout level, so the same
> expansion drawn on 5m vs 1h vs 4h produces *different* ladders — the higher timeframe
> reads a lower (bull) / higher (bear) CISD, giving a bigger unit and a deeper ladder. On a
> large move the higher-timeframe CB frames the true exhaustion zone better. When timeframes
> disagree, weight the higher-TF T5.

---

## 2 — Extracting the CB drawing via `ui_evaluate`

The CB is a `LineToolFibRetracement` carrying T1–T5 level labels. Extract it from the
TradingView chart's data sources:

```javascript
(function(){
  try{
    var cw=window._exposed_chartWidgetCollection.activeChartWidget.value();
    var ts=cw.model().timeScale();
    var ds=cw.model().model().dataSources();
    var out=[];
    for(var i=0;i<ds.length;i++){
      var s=ds[i]; var tn=s.toolname||s._toolName||'';
      if(!/FibRetracement|FibExtension|TrendBasedFib/i.test(tn)) continue;
      var pts=[];
      try{var pp=s.points?s.points():null;
        if(pp)for(var p=0;p<pp.length;p++){
          var tp=null;try{tp=ts.indexToTimePoint(pp[p].index);}catch(e){}
          pts.push({idx:pp[p].index,price:pp[p].price,t:tp});
        }}catch(e){}
      var info={};
      try{var st=s.properties().state(); info.reverse=st.reverse; info.text=st.text||'';
        var lv=[]; for(var k in st){ if(/^level\d+$/.test(k) && st[k] && st[k][2]) lv.push(st[k][0]+(st[k][3]?('='+st[k][3]):'')); }
        info.levels=lv;
      }catch(e){}
      out.push({i:i,tool:tn,pts:pts,info:info});
    }
    return JSON.stringify(out);
  }catch(e){return 'ERR: '+e;}
})()
```

The CB is the fib whose `info.levels` include `1=T1`, `1.236=T2`, `1.618=T3`, `1.902=T4`,
`2.38=T5`. Other fibs on the layout (a plain retracement, a weekly fib) will *not* carry the
T-labels — that is how to tell them apart. `pts[0]` is the `0` anchor; `pts[1]` sets the
unit. `info.reverse` is typically `true`.

> Times come back as Unix from `indexToTimePoint`. Anchors placed in the future (to extend
> the drawing) are normal — only the prices matter for the levels.

---

## 3 — Decoding the ladder (the math)

Let `P0` = anchor[0].price (the `0`), and `P_T1` = anchor[1].price (the `1.0` / T1 level).
`unit = P_T1 − P0`.

- **Bullish** (`P_T1 > P0`): `level(c) = P0 + c·unit`. Ladder ascends.
- **Bearish** (`P_T1 < P0`): same formula; `unit` is negative so the ladder descends. Or
  read it as `level(c) = P0 − c·|unit|`.

Coefficients: `0, 0.618, 0.877, 1.0 (T1), 1.236 (T2), 1.618 (T3), 1.902 (T4), 2.38 (T5)`.

**Always run `scripts/cb_trace.py`** rather than hand-computing — it derives the ladder and
traces price in one pass, and keeps the numbers identical across samples.

---

## 4 — How price moves through the tool

Price does not lurch randomly toward a target — it **walks the ladder**:

- **Sequential touches.** Price tags the levels in order — rarely skipping. Each level gets
  hit.
- **Pause-and-confirm at each level.** At a level, price pauses / consolidates, then
  confirms to the next. Levels are waypoints, not flythroughs.
- **The chop zone — T3 to T4 (1.618–1.902).** Price *often* chops hardest here — the
  longest, messiest leg. But this is a **tendency, not a rule**: price can also cascade
  straight through. The forward question (open in the methodology page) is what predicts
  chop-through vs. fast-through — candidate tells: velocity into T3, bar size, volume, and
  how long price dwelled at the earlier levels.
- **Dwell varies.** Some expansions dwell evenly; some run fast early then grind the upper
  levels; some cascade. Record the dwell pattern (bars-per-level) on every sample — it is
  the raw material for predicting pace.

---

## 5 — The T5 terminal sequence

T5 (2.38) is the terminal target. When price reaches it:

1. **Exhaustion** — the expansion is spent.
2. **Range** — price ranges around T5.
3. **Manipulate the extreme** — a sweep *beyond* T5 (above, for a bullish CB; below, for a
   bearish one). Overshoot has varied widely across samples (+16 to ±200 pts); it may scale
   with the ladder unit — an open question.
4. **Retrace into the range** — price reverses back into the body of the expansion.

This sequence is the tradeable event: **bang fades T5** — counter-trading the exhaustion
into the range-and-retrace. A clean **breakout back above T5** (bull) instead signals a
*fresh* expansion — draw a new CB.

---

## 6 — Bearish CBs (the mirror)

Everything inverts cleanly. Anchor the expansion **high**; calibrate 0.618 to the bearish
CISD; the ladder projects **down**. Terminal sequence: price reaches T5 (down), ranges,
**sweeps below** the extreme, then retraces back **up** into the range. `cb_trace.py` handles
both directions via the `--direction` flag.
