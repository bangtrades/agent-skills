# Pillar-Upgrade Checklist

Cortana is an agentic OS built on five pillars: **model**, **harness**, **memory**, **skills**, **task management**. Each pillar must be independently upgradeable without regressing the others. This document is the playbook a QA agent runs every time a pillar changes — whether the change is a model version bump, a harness fork (e.g. Paperclip → next-gen orchestrator), a new memory backend, a skill-registry refactor, or a task-management lifecycle change.

The forcing function: **regardless of what framework lands tomorrow, Cortana must be able to adopt it with rigor.** This checklist is how.

## Universal pre-upgrade checklist (all pillars)

1. **Baseline GREEN proof.** Capture canonical proofs for every pillar BEFORE touching anything. File them under `state/triage/baseline-<pillar>-<YYYY-MM-DD>/`:
   - Memory: 4-row audit log proof from a controlled smoke (canonical-commands.md §1)
   - Harness: Codex Smoke verifier JSON output (canonical-commands.md §10)
   - Model: heartbeat run row + result_json with terminal marker + token usage (canonical-commands.md §8)
   - Skills: `agent_skills` table snapshot for each canonical agent + `adapter_config.paperclipSkillSync.desiredSkills` for each
   - Task management: issue lifecycle test — file → wakeup → run → done — with all timestamps captured

2. **Identify the upgrade's blast radius.** Which pillars does the change touch? A model swap is "model only". A harness fork is "harness + every adapter + dispatch lane + transcript shape." A memory backend swap is "memory + audit schema + capability gates."

3. **Define the abort criteria.** Write down, BEFORE starting, the conditions under which the upgrade is reverted. Examples:
   - "If Codex Smoke regresses to NO_GO, revert."
   - "If audit row schema diverges from STEP-37 §6, revert."
   - "If output tokens for the canonical smoke exceed 2x the baseline, abort the model swap."

4. **Snapshot the rollback path.** For postgres-mutating upgrades, write the backup file and verify the rollback command before mutating. For source-level upgrades, tag the pre-upgrade git SHA.

5. **One pillar, one slice.** Never bundle pillar upgrades. Each upgrade gets a self-contained slice brief with ABORT branches. Cross-pillar regressions are easier to diagnose when only one pillar moved.

## Pillar 1: Model

**Upgrade examples**: Opus → Sonnet for a specific agent, vendor swap (Anthropic → OpenAI), model version bump (claude-opus-4-6 → claude-opus-5-0), reasoning-effort change.

### Pre-upgrade verification
- Capture token-usage baselines for at least 3 representative runs (warm session, fresh session, multi-tool smoke)
- Capture per-call cost baselines from `actual_cost_usd` in `calls.jsonl`
- Capture refusal/safety behavior baseline (does the agent comply with system prompts at the current model?)
- Note current adapter_config: `model`, `effort` / `reasoning`, `extraArgs`

### Upgrade execution
- Update postgres `adapter_config.model` (and `effort` / `reasoning` if applicable)
- Mirror to on-disk `config/cortana/agents/<agent>.<adapter>.json`
- DO NOT change any other adapter_config fields in the same slice

### Post-upgrade verification (run all)
1. **Tool-loop discipline** — re-run the canonical 4-tool memory smoke; expect 4 audit rows; check token count is in healthy range (sub-200 = Pattern B hallucination)
2. **Per-call cost** — compare against baseline; >1.5x is a budget regression
3. **Latency budget** — heartbeat run duration vs baseline
4. **Refusal/safety behavior** — replay a sample of older approved tasks; the new model must complete them (not refuse for policy reasons)
5. **Transcript shape** — heartbeat_run_events still produces tool_call/tool_result rows in the same order as baseline
6. **Token-loop runaway** — verify `max_iterations` ceiling still kicks in if the new model is chattier; check `_resolve_default_max_iterations()` (canonical-commands.md §13)

### Common model-swap failure modes
- **Token explosion**: new model is more verbose. Add an explicit token-budget assertion in the smoke.
- **Tool-call refusal**: new model refuses to call internal tools the old model handled. Adjust system prompt.
- **Reasoning-effort incompatibility**: codex_local's `minimal` reasoning is rejected when `search` is enabled (per upstream docs). Check `OnboardingWizard.tsx:28-29` constraints.
- **Hallucination of tool calls**: new model fabricates results without firing tools. Pattern B from SKILL.md. Add forcing-function prompt.

## Pillar 2: Harness

**Upgrade examples**: Paperclip version bump, fork of Paperclip with breaking adapter API change, swap to a different agent OS entirely (e.g. a new framework released in 2026 that supersedes Paperclip).

### Pre-upgrade verification
- Adapter classification per STEP-46: list every agent and its `adapter_class` (stateful-CLI / router-one-shot / gateway-webhook)
- Canonical primitives in the OLD harness:
  - Issue table: `issues` (Paperclip name)
  - Run table: `heartbeat_runs`
  - Wakeup queue: `agent_wakeup_requests`
  - Transcript events: `heartbeat_run_events`
  - Dispatch endpoint: `POST /api/agents/:id/wakeup`
  - Auth lane: `board_api_keys`
  - Adapter spawn: argv composition functions in each adapter package
- Snapshot every postgres table the harness owns

### Upgrade execution
- New harness lands in `workspaces/<new-harness>/` alongside the old one
- Build a shim layer that maps Cortana's pillar contracts to the new harness's primitives
- Migrate ONE agent at a time, starting with a throwaway test agent

### Post-upgrade verification (run all)
1. **Adapter argv composition** — read the new harness's argv builder for each `adapter_class`; verify Cortana's MCP bridge + capability env vars still inject (canonical-commands.md §3)
2. **Prompt delivery** — confirm task body reaches the model (Pattern G test from native-memory-smoke-case-study.md)
3. **Dispatch lane** — find the new harness's equivalent of `POST /api/agents/:id/wakeup` and `heartbeat_runs.status='queued'`; verify direct-DB enqueue is NOT the canonical lane
4. **Auth model** — find the new harness's equivalent of `board_api_keys`; document token shape + mint/revoke flow
5. **Transcript shape** — does the new harness emit tool_call/tool_result events compatible with Cortana's lifecycle classifier?
6. **Session-state semantics** — does the new harness persist sessions like `agentTaskSessions`? Same Pattern C contamination risk applies; ensure `forceFreshSession` equivalent exists
7. **Cross-pillar regression** — run every pillar's canonical gate. Memory MUST stay GREEN through a harness swap; transport names may change but the audit row schema must not.

### Common harness-swap failure modes
- **Adapter-class re-classification**: an agent previously on stateful-CLI may need to land on router-one-shot in the new harness (or vice versa). Re-walk STEP-46.
- **Dispatch-lane assumption breaks**: prior triage scripts assumed `POST /api/agents/:id/wakeup`; new harness uses GraphQL mutation or webhook. Update canonical-commands.md §6.
- **Transcript event renaming**: `heartbeat_run_events.kind="tool_call"` may become `runEvents.eventType="ToolInvocation"`. Update Pattern B verification.
- **Audit emission gap**: new harness may not emit equivalents of `tool_executed` audit rows. If lost, file the gap as a P0 and fix BEFORE the rest of the harness goes live.

## Pillar 3: Memory

**Upgrade examples**: Backend swap (`para-memory-files` → gbrain), MCP version bump, audit schema field addition, capability-gate ladder change, new transport class.

### Pre-upgrade verification
- Audit row schema snapshot — `jq '.|keys' logs/cortana-llm-router/memory-execution.jsonl` for a recent row; capture the 22 STEP-37 §6 required fields
- Capability state — `live-dispatch-approved.marker` and `live-write-approved.marker` for every active agent; capture expiry windows and path allowlists
- Transport name — current canonical is `native_cli_bridge` (MCP) or `router_tool_loop` (router lane); document new transport name
- Backend adapter registration — `MEMORY_EXECUTOR_REGISTRY` known keys

### Upgrade execution
- New backend lands as an additional `MemoryAdapter` (per S10J-2 Protocol) without removing the old one
- Migrate ONE agent's `memory_enabled` field to the new backend; keep all other agents on the old backend
- Run the full controlled smoke on the migrated agent
- Verify audit rows still land with STEP-37 §6 schema

### Post-upgrade verification (run all)
1. **Audit row schema completeness** — every row carries the 22 required fields; check `_AUDIT_CATEGORY_*` enum is still recognized
2. **Capability ladder honored** — read/write/list/search each enforce their own capability requirement (`memory_para_files_read` vs `memory_para_files_write`)
3. **Live-switch composition** — `lifecycle_state="live"` AND `live_switch_state.all_switches_open=true` only when ALL 5 gates pass (env / marker / capability / vault / lifecycle)
4. **Marker semantics unchanged** — `paired_canonical_expires_at` on write markers ≤ read marker `expires_at`; agent-uuid-keyed not adapter-keyed
5. **Backend independence** — toy fixture backend produces byte-identical audit rows to live backend (S10J-2 swap drill)
6. **Cross-agent isolation** — Agent A's memory is invisible to Agent B's reads

### Common memory-swap failure modes
- **Audit row schema drift**: new backend emits fewer fields than STEP-37 §6 requires. Drift-detector tests must fail loud.
- **Transport name collision**: new backend reuses an existing transport name without honoring its contract. Add a new name.
- **Marker semantics change**: new backend keyed on adapter rather than agent UUID — breaks isolation. Refuse the swap.
- **Capability ladder regression**: new backend defaults to "all access" instead of per-op capability check. Refuse the swap.

## Pillar 4: Skills

**Upgrade examples**: New skill registry format, tool-name allowlist change, skill-loading order refactor, new skill-vs-memory coupling.

### Pre-upgrade verification
- `agent_skills` table snapshot for each canonical agent
- `adapter_config.skills_enabled` snapshot
- `adapter_config.paperclipSkillSync.desiredSkills` snapshot
- `cortana-http-shim/lib/skill_keys.js` `ALLOWED_CANONICAL_SKILL_IDS` content
- `cortana-http-shim/lib/execute.js` auto-loader contents (the section that injects memory tools)

### Upgrade execution
- New skill registry coexists with old (skill_registry_v2/)
- Migrate skills one at a time via the registry's import lane
- Validate tool-name uniqueness EVERY time (Pattern F)

### Post-upgrade verification (run all)
1. **Tool-name uniqueness** — Anthropic's `tools: Tool names must be unique` 400 error fires the moment a duplicate slips in; run a fresh wakeup and check for HTTP 400 in router logs
2. **Skill loading order** — `agent_skills` (postgres) vs `adapter_config.skills_enabled` (JSON column) vs `adapter_config.memory_enabled` (auto-loader trigger). Document precedence; only ONE should win per tool name
3. **Skill sync idempotency** — `paperclipSkillSync.desiredSkills` should not silently re-add a skill that was explicitly removed
4. **Skill manifest validation** — every skill declares its tool names in Anthropic tool_use schema (input_schema, description, required fields)

### Common skills-swap failure modes
- **Tool-name collision across skills** (Pattern F): two skills register the same name (e.g. `cortana_memory_read` from both `cortana-memory` and `para-memory-files` auto-loader). Dedupe at the registry layer.
- **Stale `agent_skills` rows**: postgres carries skill ids that no longer exist in the new registry. Cleanup with a migration script.
- **Skill-sync re-adds removed skill**: `paperclipSkillSync.desiredSkills` is the source of truth for what Paperclip thinks the agent wants. Remove there too, not just from `agent_skills`.

## Pillar 5: Task management

**Upgrade examples**: Issue lifecycle stage addition, new approval gate, comment-delivery refactor, wakeup-payload shape change.

### Pre-upgrade verification
- Issue lifecycle states snapshot — `SELECT DISTINCT status FROM issues`; expected: backlog, todo, in_progress, in_review, done, blocked, cancelled
- Approval flow snapshot — `SELECT type, status FROM approvals GROUP BY type, status`
- Wakeup payload shape — capture a recent `PAPERCLIP_WAKE_PAYLOAD_JSON` for a comment-triggered wake
- Issue-relations integrity — `blockedByIssueIds`, `parentId`, `inheritExecutionWorkspaceFromIssueId` usage

### Upgrade execution
- New lifecycle stage added behind a feature flag if possible
- Migrate one workflow at a time; do not retire old stages until new is proven

### Post-upgrade verification (run all)
1. **Lifecycle transition completeness** — every documented status transition still works (file → claim → progress → done)
2. **Approval gate enforcement** — `request_board_approval` interactions still block downstream work
3. **Comment delivery** — comment-triggered wakeups still surface `PAPERCLIP_WAKE_COMMENT_ID` and `PAPERCLIP_WAKE_PAYLOAD_JSON`
4. **Blocker resolution wake** — `PAPERCLIP_WAKE_REASON=issue_blockers_resolved` still fires when all blockers reach done
5. **Children-completed wake** — `PAPERCLIP_WAKE_REASON=issue_children_completed` still fires when all child issues reach terminal state
6. **Stale-task dedup** — agent's heartbeat skill respects the dedup rule (no re-comment on blocked task without new context)

### Common task-management-swap failure modes
- **Status enum drift**: new harness has different status names. Update agent heartbeat skills.
- **Approval lane shift**: approvals now require a new field or routing key. Update the `request_board_approval` payload shape.
- **Wakeup payload shape change**: agents fail to parse new `PAPERCLIP_WAKE_PAYLOAD_JSON`. Update agent prompts.

## Adopting a brand-new framework

When a new agent-OS framework lands (e.g. an upstream successor to Paperclip in 2027), follow this top-down mapping process BEFORE writing any integration code:

1. **Classify it on the pillar table.**
   - Does it own its own model adapter, or is it model-agnostic?
   - Does it own its own harness (process management, dispatch queue)?
   - Does it provide a memory primitive or rely on external services?
   - Does it have a skill registry?
   - Does it have task management?
   
   The pillars it OWNS are the integration surfaces; the pillars it DELEGATES are where Cortana plugs in.

2. **Find the audit ground truth.** Every framework has one. Until you can name the file, table, or API endpoint where dispatch is recorded with timestamps + outcomes, you cannot triage failures on it. **No audit log → no adoption.**

3. **Find the auth lane.** Find the framework's authenticated dispatch endpoint. Document token shape, mint flow, revoke flow. **No scoped credential flow → no adoption.**

4. **Find the argv/spawn composition.** For each adapter class, locate the function that builds the subprocess invocation. Read it. **No source-level argv reading → don't propose config changes.**

5. **Map primitives**:
   - Old: `agents` table → New: `?`
   - Old: `heartbeat_runs` → New: `?`
   - Old: `agent_wakeup_requests` → New: `?`
   - Old: `heartbeat_run_events` → New: `?`
   - Old: `adapter_config` JSONB → New: `?`
   - Old: `board_api_keys` → New: `?`
   - Old: `memory-execution.jsonl` → New: `?`
   - Old: `cortana-memory-mcp` bridge → New: `?`

6. **Run the pillar-upgrade triage above** treating the framework swap as a harness upgrade. Every pillar's canonical gate must pass on the new framework before retiring the old one.

7. **Write a STEP doc** capturing the framework's contract on Cortana's pillar surfaces. Future triage must be able to read THIS doc, not the upstream's, to understand how Cortana uses the framework.

## QA-agent contract

A future QA agent running this skill should be able to:

1. Detect a pillar regression within one verification gate run
2. Classify the regression against the 11 known failure patterns in SKILL.md
3. Locate source-level proof for any config-shape question in under 5 minutes
4. Mint a scoped credential, fire an authenticated wakeup, capture audit rows, and revoke the credential — autonomously
5. Write a slice brief with proper ABORT branches when a regression needs an agent-driven fix
6. Update this skill (bump `version:`) with any new failure pattern it discovers

The objective: any future framework adoption is bounded by the time to map primitives + run the gates, not the time to discover what's broken.
