---
name: langgraph-triage
description: Layered triage for self-hosted LangGraph Platform (langgraph-api) deployments — boot crashes, 502s, auth holes, silent graph failures, and model/provider errors. Trigger whenever a LangGraph deployment misbehaves on any host (Railway, Fly, Render, ECS, K8s, Docker): "langgraph crashed", "deploy is crash-looping", "502 from the langgraph server", "runs stay running forever", "agent never calls tools", "approvals never appear", "thread won't resume", "interrupt is stuck", KeyError Config missing, License verification failed, "no endpoints found for model", "relation thread_ttl does not exist", or any langgraph-api / langgraph-cp / control-plane deployment issue. Also trigger BEFORE a first LangGraph deploy to run the pre-flight checklist. Do NOT trigger for Paperclip/Cortana agent issues (paperclip-triage) or generic app debugging (systematic-debugging).
version: 0.1.0
---

# LangGraph Triage

Incident-grade triage for self-hosted LangGraph Platform deployments (the `langchain/langgraph-api` image and its Go core + Python API pair). Distilled from a full production bring-up that hit **eleven distinct failures in one day** — every one is cataloged in `references/failure-catalog.md` with its exact error signature, root cause, and fix.

The architecture under triage is always the same shape: **App server** (owns data + tool boundary) ↔ **LangGraph server** (graph runtime; Postgres checkpoints, Redis queue) ↔ **Model provider/router**. The LangGraph server should hold NO app credentials — its only write path is the app's authenticated tool API.

## Core principles

1. **The failure is an onion — config validation is sequential.** The server validates one requirement at a time and crashes on the first miss. Fixing `DATABASE_URI` reveals `REDIS_URI`; fixing that reveals the license check. Expect 3–6 rounds on a first deploy; read each new traceback fresh instead of assuming the previous fix failed.
2. **Identify the layer before touching anything.** Build → boot config → persistence → edge/networking → API auth → dispatch → graph runtime → model provider → graph logic. The error's *source* names the layer: platform proxy errors are edge; `uvicorn`/`starlette.config` tracebacks are boot; `langgraph_api.worker` errors are graph runtime; `openai.*` exceptions are the provider hop (even for non-OpenAI models — the OpenAI client is the transport).
3. **Two processes share one container.** The Python API (uvicorn) and the Go core-server boot together and do NOT read config identically — the Go side ignores URI `?options=` parameters the Python side honors. Any "works in one log, fails in another" symptom is usually this split. Fix config at a level both honor (e.g., Postgres role settings, plain env vars).
4. **Distrust green checkmarks.** "Deployment SUCCESS" ≠ serving (port mismatch), "run succeeded" ≠ work done (plan-once graphs), an HTTP fetch with an empty body ≠ healthy (some fetch tools swallow 502s). Verify each layer with its own ground truth: the uvicorn bind line, the platform's http/proxy logs with upstream errors, `GET /info` returning real JSON, and rows in the checkpoint schema.
5. **The graph state schema is a silent filter.** LangGraph drops any run-input key not declared in the `State` TypedDict — no error, no warning. If the model asks for information you're certain you sent, the schema ate it.
6. **Replay is not a bug.** On resume after `interrupt()`, the node body re-executes from the top. Side effects before the interrupt run twice — they must be idempotent (dedupe server-side by canonical `(tool, args)` per run) or moved after the interrupt.
7. **Auth defaults to wide open.** A fresh self-hosted server runs `auth=noop`: the entire `/threads` API — including reading thread state and starting runs — is public. Test it, prove it, close it (see catalog §10).

## The triage ladder

Work top-down; stop at the first failing layer. Each layer's verification is independent.

| # | Layer | Verify with | Failing signature → catalog § |
| --- | --- | --- | --- |
| 1 | Build | Platform build logs | Docker build errors; regenerate Dockerfile with `langgraph dockerfile` §12 |
| 2 | Boot config | Deploy logs (Python traceback near "Starting API server") | `KeyError: "Config 'X' is missing"` §1–2; `License verification failed` §3 |
| 3 | Persistence | Checkpoint tables land in the intended schema; no sweeper errors | `relation "thread_ttl" does not exist` / SQLite "no such table: run" §4; `SET ROLE` §5; IPv6 unreachable §6 |
| 4 | Edge / port | `GET /ok`, `GET /info` return JSON; http/proxy logs show 200s | 502 "connection refused" upstream §7 |
| 5 | API auth | Unauthenticated `GET /threads/<uuid>/state` should 401/403 | Returns data → server is public §10 |
| 6 | Dispatch | App logs: `POST /threads/{id}/runs` → 200 | 404 thread not found §8; 401 from app→server key mismatch §10 |
| 7 | Graph runtime | `run` table in checkpoint schema: `status`; worker logs `Run encountered an error` | provider errors §13–15; graph exceptions |
| 8 | Model provider | The `openai.*` exception's HTTP code + body | 401 empty header §13; 404 model slug §14; 400 tool names §15 |
| 9 | Graph logic | Run "succeeded" but expected side effects absent | dropped state keys §16; plan-once vs loop §17; stuck interrupts §18 |

## Quick diagnostics

```bash
# Layer 4 — is it actually serving? (/info returns JSON with versions)
curl -sS https://<host>/ok ; curl -sS https://<host>/info

# Layer 4 — what port did uvicorn ACTUALLY bind? (must match domain target port)
#   platform deploy logs, filter: "Uvicorn running"

# Layer 5 — is the API public? (a 200 here is a security incident)
curl -sS -o /dev/null -w "%{http_code}" https://<host>/threads/00000000-0000-0000-0000-000000000000/state

# Layer 7 — what does the graph runtime think happened?
#   SQL against the checkpoint schema:
select run_id, thread_id, status, created_at from <schema>.run order by created_at desc limit 5;

# Layer 7 — the real exception:
#   platform deploy logs, filter: "Run encountered an error"

# Layer 9 — what did the model actually say/do? (thread state, needs auth once closed)
curl -sS -H "x-api-key: $KEY" https://<host>/threads/<thread_id>/state
```

## Pre-flight checklist (run BEFORE first deploy)

- [ ] Env vars: `DATABASE_URI` (not `_URL`), `REDIS_URI` (Redis service exists), `LANGSMITH_API_KEY` (free key; required for Self-Hosted Lite license), model provider key, app tool-API URL + shared token.
- [ ] `PORT` env var explicitly pinned to the public domain's target port (langgraph-api obeys injected `PORT`, overriding its 8000 default) — §7.
- [ ] Postgres: dedicated login role + schema; `alter role <role> set search_path = <schema>` at the ROLE level (URI `?options=` is ignored by the Go core) — §4. No grants on the app's schema.
- [ ] Auth: `langgraph.json` has an `"auth"` entry; `auth.py` enforces `x-api-key` with `hmac.compare_digest`; Dockerfile regenerated after adding it — §10.
- [ ] Client run-creation includes `"if_not_exists": "create"` if the app mints thread ids — §8.
- [ ] Model slug verified against the router/provider catalog TODAY (slugs retire) — §14.
- [ ] Tool names model-safe: `^[a-zA-Z0-9_-]{1,128}$` — no dots; sanitize/round-trip if internal ids differ — §15.
- [ ] Every run-input key declared in the `State` TypedDict — §16.
- [ ] Graph loops (tool results → model → …) with a turn cap, and reports completion to the app on **all** exit paths: natural finish, tool error, model error, turn cap — §17.
- [ ] Resume fires on BOTH approve and reject decisions — a reject that never resumes freezes the thread forever — §18.
- [ ] Env-change discipline: platform env edits only apply to deployments created AFTER the edit. Change vars → then deploy — §9.

## Working style

- Prefer platform MCP/API log access over asking the operator to paste logs — filter deploy logs for `Uvicorn running`, `Run encountered an error`, and read http/proxy logs' `upstreamErrors` field.
- When a platform agent/UI config edit "succeeds", re-read the config to confirm it persisted; prefer env-var pinning over UI-side settings when both can express the fix.
- Verify from both sides: the app's runtime errors name the request that failed; the LangGraph server's worker logs name why. The checkpoint schema's `run.status` arbitrates.
- Keep a running fix log — first deploys are onions, and the catalog grows from every new layer found. Append new signatures to `references/failure-catalog.md`.

## References

- `references/failure-catalog.md` — the full error-signature catalog: 18 numbered failures with verbatim signatures, root causes, fixes, and verification steps.
