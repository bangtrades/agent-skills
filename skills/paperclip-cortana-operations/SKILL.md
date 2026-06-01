---
name: paperclip-cortana-operations
description: "Operate and triage Cortana-on-Paperclip agency stacks: handoff review, roster activation, agent runtime readiness, adapter config audits, and memory-bridge proof."
version: 0.1.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [Paperclip, Cortana, agents, operations, triage, memory-bridge]
---

# Paperclip / Cortana Operations

Use this skill when the user asks to study or continue work in a Cortana/Paperclip platform directory, activate or verify an agent roster, debug agent heartbeat runs, inspect Cortana plugin-layer readiness, or move a Paperclip-based AI agency toward full operation.

## Operating posture

Cortana v2-style stacks are best treated as **vanilla Paperclip plus a thin Cortana plugin layer**. Do not assume source-tree modification is allowed. Keep the layers distinct:

1. **Paperclip runtime:** Docker services, Paperclip server, `paperclip` database, `agents`, `issues`, `heartbeat_runs`, `board_api_keys`.
2. **Cortana plugin state:** `state/agents`, manifests, capability markers, vault/memory layout, activation approvals.
3. **Harness config:** agent `adapter_config`, per-agent Hermes profiles, provider/model selection, auth posture.
4. **Memory bridge:** router `/v1/memory/*`, MCP bridge, `memory-execution.jsonl` audit rows.
5. **Docs/run-sheets:** sprint ledger, STEP docs, session handoffs, operator run-sheets.

## First-pass review sequence

1. **Read the current handoff and sprint ledger first.** Look for `docs/session-handoff-*.md`, `docs/CORTANA-SPRINTS.md`, the active run-sheet, and relevant STEP docs.
2. **Name the active slice and next gate.** If another agent handed off “run Phase B3 agent X next,” do not skip ahead to broad cleanup.
3. **Map the repo without drowning in dependency trees.** Exclude `.git`, `node_modules`, data volumes, logs, archives, and generated build dirs.
4. **Reconcile truth surfaces:** docs say intended state, disk markers/manifests show plugin identity state, but live DB rows are runtime-authoritative for status and adapter config.
5. **Separate proven from unproven.** If Docker/DB access is unavailable, say exactly which live claims are unverified and ask for the smallest SQL/log output needed.

## Runtime readiness checklist

A roster or agent is not “fully operational” until there is evidence at each necessary layer:

- services are up and reachable
- expected agents are present and `idle` in live DB
- temporary activation tokens are revoked
- capability markers exist on disk for the agent(s)
- `adapter_config` has canonical provider/model/env shape
- env values are plain strings, not UI-wrapped `{type,value}` objects
- no subscription-auth agent has API keys in env/config
- representative heartbeat run reaches `succeeded`
- issue status/comment prove semantic task completion
- memory work, when relevant, has fresh `memory-execution.jsonl` rows showing actual dispatch

Paperclip `heartbeat_runs.status='succeeded'` is not enough by itself. The audit log is the lower-layer proof for memory tools.

## Adapter and auth pitfalls

- Treat live DB `agents.adapter_config` as runtime truth; disk manifests may lag after SQL patch runs.
- Some `hermes-paperclip-adapter` versions do not accept `anthropic` through their normal provider allowlist. In that case, Anthropic OAuth routing requires `extraArgs: ["--provider", "anthropic"]` and a plain model id such as `claude-opus-4-7`.
- Avoid editing Cortana agent adapter config through the Paperclip UI when the UI wraps env values into `{"type":"plain","value":...}`. SQL-edit and normalize instead; wrapped env values can become `HERMES_HOME=[object Object]` at process spawn.
- Respect subscription-only lanes: Claude/Codex subscription agents should not get `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` injected into control-plane or agent env.
- Back up Postgres before mutating live agent rows. Use scoped board API keys for wakeups and revoke them after the smoke.

## Operator-facing output style

For Bang/operator handoffs, produce run-sheet-grade output:

- what was actually inspected
- what is proven vs unproven
- active slice and next gate
- blockers with exact evidence
- minimal targeted questions needed to continue
- paste-ready SQL/curl blocks when the next step is known

Avoid a generic narrative. The deliverable should let the operator continue work immediately.

## References

- `references/cortana-v2-operational-readiness.md` — condensed readiness pattern and acceptance checks from a `platform-v2` review session.
