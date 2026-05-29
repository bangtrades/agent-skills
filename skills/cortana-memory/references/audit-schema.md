# Memory Audit Schema (STEP-37 §6)

The audit row is the single ground-truth artifact for every memory dispatch. This file is the canonical reference for the schema, the controlled vocabulary, and the drift-detection rules.

## File location

`logs/cortana-llm-router/memory-execution.jsonl` — one JSON object per line, append-only. Inside the router container, the path is `/logs/cortana-llm-router/memory-execution.jsonl` (read-only bind mount in the Paperclip container).

## Required fields (22-field schema floor)

Every row MUST contain all 22 fields below. Backends may add extras; they cannot omit any of these.

| Field | Type | Example | Pin |
| --- | --- | --- | --- |
| `ts` | RFC 3339 UTC string | `"2026-05-18T20:43:01.157Z"` | wall-clock time of dispatch |
| `agent_id` | uuid v4 string | `"0ac0a120-31a2-44c2-b30e-97569a2dc913"` | canonical agent UUID |
| `extension_id` | string | `"para-memory-files"` | the backend's registered id |
| `adapter_id` | string | `"para-memory-files"` | the executor's resolved adapter (today same as extension_id; future-proof for adapter↔extension split) |
| `memory_backend` | string | `"para-memory-files"` | redundant identity; preserved for operator grep continuity |
| `operation` | enum | `"write"` | one of {write, read, list, search, delete, submit_candidate, ...} |
| `decision` | enum | `"allowed"` | one of {allowed, refused} |
| `audit_category` | enum | `"live_write_success"` | controlled vocabulary; see § below |
| `refusal_reason` | string \| null | `null` | populated when decision=refused; null otherwise |
| `transport` | string | `"native_cli_bridge"` | one of {native_cli_bridge, router_tool_loop} |
| `lifecycle_state` | enum | `"live"` | one of {live, candidate, retired, unknown} |
| `live_switch_state` | object | `{"all_switches_open":true,"matrix_live_dispatch_enabled":true,"module_live_dispatch":true,"policy_live_dispatch":true}` | five-gate composite + per-gate detail |
| `approval_state` | enum | `"OK"` | one of {OK, MISSING, EXPIRED, AGENT_NOT_LISTED} |
| `capability_state` | object | `{"granted_subset":["memory_para_files_read","memory_para_files_write"],"missing":[],"ok":true,"required":["memory_para_files_read","memory_para_files_write"]}` | per-op capability check detail |
| `scope` | enum | `"private"` | one of {private, shared, candidate} |
| `relative_path` | string \| null | `"smoke/s10j-fresh-002.md"` | the path the op targeted; null when op has no path |
| `target_path_sha256_prefix` | string (16 hex) | `"332569e7c6eb33b2"` | sha256 prefix of resolved abs path; correlates without leaking path |
| `bytes_processed` | int | `135` | total bytes touched (write: bytes_written; read: bytes_read; list: item_count; search: match_count) |
| `bytes_read` | int | `135` | bytes read in this op (0 for write/list) |
| `bytes_written` | int | `135` | bytes written in this op (0 for read/list/search) |
| `payload_size_bytes` | int | `135` | size of the request payload (write content size, search query size, etc.) |
| `schema_version` | int | `1` | bump on schema-breaking change |

## Operation-specific extras (NOT required but stamped when applicable)

| Field | Operation | Notes |
| --- | --- | --- |
| `item_count` | list, search | number of items returned |
| `truncated` | list | true if results were cut off |
| `case_sensitive` | search | search behavior |
| `files_scanned` | search | total files inspected |
| `files_skipped_binary` | search | files skipped due to binary content |
| `files_skipped_too_large` | search | files skipped due to size threshold |
| `files_truncated` | search | true if scan was cut off |
| `matches_truncated` | search | true if match count exceeded threshold |
| `search_query_length` | search | length of the query string |
| `request_id` | all | mcp-... prefix for native_cli_bridge; llmreq_... prefix for router_tool_loop |
| `company_id` | all | nullable; populated when known |
| `issue_id` | all | nullable; populated when wakeup carried an issue context |
| `run_id` | all | nullable; populated when known (transport often does not carry it) |

## audit_category controlled vocabulary

The `audit_category` field is from a closed set. Today's vocabulary is 18 values; any backend emitting a value outside this set fails the drift detector.

### Success categories (5)

| Category | Operation | Meaning |
| --- | --- | --- |
| `live_write_success` | write | append succeeded; bytes written |
| `live_read_success` | read | bytes returned |
| `live_list_success` | list | entries returned |
| `live_search_success` | search | scan completed; matches counted |
| `live_delete_success` | delete | entry removed (only on backends that support delete) |

### Refusal categories (9)

| Category | Common cause |
| --- | --- |
| `refused_pre_live` | `lifecycle_state != live` |
| `refused_live_disabled` | env gate closed (`CORTANA_MEMORY_LIVE_DISPATCH != 1`) |
| `refused_marker_missing` | `live-dispatch-approved.marker` not present or unreadable |
| `refused_marker_expired` | marker present but `expires_at < NOW()` |
| `refused_marker_agent_not_listed` | marker present, agent UUID not in `agent_ids[]` |
| `refused_capability_missing` | required capability marker missing |
| `refused_vault_scope_violation` | target path outside agent's allowed scope |
| `refused_write_path_not_allowed` | write target not matched by `live-write-approved.marker.write_paths_allowlist[]` |
| `refused_other` | catch-all for refusals with a specific `refusal_reason` (e.g. `live_memory_write_approval_missing`, `memory_read_target_missing`, `memory_operation_not_implemented`) |

### Candidate-promotion categories (5)

| Category | Stage |
| --- | --- |
| `candidate_submit_accepted` | submit_candidate accepted; file moved to candidates/<agent-id>/ |
| `candidate_submit_refused` | submit_candidate refused (ineligible per rules) |
| `candidate_promotion_auto_approved` | classifier matched all auto-approve rules |
| `candidate_promotion_escalated` | classifier matched at least one escalate rule |
| `candidate_promotion_completed` | operator-approved promotion materialized into shared/ |

The vocabulary lives canonically in `config/cortana/memory-capability-contract.schema.json` and is enforced by the drift detector test.

## Drift detector

The drift detector is the test that prevents schema-floor regressions. It runs as part of the test suite and the release gates.

### Schema-floor test

`containers/cortana-llm-router/test/test_step37_schema_floor.py` (Step37BackendIndependentEmissionTests).

For each backend (live + fixture toy), the test:

1. Drives a representative dispatch through the executor
2. Inspects the emitted audit row
3. Asserts ALL 22 required fields are present
4. Asserts `audit_category` is in the controlled vocabulary
5. Asserts `transport` is in the registered set
6. Asserts `lifecycle_state` is in the registered set

Fail-mode: any missing field, unknown category, or unknown transport produces a hard test failure with the offending field/value named.

### Backend-independence test (swap drill)

`containers/cortana-llm-router/test/test_memory_backend_swap_drill.py`.

Runs the same N-operation fixture script against both the live backend and the toy backend, captures audit rows from each, and asserts:

- Same row count per operation
- Same canonical-field values (modulo the `extension_id` / `adapter_id` / `memory_backend` triad which differs by design)
- Same `audit_category` per operation
- Same `transport` per operation

Fail-mode: any drift between backends marks the candidate non-conformant.

### Vocabulary admittance

When a new `audit_category` value is needed (e.g. for a new operation type a future backend introduces):

1. Add the value to the JSON schema `config/cortana/memory-capability-contract.schema.json` enum
2. Update the executor's `_AUDIT_CATEGORY_*` constants
3. Update this file's controlled vocabulary section
4. Update the verifier scripts that grep for category values
5. Run the drift detector — every backend must emit the new value where applicable

The schema enum is the single source. The other surfaces (constants, this doc, verifiers) MUST converge on it.

## Quick checks

### "How many memory rows for agent X in window Y?"

```bash
AGENT=<uuid>
START=<iso>
END=<iso>
jq -c --arg a "$AGENT" --arg s "$START" --arg e "$END" \
   'select(.agent_id==$a and .ts >= $s and .ts <= $e)' \
   /Users/nolan/Cortana/platform/logs/cortana-llm-router/memory-execution.jsonl \
   | wc -l
```

### "Did all 22 required fields land on the latest row?"

```bash
jq -c 'keys | sort' /Users/nolan/Cortana/platform/logs/cortana-llm-router/memory-execution.jsonl \
  | tail -1
# manually compare against the 22-field list above
```

### "What audit_category values are in use today?"

```bash
jq -r '.audit_category' /Users/nolan/Cortana/platform/logs/cortana-llm-router/memory-execution.jsonl \
  | sort -u
# every value MUST be in the 18-value controlled vocabulary
```

### "How many refusals per refusal_reason this week?"

```bash
START="$(date -u -v -7d +%Y-%m-%dT%H:%M:%S.000Z 2>/dev/null || date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%S.000Z)"
jq -r --arg s "$START" \
   'select(.decision=="refused" and .ts >= $s) | .refusal_reason' \
   /Users/nolan/Cortana/platform/logs/cortana-llm-router/memory-execution.jsonl \
   | sort | uniq -c | sort -rn
```

### "Are all rows for agent X coming through the canonical transport?"

```bash
jq -r --arg a "<uuid>" 'select(.agent_id==$a) | .transport' \
   /Users/nolan/Cortana/platform/logs/cortana-llm-router/memory-execution.jsonl \
   | sort -u
# Expected for stateful-CLI agents: native_cli_bridge only
# Expected for legacy router-lane (deprecated): router_tool_loop only
# Mixed = transport migration in progress; resolve by audit
```

## Adding a field (schema bump procedure)

When a new field is needed (e.g. a new backend reports an additional context):

1. Decide if it's a required field (schema floor) or optional (operation-specific extra).
2. Update STEP-37 § 6 to include the field with type and meaning.
3. Update this file's table.
4. If required: bump `schema_version` (today 1; next bump 2). Update the drift detector to enforce the new field's presence.
5. If optional: add to the operation-specific extras table; the drift detector doesn't enforce.
6. Update every backend to emit the field.
7. Run the swap drill — backends agree byte-for-byte (modulo the documented triad).

Never silently add a field. Operator-visible drift is a confidence killer.

## Removing or renaming a field

Schema-floor fields cannot be removed without bumping `schema_version` and writing a migration runbook in STEP-37 § 9.

Renames go through a 3-phase rollout:
1. Emit BOTH old and new field names; mark old as deprecated in STEP-37 § 6.
2. Update all consumers (verifiers, grep patterns, dashboards) to use the new name.
3. Bump `schema_version` and stop emitting the old name.

Operator grep continuity is sacred. A user's saved query against the audit log should not break silently.
