---
name: orchestration
description: "Use when coordinating one authorized, bounded outcome with a fresh implementer, independent review, saved evidence and explicit closeout."
---

# Orchestration

Deliver one verified outcome. User authority and acceptance requirements prevail; this skill grants no delegation, publication or spending authority.

## Default path

1. **Select and reconcile.** Check one ticket against current source and tracker state. Freeze one actual-caller behavior, assertions, owned paths and exact verification command in the [compact contract](references/task-contract.md). Parent requirements stay open unless individually proven. Preserve existing work.
2. **Plan once through closeout.** Record a realistic cumulative envelope before dispatch, including controller/skill work, implementation, independent review, one coherent repair, integration and reporting. Reserve 20% for closeout. No universal token default: estimate responses × input plus output for this host and scope. At 80%, stop new implementation scope. Do not repeatedly raise the envelope after failure; preserve evidence and report incomplete work when remaining mandatory gates cannot fit. Explicit user limits bind.
3. **Dispatch compactly.** When authorized, use one fresh GPT-6 Luna implementer and one independent GPT-6 SOL reviewer, no history fork. Explicit user model choices override defaults. Brief target: 400 words; include constraints, base, owned paths, assertions, one executable verification command and return path. Give workers no telemetry debugging task. Root owns Git and tracker closeout; it does not duplicate implementation or full QA.
4. **Execute and observe.** Save complete logs with `scripts/run_bounded.py`; return exit, counts/skips, short failure excerpt, hash and path. Read focused source; expand only for a named uncertainty. Controller collects deterministic usage at material transitions using [usage.md](references/usage.md). No mandatory every-four-operation model checkpoints or monitoring-only worker turns. Communicate BLOCKED, READY_FOR_QA, FAILED_GATE or DONE; use event waits, not timer-only sweeps or acknowledgement loops.
5. **Review frozen work.** Producer must finish every required assertion/check before acceptance QA. One independent reviewer checks the focused diff, actual caller, negative controls and source/evidence identity. Reproduce findings; allow one coherent repair and delta review. Missing/skipped/stale evidence stays unverified. Repeated failure requires diagnosis or honest incomplete closeout, never weakened acceptance.
6. **Close once.** Root checks identity/coverage, mandatory integration checks and a real-seam smoke. Update the selected ticket only at material transitions, with gate admission explicitly controlling any mutation. Report accepted outcome and parent closure separately; preserve full evidence. Measure cached input, uncached input, output, controller share, repairs and elapsed time. Footprint reductions are not development savings; compare only equivalent scope and quality, never invent dollar costs.

## Guarded execution

`workflow_gate.py` checks the cumulative envelope, remaining forecast and required receipts. Use its `--execute` option for commands/mutations it owns: denied, missing, malformed or stale admission runs no command. Native tool calls must be conditionally invoked by their caller only after a successful fresh gate; a separate gate invocation does not intercept them. Scripts cannot impose provider billing caps, interrupt arbitrary native tools, prove omitted telemetry complete or establish assertion semantics. Unknown telemetry is not zero or admission.

## Quality and custody

- Prove behavior through actual application roles, chronological migrations, pinned SDKs and production composition. Helper-only tests are insufficient.
- Check postconditions and freshness. Changed money, authorization or production-data guards need a scoped negative control; restore exact bytes. Keep private holdouts isolated.
- Keep implementation and mounting together; pin and test contracts across seams. Evidence is reusable only while relevant source, inputs, toolchain, configuration and rubric match.
- One Git custodian; explicit paths and isolated worktrees/fixtures. Never stash, prune worktrees, overwrite dirty work or delete unfinished worktrees. Verify premises before destructive actions.

## Optional references and skill maintenance

Load only for the current decision: [Git custody](references/git-custody.md), [verification risks](references/verification.md), [research](references/research.md), [operations](references/operations.md). Incident/history material is optional: [case study](references/efficiency-case-study.md), [changelog](references/changelog.md), [legacy checkpoint protocol](references/legacy-checkpoint-protocol.md).

Stage changes in an isolated Cortana inbox batch, compare registry/staging/harness copies, preserve old staging and append dated provenance. Test executable changes, publish reviewed bytes through `bin/publish-skill.sh` under existing authority, then verify published harness links/hashes. Report measured footprint separately from delivery results. Do not build another orchestration framework.
