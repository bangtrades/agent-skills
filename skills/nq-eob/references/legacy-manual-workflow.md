# NQ EOB Workflow Reference

Use this reference for executing `nq-eob` captures during the OR-EOB backtest.

## Command intent parsing

| User phrase | Meaning |
|---|---|
| `nq-eob capture` | Capture/log current marked OR-EOB trade. |
| `nq-eob screenshot` | Classify screenshot only; ask for missing entry/stop/target if needed. |
| `nq-eob fail high` | Failed break above OR high; likely short fade. |
| `nq-eob fail low` | Failed break below OR low; likely long fade. |
| `nq-eob cont up` | Accepted break above OR; bullish continuation backtest. |
| `nq-eob cont down` | Accepted break below OR; bearish continuation backtest. |

## Data pull sequence

1. `tv status`
2. `tv state`
3. `tv values`
4. `tv ohlcv -n 300`
5. `tv draw list` — optional; if it fails, log the error and use manual fields.
6. Screenshot if needed.

## OR derivation

Default BT VWAP OR parameters:

- session: `0930-1600` ET
- OR length: `30` minutes
- OR window: `09:30–10:00 ET`

Compute:

```text
or_high = max(high in 09:30–10:00 ET)
or_low = min(low in 09:30–10:00 ET)
or_mid = (or_high + or_low) / 2
or_size = or_high - or_low
or_full_target_up = or_high + or_size
or_full_target_dn = or_low - or_size
```

Record `or_source`:

- `bt_vwap` — extracted directly from BT VWAP values/table/labels.
- `computed_ohlcv` — computed from candle data.
- `screenshot_estimate` — visually estimated from user image.
- `manual` — user supplied.

## EOB derivation

Prefer EOB Advanced v3 (`BT_EOB_v2.pine`) fields:

- type: Turtle Soup / CISD / Continuation
- direction: bullish / bearish
- grade and score
- zone top/bottom
- SL and target
- FVG yes/no
- in session yes/no
- regime/chop
- EOB bias and HTF bias

If only labels are visible, parse label text:

- `EOB · CISD · A/B/C`
- `EOB · Turtle Soup · A/B/C`
- `EOB · Continuation · A/B/C`
- optional `FVG`

## Setup classification decision tree

1. Is the trade fading a failed break above OR high?
   - yes → `OR-EOB-Fail-High`
2. Is the trade fading a failed break below OR low?
   - yes → `OR-EOB-Fail-Low`
3. Is price accepted above OR and the EOB is a bullish backtest/continuation?
   - yes → `OR-EOB-Cont-Up`
4. Is price accepted below OR and the EOB is a bearish backtest/continuation?
   - yes → `OR-EOB-Cont-Down`
5. Otherwise classify as `unclassified` and ask for user intent before appending a final journal row.

## Trade ID format

Use:

```text
or-eob-YYYYMMDD-NNN
```

Example:

```text
or-eob-20260605-001
```

## Minimum final response

After a capture, report:

```text
Logged <trade_id>: <setup_code> — <eob_timeframe> <eob_type> <direction>.
OR: <low> / <mid> / <high> (<or_source>).
Result: <result>, <outcome_r>R.
Dashboard: <path or pending reason>.
```
