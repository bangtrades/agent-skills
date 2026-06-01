# Cortana Smoke Tests

All commands assume `/Users/nolan/Cortana/platform`.

## Safe Default Snapshot

```bash
./workspaces/cortana-skills/cortana-troubleshooting/scripts/cortana-system-snapshot.sh
```

This is read-only and suitable for first response.

## Core Health

```bash
./scripts/healthcheck.sh
curl -fsS http://127.0.0.1:4400/healthz
curl -fsS http://127.0.0.1:4400/readyz | python3 -m json.tool
curl -fsS http://127.0.0.1:4200/api/health
```

If `/api/health` is unavailable, use the browser at
`http://localhost:4200/COR/dashboard` and inspect container logs.

## Current Regression Gate

```bash
./scripts/verify-s10d-9-router-ui-budget.sh --vitest
```

Use this after any Paperclip UI, router-result, chat-dedupe, or budget-display
change.

## Broader Verifier

```bash
./scripts/verify-cortana.sh
```

Use the broad verifier before handing a larger slice back to the operator.

## Router Unit Tests

```bash
cd containers/cortana-llm-router
python3 -m pytest test
```

Prefer targeted tests while debugging provider/auth/budget changes.

## Paperclip UI Tests

Run targeted tests from the Paperclip workspace. Use the package manager already
configured by the repo.

```bash
cd workspaces/paperclip
pnpm test -- issue-chat-messages
pnpm typecheck
```

Adjust exact test selectors to match existing scripts.

## Read-Only Database Checks

Use these only for inspection. Do not update or delete rows without explicit
operator approval.

Recent agents:

```bash
docker exec cortana-postgres psql -U cortana -d cortana -c "select id, name, adapter_type, status, adapter_config from agents order by name;"
```

Recent issues:

```bash
docker exec cortana-postgres psql -U cortana -d cortana -c "select id, key, title, status, updated_at from issues order by updated_at desc limit 20;"
```

Recent runs:

```bash
docker exec cortana-postgres psql -U cortana -d cortana -c "select id, agent_id, status, created_at, completed_at from runs order by created_at desc limit 20;"
```

Router ledger:

```bash
docker exec cortana-postgres psql -U cortana -d cortana -c "select agent_id, provider, model, cost_usd, created_at from llm_cost_ledger order by created_at desc limit 20;"
```

Router audit:

```bash
docker exec cortana-postgres psql -U cortana -d cortana -c "select event_type, decision, provider, model, refusal_reason, created_at from llm_router_audit order by created_at desc limit 20;"
```

## Browser Checks

Use browser inspection for:

- One visible response container per router completion.
- Full text visible in issue chat.
- Budget observed spend matches ledger.
- Agent Configuration displays provider/model state once model routing lands.
- Skills page truthfully distinguishes tracked, synced, and executable states.

## Real-Call Guardrail

Only run paid model tests when the operator explicitly asks and the real-call
approval rails are intentionally open. Prefer existing guarded scripts:

```bash
./scripts/cortana-router-smoke-real.sh
```

Never add a new real-call script that bypasses approval markers, env flags,
budget checks, or capability checks.
