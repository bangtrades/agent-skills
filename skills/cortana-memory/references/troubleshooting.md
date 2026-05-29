# Memory Pillar Troubleshooting

Memory-specific failure patterns and canonical diagnostic commands. For cross-pillar patterns (model hallucination, session contamination, wrong dispatch lane, claude root gate, etc.) load `paperclip-triage` alongside.

## Diagnostic ordering — always

1. **Audit log first.** `logs/cortana-llm-router/memory-execution.jsonl` is ground truth. Never reason about memory dispatch without checking the audit log for the window.
2. **Decision field next.** `decision="allowed"` vs `decision="refused"` is the first split. Refusals carry a `refusal_reason` and an `audit_category` — both name the gate that closed.
3. **Marker / capability state third.** When `audit_category=refused_*`, inspect the marker or capability the audit row names.
4. **Transport / lifecycle fourth.** Wrong transport or non-live lifecycle indicates a routing or backend issue.
5. **Cross-pillar checks fifth.** If audit log is empty and the agent claims a dispatch happened, the failure is upstream (model, harness, skills, task management) — load `paperclip-triage` and run the cross-pillar patterns.

## Memory-specific failure patterns

### M-1 — Marker expired

**Symptom**: Audit row shows `decision="refused"`, `audit_category="refused_marker_expired"`, `approval_state="EXPIRED"`. Agent's `cortana_memory_*` calls all fail.

**Diagnosis**:
```bash
cat /Users/nolan/Cortana/platform/state/cortana-memory/live-dispatch-approved.marker | jq '{expires_at, issued_at, agent_ids}'
date -u
```
The `expires_at` is in the past.

**Fix**: Re-grant the read marker. See `operations.md` § "grant read approval".

**Prevention**: Track marker TTL; set up a daily check + 24h-before-expiry alert.

### M-2 — Agent not in marker's agent_ids[]

**Symptom**: Audit row `decision="refused"`, `audit_category="refused_marker_agent_not_listed"`, `approval_state="AGENT_NOT_LISTED"`.

**Diagnosis**:
```bash
AGENT=<uuid>
jq --arg a "$AGENT" \
   '.agent_ids[] | select(. == $a)' \
   /Users/nolan/Cortana/platform/state/cortana-memory/live-dispatch-approved.marker
# Empty output = agent not listed
```

**Fix**: `cortana-memory-live-approval.sh grant` for the agent. Note: grants append to `agent_ids[]`; they do NOT replace.

### M-3 — Write refused despite write marker existing (Pattern from S10J)

**Symptom**: Audit row `audit_category="refused_other"`, `error="live_memory_write_approval_missing"`, but `approval_marker_attempts[].ok=true`.

**Diagnosis**: Write marker is present but failing one of:
1. `expires_at < NOW()` (expired)
2. `agent_id` doesn't match (or agent UUID not in `agent_ids[]` if the marker is multi-agent)
3. `paired_canonical_expires_at` doesn't match the current read marker's `expires_at` (paired-marker drift)
4. Target path doesn't match any glob in `write_paths_allowlist[]`
5. `ceremony_acknowledged != true`

```bash
WRITE_MARKER=/Users/nolan/Cortana/platform/state/cortana-memory/live-write-approved.marker
READ_MARKER=/Users/nolan/Cortana/platform/state/cortana-memory/live-dispatch-approved.marker

jq '{expires_at, paired_canonical_expires_at, agent_id, write_paths_allowlist, ceremony_acknowledged}' "$WRITE_MARKER"
jq '.expires_at' "$READ_MARKER"
date -u
```

Cross-check each field against the failure modes above.

**Fix**: Re-grant write marker with corrected fields. See `operations.md` § "grant write approval". Common mistake: `--expires-hours 168` when only ~150h remain on the read marker; the script refuses; reduce `--expires-hours`.

### M-4 — Write target outside allowlist

**Symptom**: Audit row `audit_category="refused_write_path_not_allowed"`, `relative_path="<some-path-outside-allowlist>"`.

**Diagnosis**:
```bash
jq '.write_paths_allowlist' /Users/nolan/Cortana/platform/state/cortana-memory/live-write-approved.marker
```
Compare against the `relative_path` in the failed audit row.

**Fix**: Either change the agent's prompt to target an allowlisted path, OR re-grant write marker with a broader allowlist. Be specific — don't grant `**/*` unless intentional.

### M-5 — Capability missing

**Symptom**: Audit row `audit_category="refused_capability_missing"`, `capability_state.missing=["memory_para_files_write"]`.

**Diagnosis**:
```bash
AGENT=<uuid>
ls /Users/nolan/Cortana/platform/state/agents/${AGENT}/capabilities/
```
Look for the missing capability marker.

**Fix**: Grant the capability via `scripts/cortana-capability.sh grant`. See `operations.md` § "Grant a capability". Note: capability ≠ approval marker. Both must be present for live dispatch.

### M-6 — Vault scope violation

**Symptom**: Audit row `audit_category="refused_vault_scope_violation"`.

**Diagnosis**:
```bash
jq '.target_path_sha256_prefix, .scope, .relative_path' <audit-row>
```
The agent tried to read or write outside its allowed scope. Common causes:
- Agent A trying to read agent B's private scope
- Agent trying to write to `shared/` (shared is read-only for non-promotion ops)
- Path escapes the vault root (e.g. `../../../etc/passwd`)

**Fix**: Verify the path the agent intended. If legitimate, the path needs to land in the agent's private scope OR be promoted to shared via the candidate ceremony.

### M-7 — Read target missing (file doesn't exist)

**Symptom**: Audit row `audit_category="refused_other"`, `error="memory_read_target_missing"`. Decision is `refused`.

**Diagnosis**: The agent asked to read a path that doesn't exist in the vault.

```bash
AGENT=<uuid>
PATH=<relative-path>
ls -la /Users/nolan/Cortana/platform/state/cortana-memory/${AGENT}/${PATH}
```

**Fix**: Not actually a system error — this is the normal "file not found" path. If the agent is hallucinating the file should exist, fix the agent's prompt or workflow. If the file SHOULD have been written by a prior operation, check the audit log for the write op's outcome.

### M-8 — Lifecycle gate closed

**Symptom**: Audit row `lifecycle_state` is `candidate` or `retired`, audit_category typically `refused_pre_live`.

**Diagnosis**:
```bash
jq '.lifecycle_state, .live_switch_state' <audit-row>
```

**Fix**: The backend is in non-live state. If the backend was deliberately put in candidate (during swap drill), wait for promotion. If retired, the agent needs to be migrated to a live backend. Check `compatibility-matrix.json` for the canonical lifecycle.

### M-9 — Live-switch composition incomplete

**Symptom**: Audit row `live_switch_state.all_switches_open=false` with one or more of `matrix_live_dispatch_enabled`, `module_live_dispatch`, `policy_live_dispatch` set to `false`.

**Diagnosis**: One of the five gates is closed at the matrix / module / policy layer.

```bash
jq '.live_switch_state' <audit-row>
```

- `matrix_live_dispatch_enabled=false` → check `config/cortana/extension-compatibility-matrix.json` for the backend's `live_dispatch_enabled` flag
- `module_live_dispatch=false` → backend's internal kill switch is open
- `policy_live_dispatch=false` → environment / policy gate is closed (`CORTANA_MEMORY_POLICY != allow`)

**Fix**: Flip the appropriate gate. Each is operator-controlled; never auto-open.

### M-10 — Transport drift (agent on wrong lane)

**Symptom**: Stateful agent's audit rows show `transport="router_tool_loop"` instead of `native_cli_bridge`.

**Diagnosis**: Agent's `adapter_type=cortana_llm_router` instead of `claude_local` (or similar stateful-CLI member).

```bash
docker exec cortana-postgres psql -X -U cortana -d cortana -c \
  "SELECT id, adapter_type FROM agents WHERE id='<uuid>'"
```

**Fix**: Migrate to `claude_local` per STEP-46 § 7.1 deprecation. See `operations.md` § "Migrating an agent's memory transport". This was the canonical S10J fix.

### M-11 — Schema floor violation (drift detector)

**Symptom**: Drift detector test (`test_step37_schema_floor.py`) fails. New backend or recent change has dropped a required field.

**Diagnosis**:
```bash
# Inspect the failing row
tail -1 /Users/nolan/Cortana/platform/logs/cortana-llm-router/memory-execution.jsonl | jq 'keys | sort'
# Compare against the 22 required fields in audit-schema.md
```

**Fix**: Re-emit the missing field at the executor / adapter boundary. The schema floor is non-negotiable. Never patch the drift detector to ignore the missing field; fix the emission.

### M-12 — Unknown audit_category

**Symptom**: Drift detector or operator grep shows a value not in the 18-value controlled vocabulary.

**Diagnosis**:
```bash
jq -r '.audit_category' /Users/nolan/Cortana/platform/logs/cortana-llm-router/memory-execution.jsonl | sort -u
```

**Fix**: Either (a) the value is a typo from a backend — fix the backend; (b) the value is legitimately new — admit it through the vocabulary admittance procedure (see `audit-schema.md` § "Vocabulary admittance"). Never let unknown values land silently.

### M-13 — Zero audit rows but agent claims success

**Symptom**: `heartbeat_runs.status=succeeded`, terminal marker in result text, but `memory-execution.jsonl` query returns 0 rows for the window.

**Diagnosis**: This is `paperclip-triage` Pattern B (model hallucination). The model fabricated tool results without firing the tools. Verify:
1. Output token count is suspiciously low (< 200 for a multi-tool smoke)
2. `heartbeat_run_events` has no `tool_call` / `tool_result` rows
3. Session may be carrying a hallucinated completion from a prior run

**Fix**: 
- Force fresh session on next wakeup (`forceFreshSession: true`)
- Use the anti-hallucination forcing-function prompt from `paperclip-triage` Pattern B
- Consider switching the agent's model if the issue is persistent

### M-14 — Audit rows landed but Paperclip's transcript missing tool entries

**Symptom**: 4 rows in `memory-execution.jsonl`, but `heartbeat_run_events` has no `tool_call` / `tool_result` rows.

**Diagnosis**: `transport=native_cli_bridge` rows come through the MCP subprocess. Some Paperclip transcript widgets only render direct `tool_call` events the CLI emits; MCP-bridged calls are recorded in the audit log but not always in the heartbeat events.

```bash
docker exec cortana-postgres psql -X -U cortana -d cortana -c \
  "SELECT event_type, COUNT(*) FROM heartbeat_run_events WHERE run_id='<run-id>' GROUP BY event_type"
```

**Fix**: Not a system error. The audit log is the ground truth. If transcript visibility matters for downstream tooling, file a separate slice to enrich heartbeat events from the audit log (cross-pillar work; harness pillar's responsibility).

### M-15 — Search returns zero matches but file exists

**Symptom**: `audit_category="live_search_success"`, `item_count=0`, but the file exists and contains the query substring.

**Diagnosis**:
1. Check `case_sensitive` — default is false, but verify
2. Check `files_scanned` — was the file actually scanned?
3. Check `files_skipped_binary` / `files_skipped_too_large` — was it skipped?
4. Confirm the query string actually matches a substring in the file (verify byte-for-byte)

```bash
grep -c "<query>" /Users/nolan/Cortana/platform/state/cortana-memory/<agent>/<file>
```

**Fix**: Adjust query, change scan threshold via backend config, or fix the file's encoding. Most often this is a substring-matching expectation mismatch.

### M-16 — MCP bridge process not running

**Symptom**: `cortana-memory-mcp-status.sh` fails. claude/codex CLI reports `cortana-memory: ✗ Not Connected`.

**Diagnosis**:
```bash
docker exec cortana-paperclip which cortana-memory-mcp
docker exec cortana-paperclip cortana-memory-mcp --version
docker exec cortana-paperclip ps -ef | grep cortana-memory-mcp | grep -v grep
```

**Fix**: Re-bootstrap the MCP bridge. Common causes:
- Bridge binary not in container PATH (re-run bootstrap)
- Wrong `CORTANA_AGENT_ID` env (check `adapter_config.mcp_servers.cortana-memory.env`)
- Router unreachable (check `/readyz` for `cortana-llm-router`)

### M-17 — Backend swap produced drift in audit rows

**Symptom**: After enabling a candidate backend, audit rows from the candidate differ from the live backend's rows on a field other than the documented `extension_id` / `adapter_id` / `memory_backend` triad.

**Diagnosis**: Run the swap drill test:
```bash
cd /Users/nolan/Cortana/platform
python3 -m unittest containers.cortana-llm-router.test.test_memory_backend_swap_drill
```

**Fix**: The candidate is non-conformant. Patch the candidate adapter to emit the missing/divergent field consistent with the Protocol contract. Do NOT promote until the swap drill is GREEN.

### M-18 — Sustained-window counter not advancing

**Symptom**: `verify-s10j-5-sustained-window.sh` returns the same `WINDOW_HOLDING_DAY_N_OF_7` value across multiple days.

**Diagnosis**:
```bash
cat /Users/nolan/Cortana/platform/state/cortana-memory/sustained-window/window-state.json
```

The script checks daily that all gates stayed GREEN and no regression entries appeared. A non-qualifying day resets or holds the counter.

**Fix**: Look at the day's state entry for the reason it didn't qualify. Common: a Codex Smoke regression, a marker expired and was re-granted (counts as instability), or an audit row outside the canonical category set landed.

## Cross-pillar overlap

Some failures look like memory but the root cause is elsewhere. Always check:

| Looks like | Often is | Pillar |
| --- | --- | --- |
| "Audit log empty but agent says succeeded" | Model hallucination (Pattern B) | Model / Harness |
| "Retry skips work" | Session contamination (Pattern C) | Harness |
| "Wakeup never fires" | Wrong dispatch lane (Pattern D) | Harness |
| "claude exits code 1 instantly" | Root permission gate (Pattern E) | Harness / Container |
| "Tool names must be unique (400)" | Skill registry collision (Pattern F) | Skills |
| "Agent does unrelated work" | Task context omitted (Pattern G) | Harness |

When in doubt, load `paperclip-triage` and walk the cross-pillar pattern list.

## Quick reference — symptom → fix

| Symptom | First check | Fix path |
| --- | --- | --- |
| `decision=refused`, `refused_marker_expired` | `live-dispatch-approved.marker.expires_at` | Re-grant read marker (M-1) |
| `decision=refused`, `refused_marker_agent_not_listed` | `.agent_ids[]` in read marker | Grant for the agent (M-2) |
| `decision=refused`, `error=live_memory_write_approval_missing` | Write marker fields | Re-grant write marker (M-3) |
| `decision=refused`, `refused_write_path_not_allowed` | `write_paths_allowlist[]` | Broaden allowlist or change target path (M-4) |
| `decision=refused`, `capability_state.missing` non-empty | Capability marker files | Grant capability (M-5) |
| `decision=refused`, `error=memory_read_target_missing` | File existence | Not a bug; fix agent or write the file first (M-7) |
| `transport=router_tool_loop` for stateful agent | `agents.adapter_type` | Migrate to claude_local (M-10) |
| `live_switch_state.all_switches_open=false` | Per-gate fields | Flip the closed gate (M-9) |
| Zero rows in audit, agent says succeeded | Output tokens + heartbeat_run_events | Pattern B (M-13) |
| MCP bridge not connected | `cortana-memory-mcp-status.sh` | Re-bootstrap (M-16) |
| Unknown `audit_category` value | Grep the audit log | Vocab admittance (M-12) |
| Schema floor test fails | Latest emitted row's `keys` | Re-emit missing field (M-11) |
| Sustained window not advancing | `window-state.json` | Inspect the non-qualifying day (M-18) |
