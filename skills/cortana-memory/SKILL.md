---
name: cortana-memory
description: Cortana platform memory pillar — spec, contracts, operations, troubleshooting, and upgrade ceremonies. Use this skill whenever an operator or agent asks about memory tools (cortana_memory_write/read/list/search/submit_candidate), the cortana-memory-mcp bridge, memory audit rows (STEP-37 §6 schema), approval markers (live-dispatch-approved / live-write-approved), vault layout (private/candidates/shared/glossary/projects/workflows/core), memory backend swap (para-memory-files → gbrain or other), candidate promotion ceremony, capability ladder (memory_para_files_read/write/etc.), memory transport names (native_cli_bridge / router_tool_loop), MemoryAdapter Protocol, memory smoke tests, or memory-pillar upgrades. Also use when an agent reports memory-related refusals (live_memory_write_approval_missing, memory_capability_missing, memory_read_target_missing) or when files under state/cortana-memory/ need inspection. Memory is one of Cortana's five pillars; this skill is the canonical reference for everything memory.
version: 0.1.0
---

# Cortana Memory Pillar

The memory pillar is one of Cortana's five pillars (model, harness, **memory**, skills, task management). This skill is the canonical reference for memory's spec, contracts, operations, troubleshooting, and upgrade ceremonies.

Treat memory as a versioned contract surface, not a feature. Every claim about how memory works has an authoritative source: a STEP doc, a Protocol module, an audit-row field, or a verified test. **If the source can't be named, the claim is unverified.**

## When to use this skill

- Designing or debugging memory tool calls (`cortana_memory_*`)
- Investigating refusals from the memory executor
- Inspecting audit rows in `logs/cortana-llm-router/memory-execution.jsonl`
- Granting / rescinding / inspecting approval markers
- Swapping a memory backend (live → candidate, or candidate → live)
- Promoting a candidate memory file to shared scope
- Auditing capability state for an agent
- Migrating an agent's memory transport (router_tool_loop → native_cli_bridge)
- Running a memory smoke test or interpreting its results
- Onboarding a new agent's memory wiring (MCP bridge + markers + capabilities + vault scope)
- Triaging cross-pillar incidents where memory may be implicated (load `paperclip-triage` alongside)

## Core principles

1. **Audit log is ground truth.** `logs/cortana-llm-router/memory-execution.jsonl` is the canonical record. Heartbeat-run status, assistant text, and Paperclip's classifier are secondary signals. A run can be flagged `succeeded` with zero memory rows landed — see `paperclip-triage` Pattern B.

2. **Adapter class determines transport.** Per STEP-46:
   - `stateful-CLI` agents (claude_local, codex_local, cursor, ...) use `transport=native_cli_bridge` via the MCP bridge.
   - `router-one-shot` agents (cortana_llm_router) use `transport=router_tool_loop` via the in-router executor.
   - `cortana_llm_router` is **deprecated for stateful agents** per STEP-46 § 7.1 (and proven by S10J § 7.2).

3. **Five gates, all must open.** Every memory dispatch is gated by env / marker / capability / vault / lifecycle. The audit row's `live_switch_state.all_switches_open=true` is the single composite signal.

4. **Backends are pluggable behind one Protocol.** STEP-45 / S10J-2 pins the `MemoryAdapter` Protocol (seven methods: describe, health_check, read, write, list, search, delete). Swap is a Protocol-conformant exchange, not a router rewrite.

5. **Markers are agent-UUID-keyed, not adapter-keyed.** Adapter changes (e.g. cortana_llm_router → claude_local) do NOT invalidate `live-dispatch-approved.marker` or `live-write-approved.marker` for an agent. The marker integrity check is a precondition for migration, not a barrier.

6. **Schema floor is 22 fields, frozen by STEP-37 §6.** Any backend / transport / executor that emits fewer fields is non-conformant and fails the drift detector.

## What lives in this skill

- `references/architecture.md` — consolidated map of STEP-37 / STEP-43 / STEP-44 / STEP-45 / STEP-46 / STEP-47 against the pillar's surfaces
- `references/audit-schema.md` — STEP-37 §6 22-field schema, transport names, audit_category vocabulary, drift-detector rules
- `references/operations.md` — granting/revoking/inspecting markers, swap drill, candidate promotion, cleanup ceremonies
- `references/troubleshooting.md` — memory-specific failure patterns + canonical diagnostic commands
- `references/upgrade-ceremony.md` — the procedure for safely swapping a memory backend, adding audit fields, renaming a transport, or extending the capability ladder
- `references/tool-reference.md` — `cortana_memory_*` tool surface, `cortana-memory-mcp` server, router HTTP endpoints

Load only the reference you need; this SKILL.md surfaces the index.

## Pillar boundary

The memory pillar **owns**:

- Vault layout (private / candidates / shared / glossary / projects / workflows / core)
- Memory adapter implementations (para-memory-files; future: gbrain, custom)
- Audit row schema (STEP-37 §6) and emission discipline
- Approval marker contracts (read + write, paired expiry, ceremony_acknowledged)
- Capability ladder (memory_para_files_{read,write}, memory_<backend>_{op})
- Tool schema (`cortana_memory_*`)
- MCP bridge runtime (`cortana-memory-mcp`)

The memory pillar **delegates** to:

- **Model pillar** — tool-call discipline, hallucination resistance (Pattern B / K)
- **Harness pillar** — dispatch lane, transcript visibility, session-state semantics, capability marker discovery path
- **Skills pillar** — tool-name uniqueness, skill registry, skill sync (Pattern F)
- **Task management pillar** — issue lifecycle, wakeup payload, comment delivery (Pattern G)

Cross-pillar incidents: load this skill **plus** the affected pillar's skill (when those exist; today, `paperclip-triage` covers the others).

## Canonical proof commands

Always-true canonical proofs for this pillar:

```bash
# 1. The 4-row audit proof for a memory smoke (Pattern B reliability check):
SYMBA=0ac0a120-31a2-44c2-b30e-97569a2dc913
SMOKE_START="$(date -u -v -15M +%Y-%m-%dT%H:%M:%S.000Z 2>/dev/null \
              || date -u -d '15 min ago' +%Y-%m-%dT%H:%M:%S.000Z)"
jq -c --arg a "$SYMBA" --arg t "$SMOKE_START" \
   'select(.agent_id==$a and .ts > $t)' \
   /Users/nolan/Cortana/platform/logs/cortana-llm-router/memory-execution.jsonl

# 2. Schema floor check (every row must have all 22 STEP-37 §6 fields):
jq -c 'keys' /Users/nolan/Cortana/platform/logs/cortana-llm-router/memory-execution.jsonl \
  | head -1 | jq -r '. | length'   # → 22+ (extras allowed; core 22 required)

# 3. Marker integrity:
cat /Users/nolan/Cortana/platform/state/cortana-memory/live-dispatch-approved.marker | jq '.'
cat /Users/nolan/Cortana/platform/state/cortana-memory/live-write-approved.marker  | jq '.'

# 4. Codex Smoke regression (memory pillar control baseline):
bash /Users/nolan/Cortana/platform/scripts/verify-s10i-6-controlled-codex-memory-smoke.sh --json
```

## Quick decision tree

| Scenario | Load reference | First command |
| --- | --- | --- |
| "Memory tool refused" | `troubleshooting.md` | Audit-row query for agent + recent window |
| "Need to grant write approval" | `operations.md` | `cortana-memory-live-approval.sh grant-write …` |
| "Swap to a new backend" | `upgrade-ceremony.md` + `architecture.md` § Protocol | Read STEP-45 § 9 swap runbook |
| "Add a new audit field" | `audit-schema.md` § drift-detector | Run the schema-floor test |
| "Audit log shows zero rows but agent says succeeded" | `troubleshooting.md` § Pattern B | Token-usage heuristic + heartbeat_run_events check |
| "Migrate transport to MCP" | `operations.md` § agent migration + `architecture.md` § transport map | Validate marker integrity (agent-UUID keyed) |
| "Promote a candidate file to shared" | `operations.md` § candidate promotion ceremony | Check escalate rules; only auto-approve if all green |
| "Audit fields keep drifting between backends" | `audit-schema.md` + `upgrade-ceremony.md` § drift-detector | Run the byte-for-byte agreement test against fixture backend |

## Hard rules

- Never read or write `/Users/Nolan/Documents` or `/Users/nolan/Documents`.
- Never mutate another agent's marker / capability / vault scope.
- Always read-row → write-backup → compute-target → UPDATE for postgres mutations. Backup mode 0600.
- Approval grants follow the canonical ceremony in `operations.md`; never hand-edit marker files.
- Marker TTLs ≤ 7 days for production grants, ≤ 1 hour for triage runs.
- Live writes are gated by both the read marker AND the paired write marker; both must be unexpired AND agent-UUID-listed.
- New backends MUST emit all 22 STEP-37 §6 fields; the drift-detector test is non-negotiable.
- A backend swap goes through the swap drill in `upgrade-ceremony.md` BEFORE flipping any agent to it.
- Cross-pillar issues require both pillar skills loaded — never diagnose a memory failure with only memory context if the failure surface is in the harness or model layer.

## End-of-session self-improvement

If a memory-pillar investigation surfaces:

1. A new failure pattern not in `troubleshooting.md` → add it, bump SKILL.md version minor.
2. A new audit field added by a backend → update `audit-schema.md` and re-run the drift detector.
3. A new transport or backend → update `architecture.md` § transport map and the `tool-reference.md`.
4. A new ceremony step (e.g. for a new approval class) → update `operations.md`.

Prefer crisp additions over narrative. The skill should remain loadable in under 30 seconds of context.

## Cross-pillar references

- `paperclip-triage` skill — meta-triage skill that loads cross-pillar context. Use this skill alongside it when memory is implicated in a multi-pillar incident.
- Future: `cortana-harness`, `cortana-model`, `cortana-skills`, `cortana-task-management` skills (per-pillar; one at a time as the pillars mature).

## Canonical Cortana docs

- `docs/STEP-37-paperclip-native-memory-architecture.md` — the memory pillar's master spec
- `docs/STEP-43-cortana-vault-memory-layout.md` — vault sub-tree contract
- `docs/STEP-44-candidate-promotion-ceremony.md` — candidate → shared lifecycle
- `docs/STEP-45-memory-backend-swap-contract.md` — Protocol + swap runbook
- `docs/STEP-46-cortana-adapter-classification.md` — adapter class contract (delegates from harness pillar but pins memory transport per class)
- `docs/STEP-47-agent-harness-contract.md` — agent harness template (the per-agent vault scope + capability dir conventions)
