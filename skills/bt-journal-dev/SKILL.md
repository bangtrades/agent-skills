---
name: bt-journal-dev
description: Development playbook for bang's BT Journal app (FastAPI + SQLite + vanilla JS, ~/Projects/Trading/journal/) — the trading journal + Backtest Lab + BT Agent. Use whenever modifying, extending, debugging, or reviewing ANY part of the journal app — server.py, backtest.py, agent.py, features.py, static/ frontend, the backtest.db schema, or the agent config. Trigger on "BT Journal", "journal app", "backtest lab", "backtest page", "the agent in the journal", port 8765, bt.js, backtest.db, or any feature request touching trade samples, screenshots, indicators, analytics, journal sections, or audio notes. Encodes the house rules (merge-never-clobber, state-first saves, R-based analytics), the verification protocol (in-process endpoint tests, throwaway-model fixtures, live-DB drift checks), and the sandbox gotchas (reaped servers, mount unlink EPERM, cache-busting). Read this BEFORE writing any code in the app.
---

# BT Journal — Development Playbook

The BT Journal is bang's local trading journal + backtest research app. It is
**deliberately lightweight**: FastAPI + SQLite (WAL) + vanilla JS, no frontend
framework, no ORM, stdlib-only analytics. Respect that bias in every change —
prefer ~150 lines with clean seams over a new dependency. (When bang asked for
an in-app AI agent, the right call was a framework-free provider/tools/loop
module, NOT LangGraph. Same logic applies to future subsystems.)

## Map

| Piece | File | Notes |
|---|---|---|
| Server + Journal + audio + report | `journal/app/server.py` | includes bt + agent routers before static mount |
| Backtest Lab backend | `journal/app/backtest.py` | schema + additive migrations in `init_db()`, `_enrich` auto-calc, analytics, vault commit |
| Session indicator engine | `journal/app/features.py` | pure stdlib; VWAP/EMA/ATR/OR/Keltner from `bt_bars`; `pt_to_epoch` for PT→UTC |
| BT Agent | `journal/app/agent.py` | OpenRouter client / tool registry / bounded loop; config `data/agent_config.json` |
| Frontend | `static/app.js` (journal) · `static/bt.js` (backtest+agent) · `index.html` · `styles.css` | cache-bust `?v=YYYYMMDDx` on ALL THREE tags in index.html — bump every ship |
| DB | `app/data/backtest.db` | tables: bt_models, bt_days, bt_trades, bt_bars, bt_screenshots, bt_indicators |
| Journal data | `app/data/drafts/{date}.json`, `audio/{date}/`, `transcripts/{date}/` | six sections + trades list per day |
| Run | `cd journal/app && .venv/bin/python -m uvicorn server:app --host 127.0.0.1 --port 8765 --reload` | bare `python` may resolve to a uvicorn-less Homebrew build |

Repo: `journal/` is a git repo (private GitHub `bt-journal`). `app/data/` and
`.env` are gitignored — they hold personal journal entries, the DB, audio, and
the agent API key. Commit locally after shipping; bang pushes.

## House rules (operator-set — do not violate)

1. **Trust but verify.** Nothing is "done" until confirmed against disk/DB.
   Never trust an empty curl response; verify the row, the file, the route.
2. **Merge, never clobber.** bang's manual fields always survive machine
   writes: tp, notes, grade, htf_bias, regime, managed_outcome, day notes,
   indicator settings text. Machine text is prefixed `auto:`; re-extraction
   replaces only the auto block. Auto-computation (MFE/MAE, OCR settings)
   fills ONLY when the target is blank.
3. **Judgment fields stay blank on machine inserts** (grade/bias/regime) —
   they are bang's calls.
4. **Analytics are R-based, not $.** Never merge reversal and continuation
   stats.
5. **State-first saves.** Frontend keystrokes land in JS state immediately;
   PUTs are debounced from state; `flushSaves()` before any re-render or
   commit. A prior session lost trades violating this.
6. **Additive migrations only.** New columns via `ALTER TABLE` in the
   `init_db()` try/except loop; new tables in SCHEMA. Never rewrite tables.
7. **`_db()` is a closing contextmanager** — bare `with sqlite3.connect()`
   leaks fds (`Errno 24`). Keep it.
8. **Friction-free data entry.** Auto-derive everything derivable (`_enrich`:
   direction from stop, R from tp, session from time, MFE/MAE from bars).
   Every new field should ask: can the app fill this itself?
9. **Versioned indicators:** never overwrite v1 of a Pine script — write v2/v3.
10. **Live market data via firecrawl**, not web_fetch (stale-cache incident).

## The live-DB reality

The app's real server runs on bang's machine (port 8765) against the SAME
`backtest.db` you touch through the mount. **bang works in the app while you
develop.** Consequences:

- **Re-check DB state before every write session** — models get deleted and
  created between your reads (30m-or-eob vanished mid-session on 2026-07-05
  while its replacement was being filled in). Never act on a cached roster.
- **Test against throwaway fixtures, never live rows.** Pattern: create a
  `ZZ Selftest …` model via the real endpoint functions → run the full
  lifecycle → delete it → assert live models untouched. Zero contamination.
- **Cross-check data plausibility** when two sources should agree (e.g. trade
  entry prices vs that date's `bt_bars` session range) and FLAG mismatches to
  bang rather than silently persisting derived values.
- Backend changes require bang to **restart the server + hard-refresh
  (Cmd+Shift+R)** — say so at the end of every ship.

## Verification protocol (the sandbox cannot run servers)

The Cowork sandbox reaps background processes between bash calls — `uvicorn &`
dies (exit 143). Never HTTP-smoke-test. Instead:

- **Routes:** `python3 -c "from backtest import router; print(sorted(r.path for r in router.routes))"`
  (import `server` for the full app; needs `pip install fastapi httpx python-multipart --break-system-packages` in a fresh sandbox).
- **Endpoints:** call the endpoint FUNCTIONS in-process (`asyncio.run(add_trade(...))`)
  so the canonical code path runs — not hand-rolled SQL.
- **Math:** compute expected values INDEPENDENTLY in the test (e.g. hand-walk
  MFE/MAE from raw bars) and assert the app matches. When a result surprises
  (exit-bounded MAE > first-touch MAE), reason through whether it's correct
  before "fixing" it — that one was correct (wicks through the stop are real
  excursion when the user says the trade lived longer).
- **LLM code:** monkeypatch the provider client with a fake returning a tool
  call then a final message — verifies the loop/dispatch/trace without a key.
- **JS:** `node --check static/*.js` + a focused review of every new event
  path (paste/drop routing, re-render vs focus).
- **Never verify by claiming.** Print the DB row / file listing in the test.

## Sandbox gotchas

- **Mount forbids `unlink`/`rm`** on many paths: expect EPERM deleting files.
  Wrap unlinks in try/except in app code (rows must still delete); tell bang
  to `rm` leftovers on his machine. Git side-effect: stale `.git/*.lock` +
  `tmp_obj_*` files bang must remove before `git gc`.
- File tools (Read/Write/Edit) use Mac paths; bash uses `/sessions/...` mount
  paths. Same files.
- `pip install --break-system-packages`; installs don't persist sessions.

## BT Agent subsystem (agent.py)

Three seams — keep them clean so a LangGraph lift stays possible:
1. `chat_completion()` — OpenAI-compatible; OpenRouter default, base_url
   override. Key from config file or env `OPENROUTER_API_KEY`; ALWAYS masked
   in API responses.
2. `TOOLS` registry — plain async funcs over the app's own data. Add tools
   here, keep results compact JSON, cap tool-result size.
3. `run_agent()` — bounded rounds; tool errors return as results, never kill
   the turn.

Model-capability truth lives in the OpenRouter catalog: `architecture.
input_modalities` gates the vision picker, `supported_parameters` ⊇ tools
gates chat. When a model "isn't available" in a picker, check the catalog
entry before suspecting keys/providers (GLM 5.2 is text-only — that's why it's
absent from the vision list, not an account issue). Pickers are filtered
suggestions, not gates — typed ids save fine.

## Shipping checklist

- [ ] Migration additive + idempotent; runs on import.
- [ ] Merge-never-clobber respected on every machine write path.
- [ ] In-process tests on a throwaway model passed; live models listed
      untouched afterward.
- [ ] `node --check` on touched JS; cache-bust bumped on all three tags.
- [ ] Memory file updated if the model roster / schema / conventions changed.
- [ ] Commit to the `journal/` repo with a change-grouped message.
- [ ] Tell bang: restart 8765 + Cmd+Shift+R, and anything he must do (push,
      rm leftovers, add API key).
