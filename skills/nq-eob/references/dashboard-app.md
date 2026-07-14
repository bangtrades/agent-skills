# EOB Dashboard App Pattern

Session-derived pattern for building the local EOB analytics UI from the SQLite journal.

## When to use

Use this when Nolan asks to view, filter, or analyze the EOB backtest data in an app/dashboard. Keep the SQLite database as the source of truth and export browser-ready static data for the dashboard.

## Directory convention

Create app code under:

```text
/Users/nolan/Projects/Trading/Backtesting/app/
```

Keep model data in:

```text
/Users/nolan/Projects/Trading/Backtesting/EOB/eob_backtest.sqlite
```

Recommended app structure:

```text
app/
  index.html
  styles.css
  app.js
  README.md
  scripts/export-data.py
  data/eob-data.json
  data/eob-data.js
  assets/screenshots/
```

## Static dashboard export pattern

For a dependency-free first version, export SQLite rows into both JSON and a JS wrapper:

```text
data/eob-data.json   # inspectable export
data/eob-data.js     # window.EOB_DATA = {...}; for local file/server loading
```

This avoids browser `fetch()` issues when the user opens `index.html` directly and also works over `python3 -m http.server`.

The export script should:

1. Read `sessions`, `opening_ranges`, `trades`, and candles for each stored timeframe.
2. Copy referenced screenshot evidence into `app/assets/screenshots/`.
3. Add `screenshot_rel` paths to each trade row.
4. Compute dashboard summary metrics: trade count, wins, win rate, gross R, expectancy R, pnl points, average risk/reward.
5. Compute grouped analytics by setup code, EOB timeframe, and EOB type.
6. Compute a cumulative R equity curve.
7. Write `data/eob-data.json` and `data/eob-data.js`.

## UI features to prioritize

Use TradeZella as the feature reference:

- performance KPI cards
- reports by setup/timeframe/type/regime
- cumulative R curve
- searchable/filterable trade journal
- detail drawer/card per trade
- screenshot evidence per row
- strategy/playbook tracking rules
- replay/candle context panel with timeframe toggles

Use the WaiveLabs site as the local style reference when requested:

- Inter + Sora typography
- dawn/light-to-deep navy surfaces
- blue/orange accents
- rounded cards, soft shadows, subtle grid backgrounds
- cinematic hero plus data-dense report cards

## Verification checklist

Before telling the user the app is done:

- Run the export script and assert expected trade/candle counts.
- Serve the app locally, e.g.:

```bash
cd /Users/nolan/Projects/Trading/Backtesting/app
python3 -m http.server 8765
```

- Open `http://127.0.0.1:8765/` in the browser.
- Check browser console for JS errors.
- Use visual inspection to confirm hero, reports, journal, and replay sections render.
- Exercise at least one filter/search interaction and verify the journal count/detail pane updates.

## Pitfalls

- Do not make the dashboard depend on screenshots as the data source. Screenshots are evidence only; SQLite rows drive analytics.
- Do not hard-code only the current two trades. Generate options and reports from exported rows so the app scales as new sessions are logged.
- Do not skip visual/browser verification; an app can pass file validation while layout or JS rendering is broken.
- Keep the app under the Backtesting folder, not random project folders or `.hermes`.
