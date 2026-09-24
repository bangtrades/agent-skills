# Usage measurement and admission

Run the guard locally; never send prompts or logs to another service. It reads only explicit paths. Find the active root turn and descendant rollout paths using the host's supported usage facilities or read-only thread metadata; do not scan unrelated histories or protected directories. Include root plus all batch workers and call again with fresh data before admission. Native Codex JSONL `token_usage_record` and the case-study normalized JSON array are supported; other providers need an explicit adapter preserving scope and field semantics. Unscoped records are excluded, not silently attributed.

```sh
python3 <skill>/scripts/usage_guard.py measure --files <root.jsonl> <worker.jsonl> --root-turn <id> --since <batch-start-UTC> --out <batch>/usage.json
python3 <skill>/scripts/usage_guard.py gate --metrics <batch>/usage.json --policy <skill>/references/budget-policy.json --root-turn <id> --action dispatch
```

Replace angle-bracket values. `measure --until <UTC>` is for historical audits, not fresh admission. `gate` exits 0 for admission, 2 for denial/error. Read reasons. All measured workers are considered active by default. Pass `--retired-worker <id>` only after verifying that context completed or was replaced. Its usage stays in totals while its lifecycle triggers stop blocking fresh contexts. Unknown retired IDs and retiring the current root deny admission. The script cannot discover omitted usage files or verify your retirement claim; the controller must reconcile its live worker inventory. `review`/`integrate` may use the reserved 20%; they cannot exceed the full envelope. Never use those actions to disguise implementation.

Cached input is part of input; reasoning is part of output. Count `input+output`, including compaction responses. Response IDs deduplicate; conflicting duplicates and malformed counters fail. A zero-record result is unknown; it cannot authorize dispatch. Snapshot freshness checks detect an old file, not omitted worker paths: the controller must verify its worker inventory and capture completeness. Agent lifecycle metrics cover the supplied interval; do not reset `--since` to conceal unfinished same-task usage. Keep the parent run ledger across batches and apply explicit user limits cumulatively.

Native compaction counts are detected from compacted events; normalized response-only exports retain compaction tokens but may omit event identity. Use native logs for lifecycle enforcement. A session's baseline includes fixed harness overhead; measure input growth above that floor rather than promising a 24K total context when the platform injects more.

The limits are configurable planning controls, not provider-enforced ceilings. This script does not interrupt an active agent or stop a model from bypassing it. For a true hard limit, the host must enforce per-agent/run budgets. Never describe prospective savings as observed delivery performance.
