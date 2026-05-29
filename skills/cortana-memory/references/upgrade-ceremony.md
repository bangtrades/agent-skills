# Memory Pillar Upgrade Ceremony

Procedure for safely upgrading the memory pillar without regressing the rest of Cortana. Covers four upgrade classes: backend swap, audit schema bump, transport rename, capability ladder extension. Each has preconditions, sequenced steps, abort criteria, and rollback.

## Upgrade classes

| Class | Examples | Blast radius |
| --- | --- | --- |
| Backend swap | `para-memory-files` → `gbrain`; admitting a new candidate backend | Audit transport name, capability ladder, write semantics, Protocol completeness |
| Audit schema bump | Adding a new required field; renaming a field; bumping schema_version | Drift detector, verifiers, dashboards, operator grep continuity |
| Transport rename | Renaming `native_cli_bridge` to something else (rare) | Audit log consumers, gate scripts, dashboards |
| Capability ladder extension | Adding `memory_<backend>_<new-op>` capability | Per-agent capability markers, granting ceremony, executor's check list |

## Universal pre-upgrade checklist

Before ANY memory-pillar upgrade:

1. **Capture the baseline GREEN proof.**
   ```bash
   mkdir -p /Users/nolan/Cortana/platform/state/triage/memory-baseline-$(date -u +%Y%m%dT%H%M%SZ)
   BASE=/Users/nolan/Cortana/platform/state/triage/memory-baseline-$(date -u +%Y%m%dT%H%M%SZ)
   bash /Users/nolan/Cortana/platform/scripts/verify-s10i-6-controlled-codex-memory-smoke.sh --json > "$BASE/codex-smoke.json"
   bash /Users/nolan/Cortana/platform/scripts/verify-s10i-12-native-memory-e2e.sh --json     > "$BASE/native-e2e.json"
   bash /Users/nolan/Cortana/platform/scripts/verify-s10j-1-memory-adapter-protocol.sh --json > "$BASE/protocol.json"
   bash /Users/nolan/Cortana/platform/scripts/verify-s10j-4-shared-memory-isolation.sh --json > "$BASE/isolation.json"
   bash /Users/nolan/Cortana/platform/scripts/verify-s10j-5-sustained-window.sh --json       > "$BASE/sustained.json"
   tail -200 /Users/nolan/Cortana/platform/logs/cortana-llm-router/memory-execution.jsonl   > "$BASE/recent-audit.jsonl"
   ```

2. **Confirm the abort criteria in writing.** Examples:
   - "If `verify-s10i-6` regresses to NO_GO, revert."
   - "If audit schema floor drops below 22 required fields, revert."
   - "If any active agent's existing capability markers are invalidated, revert."

3. **Identify cross-pillar consumers.** Audit log readers (verifiers, dashboards, the QA agent itself). Backend swap-side: capability check sites, executor branches, MCP server config.

4. **Snapshot the rollback artifacts.** For backend swaps: the previous backend's Protocol implementation stays compiled in. For postgres-touching upgrades: backup row per `operations.md` § "backup-before-mutate". For schema bumps: tag the pre-bump `schema_version` value.

5. **One pillar, one slice.** Memory upgrade does NOT bundle with model or harness or skills changes. Cross-pillar regressions are easier to diagnose when only memory moved.

## Ceremony A — Backend swap

Goal: admit a new memory backend (replace or run alongside the live one). STEP-45 § 9 has the canonical runbook; this is the operational summary.

### A.1 — Pre-flight

- The candidate backend must implement the full MemoryAdapter Protocol (7 methods)
- The candidate must register under a unique `extension_id` in the extension registry
- The candidate's `describe()` must return canonical metadata (id, version, capabilities, deterministic flag)
- The candidate must be admitted by `lib/memory_adapter_contract.known_adapter_ids()` (registry of admitted backends)

### A.2 — Swap drill (tests-only, no production switch)

Run the swap drill against the live + candidate backends:

```bash
cd /Users/nolan/Cortana/platform
python3 -m unittest containers.cortana-llm-router.test.test_memory_backend_swap_drill
```

The drill:
- Creates a tempfs scratch dir
- Sets `CORTANA_TEST_FIXTURE=1` so test backends accept registration
- Runs an N-operation fixture (write, read, list, search, delete-if-supported)
- Captures audit rows from both backends
- Asserts byte-for-byte agreement (modulo `extension_id` / `adapter_id` / `memory_backend` triad)

Acceptance: ZERO diffs. Any drift fails the drill; the candidate is non-conformant and cannot proceed.

### A.3 — Protocol-completeness gate

```bash
bash /Users/nolan/Cortana/platform/scripts/verify-s10j-1-memory-adapter-protocol.sh --json
```

Asserts: the candidate's Protocol surface matches the 7-method contract. Refuses if any method is missing or has a divergent signature.

### A.4 — Compatibility matrix update

Add the candidate to `config/cortana/extension-compatibility-matrix.json` with `live_dispatch_enabled: false` (admitted but not live). This makes the backend visible to `/readyz` and the executor's class_executor_status surface, but does NOT route any agent through it.

### A.5 — One-agent canary

Migrate ONE non-critical agent (typically a fresh test agent from S10K-1 harness) to the candidate:

```bash
# Update the agent's memory_enabled to the candidate's extension_id
AGENT=<test-agent-uuid>
CANDIDATE_ID=<new-backend-id>
docker exec -i cortana-postgres psql -X -v ON_ERROR_STOP=1 -U cortana -d cortana <<SQL
UPDATE agents SET adapter_config = jsonb_set(
  adapter_config, '{memory_enabled}', '["${CANDIDATE_ID}"]'::jsonb, true
) WHERE id='${AGENT}';
SQL

# Grant the corresponding capability markers
bash /Users/nolan/Cortana/platform/scripts/cortana-capability.sh grant \
  --agent-id "$AGENT" \
  --capability "memory_${CANDIDATE_ID}_read" \
  --yes
# (and _write if the candidate supports writes)
```

Flip `live_dispatch_enabled: true` for the candidate. Run a controlled smoke against the canary. Verify:
- 4 audit rows land with `memory_backend=<candidate>`
- `audit_category` values match the live-success vocabulary
- Schema floor test passes
- Codex Smoke regression stays GREEN (proves the live backend wasn't affected)

### A.6 — Sustained-window observation

The candidate must produce stable output for 7 consecutive days under `verify-s10j-5-sustained-window.sh`. The counter does NOT advance if the candidate produces any regression entries (refusals on previously-passing operations, schema drift, marker semantic changes).

### A.7 — General promotion

After day 7 GREEN:

1. Update `extension-compatibility-matrix.json` — candidate → promoted
2. Migrate additional agents one at a time
3. Once all agents migrated, optionally deprecate the old backend (do NOT remove the Protocol implementation; leave for rollback continuity)

### A.8 — Abort criteria

Abort the swap and revert IF any of:
- Swap drill diffs (non-conformant audit emission)
- Protocol-completeness gate fails
- Canary smoke regresses to NO_GO
- Codex Smoke regression goes RED during canary
- Schema floor test fails
- Sustained-window counter resets within 7 days

Abort = flip `live_dispatch_enabled: false` on candidate, migrate canary back to old backend, document the regression class in a slice report.

## Ceremony B — Audit schema bump

Goal: add a required field to the audit row, OR bump `schema_version` for a breaking change.

### B.1 — Adding an optional (non-required) field

The simplest case. Adapter emits the new field on `audit_context`; the executor passes it through. Required:

1. Update STEP-37 § 6 to document the field (type, meaning, when emitted)
2. Update `audit-schema.md` § "Operation-specific extras" table
3. Add tests asserting the field's presence (when applicable)
4. NO `schema_version` bump
5. NO drift-detector update (it ignores extras)

### B.2 — Adding a required field

Breaking change. Procedure:

1. **Phase 1 — emission**: every backend emits the new field; the drift detector still tolerates absence (warning only, not fail).
2. **Phase 2 — enforcement**: drift detector flips the new field to required (fails when absent). All consumers (verifiers, dashboards) updated to read the new field. `schema_version` bumped.
3. **Phase 3 — cleanup**: any legacy backend that still misses the field is retired.

Document the rollout in STEP-37 § 9 (migration log).

### B.3 — Renaming a field

Three-phase rollout to preserve operator grep continuity:

1. **Phase 1 — dual emission**: every backend emits BOTH old and new field names with identical values. Drift detector accepts either.
2. **Phase 2 — consumer migration**: every consumer (verifier, dashboard, QA agent prompt) reads the NEW field. Old field marked deprecated in STEP-37 § 6.
3. **Phase 3 — old field removal**: backends stop emitting the old field. `schema_version` bumped.

Never short-cut to a single-phase rename. Saved operator queries break silently.

### B.4 — Bumping schema_version

When the row shape is breaking (renames + removals together, type changes), bump `schema_version`:

1. New version's full spec lands in STEP-37 § 6 with the version delta
2. Drift detector accepts both versions during the migration window
3. Backends emit the new version after a date threshold
4. Old-version rows in the audit log are tagged with their schema_version for replay continuity
5. Migration window closes; drift detector enforces new version only

### B.5 — Abort criteria

Abort the bump and revert if:
- A consumer can't migrate (a downstream system has hard-coded the old field name)
- Operator queries break and the migration window is too short
- A backend can't emit the new field

## Ceremony C — Transport rename

Rare. Renaming `native_cli_bridge` or `router_tool_loop` (e.g. to align with an upstream framework's terminology).

### C.1 — Procedure

1. **Phase 1 — dual labeling**: audit row emits BOTH old name (in `transport`) and new name (in `transport_v2` or similar). Drift detector accepts either.
2. **Phase 2 — consumer migration**: verifiers + dashboards + gate scripts updated to read `transport_v2`. Old name marked deprecated.
3. **Phase 3 — rename complete**: emit only the new name in `transport`. `schema_version` bumped.

### C.2 — Abort criteria

- A gate script cannot be updated in time
- The new name conflicts with another framework's vocabulary

## Ceremony D — Capability ladder extension

Goal: add a new capability (e.g. `memory_<backend>_<new-op>` or a cross-cutting capability like `memory_para_files_high_volume`).

### D.1 — Procedure

1. **Document the capability**: STEP-37 § 3 capability table, `architecture.md` § Capability ladder, this file
2. **Implement at executor**: the executor's check list adds the new capability for the relevant operation(s)
3. **Implement at adapter**: backend respects the new capability (e.g. refuses high-volume writes when the cap is absent)
4. **Implement granting**: `cortana-capability.sh grant` accepts the new capability id
5. **Run the canary**: grant the cap to one test agent; verify dispatch behavior changes as designed (allowed vs refused)
6. **Update verifiers**: gate scripts may need to assert the new cap is honored

### D.2 — Abort criteria

- New cap conflicts with an existing cap's semantics
- Executor's check list can't enforce it consistently across backends

## Adopting a brand-new memory framework

When a new memory framework lands (e.g. an upstream successor to MCP, or a new vector-search backend like a managed Pinecone analogue), use this top-down mapping:

1. **Classify it.** Is it a backend (implements MemoryAdapter) or a transport (delivers calls to backends)? Different procedures.
2. **Find its audit ground truth.** What's its equivalent of `memory-execution.jsonl`? If it emits no audit, build a shim that emits ours.
3. **Find its capability model.** Does it have native capability tokens? Or does Cortana own the capability layer with the framework as an opaque substrate?
4. **Map the schema.** Every operation's request/response must round-trip through MemoryAdapter's request types (or be admitted as a Protocol extension).
5. **Run the swap drill** treating it as a backend admission.
6. **Document in STEP-45** as a new backend or as a Protocol extension.

## Hard rules (upgrades)

- One pillar, one slice — never bundle pillar upgrades.
- Backend swap MUST pass swap drill before any agent migration.
- Schema floor (22 required fields) cannot be silently dropped; bump `schema_version` instead.
- Field renames go through 3-phase dual-emission rollouts.
- Transport renames same — never single-phase swap a transport label.
- Capability ladder additions need the executor's check list updated; never granted-but-not-checked.
- Codex Smoke regression stays GREEN throughout every upgrade.
- Operator grep continuity is sacred. A saved query against the audit log should not break silently.
- Sustained-window counter must hit day 7 before a candidate backend is general-promoted.
- Every upgrade ceremony produces a slice report named `docs/agent-reports/agent-<N>-<sprint>-memory-<class>.md` documenting before/after, regression evidence, and rollback artifacts.

## Quick reference — common upgrade flows

| You want to ... | Ceremony | First step |
| --- | --- | --- |
| Admit a new memory backend | A — Backend swap | Implement Protocol, then A.2 swap drill |
| Add an optional audit field | B.1 | STEP-37 § 6 + audit-schema.md update |
| Add a required audit field | B.2 | Phase 1 emission across all backends |
| Rename an audit field | B.3 | Phase 1 dual emission |
| Rename a transport | C.1 | Phase 1 dual labeling |
| Add a new capability | D | Document + executor check + grant flow |
| Adopt a brand-new framework | "Adopting a brand-new memory framework" | Classify as backend or transport first |
