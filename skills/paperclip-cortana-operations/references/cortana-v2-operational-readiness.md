# Cortana v2 operational-readiness review pattern

Use this reference when asked to study `platform-v2`, continue another agent's work, or decide what is needed to make a Paperclip/Cortana agency operational.

## Scope model

Cortana v2 is a **vanilla Paperclip + thin Cortana plugin layer** stack. Do not assume Paperclip source modifications are acceptable. Treat these as distinct layers:

1. Paperclip runtime and DB (`paperclip` database, agents/issues/heartbeat tables).
2. Cortana plugin state (`state/agents`, capability markers, vault/memory layout).
3. Hermes/Paperclip adapter config (`agents.adapter_config`, per-agent Hermes profiles).
4. Memory bridge/router (`/v1/memory/*`, `memory-execution.jsonl`).
5. Sprint/STEP docs and operator run-sheets.

## Fast review sequence

1. Read the current handoff and sprint ledger first:
   - `docs/session-handoff-*.md`
   - `docs/CORTANA-SPRINTS.md`
   - active run-sheet, e.g. `docs/co-roster-activation-runsheet.md`
2. Identify the active slice and exact next gate. For roster activation, the handoff may point to a specific B3 spot-check agent; do not skip ahead.
3. Reconcile three truth surfaces:
   - docs/run-sheets: intended state and sequence
   - disk manifests/markers: identity/capability state
   - live DB rows: authoritative runtime config/status
4. If Docker/DB access is unavailable, state that limitation and request/prompt for the smallest pasteable SQL outputs. Do not infer live status from files alone.
5. For operational readiness, require proof at the lowest layer that matters:
   - heartbeat `succeeded` proves adapter run completion only
   - issue comment/status proves semantic task completion
   - `memory-execution.jsonl` proves actual memory tool dispatch

## Roster activation acceptance

For a Cortana v2 roster to be considered operational, collect all of:

- expected agents are `idle` in live DB
- scoped activation board tokens revoked
- per-agent memory markers present on disk
- adapter config has canonical provider/model/extraArgs/env shape
- `adapter_config.env` values are plain strings, not UI-wrapped objects
- no API keys are present in agent env/config for subscription-auth agents
- representative fresh heartbeat smokes succeeded
- at least one representative fresh memory smoke has audit rows with `decision=allowed` and `audit_category=live_*_success`

## Provider/config pitfalls

- `agents.adapter_config` in the DB is runtime-authoritative. Disk manifests may be stale identity metadata; flag drift instead of assuming manifests control routing.
- For `hermes-paperclip-adapter` versions whose provider allowlist lacks `anthropic`, Anthropic routing requires `extraArgs: ["--provider", "anthropic"]` plus a plain model id like `claude-opus-4-7`.
- Do not edit Cortana agent adapter configs in the Paperclip UI if the UI wraps `env` values into `{type,value}` objects; SQL-edit and normalize instead.
- Subscription-only posture means no `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` in agent env or control-plane config for Claude/Codex subscription agents.

## Minimal questions after a platform review

Ask only questions that change the next action. Usually:

1. Did the currently named activation/heartbeat smoke land `succeeded`?
2. Is Docker/DB access available in this session, or should the agent provide operator paste blocks?
3. Is the documented provider/cost tier still the desired posture?
4. Should cleanup slices wait until the active activation slice is closed?

## Output shape for Bang/operator

The useful deliverable is an operator-grade readiness report:

- what was actually inspected
- what is proven vs unproven
- active slice / next gate
- blockers with exact evidence
- minimal targeted questions needed to continue
- paste-ready SQL/curl blocks only when the next step is clear

Avoid turning the report into a long narrative; preserve the run-sheet orientation.
