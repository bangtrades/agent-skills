# Native Memory Smoke Case Study

This case study captures the failure pattern from the Cortana Codex Smoke native memory bridge investigation that culminated on May 13-14, 2026.

## Incident Shape

The operator repeatedly ran controlled native memory bridge smoke tests. Static readiness and MCP runtime checks were intermittently green, but controlled smoke issues kept failing with combinations of:

- `MEMORY_READ=no`
- `PHRASE_PRESENT=no`
- `NO_MCP_RESOURCE_WORDING`
- `MCP tool call cancelled`
- later, `MCP_TOOL_VISIBLE=0` with no fresh audit rows

Multiple small fixes addressed real but secondary problems: TOML env serialization, fresh-session hygiene, MCP auto-approval, runtime PATH/symlink, and gate freshness. The final blocker was prompt delivery.

## Root Cause Pattern

Paperclip heartbeat built the issue assignment into `context.paperclipTaskMarkdown`, including the issue description:

```text
Use the Cortana memory MCP tool to read:
operator-tests/codex-smoke-native-bridge-readonly-01.md
```

The `codex-local` adapter built the model prompt from wake metadata, handoff notes, and the default heartbeat prompt, but omitted `paperclipTaskMarkdown`. The model saw that it had been assigned an issue but not the actual issue body. It did unrelated repo work instead of calling the memory MCP tool.

Claude-local already included `paperclipTaskMarkdown`, which made the discrepancy easy to miss unless adapters were compared side by side.

## Diagnostic Proof

The decisive evidence was:

- The issue body contained the correct smoke instructions.
- The run context snapshot contained `paperclipTaskMarkdown`.
- The `codex-local` prompt assembly omitted `context.paperclipTaskMarkdown`.
- The run log showed fresh-session and memory bridge config were active.
- The agent output contained unrelated implementation work.
- The gates showed `MCP_TOOL_VISIBLE=0`, no MCP lifecycle, and no fresh memory audit rows.

This proved the problem was neither router authorization nor MCP runtime. The task never reached the model.

## Durable Fix

Inject `paperclipTaskMarkdown` into local adapter prompts and expose `taskContextChars` in prompt metrics. Add a fake adapter test that captures stdin and asserts the controlled smoke issue body, target path, expected phrase, and completion marker are present.

Apply the same pattern across all local adapters, not only Codex, to prevent adapter-specific task-context drift.

## Future Gate Improvement

Add a gate classification such as `NO_GO_TASK_CONTEXT_OMITTED` when a controlled issue has:

- No MCP lifecycle rows.
- No fresh memory audit rows.
- No body canaries in the agent comment.
- A run log/context snapshot showing `paperclipTaskMarkdown` exists but was not delivered, or no prompt evidence of issue body.

This avoids misclassifying prompt delivery bugs as generic MCP runtime failures.
