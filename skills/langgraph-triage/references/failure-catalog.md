# LangGraph deployment failure catalog

Verbatim error signatures → root cause → fix → verification. Numbered; SKILL.md's triage ladder references these sections. All observed in production bring-ups of the `langchain/langgraph-api` self-hosted image; host examples use Railway but every failure is host-agnostic unless noted.

---

## Boot-time config (sequential — fixing one reveals the next)

### §1 — `KeyError: "Config 'DATABASE_URI' is missing, and has no default."`

Python traceback through `starlette/config.py`, crashes uvicorn at import. A Go-side symptom often appears alongside: `SQL logic error: no such table: run` (SQLite language — part of the runtime fell back to in-memory mode without Postgres).

**Cause:** env var not reaching the container. In order of likelihood: variable added *after* the deploy started building (env snapshots — see §9); named `DATABASE_URL` instead of `DATABASE_URI`; set at project/shared level but not attached to the service; set in the wrong environment; value still contains a placeholder like `REPLACE_ME`.

**Fix:** set `DATABASE_URI` on the service itself, exact spelling, raw `postgresql://...` (no quotes, no `psql` prefix), then trigger a fresh deploy.

### §2 — `KeyError: "Config 'REDIS_URI' is missing, and has no default."`

**Cause:** langgraph-api requires Redis (run queue / pubsub); easy to omit because tutorials rarely mention it.

**Fix:** provision a Redis instance alongside the service. On Railway: add a Redis database service, then `REDIS_URI=${{Redis.REDIS_URL}}` (prefer the private-network URL where offered).

### §3 — `ValueError: License verification failed.` / `No enterprise license key or LangSmith API key found`

Boot proceeds through Postgres migration, THEN dies — the license check runs after persistence init, so this can masquerade as "crashed after running for a couple of minutes."

**Cause:** `LANGSMITH_API_KEY` missing or invalid. Self-Hosted Lite requires it (free key suffices) for a phone-home license check.

**Fix:** create a key at smith.langchain.com → Settings → API Keys; set `LANGSMITH_API_KEY`. (Enterprise: `LANGGRAPH_CLOUD_LICENSE_KEY`.)

---

## Persistence

### §4 — `ERROR: relation "thread_ttl" does not exist (SQLSTATE 42P01)` from sweepers, while Python-side migrations succeeded

**Cause:** split-brain between the container's two processes. The Python API honors the `?options=-c%20search_path%3D<schema>` URI parameter and created its ~11 tables in the isolated schema; the Go core-server ignores `options` and looks in `public`.

**Fix (driver-proof):** set the search path at the ROLE level so every connection gets it regardless of driver:
```sql
alter role <langgraph_role> set search_path = <schema>;
```
Restart/redeploy (existing pools don't pick up role settings). The URI suffix may stay — harmless.

**Verify:** sweeper errors stop; `select table_schema, count(*) from information_schema.tables where table_name in ('run','thread','assistant','checkpoints','thread_ttl') group by 1;` shows everything in the isolated schema, nothing in `public`.

### §5 — `ERROR: 42501: must be able to SET ROLE "<role>"` when creating the schema

**Cause:** Supabase (and other managed Postgres) `postgres` user isn't a superuser; it can't create objects owned by another role without membership.

**Fix:**
```sql
grant <role> to postgres;   -- postgres acts on behalf of the new role; isolation unchanged
create schema if not exists <schema> authorization <role>;
```

### §6 — Postgres unreachable (`ENETUNREACH` / connect timeouts) from the deploy host

**Cause:** Supabase's direct host (`db.<ref>.supabase.co:5432`) is IPv6-first; many container platforms lack outbound IPv6 by default.

**Fix:** enable outbound IPv6 on the service (Railway has a toggle), or switch to the provider's session-pooler URI (IPv4), keeping the role/search-path setup identical.

---

## Edge / networking

### §7 — 502 `"Application failed to respond"`; proxy logs show `upstreamErrors: connection refused`

Deployment status is SUCCESS; app logs are healthy; nothing answers.

**Cause:** port mismatch. The platform injects a `PORT` env var and **langgraph-api's uvicorn honors it**, overriding its 8000 default — while the public domain routes to whatever target port was configured. Region moves and redeploys can silently change the injected value.

**Fix (deterministic):** pin `PORT=<domain target port>` as an explicit service env var so both sides agree forever. Verify via the deploy-log line `Uvicorn running on http://0.0.0.0:<port>` matching the domain config.

**Trap:** naive health probes lie — some fetch tools return an empty body for a 502 page and look "successful." Trust the platform's http/proxy logs (status + upstreamErrors) and require real JSON from `GET /info`.

---

## Client ↔ server API

### §8 — `POST /threads/{id}/runs` → 404 when the app mints its own thread ids

**Cause:** threads must exist before runs unless the request opts into creation.

**Fix:** include `"if_not_exists": "create"` in the run-creation body (both initial runs and resume calls).

### §9 — App dispatches with stale/missing config after env var changes

Symptoms: "X unset — dispatch skipped" notices, or 401s against the LangGraph server right after adding the key.

**Cause:** serverless platforms (Vercel et al.) snapshot env at build time. A var added after the running deployment was built does not exist in production until a NEW deployment.

**Fix + habit:** change env vars first, then deploy. Verify by checking which deployment the erroring function ran on (runtime error metadata names it).

### §10 — The LangGraph API is publicly open (`auth type=noop` in boot logs)

**Test:** unauthenticated `GET https://<host>/threads/<any-uuid>/state` from the public internet. If it returns JSON instead of 401, anyone can read threads and start runs (spend your model budget, exfiltrate state).

**Fix:** custom auth. `langgraph.json`:
```json
"auth": { "path": "./src/<pkg>/auth.py:auth" }
```
`auth.py`:
```python
import hmac, os
from langgraph_sdk import Auth
auth = Auth()

@auth.authenticate
async def authenticate(headers: dict) -> Auth.types.MinimalUserDict:
    expected = os.environ.get("LANGGRAPH_API_KEY", "")
    raw = headers.get(b"x-api-key") or headers.get("x-api-key") or b""
    provided = raw.decode() if isinstance(raw, bytes) else raw
    if not expected or not provided or not hmac.compare_digest(provided, expected):
        raise Auth.exceptions.HTTPException(status_code=401, detail="invalid or missing x-api-key")
    return {"identity": "app-server"}
```
Regenerate the Dockerfile (`langgraph dockerfile Dockerfile`) so `LANGGRAPH_AUTH` is baked in. Set the SAME `LANGGRAPH_API_KEY` on both the LangGraph host and the app host; app sends it as `x-api-key`. Deploy order: app first (starts sending the header — harmless against a noop server), then the LangGraph server (starts enforcing).

### §11 — Interrupted thread never resumes after operator decision

**Cause:** the app only calls the resume API on *approval*. A rejection leaves the graph parked at `interrupt()` forever.

**Fix:** resume on BOTH decisions, passing the verdict (`{approvalId, approved: bool}`); the graph converts a rejection into tool feedback ("operator rejected, do not retry") so the model can adapt.

**Related replay trap:** on resume, LangGraph re-executes the interrupted node body from the top. Side effects before `interrupt()` run again. Make the app-side effect idempotent — e.g., dedupe approval creation per run by canonical JSON of `(tool, args)` (sorted keys), returning the existing approval id instead of minting duplicates.

### §12 — Build/packaging drift

Regenerate the Dockerfile with the langgraph CLI (`pip install langgraph-cli && langgraph dockerfile Dockerfile`) whenever `langgraph.json` changes (graphs, auth, deps) — several settings are baked into image env at generation time (`LANGSERVE_GRAPHS`, `LANGGRAPH_AUTH`). Add a `.dockerignore` covering `.env*`, `__pycache__`, `.venv`.

---

## Model / provider hop (surface as `openai.*` exceptions in `langgraph_api.worker` logs regardless of actual provider)

### §13 — `openai.AuthenticationError: 401 ... 'Missing Authentication header'`

**Cause:** the provider key env var exists but is EMPTY — the client sends no Authorization header at all. Classic after a key rotation that never reached the deploy host. (An *invalid* key yields a different message — "invalid key/unauthorized" — with the header present.)

**Fix:** paste the current key into the service env; redeploy.

### §14 — `openai.NotFoundError: 404 ... 'No endpoints found for <model-slug>'`

**Cause:** retired or wrong model slug (router catalogs churn — a slug that worked at project start can be gone months later). Auth is fine (the error includes your org/user id).

**Fix:** verify the slug against the router/provider catalog TODAY; update everywhere it's declared — service env (`DEFAULT_MODEL`), any DB-seeded per-agent model fields, code fallbacks, and `.env.example`. Don't edit applied migrations; seeds and env only.

### §15 — `400 ... "tools.0.custom.name: String should match pattern '^[a-zA-Z0-9_-]{1,128}$'"` from every provider

**Cause:** dots (or other punctuation) in model-facing tool names. Namespaced internal ids like `domain.tool_name` are fine internally but illegal as function names for Anthropic (and enforced across providers when routed).

**Fix:** sanitize at the spec boundary — `name = tool_id.replace(".", "__")` when building tool specs; translate back before execution — `tool_id = name.replace("__", ".")` (idempotent for already-dotted input). Internal registries, DBs, and audit logs keep dotted ids.

---

## Graph logic (run "succeeds" but the work is wrong)

### §16 — Model asks for context you definitely sent (`"the payload doesn't include an engagement ID..."`)

**Cause:** LangGraph **silently drops** any run-input key not declared in the `State` TypedDict. No error. The model never saw the data.

**Fix:** declare every input key in the state schema, and put critical identifiers (ids/UUIDs the tools require) directly into the prompt text with "use these verbatim in your tool calls."

**Diagnose:** `GET /threads/<id>/state` — read `values.messages` to see exactly what the model received and replied; `values` shows which state keys survived.

### §17 — Run reports `succeeded`, zero tool effects (or one read, then stop)

**Cause:** plan-once-execute-once skeleton: the model gets ONE turn; if it sensibly reads data first, it never gets a second turn to act. Also: completion reporting attached only to one node means model-node errors strand runs at `running`.

**Fix:** a real agent loop — tool results append as `ToolMessage`s (with `tool_call_id`), model re-invoked until it stops calling tools; hard turn cap (e.g., 8) reporting `failed: turn limit`; report completion to the app on ALL exit paths: natural finish, tool exception, model/provider exception, turn cap. Re-raise `GraphInterrupt` — pausing is not a failure.

### §18 — Runs stuck at `running` in the app while the graph errored/finished

**Cause:** no completion sync — the app's run record has no way to learn the graph's fate; and/or §11's reject-freeze.

**Fix:** token-authenticated completion endpoint on the app (`PATCH /api/agent-runs` style: terminal-status write-once, syncs parent task) called best-effort by the graph on every exit path; plus an operator "mark done/failed" control in the app UI for runs that predate the sync or died outside it.

---

## Platform-specific traps observed (extend as new ones appear)

- **Railway**: variable-reference syntax `${{Service.VAR}}`; UI/agent config edits can report "applied" without persisting — re-read config to confirm, prefer env-var pinning; region move restarts change injected `PORT`; trial workspaces pause services when expired.
- **Vercel**: env snapshot semantics (§9); GitHub repo transfers keep repo-ID redirects for `git push` but can silently break deploy webhooks — check whether the latest deployment's commit matches `origin/main`, and reconnect the Git integration to the new owner if not.
- **Supabase**: §5 SET ROLE quirk; §6 IPv6-first direct host; SQL editor runs as non-superuser `postgres`.
- **Git**: a crashed process (including a sandboxed agent's) can leave `.git/index.lock` — `add/commit` fail but a bare `push` reports "Everything up-to-date", making it look like the push worked. Remove the lock, re-run all three.
