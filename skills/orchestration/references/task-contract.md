# One batch, one contract

Keep one small manifest (target under 2KB), plus immutable attempt logs. Update it on material transitions. Do not repeatedly reread or rewrite a growing chronological receipt. Put nonessential evidence outside model context.

```json
{
  "outcome": "one externally observable behavior",
  "base": "exact commit",
  "slices": ["id; caller and implementation owned together"],
  "acceptance": ["required behavioral assertions"],
  "checks": ["commands; roles/config; expected postconditions"],
  "budget_policy": "path; overrides with reasons; parent remaining limit",
  "workers": ["task id; model; scope; usage file; state"],
  "candidate": "commit/tree or scoped content hashes",
  "evidence": ["command + code/input/lock/config identity + result + log path"],
  "blocker": null,
  "next": "one decision"
}
```

Producer brief: outcome and acceptance; exact base/caller; allowed paths and dependencies; safety/authority restrictions; required checks; bounded budget; event-only reporting. Include applicable no-stash/no-prune and protected-path rules verbatim. Relevant excerpts replace transcript forks. A 400-word target is a guard against duplication, never permission to omit a constraint.

Return packet, target 150 words: verdict, frozen identity, changed paths, required checks/results/skips, unresolved acceptance, evidence pointers and requested decision. Do not paste full logs. If the producer cannot fit a failure explanation, put reproducer details in a linked artifact and summarize the invariant.

QA reads that contract, exact diff and relevant code/evidence. It independently runs the critical actual caller and applicable negative control. It need not reconstruct the entire project history. Root verifies identity and coverage, runs required merged integration checks, and reports local acceptance separately from deployed/customer acceptance. Fixes invalidate only evidence whose relevant inputs changed; repository-required broad gates still run.
