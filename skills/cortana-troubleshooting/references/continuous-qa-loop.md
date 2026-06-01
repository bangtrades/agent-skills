# Continuous QA Loop

Use this reference when assigning a Cortana QA agent to monitor platform health.
The QA loop must be useful without spending cloud tokens or mutating state.

## Cadence

Run lightweight checks frequently and expensive checks only on demand.

Suggested local cadence:

- Every 15 minutes: read-only snapshot.
- Every hour: `./scripts/healthcheck.sh`.
- After each code slice: targeted regression gate.
- Before operator live testing: current sprint verifier.
- After real-call tests: ledger/budget reconciliation.

## Allowed By Default

- Read Docker container status.
- Read Paperclip/router health endpoints.
- Read logs with bounded `--tail`.
- Run no-spend verifier gates.
- Read Postgres tables with `select`.
- Inspect UI pages through browser automation.
- Produce incident reports and proposed fixes.

## Requires Operator Approval

- Running paid OpenAI/Anthropic calls.
- Changing model/provider configuration.
- Granting capabilities or opening real-call rails.
- Deleting or updating Paperclip tasks/issues/comments/runs.
- Recreating containers.
- Editing `.env`, Keychain entries, OAuth tokens, or API keys.

## Standard QA Output

Produce a compact report:

```markdown
# Cortana QA Snapshot

Time:
Overall state: green | yellow | red

Checks:
- Paperclip:
- Router:
- Shim:
- Budget:
- Tasks:
- Skills:
- Memory:
- UI:

Findings:
1.

Recommended action:

Regression coverage:
```

## Anti-Loop Rule

A QA agent must not assign itself or Symba repeated tasks to test heartbeats
unless the task title contains `QA-SMOKE` and the prompt includes a hard
completion sentinel such as `TASK_COMPLETE`. Prefer script-level checks over
Paperclip heartbeat tests.

## Spend Rule

Treat every provider call as production spend. A monitoring agent should not
call cloud providers merely to prove the monitoring agent is alive. Use health,
readiness, dry-run, and ledger reconciliation instead.

## Adaptation Rule

After each resolved incident, append a short entry to
`references/adaptation-log.md` with:

- Date.
- Symptom.
- Root cause.
- Fix.
- Regression gate.
- Any new "never again" rule.
