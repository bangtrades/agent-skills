# Worked example — Fable 5 session, 2026-07-05 (BT Journal)

Turn-by-turn extraction of reasoning → decision → execution → delivery from
the session that produced: 6/1 bars backfill, indicators + paste/drop upload,
the BT Agent, MFE/MAE automation, setup dropdown, git init/push, and the GLM
5.2 diagnosis. Each turn lists the pattern it exemplifies.

## Turn 1 — "Review this handoff file"

- **Reasoning:** a handoff is a set of claims about reality; the house rule is
  trust-but-verify. The cheapest high-value act is to test its load-bearing
  assertions (5 new routes, DB counts, seeded bars) before doing anything.
- **Execution:** sandbox lacked deps → installed; `server.py` import blocked on
  httpx → verified the ROUTER directly instead (verify the thing that matters,
  not the ceremony around it). Found a handoff nit (`day_date` column doesn't
  exist; it's `date`) — reported it.
- **Delivery:** verification table + the handoff's standing open question asked
  verbatim via a structured question (the operator's decision, not mine).
- **Patterns:** ground-before-act; verify claims cheaply; route around
  irrelevant blockers; user-owned forks go to the user.

## Turn 2 — "Yes, pull the next day"

- **Reasoning chain:** health check → chart on wrong symbol/TF → extracted
  shapes → zero position tools → hypothesis: wrong tab → tab_switch → identical
  results across "different" tabs → suspicion → probe `location.href` inside
  the eval → PROOF the CDP session is pinned to one tab regardless of
  tab_switch. Workaround: `layout_switch` on the attached tab. Then: drawings
  are symbol-synced → checked NQ1! too → conclusively no marked day anywhere.
- **Decision:** blocked ≠ stalled. The handoff listed a known-pending item that
  needs no markings: 6/1 bars backfill + feature recompute. Pivot there.
- **Execution:** noted the operator's replay frontier BEFORE touching replay;
  learned `replay_start date=D` semantics from observation (frontier = D−1
  23:59:59) → used D+1 to cover the session; 300 bars integrity-checked
  (count, monotonic times, single maintenance gap, OHLC sanity) before
  persisting; inserts through the app's own endpoint functions; features
  verified with entry-price-inside-mapped-bar for every trade; restored the
  replay near his frontier and said what moved.
- **Delivery:** verified backfill + updated behavior stats + the blockage
  reported with a concrete ask (mark the next day; was 5/5 a skip?).
- **Patterns:** authoritative probes over assumptions; pivot-to-adjacent-value;
  integrity gates before persistence; restore operator state; canonical-path
  writes.

## Turn 3 — run command failing

- Homebrew `python` had no uvicorn → looked for the project venv before
  suggesting installs → `.venv/bin/python`. Fix the environment mismatch, not
  the symptom.

## Turn 4 — paste/drop screenshots + indicators

- **Reasoning:** read the entire upload pipeline first (button → FormData →
  endpoint → disk+DB) and the integration points (collapse engine, cache-bust,
  state-first saves). Designed paste ROUTING deterministically (focus inside an
  indicator row → that indicator; else day shot; text pastes untouched) instead
  of heuristics.
- **Mid-flight discovery:** the live DB's model roster had CHANGED during the
  session (operator deleted model 2, created model 3, was entering trades).
  Consequence absorbed: tests moved to a throwaway model; the anomaly (his 6/1
  entries above that day's stored session range) was FLAGGED, not "fixed".
- **Verification:** full lifecycle on `ZZ Selftest` model incl. commit dry-run
  against a tmp vault dir (zero side effects); sandbox unlink EPERM discovered
  → app code hardened (try/except), leftover reported for manual rm.
- **Patterns:** recheck shared state; throwaway fixtures; flag-don't-fix
  operator data; environment honesty; memory updated (roster change).

## Turn 5 — "helper agent — LangGraph like WaiveBoard?"

- **Decision handling:** three genuinely user-owned forks batched into ONE
  question round — framework (recommended AGAINST the heavier one with stated
  reasoning: each v1 workflow = one model call + small loop; seams keep the
  LangGraph lift cheap), provider (recommended against Codex-OAuth-as-API:
  brittle + ToS gray; offered base_url override as the escape hatch), surface.
- **Research before build:** fetched the CURRENT OpenRouter API surface
  (models schema, input_modalities, tool filters) rather than trusting
  training-data memory of an API.
- **Build:** one file, three seams (client / tool registry / bounded loop);
  key masked everywhere; OCR merge = manual text survives, `auto:` block
  replaced on re-run, name filled only if blank (the merge-never-clobber rule
  applied to a NEW subsystem without being asked).
- **Verification:** mock LLM through the real loop (tool dispatch, trace,
  usage), merge-rule unit cases, config round-trip with masking, guard rails;
  the only unverifiable leg (real API call) named explicitly in delivery.
- **Patterns:** clarify-then-build; argue against complexity; research current
  APIs; propagate house rules unprompted; name what wasn't verified.

## Turn 6 — "What are MFE/MAE? Automate? Setup dropdown?"

- **Explain, then automate with the house semantics:** auto-compute ONLY when
  both fields blank (typed values win forever), from the persisted bars,
  bounded by exit_time / first-touch / EOD.
- **Verification with independent recomputation:** expected MFE/MAE hand-walked
  from raw bars in the test, asserted equal to the endpoint's output. A
  surprise (exit-bounded MAE 1.94 > first-touch 1.34) was reasoned through and
  recognized as CORRECT domain behavior (wicks through the stop are real heat
  if the trade lived longer) — not patched away.
- **Consistency design:** dropdown fed by a per-model `setup_tags` list stored
  as part of the model definition (edited where rules live), union'd with
  in-use tags so legacy rows stay valid.
- **Patterns:** teach + build; never-clobber semantics; independent math
  verification; interrogate surprises; data-consistency via source-of-truth
  lists.

## Turns 7–9 — git

- Discovered no repo existed (a .gitignore stub ≠ a repo); chose repo root to
  include docs; gitignored ALL personal data (DB, drafts, audio, agent key)
  and verified 0 tracked matches before committing; wrote a change-grouped
  commit message; handed the push to the operator (his creds); when sandbox
  lock litter blocked his `git gc`, explained exactly what happened and the
  one-line fix. Triage noise (gh upgrade nag) as noise.
- **Patterns:** privacy-first VCS setup; verify exclusions; environment
  honesty; creds stay with their owner.

## Turn 10 — "GLM 5.2 not available"

- **Debug from the system of record:** one catalog lookup
  (`/api/v1/model/z-ai/glm-5.2` → `input_modalities: ["text"]`) collapsed the
  whole hypothesis space (providers, allowlists, keys). Explained the
  filter-vs-gate distinction (vision picker filters by image input; typing any
  id still saves) and prescribed the correct pairing (5.2 for chat, 5v-turbo
  for vision).
- **Patterns:** authoritative-source debugging; one lookup > three theories;
  explain the mechanism, not just the fix.

## Meta

The through-line: every turn ends with something VERIFIED, the operator's
required actions named, and the world-model (memory/skills) updated when
reality shifted. Confidence comes from observation, not fluency.
