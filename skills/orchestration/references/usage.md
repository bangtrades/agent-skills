# Deterministic usage and guarded commands

Controller only: identify this run's explicit root/worker usage files through host metadata. Never scan unrelated histories. Keep the original run/start and all completed workers in the cumulative ledger. Native `token_usage_record` JSONL and normalized exports are supported. Missing telemetry is unknown; repair collection deterministically or stop expensive continuation with preserved evidence. Do not assign a model worker to diagnose monitoring.

```sh
python3 <skill>/scripts/usage_guard.py measure --files <root.jsonl> <worker.jsonl> --root-turn <id> --since <start-UTC> --out <usage.json>
python3 <skill>/scripts/workflow_gate.py --contract <contract.json> --metrics <usage.json> --policy <policy.json> --root-turn <id> --action dispatch --log <new-log> --execute <program> <argument>
```

Replace placeholders once in a tested launcher; workers receive its exact invocation, not this template. Measure at dispatch, repair, review and integration, outside model reasoning. A gate without `--execute` is read-only admission; its exit 0 AND JSON `admit: true` must condition a subsequent native tool call in the caller. Never put an unconditional mutation after a gate. Native dispatch cannot be made atomic by this Python script.

With `--execute`, the gate validates its input immediately, then invokes only the supplied argv (no shell), saves full output exclusively and returns a compact result. Missing files, malformed values, denial or stale usage prevent execution. Command failure propagates; old logs are never overwritten. This is owned-command enforcement, not a universal tool interceptor or provider billing cap. Trusted local files and reconciled usage inventory are required; hashes establish evidence bytes, not truth or source semantics.

Cached input is a subset of input; report uncached as input minus cached. Reasoning is included in output. Deduplicate response IDs; malformed/conflicting records fail. Record observation time and note unfinished final-report usage. Final measured tokens can exceed forecasts because running responses are not interruptible here.

Default policy disables legacy context-growth/compaction checkpoints; full-run limits and reserve still gate transitions. Optional legacy `worker-check` remains compatible, documented only in [legacy-checkpoint-protocol.md](legacy-checkpoint-protocol.md). Do not renew workers just because a fixed context-growth threshold fired.

For verification without admission (e.g. initial controller skill tests):

```sh
python3 <skill>/scripts/run_bounded.py --log <new-log> --max-chars 2000 --timeout 120 -- <program> <argument>
```

Full stdout/stderr is saved privately; bounded tail, exit, bytes and SHA-256 are returned. Timeout kills the process group on POSIX. Counts/skips and required assertions still need validation. Logs are not redacted; keep them in authorized locations. Character caps are approximate, not tokenizer limits.
