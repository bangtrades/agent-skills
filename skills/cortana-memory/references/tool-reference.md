# Memory Tool Reference

Concrete API surface for the memory pillar: tool schemas, MCP bridge contract, router HTTP endpoints, request/response shapes, and example payloads.

## Tool surface (5 tools)

All tools follow Anthropic tool_use schema. The canonical manifest lives at `workspaces/cortana-extensions/skills/cortana-memory/skill.json`.

### `cortana_memory_write`

Append-only write to the agent's vault scope.

**Input schema**:
```json
{
  "type": "object",
  "properties": {
    "relative_path": {
      "type": "string",
      "description": "Path relative to the agent's vault scope; must match a glob in live-write-approved.marker.write_paths_allowlist[]"
    },
    "content": {
      "type": "string",
      "description": "UTF-8 text to write. Bounded by MAX_PAYLOAD_BYTES."
    }
  },
  "required": ["relative_path", "content"]
}
```

**Response (success)**:
```json
{
  "ok": true,
  "content": "Wrote <N> bytes to '<relative_path>' under <backend>.",
  "bytes_written": 135,
  "audit_category": "live_write_success"
}
```

**Response (refusal)**:
```json
{
  "ok": false,
  "error": "live_memory_write_approval_missing",
  "message": "router refused before dispatch (live_memory_write_approval_missing)",
  "audit_category": "refused_other"
}
```

**Capability required**: `memory_<backend>_write`
**Approval markers required**: read marker + write marker (see operations.md)

### `cortana_memory_read`

Read a file from the agent's vault scope.

**Input schema**:
```json
{
  "type": "object",
  "properties": {
    "relative_path": { "type": "string" }
  },
  "required": ["relative_path"]
}
```

**Response (success)**:
```json
{
  "ok": true,
  "content": "<file contents as UTF-8 string>",
  "bytes_read": 135,
  "audit_category": "live_read_success"
}
```

**Response (file missing)**:
```json
{
  "ok": false,
  "error": "memory_read_target_missing",
  "audit_category": "refused_other"
}
```

**Capability required**: `memory_<backend>_read`

### `cortana_memory_list`

List entries under a vault sub-path.

**Input schema**:
```json
{
  "type": "object",
  "properties": {
    "relative_path": {
      "type": "string",
      "description": "Sub-directory to list. '' or '/' lists the vault root."
    }
  },
  "required": ["relative_path"]
}
```

**Response (success)**:
```json
{
  "ok": true,
  "content": "Listed <N> entries under '<relative_path>'.",
  "item_count": 5,
  "truncated": false,
  "audit_category": "live_list_success"
}
```

**Capability required**: `memory_<backend>_read`

### `cortana_memory_search`

Substring scan across the agent's vault scope.

**Input schema**:
```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "Literal substring to scan for"
    },
    "relative_path": {
      "type": "string",
      "description": "Sub-directory to scan; '' scans the vault root"
    },
    "case_sensitive": {
      "type": "boolean",
      "default": false
    }
  },
  "required": ["query"]
}
```

**Response (success)**:
```json
{
  "ok": true,
  "content": "Found <N> match(es) for '<query>' in <M> file(s).",
  "item_count": 1,
  "files_scanned": 5,
  "files_skipped_binary": 0,
  "files_skipped_too_large": 0,
  "files_truncated": false,
  "matches_truncated": false,
  "audit_category": "live_search_success"
}
```

**Capability required**: `memory_<backend>_read`

### `cortana_memory_submit_candidate`

Submit a file for promotion to shared scope.

**Input schema**:
```json
{
  "type": "object",
  "properties": {
    "relative_path": {
      "type": "string",
      "description": "Path in agent's private scope to submit"
    },
    "target_sub_tree": {
      "type": "string",
      "enum": ["core", "projects", "workflows", "glossary"],
      "description": "Where in shared/ the candidate should land if promoted"
    },
    "rationale": {
      "type": "string",
      "description": "Why this should be shared"
    }
  },
  "required": ["relative_path", "target_sub_tree", "rationale"]
}
```

**Response (success)**:
```json
{
  "ok": true,
  "content": "Candidate accepted. Classification: <auto_approved | escalated>.",
  "audit_category": "candidate_submit_accepted",
  "promotion_classification": "auto_approved"
}
```

**Capability required**: `memory_<backend>_read` + `memory_<backend>_submit_candidate`

## MCP bridge (cortana-memory-mcp)

The native CLI bridge between stateful-CLI adapters (claude_local, codex_local) and the router's memory endpoints. Lives at `workspaces/cortana-adapters/cortana-memory-mcp/`.

### MCP server configuration (claude_local)

Inside the container, claude's MCP config is at `~/.claude.json` (CLAUDE_CONFIG_DIR=/state/claude-home):

```json
{
  "mcpServers": {
    "cortana-memory": {
      "command": "cortana-memory-mcp",
      "args": []
    }
  }
}
```

The server consumes env vars at spawn time (injected via `adapter_config.mcp_servers.cortana-memory.env`):

| Env var | Purpose |
| --- | --- |
| `CORTANA_AGENT_ID` | The agent UUID (trusted identity; never read from the JSON body) |
| `CORTANA_MEMORY_BRIDGE_URL` | Router base URL (`http://cortana-llm-router:4400`) |
| `CORTANA_MEMORY_BRIDGE_READ_ONLY` | "1" to refuse write/delete at the bridge; "" or unset for read-write |

### MCP tool surface

The MCP server exposes the same 5 `cortana_memory_*` tools via the MCP protocol. CLI sees them in `claude mcp list` as:

```
cortana-memory: cortana-memory-mcp - ✓ Connected
```

The CLI dispatches tool_use blocks → MCP server translates to HTTP `POST /v1/memory/{op}` → router executes → response threads back as tool_result.

### MCP server lifecycle

- Spawned as a subprocess of the CLI on each run
- Reads `CORTANA_AGENT_ID` from env (never from a request body — server-side identity)
- Forwards each tool call to the router with `X-Cortana-Agent-Id` header
- Server-side authoritative; the bridge does NOT make policy decisions

## Router HTTP endpoints (router-side memory bridge)

For native_cli_bridge transport, the MCP server hits these endpoints. For router_tool_loop transport, the router's in-process executor handles tool calls directly.

### `POST /v1/memory/write`

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "X-Cortana-Agent-Id: <uuid>" \
  -H "X-Cortana-Request-Id: <optional-id>" \
  -d '{"relative_path": "smoke/test.md", "content": "hello"}' \
  http://cortana-llm-router:4400/v1/memory/write
```

**Status codes**:
- `200` — `{"ok": true, ...}`
- `400` — malformed JSON or invalid op-specific args
- `401` — missing `X-Cortana-Agent-Id`
- `422` — resolver or executor refused (envelope.ok=false with audit_category)

### `POST /v1/memory/read`

Body: `{"relative_path": "smoke/test.md"}`. Same status codes.

### `POST /v1/memory/list`

Body: `{"relative_path": "smoke/", "max": 100}` (max optional).

### `POST /v1/memory/search`

Body: `{"query": "hello", "relative_path": "smoke/", "max": 50, "case_sensitive": false}`.

### `POST /v1/memory/delete`

Body: `{"relative_path": "smoke/test.md"}`. Append-only backends (like para-memory-files) refuse with `memory_operation_not_implemented`.

### `GET /v1/memory/status`

Returns the bridge's readiness state. Used by `cortana-memory-mcp-status.sh`.

```bash
curl http://cortana-llm-router:4400/v1/memory/status | jq '.'
```

Response:
```json
{
  "service": "cortana-llm-router",
  "memory_bridge": {
    "ready": true,
    "adapter_id": "para-memory-files",
    "lifecycle_state": "live"
  },
  "extensions": {
    "para-memory-files": {
      "registered": true,
      "live_dispatch_enabled": true
    }
  }
}
```

## Request flow — write operation, end-to-end

For a `cortana_memory_write` on a stateful-CLI agent (claude_local):

1. **Model** emits `tool_use` block for `cortana_memory_write` with `{relative_path, content}`
2. **claude CLI** receives the tool_use, dispatches to its MCP runtime
3. **MCP runtime** routes to the `cortana-memory` server (per `~/.claude.json` mcpServers)
4. **cortana-memory-mcp** translates to `POST /v1/memory/write` with `X-Cortana-Agent-Id: <uuid>`
5. **Router HTTP handler** parses request, calls `memory_bridge.execute_write(...)`
6. **memory_bridge** invokes `memory_executor.execute_plan(...)` with the write request
7. **memory_executor** runs five-gate composition:
   - Env gate: `CORTANA_MEMORY_LIVE_DISPATCH=1` AND `CORTANA_MEMORY_MODULE=para-memory-files`
   - Marker gate: read marker present + agent listed + unexpired
   - Marker gate (write): write marker present + agent listed + unexpired + path in allowlist + ceremony_acknowledged
   - Capability gate: `memory_para_files_write` marker present
   - Vault gate: target path under agent's private scope
   - Lifecycle gate: backend is `live` (not candidate)
8. If ALL gates open, executor calls `para_memory_files.write(request)` (the MemoryAdapter)
9. Backend writes the file, returns `MemoryExecutionResult` with `audit_context`
10. Executor stamps the canonical STEP-37 §6 audit row to `memory-execution.jsonl` with `transport=native_cli_bridge`
11. Response threads back: backend → executor → bridge → HTTP response → MCP server → CLI → model
12. Model receives tool_result with `{ok: true, bytes_written: N, audit_category: "live_write_success"}`

For a refusal at any gate, the executor stamps a `decision=refused` audit row with the appropriate `audit_category` and `refusal_reason`, returns the refusal envelope.

## Bounds and limits

| Bound | Value | Source |
| --- | --- | --- |
| MAX_PAYLOAD_BYTES (write) | 1 MB (configurable via `CORTANA_MEMORY_MAX_PAYLOAD_BYTES`) | `memory_executor.py` |
| MAX_LIST_ENTRIES | 1000 | per-backend; default in para-memory-files |
| MAX_SEARCH_FILES_SCANNED | 10000 | per-backend |
| MAX_SEARCH_MATCHES_RETURNED | 100 | per-backend |
| MAX_PATH_DEPTH | 16 | vault gate enforces |
| MAX_PATH_LENGTH | 1024 chars | vault gate enforces |
| Marker TTL (production) | ≤ 7 days | operator policy |
| Marker TTL (triage) | ≤ 1 hour | operator policy |
| Write marker `--expires-hours` ceiling | paired read marker's `expires_at` | script enforces |

## Tool authorization shorthand

For a quick check of whether an agent can perform a memory operation right now, the chain is:

```
adapter_type stateful-CLI?
  └─ AND skills_enabled includes "cortana-memory" OR memory_enabled triggers auto-loader?
      └─ AND MCP bridge connected (claude mcp list shows ✓)?
          └─ AND read marker present + agent listed + unexpired?
              └─ AND (if write op) write marker present + agent listed + unexpired + path in allowlist?
                  └─ AND capability marker for op present + unexpired?
                      └─ AND target path under allowed vault scope?
                          └─ → AUTHORIZED → executor runs the backend, stamps audit row
```

Any failure in the chain → refusal at that gate → audit row with the corresponding category.

## Cross-references

- `operations.md` — how to grant / revoke markers and capabilities
- `audit-schema.md` — what the audit row contains
- `architecture.md` — where in the codebase each surface lives
- `troubleshooting.md` — symptom → fix table for each refusal category
- `upgrade-ceremony.md` — how to add a new tool, change schema, or admit a backend
