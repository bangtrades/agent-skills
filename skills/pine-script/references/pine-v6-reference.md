# Pine Script v6 Reference

Consult this before writing any Pine Script to ensure correct syntax.

## Table of Contents
1. [v6 Fundamentals](#v6-fundamentals)
2. [Type System](#type-system)
3. [Input Functions](#input-functions)
4. [Collections: Arrays, Maps, Matrices](#collections)
5. [User-Defined Types (UDTs)](#udts)
6. [Enums (v6 only)](#enums)
7. [String Handling](#strings)
8. [request.security() and MTF](#mtf)
9. [Drawing Objects](#drawing-objects)
10. [Tables](#tables)
11. [Strategy API](#strategy-api)
12. [v5 → v6 Migration Notes](#v5-v6-migration)

---

## v6 Fundamentals

```pine
//@version=6                    // MUST be line 1, no blank lines above
indicator("Name", overlay=true) // or strategy()
```

Key namespaces: `ta.*`, `math.*`, `str.*`, `request.*`, `syminfo.*`, `ticker.*`, `timeframe.*`,
`color.*`, `array.*`, `map.*`, `matrix.*`, `table.*`, `line.*`, `label.*`, `box.*`,
`polyline.*`, `chart.*`, `log.*`

---

## Type System

Pine v6 types: `int`, `float`, `bool`, `string`, `color`, `line`, `label`, `box`, `table`,
`linefill`, `polyline`, plus UDTs and enums.

**Qualifiers** (critical for avoiding errors):
- `simple` — known at bar 0, constant across all bars. Required for function length params.
- `series` — changes bar-to-bar. Most runtime values are series.
- `const` — literal or compile-time known.
- `input` — set by user input, constant at runtime (qualifies as simple).

```pine
// This is why ta.ema(close, seriesLength) fails:
// The length parameter requires 'simple int', not 'series int'
len = someCondition ? 9 : 21   // series int — INVALID as length
// Fix: compute both, select result
```

**Explicit type declarations** (v6 supports and encourages):
```pine
float myPrice = na
int   counter = 0
string label_text = ""
```

**`na` handling**:
```pine
float val = na          // typed na
x = nz(val)             // replace na with 0
x = nz(val, -1.0)       // replace na with default
y = na(val)             // returns true if val is na — NOTE: na() is the test, nz() is the fix
```

---

## Input Functions

v6 requires typed input functions (bare `input()` errors):

```pine
input.int(defval, title, minval, maxval, step, tooltip, inline, group, confirm)
input.float(defval, title, minval, maxval, step, tooltip, inline, group, confirm)
input.bool(defval, title, tooltip, inline, group, confirm)
input.string(defval, title, options, tooltip, inline, group, confirm)
input.color(defval, title, tooltip, inline, group, confirm)
input.source(defval, title, tooltip, inline, group)
input.timeframe(defval, title, tooltip, inline, group, confirm)
input.session(defval, title, tooltip, inline, group, confirm)
input.time(defval, title, tooltip, inline, group, confirm)
input.symbol(defval, title, tooltip, inline, group, confirm)
input.text_area(defval, title, tooltip, group, confirm)    // v6: multi-line text input
```

**`group=`** clusters inputs in the settings panel.
**`inline=`** places inputs on the same row (same inline string = same row).
**`tooltip=`** adds hover explanation.
**`confirm=`** if true, prompts user to confirm when adding to chart.
**`options=`** for `input.string()` creates a dropdown.

---

## Collections

### Arrays
```pine
// v6 generic syntax:
a = array.new<float>(0)
a = array.new<int>(size, initial_value)
a = array.from(1.0, 2.0, 3.0)

// Common methods:
a.push(val)             a.pop()
a.get(index)            a.set(index, val)
a.size()                a.clear()
a.sort()                a.sort(order.descending)
a.slice(start, end)     a.includes(val)
a.indexof(val)          a.avg()
a.sum()                 a.min()  / a.max()
a.stdev()               a.median()
a.first()               a.last()
a.insert(index, val)    a.remove(index)
a.binary_search(val)    a.binary_search_leftmost(val)
```

### Maps
```pine
var m = map.new<string, float>()
m.put("key", 1.0)
val = m.get("key")       // returns na if key missing
m.contains("key")        // bool
m.remove("key")
m.keys()                 // returns array<string>
m.values()               // returns array<float>
m.size()
m.clear()
```

### Matrices
```pine
var mtx = matrix.new<float>(rows, cols, initial_value)
mtx.set(row, col, val)
val = mtx.get(row, col)
mtx.rows()              mtx.columns()
mtx.add_row(index, arrayOrVal)
mtx.add_col(index, arrayOrVal)
mtx.row(index)          // returns array
mtx.col(index)          // returns array
mtx.det()               mtx.inv()
mtx.transpose()         mtx.mult(other_matrix)
```

---

## UDTs

```pine
type TradeSignal
    string direction
    float  entry_price
    float  stop_loss
    float  take_profit
    int    bar_idx

// Constructor
sig = TradeSignal.new("long", close, close - atr, close + 2*atr, bar_index)

// Access
sig.entry_price
sig.direction

// Arrays of UDTs
var signals = array.new<TradeSignal>(0)
signals.push(sig)
```

v6 supports exporting UDTs from libraries. v5 does not.

---

## Enums (v6 Only)

```pine
enum Regime
    Trend
    Range
    Pullback
    Weakening

var Regime state = Regime.Range

if adx > 25 and trend_aligned
    state := Regime.Trend

label_text = switch state
    Regime.Trend     => "TREND"
    Regime.Range     => "RANGE"
    Regime.Pullback  => "PULLBACK"
    Regime.Weakening => "WEAK"
```

In v5, use int/string constants instead of enums.

---

## Strings

v6 prefers `str.format()` (Java MessageFormat syntax):

```pine
// v6 idiomatic:
txt = str.format("Price: {0,number,#.##} | Vol: {1,number,#}", close, volume)
// {0} = first arg, {1} = second arg
// {0,number,#.##} = number with 2 decimal places
// {0,number,percent} = percentage format

// Also works (and required in v5):
txt = "Price: " + str.tostring(close, "#.##")

// String methods:
str.contains(s, substr)     str.startswith(s, prefix)
str.endswith(s, suffix)     str.replace_all(s, old, new)
str.split(s, separator)     str.lower(s)  / str.upper(s)
str.length(s)               str.substring(s, start, end)
str.match(s, regex)         str.pos(s, substr)
```

---

## request.security() and MTF

```pine
// Basic HTF data fetch:
htf_close = request.security(syminfo.tickerid, "D", close)

// NON-REPAINTING pattern (critical for backtesting):
htf_close = request.security(syminfo.tickerid, "D", close[1], lookahead=barmerge.lookahead_on)

// Tuple return:
[htf_o, htf_h, htf_l, htf_c] = request.security(syminfo.tickerid, "D", [open, high, low, close])

// Lower timeframe aggregation (v6):
// request.security_lower_tf() returns an array of values from LTF bars within the current bar
ltf_closes = request.security_lower_tf(syminfo.tickerid, "1", close)

// Other request functions:
request.financial(syminfo.tickerid, "EARNINGS_PER_SHARE", "FQ")
request.economic("US", "GDP")
request.dividends(syminfo.tickerid)
request.splits(syminfo.tickerid)
request.earnings(syminfo.tickerid)
request.quandl("FRED/GDP")
request.seed(source, symbol, expression)
```

**Repainting rules**:
- Without `lookahead`: HTF value updates in real-time as the HTF bar builds → repaints
- With `lookahead=barmerge.lookahead_on` + `[1]` offset: uses confirmed (closed) HTF bar → safe
- `barmerge.gaps_on` vs `gaps_off`: controls whether na fills between HTF bars

---

## Drawing Objects

```pine
// Lines
var myLine = line.new(x1, y1, x2, y2, color=color.red, width=2, style=line.style_dashed)
myLine.set_xy1(new_x1, new_y1)
myLine.set_xy2(new_x2, new_y2)
myLine.delete()

// Labels
var myLabel = label.new(x, y, "text", color=color.blue, textcolor=color.white,
                        style=label.style_label_down, size=size.normal)
myLabel.set_text("new text")
myLabel.set_xy(new_x, new_y)
myLabel.delete()

// Boxes
var myBox = box.new(left, top, right, bottom, border_color=color.gray,
                    bgcolor=color.new(color.blue, 80))
myBox.set_lefttop(new_left, new_top)
myBox.set_rightbottom(new_right, new_bottom)
myBox.delete()

// Polylines (v6)
var points = array.new<chart.point>(0)
points.push(chart.point.from_index(bar_index, close))
polyline.new(points, line_color=color.blue)
```

**Drawing limits**: ~500 drawing objects on screen. Use `var` for references and delete old
objects before creating new ones to stay under the limit.

---

## Tables

```pine
var t = table.new(position.top_right, columns=3, rows=5,
                  bgcolor=color.new(color.black, 30), border_width=1)

if barstate.islast
    table.cell(t, 0, 0, "Metric",  text_color=color.white, text_halign=text.align_left)
    table.cell(t, 1, 0, "Value",   text_color=color.white, text_halign=text.align_right)
    table.cell(t, 0, 1, "Sharpe",  text_color=color.gray)
    table.cell(t, 1, 1, str.format("{0,number,#.##}", sharpe_val), text_color=color.white)
    // ... more rows
```

Wrap table updates in `if barstate.islast` — tables only need the final bar's state, and
updating every bar wastes performance.

---

## Strategy API

```pine
strategy("Name", overlay=true,
    initial_capital=100000,
    default_qty_type=strategy.percent_of_equity,
    default_qty_value=100,
    commission_type=strategy.commission.cash_per_contract,
    commission_value=0.62,
    slippage=2,
    pyramiding=0,
    calc_on_every_tick=false,
    process_orders_on_close=false,
    margin_long=100, margin_short=100)    // 100 = no leverage, 50 = 2x, etc.

// Entry / Exit
strategy.entry(id, direction, qty, limit, stop, comment)
strategy.exit(id, from_entry, qty, limit, stop, trail_points, trail_offset, comment)
strategy.close(id, comment)
strategy.close_all(comment)
strategy.cancel(id)
strategy.cancel_all()
strategy.order(id, direction, qty, limit, stop, comment)  // raw order, no position mgmt

// Position info
strategy.position_size      // + long, - short, 0 flat
strategy.position_avg_price
strategy.opentrades
strategy.closedtrades
strategy.netprofit
strategy.equity
strategy.initial_capital
strategy.grossprofit / strategy.grossloss

// Trade data access (per-trade stats)
strategy.opentrades.entry_price(trade_num)
strategy.opentrades.entry_bar_index(trade_num)
strategy.opentrades.entry_time(trade_num)
strategy.opentrades.size(trade_num)
strategy.opentrades.profit(trade_num)
strategy.opentrades.max_runup(trade_num)
strategy.opentrades.max_drawdown(trade_num)
strategy.closedtrades.entry_price(trade_num)
strategy.closedtrades.exit_price(trade_num)
strategy.closedtrades.profit(trade_num)
strategy.closedtrades.max_runup(trade_num)
strategy.closedtrades.max_drawdown(trade_num)
strategy.closedtrades.commission(trade_num)
```

---

## v5 → v6 Migration Notes

| Change | v5 | v6 |
|---|---|---|
| Array creation | `array.new_float(0)` | `array.new<float>(0)` |
| Bare input | `input(14, "Len")` works | Errors — use `input.int()` etc. |
| Enums | Not available | `enum Name ... end` |
| str.format | Not available | `str.format("{0}", val)` |
| UDT export | Not in libraries | Exportable from libraries |
| input.text_area | Not available | Multi-line text input |

When working in v5, avoid: `enum`, `str.format()`, generic array syntax, `input.text_area()`.
Everything else is shared across both versions.
