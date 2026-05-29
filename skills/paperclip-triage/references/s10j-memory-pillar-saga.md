# S10J Memory Pillar Saga — Two Days of Misdiagnoses, Then Source-Level Truth

This case study covers the May 16–18, 2026 effort to bring Symba's memory pillar GREEN. It cost two days of patching and several misleading "almost done" signals. The lessons here are canonical for adapter-class mismatches, model hallucinations of tool calls, dispatch-lane confusion, session-state contamination, and the claude-code root-permission gate. A QA agent that internalizes this saga will save days on the next analogous incident.

## Cast

- **Symba** — agent uuid `0ac0a120-31a2-44c2-b30e-97569a2dc913`, role CEO, originally on `cortana_llm_router` adapter
- **Codex Smoke** — agent uuid `fe014446-1aca-4408-8d4f-b478e3f4d1cf`, on `codex_local`, GREEN throughout (control baseline)

## Phase 1 — Patching the wrong adapter (Days 1-2)

**Symptom**: Symba kept failing on her 4-tool memory smoke. Anthropic returned tool_use blocks; Paperclip's classifier flagged `non_retryable_tool_loop`. Audit log showed zero rows for the failed run window.

**False leads chased**:
- Tool-name uniqueness (Anthropic HTTP 400) — fixed by removing `cortana-memory` from `agent_skills` while keeping `memory_enabled=["para-memory-files"]`. Real bug. Pattern F.
- Marker expiry — `live-write-approved.marker` expired at 24h; refreshed to 168h. Real bug.
- `max_iterations=4` was too low — agent's 4-step prompt consumed all iterations on tool dispatches with no iteration left for the final text. Real bug but a symptom of a deeper mismatch.
- Various skills-registry / shim-config patches.

**Root cause finally diagnosed**: The `cortana_llm_router` adapter hides its tool loop server-side. Paperclip's lifecycle classifier expects to see `tool_call` / `tool_result` transcript entries from the adapter (the contract upstream CLI adapters honor). The router-shim returned only the final response with no transcript events; the classifier therefore saw "tool_use present, tool_calls absent" and flagged every run as failed even when the underlying tool dispatch worked.

**Lesson**: The issue was an **adapter-class mismatch** between Symba's stateful, multi-turn use case and `cortana_llm_router`'s one-shot router lane. Stateful agents need a stateful-CLI adapter (claude_local, codex_local). Codex Smoke worked because it was already on the right class.

**Resolution (S10J-6, S10J-7, S10J-8)**:
- Migrate Symba to `claude_local` (transport flips from `router_tool_loop` to `native_cli_bridge`)
- Synthesize Paperclip-shaped transcript events from router's `tool_loop_audit_rows` in the shim for any remaining router-lane agents (S10J-7)
- Raise `max_iterations` default 4 → 12, env-overridable
- Write STEP-46 with the adapter classification and deprecation policy: **no new stateful agents on `cortana_llm_router`**

## Phase 2 — Dispatch lane confusion (S10J-INTEGRATE)

**Symptom**: Cutover landed in postgres but Symba's controlled smoke never dispatched.

**False lead**: Directly `INSERT INTO agent_wakeup_requests` (the lane the harness brief prescribed).

**Diagnosis**: Paperclip's dispatcher claims `heartbeat_runs.status='queued'` rows, not `agent_wakeup_requests` rows. The translation happens inside `heartbeat.wakeup(...)`, which is called by the authenticated `POST /api/agents/:id/wakeup` endpoint. An orphan `agent_wakeup_requests` row with no matching heartbeat_run is never claimed.

**Resolution (S10J-INTEGRATE-2)**:
- Discover the canonical auth lane: `Authorization: Bearer pcp_board_<48hex>`; key minted in `board_api_keys` table, secret never echoed, revoked at slice end
- Token shape: `pcp_board_<48 hex chars>`; hash: `sha256(token)` → `key_hash`
- Use `POST /api/agents/:id/wakeup` with body `{"source": "on_demand", "triggerDetail": "manual", "reason": "<distinctive>", "forceFreshSession": true}`

## Phase 3 — claude-code root-permission gate (S10J-INTEGRATE-3, -4)

**Symptom**: After cutover + auth lane, claude exits code 1 with `--dangerously-skip-permissions cannot be used with root/sudo privileges for security reasons`. Duration: <1 second. No tool calls fire.

**False starts**:
- Set `IS_SANDBOX=1` env var alone — necessary but not sufficient
- Add `--permission-mode bypassPermissions` to extraArgs alone — also blocked by the same gate
- Remove `dangerouslySkipPermissions` from adapter_config — believed but not verified to actually clear the argv flag

**Source-level proof (the breakthrough)**:

Read paperclip's adapter argv builder at `workspaces/paperclip/packages/adapters/claude-local/src/server/execute.ts:318`:

```typescript
const dangerouslySkipPermissions = asBoolean(config.dangerouslySkipPermissions, true);
```

The `asBoolean(value, fallback)` helper at `packages/adapter-utils/src/server-utils.ts:194`:

```typescript
export function asBoolean(value: unknown, fallback: boolean): boolean {
  return typeof value === "boolean" ? value : fallback;
}
```

**The default fallback is `true`**. Removing the field doesn't disable it. You must set the field to a literal JSON boolean `false`. Setting it to a string `"false"` or null preserves the default.

Then extract the compiled claude-code v2.1.143 root-gate from the binary:

```
docker exec cortana-paperclip sh -c \
  'find / -path "*claude-code*" -type f \( -name "*.js" -o -name "*.mjs" \) 2>/dev/null | head -1 \
   | xargs grep -l "cannot be used with root" 2>/dev/null'
# then for the located binary/file:
docker exec cortana-paperclip sh -c \
  'tr -c "[:print:][:space:]" "\n" < <located-file> | grep -B2 -A4 "cannot be used with root"'
```

Result (cleaned):

```javascript
if (K === "bypassPermissions" || _) {
  if (process.getuid() === 0
      && process.env.IS_SANDBOX !== "1"
      && !b8(process.env.CLAUDE_CODE_BUBBLEWRAP)) {
    console.error("--dangerously-skip-permissions cannot be used with root/sudo "
                  + "privileges for security reasons");
    process.exit(1);
  }
}
```

**Both** the legacy flag `_` AND the new flag `--permission-mode bypassPermissions` trigger the gate. Only `IS_SANDBOX=1` (or `CLAUDE_CODE_BUBBLEWRAP`) opens it.

**Resolution — all three keys required**:

```sql
UPDATE agents SET adapter_config = adapter_config
  || '{"dangerouslySkipPermissions": false}'::jsonb
  || jsonb_build_object('extraArgs', '["--permission-mode","bypassPermissions"]'::jsonb)
  || jsonb_build_object('env', COALESCE(adapter_config->'env','{}'::jsonb) || '{"IS_SANDBOX":"1"}'::jsonb)
WHERE id = '<agent-uuid>';
```

Mirror the on-disk canonical config (`config/cortana/agents/<agent>.claude-local.json`) so future re-migrations stay consistent.

**Runtime probe without API call**: point `CLAUDE_CONFIG_DIR` at a non-existent path; if the failure changes from the root-permission error to `Not logged in · Please run /login`, the gate is past.

## Phase 4 — Model hallucinates tool calls (post-fix, pre-GREEN)

**Symptom**: heartbeat_run `status=succeeded`, terminal marker `MEMORY-SMOKE-COMPLETE` present in result text, but `memory-execution.jsonl` shows zero new rows in the run window.

**False conclusion**: I assumed Symba was hallucinating tool calls in the run we examined. I was wrong — the audit log eventually proved the calls DID fire (in a separate session). But the hallucination pattern is real and showed up in earlier runs.

**Reliable verification, in order**:

1. **Audit log row count** — the ground truth. Zero rows in the run window = no dispatch, regardless of `status=succeeded` or terminal marker.
2. **Token usage heuristic** — output tokens < 200 for a multi-tool smoke is suspicious. A real loop with N tool calls produces ~N × 200+ output tokens for the tool_use + tool_result + final text. Sub-200 = likely text-only.
3. **Heartbeat run events** — `SELECT kind FROM heartbeat_run_events WHERE run_id=...` looking for `tool_call` / `tool_result` rows. Absence proves nothing fired (though some transports route tool execution through MCP subprocesses that don't always emit heartbeat events — verify with the audit log first).

**Anti-hallucination prompt design**:
- Reject any continuation summary claiming prior completion
- Force first output token to be a `tool_use` block opening
- Explicitly tell the model: "Audit log is ground truth. Zero rows = fabricated response."
- Use `forceFreshSession: true` on every wakeup during triage

## Phase 5 — Session-state contamination (final shape)

**Symptom**: Retried run from Paperclip UI emits `MEMORY-SMOKE-COMPLETE` instantly, no tool calls fire, issue gets marked done by the agent calling the `paperclip` skill — but the underlying tools never ran.

**Diagnosis**: `agentTaskSessions` persists session keys per agent-task pair. Claude/Codex resume the prior session and inherit its prior context — including hallucinated completion claims from older failed runs. On retry, the agent reads "this was already done" from the session state and short-circuits.

**Fix**:
- Paperclip UI: "clear session for these issues" button on the run page
- API: `{"forceFreshSession": true}` on the wakeup body
- Best: file a fresh issue (not a retry) so the session key is brand new

## Phase 6 — GREEN proof

The canonical 4-row audit proof for Symba's first true GREEN smoke:

```jsonc
{"ts":"2026-05-18T20:43:01.157Z","operation":"write","decision":"allowed","audit_category":"live_write_success",
 "transport":"native_cli_bridge","bytes_written":135,"relative_path":"smoke/s10j-fresh-002.md",
 "agent_id":"0ac0a120-31a2-44c2-b30e-97569a2dc913","extension_id":"para-memory-files",
 "capability_state":{"granted_subset":["memory_para_files_read","memory_para_files_write"],"ok":true},
 "live_switch_state":{"all_switches_open":true}}
{"ts":"2026-05-18T20:43:04.158Z","operation":"read","decision":"allowed","audit_category":"live_read_success",
 "transport":"native_cli_bridge","bytes_read":135,"relative_path":"smoke/s10j-fresh-002.md", ...}
{"ts":"2026-05-18T20:43:06.793Z","operation":"list","decision":"allowed","audit_category":"live_list_success",
 "transport":"native_cli_bridge","item_count":5,"relative_path":"smoke/", ...}
{"ts":"2026-05-18T20:43:09.043Z","operation":"search","decision":"allowed","audit_category":"live_search_success",
 "transport":"native_cli_bridge","item_count":1,"search_query_length":32, ...}
```

Time window: 9 seconds. Four ops covering write/read/list/search. All `decision=allowed`. All `transport="native_cli_bridge"` (the MCP path, same lane Codex Smoke uses). All capability gates and live switches open.

## Lessons distilled

1. **Adapter-class mismatch produces failures that look like config bugs.** Always classify the adapter against the use case before patching. STEP-46 is the contract.
2. **The audit log is the only ground truth.** Status fields, terminal markers, transcript widgets, and even token counts are secondary signals. A run can `succeed` administratively with zero tool dispatch.
3. **Source-level proof beats config-shape speculation.** Reading 50 lines of `execute.ts` saved 2 days of patches. Always read the adapter's argv builder and the binary's gate string before guessing config.
4. **Defaults matter.** `asBoolean(value, true)` means missing keys evaluate to true. Removing a field doesn't disable a feature; you must set it to a literal `false`.
5. **The dispatch lane has authentication.** `agent_wakeup_requests` is bookkeeping; `heartbeat_runs.status='queued'` is the dispatch queue, created transactionally inside `heartbeat.wakeup(...)` behind board_api_key auth.
6. **Sessions persist hallucinations.** Always `forceFreshSession: true` during triage. Prefer fresh issues over retries when validating fixes.
7. **Slice briefs need branching contracts.** Every failure mode gets a distinct ABORT code. Never plow through partial success.
8. **Operator-vs-agent boundaries are explicit.** Some actions require UI clicks (session clear, board sign-in). Name them in the slice brief; halt and hand off when they're needed.
9. **Backup before mutate.** Always read-row → write-backup → compute-target → UPDATE. Refuse if the backup file already exists for the run-ts.
10. **A working control baseline is priceless.** Codex Smoke stayed GREEN throughout. That regression baseline pinned every change as "did the cutover break Codex?" with one verifier command. Never triage without a working baseline.

## Cross-references

- `docs/STEP-37-paperclip-native-memory-architecture.md` — STEP-37 §6 audit row schema (the 22 fields every memory dispatch must stamp)
- `docs/STEP-46-cortana-adapter-classification.md` — adapter classes + deprecation policy
- `docs/STEP-47-agent-harness-contract.md` — agent harness scaffold (S10K-1)
- `docs/agent-reports/agent-1-s10j-6-symba-claude-local-migration.md` — staging the cutover
- `docs/agent-reports/agent-2-s10j-7-router-shim-paperclip-compat.md` — transcript synthesizer + max_iterations
- `docs/agent-reports/agent-4-s10j-8-adapter-classification-and-sprint-close.md` — STEP-46 origin
- `docs/agent-reports/agent-3-s10k-1-agent-harness-scaffold.md` — agent harness
- `docs/agent-reports/agent-1-s10j-integrate-memory-pillar-cutover.md` — wrong dispatch lane
- `docs/agent-reports/agent-1-s10j-integrate-2-symba-smoke-dispatch.md` — auth lane discovered
- `docs/agent-reports/agent-1-s10j-integrate-3-permission-fix-and-green.md` — IS_SANDBOX landed (insufficient alone)
- `docs/agent-reports/agent-1-s10j-integrate-4-symba-config-lockdown.md` — source-level proof + 3-key lockdown
