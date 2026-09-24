# One accepted outcome, one contract

Keep a compact mutable manifest plus immutable logs; do not reconstruct history. Freeze one actual-caller behavior. Keep broader parent requirements as a coverage ledger outside the worker context. All applicable safety/authority restrictions remain in its brief. Controller/worker model selection follows the user.

The JSON below matches `workflow_gate.py`. Replace example paths/hashes; forecast **remaining** cost at each material transition without resetting cumulative usage. Each forecast includes its controller work. Positive QA, repair and integration reserves are required for implementation admission. Zero remaining work for a completed phase is legitimate at later review/integration; total remaining work must be positive. Estimates are not ceilings enforced by the host.

```json
{
  "outcome": "A signed STOP suppresses a paused worker's stale outbound effects",
  "parent": "ticket identifier; stays open until every parent criterion passes",
  "actual_caller": "signed API route -> registered inbound worker -> commit",
  "base": "exact source identity",
  "controller": {
    "mode": "bounded_existing",
    "current_input_tokens": 60000,
    "remaining_responses": 6,
    "mitigation": "Existing task; six decision turns forecast, bounded reports"
  },
  "remaining_forecast": {
    "implementation": {"responses": 24, "mean_input_tokens": 60000, "output_tokens": 12000},
    "qa": {"responses": 10, "mean_input_tokens": 60000, "output_tokens": 5000},
    "repair": {"responses": 6, "mean_input_tokens": 60000, "output_tokens": 3000},
    "integration": {"responses": 6, "mean_input_tokens": 60000, "output_tokens": 2000}
  },
  "acceptance": [{
    "id": "stop-race", "assertion": "No stale send, transcript, quote or booking after STOP",
    "check": "exact required command", "evidence": null
  }],
  "producer_self_check": "pending",
  "candidate": null,
  "independent_qa": null
}
```

Before review, set producer_self_check to `passed`, candidate to frozen commit/tree or scoped manifest hash, and supply each criterion's evidence object:

```json
{"candidate":"same frozen identity","status":"passed","skips":0,"command":"exact command","log":"/absolute/log/path","sha256":"actual log hash"}
```

The gate checks hash freshness, required fields and forecast fit, not the truth of the assertions or the candidate's source bytes. Root verifies those. For integration, supply an independently produced QA receipt of the same form in `independent_qa`. A known incomplete candidate cannot enter acceptance QA. A targeted diagnostic review has a separate diagnostic contract and must not be represented as acceptance.

Producer brief: target 400 words. Include caller/base/paths, one outcome, all constraints, assertions/commands, assigned token allowance and native usage path/thread/root-turn/start identity. Copy the worker-check command from usage.md and require it within existing tool batches every four operations. No separate LLM turn is needed just to check a script result. If the host cannot expose these identities, report that before expensive work and use the documented telemetry fallback.

Return packet: target 150 words. Verdict, frozen identity, changed paths, exact checks/counts/skips, gaps, log references and next decision. On renewal, include only unresolved assertions, exact failing command/error and evidence references. Never send old transcripts or complete prior briefs.

QA reads the contract, focused diff and relevant evidence; independently exercises actual caller and negative controls. Root verifies coverage and integration rather than commissioning a second full review. Evidence invalidation follows changed relevant inputs; mandatory repository-wide gates still run.

Completion ledger: outcome ID, parent ID, source identity, independent verdict, total run tokens, controller tokens, response/renewal counts, repair count, later defects. Deduplicate outcomes; report accepted parent count separately. If accepted outcome count is zero, tokens per accepted outcome is unavailable. Never divide by zero or count checkpoints as accepted work.
