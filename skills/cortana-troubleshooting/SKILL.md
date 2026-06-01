---
name: cortana-troubleshooting
description: This skill should be used when the user asks to "debug Cortana", "troubleshoot Paperclip", "check the router", "investigate a stuck task", "verify Symba", "run Cortana smoke tests", "diagnose duplicate returns", "check budget drift", or "set up continuous QA for Cortana".
version: 0.1.0
---

# Cortana Troubleshooting

Diagnose Cortana platform failures across Paperclip, `cortana-http-shim`,
`cortana-llm-router`, Postgres, budget accounting, agent configuration, skills,
and the Paperclip UI. Treat this skill as the first-response playbook for local
Cortana incidents and as the baseline for a continuous QA agent.

## Operating Rules

Start from `/Users/nolan/Cortana/platform`.

Never read, write, search, stage, or use `/Users/nolan/Documents` or
`/Users/Nolan/Documents`. Treat any path under Documents as blocked even when a
tool or capability appears to allow it.

Prefer read-only diagnostics first. Do not mutate Docker state, database rows,
capability markers, dispatch gates, agent records, budgets, credentials, or
Paperclip issues until the failure mode is understood and the operator has
approved the exact remediation.

Never print secrets. Redact API keys, OAuth tokens, bearer tokens, JWTs,
database passwords, cookie values, and Keychain material from logs and reports.

Do not run paid real-model probes unless all existing real-call gates are
explicitly open and the operator asks for a real-call test. Default to dry-run,
health, readiness, verifier, and database read checks.

## First Response Workflow

1. Capture a read-only system snapshot:

   ```bash
   ./workspaces/cortana-skills/cortana-troubleshooting/scripts/cortana-system-snapshot.sh
   ```

2. Classify the incident before touching code:

   - Paperclip task lifecycle: stuck `in_progress`, repeated heartbeat,
     duplicated comments, missing completion, or stale issue status.
   - Router dispatch: provider refusal, transport failure, auth failure, budget
     refusal, tool-call mismatch, or truncated provider response.
   - Shim contract: missing task instruction, missing model/provider config,
     bad response normalization, capability pre-check mismatch, or duplicate
     comment projection.
   - UI rendering: truncated message, duplicate message container, stale budget
     display, missing model metadata, or broken agent configuration control.
   - Skills/memory: skills shown as tracked-only, missing `agent_skills` rows,
     tool execution not wired, or memory retrieval/write path not proven.

3. Inspect authoritative evidence in this order:

   - Browser-visible symptom and exact URL.
   - Paperclip run transcript and events.
   - Router `/healthz` and `/readyz`.
   - Router audit/ledger tables.
   - Paperclip issue/comment/run/task rows.
   - Shim logs and adapter config.
   - Existing verification gates.
   - Source code only after runtime evidence identifies the boundary.

4. Preserve the invariant: one successful router completion should produce one
   durable run result, one visible issue response, one terminal task transition,
   and one budget ledger entry.

5. Write a short incident note with:

   - Symptom.
   - Scope.
   - Evidence.
   - Root cause hypothesis.
   - Minimal fix.
   - Verification command.
   - Regression test to add.

## Core References

Load only the needed reference file:

- `references/triage-playbook.md` - Symptom-to-component diagnosis map for the
  failures Cortana has already hit.
- `references/smoke-tests.md` - Safe smoke, verifier, browser, and database
  checks, with paid-call guardrails.
- `references/continuous-qa-loop.md` - How to run a persistent QA agent without
  causing loops, spend leaks, or state mutations.
- `references/adaptation-log.md` - Living memory of Cortana failure patterns and
  fixes. Append new lessons after significant incidents.

## Snapshot Script

Use `scripts/cortana-system-snapshot.sh` for a read-only baseline. The script
checks Docker service state, Paperclip health, router health/readiness, current
agent/task/budget counts, recent router audit rows, key verification scripts,
and blocked Documents references. It does not start, stop, recreate, delete, or
write production state.

## Escalation Rules

Stop and ask for operator approval before:

- Deleting Paperclip issues, comments, runs, or agents.
- Updating `agents.adapter_config`.
- Opening real-call rails or running paid real-provider tests.
- Granting capability markers.
- Changing model/provider assignments.
- Running Docker recreate/down/prune commands.
- Editing upstream Paperclip code when a Cortana adapter or isolated patch can
  solve the issue.

## Regression Standards

Every fix must add or identify a regression check for the failed invariant.
Prefer existing gates:

- `./scripts/verify-cortana.sh`
- `./scripts/verify-s10d-9-router-ui-budget.sh --vitest`
- Router unit tests under `containers/cortana-llm-router/test/`
- Shim tests under `workspaces/cortana-adapters/cortana-http-shim/`
- Paperclip UI tests around issue chat, agent config, and budget pages

When a failure crosses router, shim, Paperclip lifecycle, and UI, add one
boundary-level unit test plus one end-to-end verifier assertion.
