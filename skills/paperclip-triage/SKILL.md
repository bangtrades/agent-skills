---
name: paperclip-triage
description: This skill should be used when the user asks to "triage Paperclip", "debug Paperclip", "troubleshoot Cortana agents", "fix Paperclip smoke tests", "analyze a failed controlled smoke", "debug native memory bridge", "investigate Codex Smoke", "diagnose an adapter mismatch", "verify a pillar upgrade", or mentions Paperclip issues such as COR tickets, controlled smoke gates, heartbeat runs, adapter execution, Cortana memory bridge failures, model hallucinations of tool calls, session-state contamination, or capability-marker problems. Also trigger when planning OS-level upgrades (model swap, harness change, memory backend, skill system, task-management) where the integration could regress an existing pillar.
version: 0.2.0
---

# Paperclip Triage

Incident-grade debugging skill for Paperclip/Cortana agent failures and pillar upgrades. Cortana is an agentic OS; its pillars (model, harness, memory, skills, task management) must remain composable under churn. This skill encodes the canonical triage process so a QA agent can run it autonomously.

Treat Paperclip as a control plane: issues define the assignment, heartbeat runs prove what was executed, adapter logs prove what was delivered to the model, audit JSONLs prove what tools actually fired, and gate scripts prove release readiness. Do not infer success from one layer when another layer can falsify it. **The audit log is the ground truth.** Assistant text, Paperclip's `succeeded` status, transcript widgets, and token-usage heuristics are all secondary signals.

## Core principles

1. **Audit log is ground truth.** A heartbeat_run flagged `succeeded` does NOT prove tools fired. Only rows in `logs/cortana-llm-router/memory-execution.jsonl` (or the equivalent pillar audit) prove dispatch.
2. **Read the source before guessing config.** Two days of config-shape speculation can be replaced by ten minutes reading the adapter's argv-build function plus the binary's gate string.
3. **Classify the adapter before patching.** Stateful-CLI vs router-one-shot vs gateway-webhook (STEP-46). Misclassification produces architectural mismatches that look like config bugs.
4. **Separate layers in your diagnosis.** Platform health, runtime install, adapter config, prompt delivery, tool dispatch, audit emission, semantic output. Never claim a fix on layer N when only layer M was verified.
5. **Operator vs agent boundaries are explicit.** Some actions require operator UI clicks (session-clear, board sign-in). Slice briefs and triage runs must name which side owns which action.

## Safety Rules

- Never read or write `/Users/Nolan/Documents` or `/Users/nolan/Documents`.
- Preserve user changes. Do not revert unrelated work.
- Prefer `rg` for search; use `apply_patch` for manual file edits.
- Avoid rerunning controlled smoke issues blindly. File a new sequential controlled issue after a material fix.
- Separate static readiness, runtime readiness, model prompt delivery, and semantic smoke success.
- Back up postgres rows BEFORE mutating; refuse if the backup file already exists for the same run-ts.
- No GitHub push from triage runs.
- No mutation of any other agent's row when triaging a single-agent failure.

## Triage Workflow

### 1. Establish the Exact Failure

Collect the newest user-provided output and identify:

- Gate name and final classification (e.g. `GO_NATIVE_CLI_BRIDGE`, `NO_GO_CONTROLLED_SEMANTIC_FAIL`)
- Latest issue identifier, title, status, started/completed window
- Agent id, adapter type (`claude_local` / `codex_local` / `cortana_llm_router` / ...), agent status (idle/paused), pause_reason
- Heartbeat run id, exit_code, error_code, stderr_excerpt
- Token usage (input/output counts) — **a real tool-loop with N memory calls produces > N×150 output tokens; sub-200 output ≈ no tools fired**
- Whether the failure is historical, stale, pre-fix, quota-blocked, cancelled, unparseable, or fresh
- Whether the run was a fresh start or a Retry (session reuse matters — see Failure Pattern: Session-State Contamination)

Use absolute dates and issue identifiers. Never say "latest" without naming the COR-* id and timestamp.

### 2. Classify the Adapter Lane

Before patching, place the failing agent in its STEP-46 class:

| Class | Members | Tool-loop ownership | Audit transport name | Use for |
| --- | --- | --- | --- | --- |
| `stateful-CLI` | `claude_local`, `codex_local`, `cursor`, `gemini_local`, `opencode_local`, `pi_local` | CLI process drives loop via its own MCP runtime | `native_cli_bridge` | Stateful agents (CEO, PM, dev, QA) |
| `router-one-shot` | `cortana_llm_router` | Router runs the loop server-side; shim relays transcript | `router_tool_loop` | Non-agentic one-shot LLM dispatch only |
| `gateway-webhook` | `openclaw_*` | External service owns the loop | `openclaw_dispatch` | Third-party agent platforms |

If the failing agent is a stateful agent on `cortana_llm_router`, the root cause may be a class mismatch (S10J-6 / STEP-46 lesson). Migrate to `claude_local` before chasing config bugs.

### 3. Prove the Layer

Six layers; verify each independently. The right fix lives in the lowest layer that fails:

1. **Platform health** — containers up, router reachable, postgres healthy
2. **MCP runtime / CLI install** — `which claude` / `which codex` / `cortana-memory-mcp --version` inside the container; `claude mcp list` reports `cortana-memory: ✓ Connected`
3. **Adapter config** — `adapter_config.memoryBridge`, generated argv, capability markers
4. **Prompt delivery** — `paperclipTaskMarkdown` reaches the model prompt; session continuation is fresh or explicitly forced
5. **Tool dispatch** — actual `cortana_memory_*` calls visible in `memory-execution.jsonl` within the run window
6. **Semantic output** — required terminal markers (`MEMORY-SMOKE-COMPLETE`, `TASK_COMPLETE`) in the assistant text AND backed by audit rows

Never treat historical audit rows as fresh success. Never treat Paperclip's `succeeded` status as proof — see Failure Pattern: Model Hallucination of Tool Calls.

### 4. Read the Source Before Guessing Config

When config patches keep failing, the contract you're targeting is wrong. Three sources of ground truth:

- **Adapter argv builders**: `workspaces/paperclip/packages/adapters/<adapter>/src/server/execute.ts` — read the exact lines that compose argv. Pay attention to `asBoolean(value, fallback)` defaults; a missing field may evaluate to `true`.
- **Compiled CLI gates**: `docker exec <container> sh -c 'find / -path "*<cli-name>*" -type f \( -name "*.js" -o -name "*.mjs" \) | xargs grep -l "<error-string>" | head -1 | xargs grep -nB2 -A4 "<error-string>"'`. Extracts the actual conditional gate even from compiled binaries.
- **Postgres schema introspection**: `\d <table>` then `SELECT jsonb_pretty(adapter_config) FROM agents WHERE id='...'` for the actual current state. Do this BEFORE proposing a JSON UPDATE.

This rule alone collapsed two days of S10J patching when finally applied (S10J-INTEGRATE-4).

### 5. Use the Gates in Order

Readiness check sequence:

```bash
cd /Users/nolan/Cortana/platform
./scripts/cortana-memory-mcp-status.sh --json
./scripts/verify-s10i-4-native-cli-memory-bridge.sh --json
./scripts/verify-s10i-12-native-memory-e2e.sh --json
```

Post-fix verification sequence:

```bash
./scripts/verify-s10i-6-controlled-codex-memory-smoke.sh --json
./scripts/verify-s10i-12-native-memory-e2e.sh --json
./scripts/verify-s10i-4-native-cli-memory-bridge.sh --json
```

Interpret `NO_GO_CONTROLLED_SEMANTIC_FAIL` by checking the date on the issue the gate selected. If the issue predates the fix, file a fresh sequential controlled issue. If it postdates the fix and lacks MCP audit rows, inspect prompt delivery + run logs before more reruns.

### 6. Patch the Smallest Durable Cause

Patch only the layer proven defective. Add a regression test at the layer that failed. Examples:

- Missing container binary → fix Docker image materialization (not a temporary symlink)
- MCP approval cancellation → check `default_tools_approval_mode` in the MCP server, not just shell `approval_policy`
- Task ignored by agent → verify `paperclipTaskMarkdown` is included in adapter prompt assembly
- Stale smoke selected by gate → improve freshness windows and stale/pre-fix classification
- Adapter argv missing/extra flag → write an argv-composition unit test against the postgres row's adapter_config shape
- Session-state contamination → set `forceFreshSession: true` on wakeup AND/OR clear session via UI before retry

### 7. Controlled Smoke Acceptance

A controlled memory smoke passes only when the newest sequential issue produces all of:

```text
MCP_TOOL_VISIBLE: yes
MEMORY_<OP>: yes  (write/read/list/search as the smoke requires)
PHRASE_PRESENT: yes
PHRASE: <expected terminal marker>
TASK_COMPLETE
```

AND the gates show fresh audit evidence — at least N rows in `logs/cortana-llm-router/memory-execution.jsonl` for the same agent, target path, and issue window, with `transport: "native_cli_bridge"` (MCP path) or `"router_tool_loop"` (router-one-shot path) matching the adapter class.

Acceptance row check (canonical):

```bash
SMOKE_START="$(date -u -v -10M +%Y-%m-%dT%H:%M:%S.000Z 2>/dev/null \
              || date -u -d '10 min ago' +%Y-%m-%dT%H:%M:%S.000Z)"
jq -c "select(.agent_id==\"<agent-uuid>\" and .ts > \"${SMOKE_START}\")" \
   /Users/nolan/Cortana/platform/logs/cortana-llm-router/memory-execution.jsonl
```

Expected fields per row: `decision="allowed"`, `audit_category="live_<op>_success"`, `capability_state.ok=true`, `lifecycle_state="live"`, `live_switch_state.all_switches_open=true`.

## Known Failure Patterns

### Pattern A — Adapter class mismatch (S10J-6 / STEP-46)

**Symptom**: Stateful agent on `cortana_llm_router`. Anthropic returns tool_use blocks, but `toolCallsPresent: false` in Paperclip. Lifecycle classifier flags `non_retryable_tool_loop`. Codex Smoke (on `codex_local`) is GREEN but this agent isn't.

**Diagnosis**: The router runs `run_tool_loop` server-side; Paperclip's transcript only sees the router's final response. Stateful agents need a CLI adapter so the tool lifecycle is visible.

**Fix**: Migrate to `claude_local` (or another stateful-CLI member). Use `scripts/cortana-agent-migrate-<agent>-to-claude-local.sh`. STEP-46 deprecates new stateful agents on `cortana_llm_router`.

### Pattern B — Model hallucination of tool calls

**Symptom**: Heartbeat run reports `succeeded` with terminal text like `MEMORY-SMOKE-COMPLETE`. But `memory-execution.jsonl` shows zero new rows in the run window. Output token count is suspiciously low (< 200).

**Diagnosis**: The model emitted text claiming tool calls happened without actually emitting `tool_use` blocks. Common when session continuation carries a prior hallucinated success forward.

**Verification (in order)**:
1. Run the audit row check (above). Zero rows = no dispatch.
2. Check token usage. Real loop with N tools ≈ N×200+ output tokens. Sub-200 = text-only.
3. Check the run's heartbeat_run_events for `tool_call` / `tool_result` rows. Absence proves nothing fired.

**Fix**:
- Force fresh session on the next wakeup (`forceFreshSession: true` in the POST body, or click "clear session for these issues" in Paperclip UI)
- Use a forcing-function prompt: require the model's first output token to be the opening of a `tool_use` block
- Consider swapping to a model less prone to confabulation (e.g. claude-sonnet-4-6 over claude-opus-4-6 for tool-loop discipline)
- Add to the prompt: "The audit log is the ground truth. If it returns zero rows for this run window, you fabricated the response."

### Pattern C — Session-state contamination

**Symptom**: Retried run claims work is already done; agent skips tool calls and just closes the issue.

**Diagnosis**: `agentTaskSessions` persists session keys per agent-task. Claude/Codex CLIs resume the prior session and inherit its hallucinated context.

**Fix**: Clear the session before retry. Either:
- Paperclip UI: "clear session for these issues" button on the run page
- API: `POST /api/agents/:id/wakeup` with `{"forceFreshSession": true, ...}`
- Brand-new issue (not a Retry) so the session key is fresh

### Pattern D — Wrong dispatch lane (S10J-INTEGRATE)

**Symptom**: `INSERT INTO agent_wakeup_requests` directly. Row stays `status='queued'`. Dispatcher never claims it.

**Diagnosis**: The dispatcher reads `heartbeat_runs.status='queued'`, not `agent_wakeup_requests`. The translation happens inside `heartbeat.wakeup(...)` which is called by `POST /api/agents/:id/wakeup` (auth-gated).

**Canonical lane**:
```bash
TOKEN="pcp_board_$(openssl rand -hex 24)"
HASH="$(printf '%s' "$TOKEN" | shasum -a 256 | awk '{print $1}')"
docker exec -i cortana-postgres psql -X -v ON_ERROR_STOP=1 -U cortana -d cortana <<SQL
INSERT INTO board_api_keys (user_id, name, key_hash, expires_at)
VALUES ('<operator-user-id>', '<distinctive-slice-name>', '$HASH', NOW() + INTERVAL '1 hour');
SQL

curl -sS -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  --data '{"source":"on_demand","triggerDetail":"manual","reason":"<distinctive label>","forceFreshSession":true}' \
  http://localhost:4200/api/agents/<agent-uuid>/wakeup

# Always revoke at end:
docker exec -i cortana-postgres psql -X -v ON_ERROR_STOP=1 -U cortana -d cortana <<SQL
UPDATE board_api_keys SET revoked_at=NOW() WHERE name='<distinctive-slice-name>';
SQL
```

Token shape: `pcp_board_<48 hex>`. Hash: sha256(token) → `board_api_keys.key_hash`. Token TTL ≤ 1 hour for triage runs; revoke at end. Never echo the token to stdout or to a file outside postgres.

### Pattern E — claude-code root-permission gate (S10J-INTEGRATE-4)

**Symptom**: stderr is `--dangerously-skip-permissions cannot be used with root/sudo privileges for security reasons`. claude exits code 1 in < 1 second. No tool calls fire.

**Diagnosis**: Paperclip container runs as root; claude-code v2.1.143's compiled gate refuses both `--dangerously-skip-permissions` AND `--permission-mode bypassPermissions` when `getuid()==0`. Only `IS_SANDBOX=1` (or `CLAUDE_CODE_BUBBLEWRAP`) opens the gate.

**Source proof**: `workspaces/paperclip/packages/adapters/claude-local/src/server/execute.ts:318` reads `dangerouslySkipPermissions` via `asBoolean(value, true)` — defaults to true when absent. The compiled claude binary's gate:

```js
if (K === "bypassPermissions" || _) {
  if (process.getuid() === 0
      && process.env.IS_SANDBOX !== "1"
      && !b8(process.env.CLAUDE_CODE_BUBBLEWRAP)) {
    process.exit(1);
  }
}
```

**Fix** (all three keys required):
```sql
UPDATE agents SET adapter_config = adapter_config
  || '{"dangerouslySkipPermissions": false}'::jsonb
  || jsonb_build_object('extraArgs', '["--permission-mode","bypassPermissions"]'::jsonb)
  || jsonb_build_object('env', COALESCE(adapter_config->'env','{}'::jsonb) || '{"IS_SANDBOX":"1"}'::jsonb)
WHERE id = '<agent-uuid>';
```

Mirror the on-disk canonical config at `config/cortana/agents/<agent>.claude-local.json` so future re-migrations stay consistent.

**Runtime probe** (no API call): point `CLAUDE_CONFIG_DIR` at a non-existent path; if the root-permission error is replaced by `Not logged in · Please run /login`, the gate is past.

### Pattern F — Tool-name collision (S10J-5)

**Symptom**: Anthropic returns HTTP 400 with `tools: Tool names must be unique`. No tool calls land.

**Diagnosis**: Both `skills_enabled` (lists `cortana-memory` skill) AND `memory_enabled` (triggers the cortana-http-shim auto-loader for `para-memory-files`) registered the same `cortana_memory_*` tool names. The router sent duplicates to Anthropic.

**Fix**: Remove cortana-memory from `agent_skills` table AND from `adapter_config.paperclipSkillSync.desiredSkills` (otherwise Paperclip's sync re-adds it). Keep `memory_enabled=["para-memory-files"]` so the shim auto-loader is the single source for memory tools.

### Pattern G — Task Context Omitted (COR-537 lesson)

**Symptom**: agent does unrelated repo work, `MCP_TOOL_VISIBLE=0`, no MCP lifecycle, no fresh memory audit rows.

**Diagnosis**: `context.paperclipTaskMarkdown` exists in the run context but the adapter didn't insert it into the prompt.

**Fix**: Verify adapter's prompt-assembly logic includes the task body. Add a fake-adapter unit test that asserts the issue description, target path, expected phrase, and `TASK_COMPLETE` marker are present in stdin.

### Pattern H — MCP Tool Cancelled

**Symptom**: MCP visible and attempted, but cancelled with "user cancelled MCP tool call."

**Diagnosis**: Codex MCP server's `default_tools_approval_mode` not set to `auto`. Shell `approval_policy` is a different setting.

**Fix**: Set `default_tools_approval_mode = "auto"` in the MCP server toml under `[mcp_servers.<server-name>]`.

### Pattern I — Config Without Runtime

**Symptom**: adapter config says memory bridge enabled, but `cortana-memory-mcp-status.sh` fails.

**Diagnosis**: Bridge binary not on container PATH, host dist missing, symlink/image install incomplete, or router unreachable.

**Fix**: Re-run bootstrap; verify `which cortana-memory-mcp` inside the container; confirm router `/readyz` is GREEN.

### Pattern J — Stale Controlled Issue

**Symptom**: gates still fail against an old issue after a fix.

**Diagnosis**: Gate selected a pre-fix issue. Reopen-and-rerun does not produce fresh evidence; the prior run's audit rows persist.

**Fix**: Do not reopen old issues. File the next sequential controlled issue after material fixes.

### Pattern K — Token-usage anomaly (model-behavior heuristic)

**Symptom**: heartbeat_run `status=succeeded`, terminal marker present in result text, but audit log shows zero rows.

**Heuristic check**: If `result_json.usage.output_tokens < 200` for a multi-tool smoke, no real tool loop fired. The model emitted a text summary claiming success. See Pattern B.

## Pillar-Upgrade Triage

Cortana's pillars: **model**, **harness**, **memory**, **skills**, **task management**. Each can be upgraded independently, but integrations across pillars can regress. Before adopting a new framework, run this triage matrix:

| Pillar | Upgrade examples | What to verify post-upgrade |
| --- | --- | --- |
| Model | Opus → Sonnet, vendor swap, new release | Tool-loop discipline (Pattern B/K), per-call cost, latency budget, refusal/safety behavior, transcript shape |
| Harness | Paperclip → other agent OS, adapter API change | Adapter argv composition (Pattern E), prompt delivery (Pattern G), dispatch lane (Pattern D), session-state semantics (Pattern C) |
| Memory | Backend swap (para-memory-files → gbrain), MCP version bump | Audit row schema (STEP-37 §6), transport name, capability state, marker semantics, write-approval ceremony |
| Skills | New skill registry, tool-name allowlist change | Tool-name uniqueness (Pattern F), skill-keys allowlist, skill-vs-memory loading order, Paperclip skill sync |
| Task management | Issue routing changes, lifecycle stages, approval flow | Status transitions, wakeup payload shape, comment delivery, issue-relations integrity |

### Pillar-upgrade triage workflow

1. **Baseline GREEN proof on the OLD stack.** Capture the canonical 4-row audit proof (memory), the controlled smoke gate JSON, and a representative heartbeat run from each adapter class. Store under `state/triage/baseline-<pillar>-<date>/`.
2. **Land the upgrade in isolation.** No other pillar changes in the same slice. Use the agent-slice cadence (one self-contained slice with ABORT branches per failure mode).
3. **Re-run baseline gates.** If any go RED, classify the regression by failure pattern above and patch the smallest cause.
4. **Add forward proof on the NEW stack.** Run a fresh sequential controlled smoke. Audit log shows fresh rows post-upgrade timestamp. Token usage in healthy range.
5. **Cross-pillar regression sweep.** For every other pillar's canonical gate, re-run. Memory upgrade can regress harness (transport name change); model upgrade can regress skills (tool-loop max iterations); etc.
6. **Document the swap.** Land or amend a STEP doc (e.g. STEP-46 amendment for adapter classification) so the lesson is permanent.

### Adopting a new framework (forward compatibility)

When a new framework lands (e.g. a new agent OS replacing Paperclip, or a new MCP standard):

1. **Classify it.** Where does it sit in the pillar table? What's the canonical equivalent of `heartbeat_runs`, `agent_wakeup_requests`, `memory-execution.jsonl`, `adapter_config`?
2. **Find the audit ground truth.** Every framework has one. Until you know what it is, you cannot triage failures on it.
3. **Find the auth lane.** Every framework has a canonical authenticated dispatch path. Until you can fire it programmatically with a scoped credential, you cannot run smokes against it.
4. **Find the argv/spawn composition.** For CLI adapters, the framework spawns subprocesses with specific argv + env. Locate the composition function before patching config.
5. **Map your pillars onto its primitives.** Memory backend, skill registry, task lifecycle. If a primitive is missing, you need a shim. If a primitive maps 1:1, no shim.
6. **Run the pillar-upgrade triage above** treating the framework swap as a harness upgrade.

## Slice-Brief Discipline (for agent-driven triage)

When dispatching an agent to fix a triaged issue:

1. **One mission, one slice.** No multi-mission slices; they hide partial progress.
2. **Branching contract.** Every failure mode gets an explicit ABORT code + classification name. The agent must NOT plow through partial success.
3. **Operator vs agent boundaries explicit.** Name which side owns each action. If a UI click is required, the slice halts and hands off.
4. **Backup before mutate.** Postgres UPDATEs must follow read-row → write-backup → compute-target → UPDATE order. Backup file mode 0600.
5. **Source-level proof required.** When patching config, the slice MUST include source-reading of the argv builder / binary gate / contract function. No blind config-shape guessing.
6. **Slice report ends with `FINAL_CLASSIFICATION:`** on its own line, format `GO_<pillar>_GREEN` or `NO_GO_<specific-reason>`.

## End-of-Session Self-Improvement

End every triage session with a brief process review:

1. State the actual root cause and the false leads avoided or discovered.
2. Identify which proof finally separated symptoms from cause (audit log? source read? runtime probe? token-count heuristic?).
3. Name any gate, log, script, or UI signal that was misleading or missing.
4. Recommend one concrete improvement to this skill — a new failure pattern, a refined heuristic, a missing canonical command.
5. If the improvement is small and clearly correct, patch this skill immediately (bump `version:` minor). Otherwise file a follow-up.

Use the review to make future triage faster and less dependent on memory. Prefer adding a crisp failure pattern or checklist item over long narrative.

## References

- `references/native-memory-smoke-case-study.md` — Cortana native memory bridge controlled smoke case (Codex Smoke pattern)
- `references/s10j-memory-pillar-saga.md` — The 2-day adapter-mismatch saga (S10J-6 through S10J-CLOSE); canonical example of Patterns A, B, C, D, E in one incident
- `references/canonical-commands.md` — copy-paste-ready commands for: audit-row check, auth-lane wakeup, runtime claude probe, postgres row inspection, marker integrity check, source-reading recipes
- `references/pillar-upgrade-checklist.md` — pre/during/post checklists for each pillar upgrade type

## Cortana platform references

- `docs/STEP-37-paperclip-native-memory-architecture.md` — transport lanes, audit row schema, capability gate composition
- `docs/STEP-46-cortana-adapter-classification.md` — adapter class contract and deprecation policy
- `docs/STEP-47-agent-harness-contract.md` — agent template + create/delete script contract
- `scripts/verify-s10i-6-controlled-codex-memory-smoke.sh` — canonical Codex Smoke verifier (regression baseline)
- `scripts/cortana-agent-migrate-<agent>-to-claude-local.sh` — adapter cutover with backup and rollback
