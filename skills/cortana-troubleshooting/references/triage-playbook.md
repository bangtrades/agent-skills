# Cortana Triage Playbook

Use this file after the top-level `SKILL.md` workflow identifies the symptom.
Prefer runtime evidence before source edits.

## Component Boundaries

| Boundary | Owns | First evidence |
| --- | --- | --- |
| Paperclip lifecycle | Issues, runs, heartbeats, task status, comments, run summaries | UI run events, Postgres issue/run/comment rows |
| `cortana-http-shim` | Adapter config, task instruction extraction, capabilities, router request body, response normalization | Paperclip run transcript, shim logs, adapter tests |
| `cortana-llm-router` | Provider dispatch, auth, four-lock guard, budget enforcement, audit, ledger | `/readyz`, router logs, audit/ledger tables |
| Provider SDK | Anthropic/OpenAI/local provider request and response | Router provider result, stop reason, token counts |
| Paperclip UI | Message rendering, truncation, dedupe, budget display, model selector | Browser page, UI tests |
| Skills/memory | Skill inventory, `agent_skills`, tool schemas, future dispatcher, memory retrieval | Skills tab, skill manifests, database rows |

## Known Symptoms

### Task Loops After Successful Router Calls

Likely boundary: Paperclip lifecycle plus shim completion contract.

Check:

```bash
docker exec cortana-postgres psql -U cortana -d cortana -c "select id, status, title, updated_at from issues order by updated_at desc limit 10;"
docker exec cortana-postgres psql -U cortana -d cortana -c "select id, status, agent_id, created_at from runs order by created_at desc limit 10;"
```

Confirm whether the issue stayed `in_progress` despite a `succeeded` run.
Expected invariant: successful one-shot completion should transition the issue
to a terminal state or emit a deliberate continuation signal.

Regression gate: lifecycle test for successful router completion and
`./scripts/verify-s10d-9-router-ui-budget.sh --vitest`.

### Duplicate Chat Return Containers

Likely boundary: Paperclip UI message projection/dedupe.

Check whether a router result and a comment are both rendered for the same run.
Historical fix: dedupe must consider both `runId` and `createdByRunId`.

Regression gate: `issue-chat-messages` tests and the S10D-9 UI gate.

### Truncated Return Text

Likely boundary: UI rendering or Paperclip activity serialization.

Distinguish provider truncation from UI truncation:

- Provider truncation: router/provider response has `stop_reason=max_tokens` or
  missing tail in stored JSON.
- UI truncation: stored JSON has full text but issue chat card collapses it.

Inspect run `result_json` before changing UI.

### `router transport error: fetch failed`

Likely boundary: container network, router container health, service DNS, or
router restart.

Check:

```bash
docker ps --filter name=cortana --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
curl -fsS http://127.0.0.1:4400/healthz
curl -fsS http://127.0.0.1:4400/readyz
docker logs --tail 80 cortana-llm-router
```

If host curl succeeds but shim fails, inspect Compose network and service name.

### `no task instruction was supplied`

Likely boundary: Paperclip assignment payload extraction in shim.

Check whether the issue title/body/comment text reached the adapter invocation.
Do not call the provider when instruction text is empty. Refusal before spend is
correct; the bug is upstream payload extraction or task creation.

### Budget Page Shows `$0.00` Despite Real Calls

Likely boundary: Paperclip budget read model.

Check `llm_cost_ledger` and agent budget endpoint. Expected invariant: observed
spend should include router ledger spend by agent/provider/model for the
relevant period.

### Skills Show "Tracked Only"

Likely boundary: expected current limitation unless skill sync/runtime dispatcher
has shipped for `cortana_llm_router`.

Check `company_skills`, `agent_skills`, `adapter_config.skills_enabled`, and
`workspaces/cortana-skills/*/skill.json`. Do not claim a skill can execute until
the tool dispatcher is proven.

### Model Selection Falls Back Silently

Likely boundary: router model registry or shim request construction.

Expected invariant: requested provider/model alias must either resolve exactly
or refuse before spend. Never silently fall back from OpenAI to Anthropic or from
Opus to Sonnet.

### OpenAI OAuth/Subscription Ambiguity

Likely boundary: auth feasibility, not router code.

Use official OpenAI documentation or verified local CLI behavior. Do not claim
ChatGPT subscription OAuth can power direct API calls unless official evidence
or a supported local auth flow proves it. Record the credential mode as
`api_key`, `oauth_token`, `unsupported`, or `not_configured`.
