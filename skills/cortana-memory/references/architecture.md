# Memory Pillar Architecture — Consolidated Map

This file maps Cortana's memory STEP docs against the pillar's actual surfaces, so a QA agent or operator can navigate the system without re-reading 6 documents.

## STEP-doc index

| STEP | Title | What it pins | When to read |
| --- | --- | --- | --- |
| STEP-37 | Paperclip-native memory architecture | Transport lanes, capability composition, audit-row schema (§6), candidate-promotion grammar | First read for any memory work; canonical source of truth |
| STEP-43 | Cortana vault memory layout | Vault sub-tree (private / candidates / shared / glossary / projects / workflows / core) | Onboarding a new vault scope; renaming or restructuring vault directories |
| STEP-44 | Candidate promotion ceremony | Escalate rules + auto-approve rules; promotion lifecycle; rule set v1 | Before promoting any candidate file; when adding a new promotion rule |
| STEP-45 | Memory backend swap contract | MemoryAdapter Protocol (7 methods); swap runbook; gbrain compatibility matrix | Adding a new backend; swap-drilling a tested backend; admitting a candidate backend |
| STEP-46 | Cortana adapter classification | Adapter classes (stateful-CLI / router-one-shot / gateway-webhook); deprecation policy; § 7.1 cortana_llm_router retire; § 7.2 native_cli_bridge canonical | Before migrating any agent; before adding a new adapter type |
| STEP-47 | Agent harness contract | Agent template + create/delete script; per-agent vault scope + capability marker dir conventions | Onboarding new agents through the harness; documenting agent provisioning |

## Pillar surfaces

### Vault layout (STEP-43)

```
state/cortana-memory/
├── <agent-uuid>/                       — per-agent private scope (one dir per agent)
│   ├── smoke/                          — operator-tests + smoke artifacts
│   ├── operator-tests/                 — manual test files
│   ├── resources/                      — agent-curated reference material
│   └── ...                             — agent-driven sub-trees
├── candidates/<agent-id>/              — pending promotion to shared (per-agent submit)
├── shared/                             — promoted, multi-agent-readable
│   ├── core/
│   ├── projects/
│   ├── workflows/
│   └── glossary/
└── sustained-window/                   — pillar-level state (window-state.json)
```

Every agent's private scope is keyed on the agent UUID. Cross-agent reads of private scope are refused at the executor (vault gate).

### Transport map (per STEP-46 + STEP-37 §4)

| Transport | Adapter class | Audit row `transport` value | Path |
| --- | --- | --- | --- |
| `native_cli_bridge` | stateful-CLI (claude_local, codex_local, ...) | `native_cli_bridge` | Agent CLI → MCP runtime → `cortana-memory-mcp` → router HTTP `/v1/memory/{op}` → executor → vault |
| `router_tool_loop` | router-one-shot (cortana_llm_router) | `router_tool_loop` | Router internal tool loop → in-process memory executor → vault |
| `mcp` (planned label, audit row uses `native_cli_bridge` today) | — | — | Naming nuance: `adapter_config.memoryBridge.transport="mcp"` describes the adapter setting; audit row label is `native_cli_bridge` (the transport identity at dispatch time). Do not confuse the two — they refer to the same lane from different sides. |

**Canonical lane for stateful agents (post-S10J)**: `native_cli_bridge`. The router lane stays for one-shot non-agentic LLM dispatches only.

### Five gates (STEP-37 §3 — composition)

Every memory dispatch fires through five gates, ALL must open:

1. **Env gate** — `CORTANA_MEMORY_LIVE_DISPATCH=1` AND `CORTANA_MEMORY_MODULE=para-memory-files` (or registered backend id) AND `CORTANA_MEMORY_POLICY=allow`
2. **Marker gate** — `live-dispatch-approved.marker` present, unexpired, agent UUID in `agent_ids[]`
3. **Capability gate** — required capability(ies) present in `state/agents/<uuid>/capabilities/<cap>.marker` (e.g. `memory_para_files_read`, `memory_para_files_write`)
4. **Vault gate** — target path under the agent's private scope OR under shared (read-only for shared)
5. **Lifecycle gate** — operation is in the backend's supported set; `lifecycle_state=live` (not `candidate` or `retired`)

The audit row's `live_switch_state.all_switches_open=true` is the composite. Per-gate state lives in `capability_state`, `approval_state`, `live_switch_state.module_live_dispatch`, etc.

### MemoryAdapter Protocol (STEP-45 / S10J-2)

Every backend implements seven methods:

```python
describe()        → AdapterDescription           # static, pure, deterministic
health_check()    → MemoryExecutionResult        # cheap probe
read(req)         → MemoryExecutionResult        # bytes; agent-scoped
write(req)        → MemoryExecutionResult        # append-only, bounded by MAX_PAYLOAD_BYTES
list(req)         → MemoryExecutionResult        # sorted relative paths
search(req)       → MemoryExecutionResult        # naive literal substring (the floor)
delete(req)       → MemoryExecutionResult        # required to exist; append-only backends refuse
```

Result type is **uniform** — the executor stamps canonical STEP-37 §6 audit row regardless of backend. Adapters surface context on `MemoryExecutionResult.audit_context`; they NEVER call the audit writer themselves.

Registered backends today:
- `para-memory-files` — file-backed, live, append-only (the production backend)
- `toy_inmemory_files` — in-memory, tests-only, refuses without `CORTANA_TEST_FIXTURE=1`

Candidate backends (named, not admitted):
- `gbrain` — replace semantics on write; richer search; requires Protocol extensions (`put_page`, `graph_query`) — see STEP-45 § 7

### Tool surface

Five tools, all routed through the MemoryAdapter:

| Tool | Operation | Capability required | Notes |
| --- | --- | --- | --- |
| `cortana_memory_write` | append-only write | `memory_<backend>_write` | bounded by `MAX_PAYLOAD_BYTES`; refuses outside `live-write-approved.marker.write_paths_allowlist` |
| `cortana_memory_read` | byte fetch | `memory_<backend>_read` | per-agent containment; refuses outside agent's vault scope |
| `cortana_memory_list` | sorted relative paths | `memory_<backend>_read` | returns count + truncated flag |
| `cortana_memory_search` | substring scan | `memory_<backend>_read` | files_scanned counted; matches truncated when over threshold |
| `cortana_memory_submit_candidate` | promotion intent | `memory_<backend>_read` + promotion eligibility | creates a candidate under `candidates/<agent-id>/` for ceremony |

Tool schema lives in `workspaces/cortana-extensions/skills/cortana-memory/skill.json` (the Anthropic tool_use shape).

### Approval markers

Two markers per backend, both at `state/cortana-memory/`:

**Read marker** — `live-dispatch-approved.marker`:
- `kind: "cortana.live_dispatch_approval"`
- `extension_id: "para-memory-files"`
- `agent_ids[]: [<uuid>, ...]`
- `expires_at: <iso-utc>`
- `issued_at: <iso-utc>`
- `operator: "<operator-name>"`
- `comment: "<free-form>"`

**Write marker** — `live-write-approved.marker`:
- `kind: "cortana.live_write_approval"`
- `extension_id: "para-memory-files"`
- `agent_id: <uuid>` OR `agent_ids[]`
- `expires_at: <iso-utc>` (≤ paired read marker's `expires_at`)
- `paired_canonical_expires_at: <iso-utc>` (the read marker's expiry)
- `write_paths_allowlist[]: [<glob>, ...]`
- `ceremony_acknowledged: true`
- `operator_intent: "<reason>"`
- `issued_at: <iso-utc>`
- `operator: "<operator-name>"`

The write marker enforces:
- Read marker must exist and cover the agent (pre-write check)
- `expires_at <= paired_canonical_expires_at` (script refuses otherwise)
- `ceremony_acknowledged: true` (write-specific risk acknowledgment)
- Target path matches at least one glob in `write_paths_allowlist`

### Capability ladder

Per-backend, per-operation capability markers under `state/agents/<uuid>/capabilities/<cap>.marker`:

| Capability | Granted by | Required for |
| --- | --- | --- |
| `memory_para_files_read` | operator approval ceremony | read, list, search on para-memory-files |
| `memory_para_files_write` | operator approval ceremony + ceremony_acknowledged | write on para-memory-files |
| `memory_para_files_delete` | operator approval ceremony (rare) | delete on para-memory-files (append-only backends refuse anyway) |
| `memory_para_files_submit_candidate` | granted with read | submit_candidate operations |

Each marker is a JSON file with:
- `capability: <id>`
- `granted_at: <iso>`
- `granted_by: <operator>`
- `expires_at: <iso>` (optional; defaults to inherit from live-dispatch marker)

### Candidate promotion (STEP-44)

Candidate files live at `state/cortana-memory/candidates/<agent-id>/<relative-path>`. The agent submits via `cortana_memory_submit_candidate`. The ceremony classifier decides:

- **Escalate rules** (any match → human review required): touches glossary, touches workflow with N>1 downstream consumers, contains PII patterns, exceeds size threshold, conflicts with existing shared file
- **Auto-approve rules** (all required → auto-promote): file under known-safe sub-tree, agent in trusted set, sustained-window day ≥ 7, size under threshold
- **Default**: escalate (safe default)

Rules v1 in `config/cortana/memory-promotion-rules.json`. Active projects in `config/cortana/active-projects.json`.

### Audit chain (STEP-37 §6)

Every dispatch emits a row to `logs/cortana-llm-router/memory-execution.jsonl`. The row has 22+ required fields (see `audit-schema.md` for the full enumeration). Key invariants:

- `ts` is wall-clock UTC, RFC 3339
- `agent_id` is the canonical agent UUID
- `decision` ∈ {`allowed`, `refused`}
- `audit_category` is from the controlled vocabulary (18 values today; see `audit-schema.md`)
- `transport` names the actual dispatch lane (`native_cli_bridge` or `router_tool_loop`)
- `lifecycle_state` ∈ {`live`, `candidate`, `retired`}
- `live_switch_state.all_switches_open` is the composite gate signal

Audit emission happens at the executor, NOT in the adapter. Adapters surface `audit_context`; the executor stamps the row.

## Component map — files and code paths

| Component | Path | Purpose |
| --- | --- | --- |
| Memory executor (production) | `containers/cortana-llm-router/lib/memory_executor.py` | Stamps audit rows, runs five-gate composition, dispatches to backend adapter |
| Memory adapter Protocol | `containers/cortana-llm-router/lib/memory_adapter_protocol.py` | The 7-method Protocol module (STEP-45 / S10J-2) |
| Live backend implementation | `containers/cortana-llm-router/lib/memory_extensions/para_memory_files/` | File-backed live adapter |
| Test fixture backend | `containers/cortana-llm-router/lib/memory_extensions/toy_inmemory_files/` | In-memory tests-only backend; refuses without `CORTANA_TEST_FIXTURE=1` |
| Tool handlers (router lane) | `containers/cortana-llm-router/lib/memory_tool_handlers.py` | Registers `cortana_memory_*` tools onto the router's SkillRegistry |
| Memory bridge (HTTP surface) | `containers/cortana-llm-router/lib/memory_bridge.py` | `/v1/memory/{op}` route handlers consumed by `cortana-memory-mcp` |
| MCP server | `workspaces/cortana-adapters/cortana-memory-mcp/` | Subprocess that exposes memory tools to claude_local / codex_local CLIs |
| Live-approval ceremony script | `scripts/cortana-memory-live-approval.sh` | Grant / rescind / inspect read + write markers |
| Verification gates | `scripts/verify-s10i-*.sh`, `scripts/verify-s10j-*.sh` | Static, runtime, and controlled-smoke gates |
| Audit log | `logs/cortana-llm-router/memory-execution.jsonl` | The canonical audit chain (ground truth) |
| Markers | `state/cortana-memory/live-dispatch-approved.marker`, `state/cortana-memory/live-write-approved.marker` | Operator-intent records |
| Capability markers | `state/agents/<uuid>/capabilities/<cap>.marker` | Per-agent per-capability grant records |
| Promotion rules | `config/cortana/memory-promotion-rules.json` | Escalate + auto-approve rule set v1 |
| Active projects | `config/cortana/active-projects.json` | Promotion classifier's project context |
| Capability contract schema | `config/cortana/memory-capability-contract.schema.json` | Drift detector for audit_category vocabulary |

## Cross-pillar interfaces

| Pillar | Interface |
| --- | --- |
| Harness | `adapter_config.memoryBridge` (transport, endpoint, readOnly) + `mcp_servers.cortana-memory` for stateful-CLI; the harness owns transport visibility (transcript events) but the memory pillar owns the audit row |
| Model | Tool-call discipline + Pattern B hallucination resistance; memory pillar trusts the model to actually fire the tool calls |
| Skills | `cortana_memory_*` tool names must remain unique across the skill registry; Pattern F dedup applies |
| Task management | Issue / wakeup / heartbeat-run plumbing is the harness's responsibility, but the memory pillar exposes `request_id` and `audit_context` so a triage can correlate a heartbeat run with its memory ops |
