# Replay Markup Capture — the canonical per-day protocol

Validated end-to-end 2026-06-07 on the 2026-05-01 session (7 trades, T1–T7).
This is the PRIMARY capture method: bang marks trades on a replay chart with
long/short position tools; Claude extracts everything, computes outcomes, and
upserts into the Backtest Lab DB. Bang then refreshes the app, edits judgment
fields, and moves to the next day.

## Preconditions

- TradingView Desktop connected (`tv_health_check`).
- Chart: `CME_MINI:NQ1!` (or MNQ1!), **2m**, **replay mode** with the frontier at/after the
  session's EOD (`replay_status` → `current_date` ≈ end of target day).
- Trades marked with **Long Position / Short Position tools** (LineToolRiskReward),
  labeled T1–Tn in chronological order. Default trigger TF = 2m; bang states
  per-trade exceptions in chat (e.g. "T4 is a 3m setup").
- The Backtest Lab (journal app) holds the target model — default slug `30m-or-eob`,
  DB at `/Users/nolan/Projects/Trading/journal/app/data/backtest.db`.

## Step 1 — Extract the position drawings

`draw_list` has a known bug (`getChartApi is not defined`). Go straight to
`ui_evaluate` with the page-context charting API:

```js
(() => {
  const chart = window.TradingViewApi.activeChart();
  const shapes = chart.getAllShapes();          // [{id, name}] — filter long_position / short_position
  return JSON.stringify(shapes.map(s => {
    const sh = chart.getShapeById(s.id);
    return { id: s.id, name: s.name, points: sh.getPoints(), props: sh.getProperties() };
  }));
})()
```

Decode per tool (**NQ tick = 0.25**):

- `points[0].price` = entry price; `points[0].time` = entry epoch; `points[1].time` = drawn right edge (≈ exit region).
- `props.stopLevel` / `props.profitLevel` are **tick offsets** from entry:
  - long:  stop = entry − stopLevel·0.25 · target = entry + profitLevel·0.25
  - short: stop = entry + stopLevel·0.25 · target = entry − profitLevel·0.25
- Tool name `long_position` / `short_position` gives direction.
- T-labels: assign T1..Tn by **entry time order** (the chart text labels are not extractable reliably).
- Fib tools (`fib_retracement`) on the chart are bang's OR/STD ladders — list their ids in the raw archive, don't decode into trades.

## Step 2 — Pull candles & context

- `data_get_ohlcv count=300 summary=false` on the 2m chart (covers Globex→EOD; raise if first entry is missing).
- **Timestamps are true Unix UTC.** ET = UTC−4 (summer) / UTC−5 (winter); PT = ET−3.
  Sanity-anchor: the cash open (09:30 ET) is the bar with the day's first huge RTH volume spike.
- `data_get_study_values` for frontier (EOD) context only — live indicator panes can't be
  seeked per-bar in replay. **This is no longer a blocker for per-trade features:** the full
  2m OHLCV is now PERSISTED (Step 2b) and `features.py` recomputes every indicator
  (VWAP / EMA9-20-50 / ATR14 / OR / Keltner) deterministically at each entry bar, post-hoc.
- `capture_screenshot region=full` → this becomes the **day-level screenshot**.

## Step 2b — Persist the session bars (NEW — always do this)

The pulled OHLCV is the queryable market-behavior layer; never discard it.

1. Write the bars to the vault as `data/<YYYY-MM-DD>-nq1-2m.csv`
   (header `time,open,high,low,close,volume`, one row per 2m bar, ~300 rows).
2. POST them into the DB so they're queryable:
   `POST /api/bt/bars  {"symbol":"NQ1!","tf":"2m","date":"<date>","bars":[[t,o,h,l,c,v],...]}`.
   Verify with `GET /api/bt/bars/dates` (expect `n≈300` for the date).

This single table (`bt_bars`) powers the OR-breakout-continuation and return-to-VWAP
queries — answerable across ALL stored days, independent of whether a trade was taken.

## Step 3 — Compute OR + walk each trade

- **OR** (per BT VWAP convention): high/low of 09:30–10:00 ET bars from the pulled OHLCV.
  `or_source = computed_ohlcv`. Pre-OR trades (data prints at 08:30 ET etc.) get a
  non-canonical setup tag (`EOB-PreOR-Data`) — never force the four OR codes onto them.
- **Deterministic walk** from the entry bar until stop or target touch:
  - Fill assumed at the tool's entry price.
  - **Conservative stop-first** when one bar touches both stop and target.
  - **Stop-at-the-wick rule:** if the entry bar's extreme EXACTLY equals the stop,
    treat the entry as after the wick — start stop checks on the next bar (note it).
  - `raw_outcome` = TARGET / STOP / NEITHER. If NEITHER by the drawn right edge,
    exit = close of that bar.
  - `tp` (actual exit) = target if TARGET-first, stop if STOP-first, else end-bar close.
  - `exit_time` = resolution bar time. `MFE/MAE` = max favorable/adverse excursion
    in R over entry→resolution inclusive (MAE can exceed 1.0 on wicks through the stop).
- Classify each trade against the OR (the four canonical setup codes + entry_location).

## Step 4 — UPSERT into the Backtest Lab (merge, never clobber)

Target: the journal app API (`/api/bt/...`), which auto-derives direction/RR/R/outcomes/session
via the backend `_enrich`. Run the server (or a sandbox instance on the same DB) and:

1. `GET /api/bt/models/{id}/trades`, filter to the date.
2. **Match** extracted trades to existing rows by entry price ±2.0 pts or label.
3. Matched → `PUT`, but **preserve bang's manual fields** where filled:
   `tp` (his actual exit always wins), `notes`, `setup_tag`, `grade`, `htf_bias`,
   `regime`, `managed_outcome` (≠ PENDING), `tf`.
4. Unmatched → `POST` new trade with: label, direction, tf, entry/exit times (PT, HH:MM),
   entry/stop/target/tp, raw_outcome, mfe_r/mae_r (R values), session, setup_tag,
   and notes prefixed **`auto:`** so bang can spot machine text instantly.
5. Day note (`PUT /days/{date}`): only write if blank — his summary always wins.
6. Upload the day screenshot: `POST /models/{id}/screenshots?date=...` (no trade_id = day-level).
7. Leave judgment fields (grade, bias, regime) **blank** on inserts — they are bang's.
8. **Recompute features** once the trades + bars are in:
   `POST /api/bt/features/recompute?model_id={id}&date=<date>`. This snapshots each entry
   bar's VWAP / dist-from-VWAP-in-R / EMA stack+alignment / ATR / OR-position / Keltner
   into the trade's `features` JSON. Trades on dates without persisted bars are skipped
   (the response reports `skipped_no_bars`) — that's the signal to backfill Step 2b for them.

## Step 5 — Archive + report

- Raw extraction JSON →
  `cortana-vault/projects/nq-trading/backtests/<slug>/data/raw-YYYY-MM-DD-extraction.json`
  (drawings with tick levels + unix times, OR block with source, walk conventions used,
  fib tool ids, EOD indicator context, raw outcomes).
- Reply with the per-trade table (label/TF/in→out PT/dir/prices/raw/R/MFE/MAE/setup),
  what was UPDATED vs INSERTED, and the review checklist:
  `auto:` notes to rewrite · blank grades/bias/regime · conservative-walk caveats ·
  any stop-at-wick or both-touched ambiguities. Remind bang to **Commit → vault** from the app.

## Behavior queries unlocked by the persisted layer

Once bars + features are stored, these answer across ALL captured days:

- `GET /api/bt/behavior/or-breakout` → "when price crosses the 30m OR, what % continues
  and breaks out?" (accepted = N consecutive closes hold beyond the level; split up/down).
- `GET /api/bt/behavior/vwap-trades?model_id={id}` → R/R and win-rate on return-to-VWAP
  trades (entry within 0.30·ATR of session VWAP) vs everything else.
- `GET /api/bt/events?date=<date>` → the raw OR-cross / VWAP-touch event stream for a day.

## Known constraints

- Replay cannot seek live indicator panes per-bar — but per-trade features are now
  RECOMPUTED deterministically from the persisted 2m bars (`features.py`), so the only
  values you can't reproduce are bespoke Pine studies not re-derivable from OHLCV.
- Feature recompute needs bars: a trade whose date has no `bt_bars` rows is skipped until
  you persist that day (Step 2b). Backfill old days by writing their CSV + POST /bars.
- `draw_list` MCP tool broken → always use the `ui_evaluate` path above.
- Text labels (T1 etc.) aren't tied to tools → chronological assignment; confirm with
  bang when a day's order is ambiguous.
- Walks are price-path approximations on 2m bars — bang's managed outcome is the truth;
  the walk supplies the raw-mechanical baseline.
