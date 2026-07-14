---
name: fable-dev-method
description: Cross-project development method distilled from Fable 5 work sessions with bang — the reasoning, decision-making, and verification patterns that produce trustworthy delivery on live systems. Use at the START of any non-trivial development, debugging, data-pipeline, or automation session in any of bang's projects (BT Journal, WaiveBoard, Paperclip/Cortana, trading tools, client apps), and re-read when stuck, when a tool/environment misbehaves, when results surprise, or when about to write to a system the operator also uses live. Trigger on "plan this build", "how should we approach", session kickoffs from handoff docs, multi-step feature requests, and any moment where the next action would be a guess. This is the method LAYER — project skills (bt-journal-dev, nq-eob, paperclip-triage) supply the domain specifics.
---

# Fable Dev Method

Portable patterns for high-trust delivery. Each earned its place in a real
session (see `references/session-2026-07-05-worked-example.md` for the full
turn-by-turn extraction these were distilled from).

## 1. Ground before you act

- **Handoffs are claims, not facts.** On resuming from any handoff/memory,
  verify the load-bearing assertions against disk/DB before building on them
  (routes registered, row counts, ids, file presence). Cheap: one script.
  Note nits found (a wrong column name in a handoff caught early is an hour
  saved later).
- **Recheck shared state before every write session.** If the operator uses
  the system live, your morning's facts are stale by afternoon. A model
  deleted mid-session is normal, not exceptional. Never write against a
  cached roster; `SELECT` first.
- **Read the code you're about to change, in dependency order,** before the
  first edit — and read the *integration points* (who includes the router,
  where's the cache-bust, what's the save pipeline) not just the target file.

## 2. Decide with the user only where it's theirs to decide

- Batch the genuinely user-owned forks into ONE structured question round
  (framework choice, provider, surface area) with a recommendation and the
  reasoning stated. Everything conventional: pick the obvious default, say
  so, proceed.
- **Argue against complexity you'd profit from.** When asked "should we use
  <big framework>?", evaluate against the actual v1 workloads. If each
  workflow is one model call + a small loop, say so — build minimal with
  clean seams (provider / tools / loop) so the framework lift stays cheap
  later. Consistency-with-other-apps is a real argument; weigh it, don't
  reflexively defer to it.
- **Refuse brittle auth paths** even when the user suggests them (OAuth
  tokens designed for a specific CLI used as a general API = refresh pain,
  ToS gray zone). Offer the configurable escape hatch instead (base_url
  override) so the door stays open without the liability.

## 3. Blocked ≠ stalled — pivot to adjacent value

When the planned task can't proceed (no marked chart, missing input, absent
operator), don't idle and don't guess: switch to the highest-value
*unambiguous* item in the same workstream (the known-pending backfill), do it
fully, then report the blockage with a concrete next-step ask. One turn
delivers value AND the question.

## 4. The verification ladder

Claim nothing you didn't observe. In order of preference:
1. **Canonical path in-process** — call the app's own endpoint functions,
   not re-implemented SQL, so the test exercises real code.
2. **Independent recomputation** — for math, derive expected values by a
   second route (hand-walk the bars) and assert equality.
3. **Throwaway fixtures on live systems** — `ZZ Selftest` records created
   via real endpoints, full lifecycle, deleted after; assert the live data
   untouched. Never test on operator rows.
4. **Mocked externals** — fake the LLM/provider client to verify loops,
   dispatch, and traces without keys or spend.
5. **Static checks** — `node --check`, import-time route listing, schema
   pragmas.

When a verified result SURPRISES (a bounded-window MAE exceeding the
first-touch MAE), stop and reason about whether it's *correct* before
"fixing" it. Sometimes the surprise is the domain teaching you.

## 5. Debug from authoritative sources, not vibes

"X doesn't work" → find the system of record and look: the OpenRouter model
catalog entry (input_modalities) beats theories about keys/providers; a
`location.href` probe beats assuming tab_switch worked; `pragma table_info`
beats remembering a column name. One authoritative lookup usually replaces
three hypotheses. Distinguish **filters from gates** when explaining (a
dropdown that suggests isn't a wall that blocks).

## 6. Environment honesty

- Know your sandbox's specific disabilities (background processes reaped,
  mount unlink EPERM, creds absent) and design around them instead of
  fighting: in-process tests instead of servers; try/except unlinks + tell
  the operator what to `rm`; local commits + hand the push over.
- When your tooling damages the operator's environment (stale git locks you
  can't delete), say exactly what happened, why, and the one-line fix.
- **Never expose sandbox paths** to the operator; translate to their world.

## 7. Machine writes on human data

- **Merge, never clobber**: human-entered fields always survive; machine
  text is namespaced (`auto:` prefix) and re-runs replace only the machine
  block; auto-computation fills only blanks.
- **Judgment fields stay blank** on machine inserts — labeling is the
  human's edge.
- **Plausibility cross-checks before persisting derived data** (prices vs
  session range); on mismatch, flag loudly and skip, don't average away.

## 8. Close the loop

Every ship ends with: what changed, what was VERIFIED (not "should work"),
what the operator must do (restart/refresh/push/key), anomalies noticed in
their data (flag, don't fix unprompted), and memory/skill updates when the
world-model changed (roster changes, new conventions, environment quirks).
Terse. Lead with the outcome.

## References

- [references/session-2026-07-05-worked-example.md](references/session-2026-07-05-worked-example.md)
  — the full turn-by-turn extraction (reasoning → decision → execution →
  delivery) from the session these patterns were distilled from.
