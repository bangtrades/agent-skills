# read-file

Workspace-scoped file reader. Two tools: `read_file(path, limit, offset)` and
`list_directory(path, include_hidden)`. The first real Cortana skill —
landing this lights up the company-skills surface and gives Symba (CEO
chat) a way to look at files in her workspace without escaping.

## Capability model

- **Default scope:** the agent's workspace root. The handler resolves
  every path against the workspace root via `os.path.realpath`. Any
  path that resolves outside the root is refused with
  `path_outside_workspace`.
- **Outside scope:** if the agent holds the
  `filesystem_outside_workspace` capability marker
  (`state/agents/<agent_id>/capabilities/filesystem_outside_workspace.marker`),
  the handler permits paths anywhere on the host. Defense-in-depth —
  the handler ALSO refuses paths under `/Users/nolan/Documents` and
  any path containing `/.ssh/`, `/.aws/`, `/credentials/` regardless
  of capability state.

## Tools

### `read_file(path, limit=200, offset=0)`

Reads UTF-8 text. Refuses binary content (any byte where `b > 0x7F`
and the file is not declared `.txt`/`.md`/`.json`/`.yaml` extension)
because the LLM can't usefully consume binary data anyway.

Returns:
```
{
  "ok": true,
  "path": "<resolved-absolute-path>",
  "line_count": 42,
  "content": "1\tfirst line\n2\tsecond line\n..."
}
```

Or on refusal:
```
{
  "ok": false,
  "error": "path_outside_workspace",
  "message": "human-readable"
}
```

### `list_directory(path, include_hidden=false)`

Returns:
```
{
  "ok": true,
  "path": "<resolved-absolute-path>",
  "entries": [
    {"name": "foo.txt", "type": "file",      "size_bytes": 42},
    {"name": "bar",     "type": "directory", "entry_count": 3}
  ]
}
```

## Implementation

`lib/handler.py` is a stdlib-only Python module. As of S10F-1B / S10F-2B
the router executes this handler in-process: the cortana-llm-router
`tool_execution.run_tool_loop` dispatches `read_file` and
`list_directory` through `lib/tool_execution.py:SkillRegistry`, and
the cortana-http-shim's `loadSkillsToolset` advertises the tool
surface to Paperclip. Provider-neutral tool-call shapes (Anthropic +
OpenAI) are normalised by the executor; the handler never sees raw
provider envelopes. Audit metadata (`tool_name`, `skill_id`, `ok`,
`error`, `arguments_keys`, `path_sha256_prefix`,
`output_size_bytes`) is appended to the runtime-policy audit log
without raw paths or file contents.

### Source path

Canonical: `workspaces/cortana-extensions/skills/read-file` — the
S10G-1A registry entry's `path` field and the location every
operator-issued tool (registry status, lifecycle plan, rollback
plan) reports.

Legacy alias: `workspaces/cortana-skills/read-file` is a relative
symlink to the canonical path. Both resolve identically inside the
paperclip and router containers because both bind `/workspaces`
from the same host root, but new tooling and UI surfaces should
prefer the canonical form.

## Refusal codes

| Code | Trigger |
|------|---------|
| `path_outside_workspace` | Path resolves outside workspace and `filesystem_outside_workspace` not held |
| `path_blocked_always` | Path under `/Users/nolan/Documents`, any `/.ssh/`, `/.aws/`, `/credentials/` |
| `path_not_found` | `os.path.exists` is false |
| `path_not_a_file` | `read_file` called on a directory |
| `path_not_a_directory` | `list_directory` called on a file |
| `binary_content` | First chunk contains non-text bytes |
| `read_failure` | OSError / PermissionError during read |

## Tests

`test/test_handler.py` covers:
  - workspace-scope refusal
  - capability bypass (with marker)
  - always-blocked-path refusal (capability held but `/.ssh/` still blocked)
  - read happy path with line numbers
  - list happy path
  - non-existent path
  - directory-vs-file mismatch
  - binary content refusal
