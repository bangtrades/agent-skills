# Canonical Triage Commands

Copy-paste-ready commands a QA agent uses during triage. Every command has a purpose tag, expected output shape, and the failure mode it screens for.

All paths assume the Cortana host root `/Users/nolan/Cortana/platform`. Adjust for other deployments.

## 1. Audit-log ground truth (the most important command)

Pulls every memory operation for an agent in the last 15 minutes. Use this to prove or disprove "did the tools actually fire?"

```bash
SYMBA=0ac0a120-31a2-44c2-b30e-97569a2dc913   # replace with target agent
SMOKE_START="$(date -u -v -15M +%Y-%m-%dT%H:%M:%S.000Z 2>/dev/null \
              || date -u -d '15 min ago' +%Y-%m-%dT%H:%M:%S.000Z)"

jq -c --arg a "$SYMBA" --arg t "$SMOKE_START" \
   'select(.agent_id==$a and .ts > $t)' \
   /Users/nolan/Cortana/platform/logs/cortana-llm-router/memory-execution.jsonl
```

**Healthy output** (per row): `decision="allowed"`, `audit_category="live_<op>_success"`, `transport="native_cli_bridge"` (or `"router_tool_loop"` for router-lane), `capability_state.ok=true`, `lifecycle_state="live"`, `live_switch_state.all_switches_open=true`.

**Zero rows**: tools did NOT fire in this window. The model fabricated the result OR the dispatch was blocked at a router gate (check refusals.jsonl).

**`decision="refused"` rows**: read `refusal_reason` for the specific gate. Common: `live_memory_write_approval_missing` (need grant-write), `memory_read_target_missing` (file doesn't exist), `memory_capability_missing` (marker absent / expired).

## 2. Token-usage heuristic (quick hallucination screen)

When a run says `succeeded` but the audit log is empty, check token usage. A real tool-loop with N memory calls produces N × 200+ output tokens for the tool_use/tool_result/final-text triplets.

```bash
RUN_ID=<heartbeat-run-uuid>
docker exec cortana-postgres psql -X -U cortana -d cortana -c \
  "SELECT result_json->'usage'->>'input_tokens' AS in_t,
          result_json->'usage'->>'output_tokens' AS out_t,
          result_json->>'stopReason' AS stop_reason,
          result_json->>'taskCompleteCandidate' AS task_complete
     FROM heartbeat_runs WHERE id='${RUN_ID}'"
```

| out_t | Diagnosis |
| --- | --- |
| < 200 | Almost certainly no tool loop fired. Verify with audit log. |
| 200–800 | Single tool call or short summary; verify operations match the expected count. |
| 800+ | Multi-tool loop ran; cross-check audit row count matches expected operations. |

## 3. Source-level proof — read the adapter argv builder

When config patches keep failing, read the actual composition logic.

```bash
# Locate the adapter package
find /Users/nolan/Cortana/platform/workspaces/paperclip/packages/adapters \
  -name "execute.ts" -o -name "execute.js" 2>/dev/null

# Read the argv-build function
grep -nE "dangerously-skip-permissions|permission-mode|extraArgs|asBoolean" \
  /Users/nolan/Cortana/platform/workspaces/paperclip/packages/adapters/<ADAPTER>/src/server/execute.ts \
  | head -40

# Check the helper's default semantics
grep -nB2 -A6 "export function asBoolean" \
  /Users/nolan/Cortana/platform/workspaces/paperclip/packages/adapter-utils/src/server-utils.ts
```

Critical fact: `asBoolean(value, fallback)` defaults to the fallback when the value is missing or not a literal boolean. Missing keys evaluate to fallback, NOT false.

## 4. Source-level proof — extract a compiled binary's gate

When a CLI's behavior contradicts its docs, read the actual conditional gate.

```bash
# Locate the compiled CLI
docker exec cortana-paperclip sh -c \
  'find / -path "*<cli-name>*" -type f \( -name "*.js" -o -name "*.mjs" -o ! -name "*.*" \) \
   2>/dev/null | head -10'

# Find the file containing a known error string
docker exec cortana-paperclip sh -c \
  'find / -path "*claude-code*" -type f 2>/dev/null \
   | xargs grep -l "cannot be used with root" 2>/dev/null | head -1'

# Extract the printable strings + surrounding context
docker exec cortana-paperclip sh -c \
  'tr -c "[:print:][:space:]" "\n" < <located-file> \
   | grep -B2 -A6 "<error-or-flag-string>"'
```

This works on ELF binaries, minified JS bundles, and esbuild output. The printable strings carry conditional logic verbatim.

## 5. Postgres row inspection — agent adapter_config

```bash
docker exec cortana-postgres psql -X -U cortana -d cortana -c \
  "SELECT id, name, adapter_type,
          adapter_config->'memoryBridge'->>'transport' AS transport,
          adapter_config->'mcp_servers'->'cortana-memory'->'env'->>'CORTANA_AGENT_ID' AS mcp_agent_id,
          adapter_config->>'dangerouslySkipPermissions' AS dsp,
          adapter_config->'extraArgs' AS extra_args,
          adapter_config->'env' AS env
     FROM agents WHERE id='<agent-uuid>'"
```

Full pretty-print (use sparingly — adapter_config can be large):

```bash
docker exec cortana-postgres psql -X -U cortana -d cortana -c \
  "SELECT jsonb_pretty(adapter_config) FROM agents WHERE id='<agent-uuid>'"
```

## 6. Authenticated wakeup — the canonical dispatch lane

```bash
# Mint a 1h board_api_key. Keep TTL short during triage; revoke at end.
TOKEN="pcp_board_$(openssl rand -hex 24)"
HASH="$(printf '%s' "$TOKEN" | shasum -a 256 | awk '{print $1}')"
docker exec -i cortana-postgres psql -X -v ON_ERROR_STOP=1 -U cortana -d cortana <<SQL
INSERT INTO board_api_keys (user_id, name, key_hash, expires_at)
VALUES ('<operator-user-id>', '<slice-name>', '${HASH}', NOW() + INTERVAL '1 hour')
RETURNING id, name, expires_at;
SQL

# Fire the wakeup. forceFreshSession=true is critical during triage.
SYMBA=<agent-uuid>
curl -sS -o /tmp/wakeup.body -w '%{http_code}\n' \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  --data '{"source":"on_demand","triggerDetail":"manual","reason":"<distinctive-label>","forceFreshSession":true}' \
  http://localhost:4200/api/agents/${SYMBA}/wakeup

cat /tmp/wakeup.body | jq '{id, status, wakeupRequestId, "contextSnapshot.issueIdentifier": .contextSnapshot.issueIdentifier}'

# Revoke at end.
docker exec -i cortana-postgres psql -X -v ON_ERROR_STOP=1 -U cortana -d cortana <<SQL
UPDATE board_api_keys SET revoked_at=NOW() WHERE name='<slice-name>' AND revoked_at IS NULL;
SQL
rm -f /tmp/wakeup.body
```

**Body schema** (`wakeAgentSchema`):
- `source` ∈ {`timer`, `assignment`, `on_demand`, `automation`} (default `on_demand`)
- `triggerDetail` ∈ {`manual`, `ping`, `callback`, `system`}
- `reason` — string | null, free-form
- `forceFreshSession` — bool (default false)
- `payload` — object | null
- `idempotencyKey` — string | null

## 7. Runtime probe — claude CLI without burning API credits

Test whether the root-permission gate is past WITHOUT making a real provider call:

```bash
# Point CLAUDE_CONFIG_DIR at a non-existent path to keep credentials out of the probe.
docker exec -e CLAUDE_CONFIG_DIR=/nonexistent-claude-home -e IS_SANDBOX=1 \
  cortana-paperclip claude \
    --print --output-format=stream-json --verbose \
    --model claude-opus-4-6 \
    --permission-mode bypassPermissions \
    "echo test"
```

**Expected outcomes**:
- `--dangerously-skip-permissions cannot be used with root/sudo privileges` → root gate is STILL CLOSED (config not fully fixed)
- `Not logged in · Please run /login` → root gate PASSED; missing creds because we pointed at /nonexistent. In production with real `/state/claude-home`, this would proceed.

## 8. Heartbeat run inspection

```bash
RUN_ID=<run-uuid>
docker exec cortana-postgres psql -X -U cortana -d cortana -c \
  "SELECT id, status, started_at, finished_at, exit_code, error_code, stderr_excerpt
     FROM heartbeat_runs WHERE id='${RUN_ID}'"
```

Full result JSON:

```bash
docker exec cortana-postgres psql -X -U cortana -d cortana -c \
  "SELECT jsonb_pretty(result_json) FROM heartbeat_runs WHERE id='${RUN_ID}'"
```

Run events (lifecycle + tool_call + tool_result + assistant.text + stdout/stderr):

```bash
docker exec cortana-postgres psql -X -U cortana -d cortana -c \
  "SELECT seq, event_type, stream, level,
          COALESCE(payload->>'name', LEFT(message, 80)) AS detail
     FROM heartbeat_run_events
    WHERE run_id='${RUN_ID}'
    ORDER BY seq ASC"
```

Look for `tool_call` / `tool_result` rows. Absence + `status=succeeded` = model fabricated the result (cross-check with audit log).

## 9. Marker integrity check

```bash
ls -la /Users/nolan/Cortana/platform/state/cortana-memory/*.marker
cat /Users/nolan/Cortana/platform/state/cortana-memory/live-dispatch-approved.marker | jq '.'
cat /Users/nolan/Cortana/platform/state/cortana-memory/live-write-approved.marker | jq '.'
```

Per-marker fields to verify:
- `agent_id` (or `agent_ids[]`) contains the target uuid
- `expires_at` is in the future
- For write markers: `write_paths_allowlist` covers the smoke's paths
- `paired_canonical_expires_at` ≤ the read marker's `expires_at`

## 10. Codex Smoke regression (canonical control baseline)

After ANY platform-level change, re-run this. If it goes RED, the change regressed the proven path:

```bash
bash /Users/nolan/Cortana/platform/scripts/verify-s10i-6-controlled-codex-memory-smoke.sh --json
```

Expect `FINAL CLASSIFICATION: GO_NATIVE_CLI_BRIDGE` and `checks: pass=8 fail=0`.

## 11. Adapter container introspection

```bash
# Which adapters are even installed inside the dispatcher container?
docker exec cortana-paperclip which claude codex opencode cursor 2>&1

# Versions
docker exec cortana-paperclip sh -c 'claude --version 2>&1; codex --version 2>&1'

# Environment variables visible to the dispatcher
docker exec cortana-paperclip env | grep -iE "PAPERCLIP|CORTANA|CLAUDE|CODEX|HOME"

# In-flight CLI processes (during a run)
docker exec cortana-paperclip ps -ef | grep -E "claude|codex|cortana-memory-mcp" | grep -v grep
```

## 12. Router readiness

```bash
curl -sS http://127.0.0.1:4400/readyz | jq '{
  service, boot_id, dispatchable_to_providers,
  extension_registry: .extension_registry | {
    skill_registry_source,
    skill_registry_activated_ids,
    skill_registry_skipped_ids,
    class_executor_status,
    degraded_reasons
  }
}'
```

Healthy: non-empty `dispatchable_to_providers`, `extension_registry.loaded=true`, `degraded_reasons=[]`.

## 13. Router config knob check (S10J-7)

```bash
docker exec cortana-llm-router python3 -c \
  "import os; from lib.tool_execution import _resolve_default_max_iterations; \
   print('default=', _resolve_default_max_iterations()); \
   print('env=', os.environ.get('CORTANA_TOOL_LOOP_MAX_ITERATIONS','(unset)'))"
```

Expect default=12 (or whatever the env override sets, clamped to [1,32]).

## 14. Backup-before-mutate pattern (postgres rows)

```bash
TS=$(date -u +%Y%m%dT%H%M%SZ)
BACKUP="/Users/nolan/Cortana/platform/state/migrations/<agent>-pre-<change>-${TS}.json"
# Refuse if backup already exists
test -e "$BACKUP" && { echo "backup exists; abort"; exit 2; }

# Read row, write backup with 0600
docker exec cortana-postgres psql -X -At -U cortana -d cortana -c \
  "SELECT row_to_json(a) FROM agents a WHERE id='<agent-uuid>'" > "$BACKUP"
chmod 0600 "$BACKUP"

# THEN run the UPDATE in a separate command (so a backup failure halts BEFORE mutation)
docker exec -i cortana-postgres psql -X -v ON_ERROR_STOP=1 -U cortana -d cortana <<'SQL'
BEGIN;
UPDATE agents SET adapter_config = ... WHERE id = '<agent-uuid>';
COMMIT;
SQL
```

## 15. Issue + wakeup orphan cleanup

```bash
# Find queued wakeup_request rows with no run claim (orphans from wrong-lane attempts)
docker exec cortana-postgres psql -X -U cortana -d cortana -c \
  "SELECT id, agent_id, source, requested_at
     FROM agent_wakeup_requests
    WHERE status='queued' AND requested_at < NOW() - INTERVAL '1 hour'
    ORDER BY requested_at DESC LIMIT 10"

# Retire an orphan
docker exec cortana-postgres psql -X -U cortana -d cortana -c \
  "UPDATE agent_wakeup_requests
      SET status='skipped', finished_at=NOW(), error='superseded by triage'
    WHERE id='<wakeup-uuid>' AND status='queued'"

# Sweep revoked board_api_keys older than 7 days (hygiene)
docker exec cortana-postgres psql -X -U cortana -d cortana -c \
  "DELETE FROM board_api_keys WHERE revoked_at IS NOT NULL AND revoked_at < NOW() - INTERVAL '7 days'"
```

## 16. Cross-pillar regression matrix (post-upgrade)

Run all four after any pillar-level change:

```bash
cd /Users/nolan/Cortana/platform

# Memory pillar
./scripts/cortana-memory-mcp-status.sh --json
./scripts/verify-s10i-4-native-cli-memory-bridge.sh --json
./scripts/verify-s10i-6-controlled-codex-memory-smoke.sh --json
./scripts/verify-s10i-12-native-memory-e2e.sh --json

# Adapter classification (when STEP-46 amendments land)
./scripts/verify-s10j-4-shared-memory-isolation.sh --json

# Sustained window (memory pillar stability over 7 days)
./scripts/verify-s10j-5-sustained-window.sh --json
```

Every gate that goes from GREEN → RED on an upgrade is a regression to classify and fix before declaring the upgrade complete.

## Quick reference — common error → first command to run

| Failure symptom | First command |
| --- | --- |
| `Tool names must be unique` (Anthropic 400) | `SELECT skill_id FROM agent_skills WHERE agent_id='...'` (Pattern F dedup) |
| `non_retryable_tool_loop` | Run #1 (audit log) — zero rows = adapter-class mismatch (Pattern A) |
| `live_memory_write_approval_missing` despite marker present | `cat live-write-approved.marker` — check expiry, agent_ids[], write_paths_allowlist |
| `--dangerously-skip-permissions cannot be used with root/sudo` | Run #4 (extract gate) → Run #5 (inspect adapter_config) → 3-key fix (Pattern E) |
| `succeeded` but no audit rows | Run #2 (token heuristic) → Run #1 (audit log) — confirm hallucination (Pattern B) |
| Wakeup row stays `queued` forever | Run #6 (use POST /api/agents/:id/wakeup, not direct INSERT) (Pattern D) |
| Retry skips work | `forceFreshSession: true` OR clear session via UI (Pattern C) |
| MCP visible but tool calls cancelled | Check `default_tools_approval_mode = "auto"` in MCP toml (Pattern H) |
| Agent does unrelated work | Verify `paperclipTaskMarkdown` in adapter prompt assembly (Pattern G) |
| Static gates GREEN but smoke RED | File a fresh sequential controlled issue, not a reopen (Pattern J) |
