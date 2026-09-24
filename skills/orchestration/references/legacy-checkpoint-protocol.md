# Historical checkpoint protocol — optional compatibility reference

Superseded for default runs on 2026-09-24. Existing worker-check CLI remains available; do not load or assign this protocol routinely.

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

## Outcome admission and complete-phase forecast

After `measure`, use the workflow gate for every new dispatch, repair, acceptance review and integration:

```sh
python3 <skill>/scripts/workflow_gate.py --contract <outcome.json> --metrics <usage.json> --policy <policy.json> --root-turn <id> --action review
```

The contract schema is in task-contract.md. Gate exit 0 admits; 2 rejects. It calls the existing aggregate usage gate as well as checking the remaining forecast against the unspent full envelope. Pass verified retired contexts with repeated `--retired-worker`; never retire root. Controller share/large-context warnings are advisory and require a concrete plan, not an automatic task fork. Review requires producer completion and hash-valid, zero-skip evidence for every assertion. Integration additionally requires an independent QA receipt. Hashes do not establish source truth or test relevance.

## Cooperative worker checks

Within an existing command batch every four tool operations (never more than five), measure the worker's own explicit file(s), keeping the original root run/start and the assigned allowance:

```sh
python3 <skill>/scripts/usage_guard.py worker-check --files <worker.jsonl> --root-turn <root-turn> --since <batch-start-UTC> --thread-id <worker-id> --budget-tokens 2000000 --policy <policy.json>
```

The allowance above is an example, assigned from the complete-phase forecast. The check warns at18K context growth or80% of the allowance; exit2 asks for a safe checkpoint on24K growth, first compaction, response threshold or full allowance. Peak observed input is used, so a later smaller response cannot erase a prior overrun. This is worker-only telemetry, not full-run admission. Do not omit historical worker usage from root totals when renewing. If usage paths are unavailable, record unknown usage, cap broad reads using operation counts and checkpoint before expensive continuation while restoring telemetry. Do not assert a token ceiling was enforced.

## Bounded command output

```sh
python3 <skill>/scripts/run_bounded.py --log <new-log-path> --max-chars 8000 --timeout 120 -- node --test <focused-test>
```

Uses argv without a shell; it stores combined stdout/stderr in an exclusively created private log, preserves the command exit status, and returns hash/size plus a bounded tail. Existing logs are never overwritten. Timeout kills the process group on POSIX (only the direct process on other hosts). Logs can contain sensitive data: choose an authorized private path and do not publish them blindly. It does not redact log contents. The JSON encoding can expand special characters; 8K characters is only a roughly2K-token content target, not an exact transport/token cap. Test counts/failure excerpts should come from the saved log when not in its tail. A passed process exit is not sufficient acceptance evidence. Read source functions by line range; larger excerpts require a stated uncertainty. Full evidence remains available without flooding model context.
