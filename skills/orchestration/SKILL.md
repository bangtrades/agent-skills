---
name: orchestration
description: "Use when coordinating authorized multi-agent engineering or research: bounded batches, compact task contracts, independent verification, integration and tracker closeout. Also use to improve orchestration from measured run evidence."
---

# Orchestration

Deliver verified outcomes with bounded context and coordination. User instructions and required acceptance gates prevail. Delegation, publication and spending require existing authority; this skill does not grant them.

## Execution contract

1. **Admit one finishable outcome.** Select one observable behavior and its actual caller, with frozen assertions and exact check commands. A broad parent ticket is a backlog container, not a dispatch contract. Keep all parent requirements in a coverage ledger; accepting a slice never implicitly closes its parent. Start with one producer; use a second only for independently finishable work whose completion costs fit. Reserve independent QA capacity.
2. **Forecast through completion before dispatch.** Honor explicit user limits cumulatively. Default to a 5M-token, 120-response, 60-minute planning envelope with 20% reserved for closeout; size the actual outcome from implementation, QA, one coherent repair and integration responses × expected input, plus output. A 3–5M estimate for one narrow repair is a calibration starting point, not a demonstrated price. Include controller and renewal overhead. Read the small [task contract](references/task-contract.md), record the forecast, and use the workflow gate. Override unsuitable defaults with a recorded estimate before dispatch, never silently after overspending.
3. **Preflight the controller.** Use a genuinely fresh, authorized controller context and compact manifest when available. Do not create a user-owned task, change models or claim a summary cleared context without authority. Above 80K current input, record the context limitation and its cost. If renewal is unavailable, use a bounded existing controller with fewer turns and an explicit mitigation. Target controller consumption below 15%; this is a planning signal, not permission to omit verification. Root selects, verifies identity/coverage, integrates and manages tickets; it does not duplicate producer investigation or full QA.
4. **Bound context at ingestion.** Fresh task-specific workers, no full-history fork. Brief target 400 words: one outcome, assertions, exact caller/base/paths, constraints, check commands, assigned budget, usage-file identity and return format. Default tool output to about 2K tokens (8K characters is an approximate cap, not a tokenizer). Save complete command logs; return exit code, test counts, failure excerpt, hash and path. Search for locations, then read relevant functions. Expand for a named uncertainty; never hide failures or truncate stored evidence. Use `scripts/run_bounded.py` for noisy commands. Root and QA follow the same rule.
5. **Check usage inside workers.** Include `worker-check` in an existing command batch every four tool operations (at most five), and before another broad read. Warn at +18K input; checkpoint at a safe atomic boundary on +24K growth, first compaction or assigned-budget exhaustion. Carry a short continuation packet and evidence references, not old briefs/logs. Root still checks aggregate usage at admissions. These cooperative checks cannot interrupt native agents; never claim host-enforced limits. Missing telemetry is unknown: restore it, or checkpoint before expensive work rather than assume zero. Track renewal overhead.
6. **Coordinate on events; review ready outcomes.** Only BLOCKED, READY_FOR_QA, FAILED_GATE or DONE worker events, with compact evidence pointers. Batch routine questions; no acknowledgement loops or timer-only board sweeps. Respect host responsiveness and user-facing update requirements. Before acceptance QA, the producer must finish every assertion/check and freeze source; the workflow gate rejects missing, stale or skipped required evidence. Known incomplete work needs a producer repair or concrete blocker, not an acceptance review. Label an intentionally limited diagnostic review separately. One independent reviewer covers spec and code quality through the actual caller and negative controls; separate reviewers only for an explicit requirement or distinct risk. Reproduce findings, allow one coherent repair and delta review; repeated failure of the same invariant requires diagnosis/rescoping.
7. **Integrate once and measure accepted outcomes.** Reuse evidence only while relevant source, inputs, toolchain, config and rubric identities match. Root checks receipt identity and coverage; run mandatory merged checks and one real-seam smoke. Update tickets at material transitions. Record tokens per independently accepted slice, parent-ticket closure separately, controller share, renewal overhead, repair count and later defects. Zero accepted outcomes means the efficiency result is unproven, not zero cost. Compare equivalent quality/scope; stopping earlier is not demonstrated savings.

## Admission and replanning

Read [usage.md](references/usage.md) once. Measure explicit root and worker files, then run `scripts/workflow_gate.py` before dispatch, repair, acceptance QA or integration. It combines usage admission, complete-phase forecasting and receipt checks. `usage_guard.py worker-check` is intentionally local and never claims aggregate admission. The controller reconciles active and retired contexts; all usage remains counted.

At 80% of the planning envelope, admit no additional implementation scope. Reserve remaining capacity for verification/closeout and forecast the active outcome's remaining mandatory gates. If it cannot fit, preserve evidence and explicitly revise scope, approach or the self-selected planning envelope with a reason before continuing. Do not silently raise limits, reset the ledger, repeatedly redispatch unchanged work, or end authorized work merely because an advisory threshold fired. Explicit user limits remain binding. Seek input only when the viable continuation needs missing authority or a decision; otherwise execute the revised bounded plan. A host/context limitation is reported, never relabeled completion.

These scripts validate only when called. They cannot intercept tools, enforce provider billing or guarantee assertion semantics. Receipt hashes bind evidence bytes; independent QA and root still verify source identity, relevance and actual behavior.

## Quality and custody that remain mandatory

- Verify premises independently before destructive actions; prefer reversible operations. Summaries are navigation, not source truth.
- Prove effects through the actual application role, chronological migrations, pinned SDK and production composition. A helper-only green test or declared registry is insufficient.
- Verify postconditions and freshness. Exercise changed money, authorization and production-data guards with a scoped negative control; snapshot and restore exact bytes.
- Keep implementation and mounting together. If a contract must cross slices, pin its signature and test the real pairing.
- Keep private holdouts isolated. Missing evidence stays unverified. Do not weaken acceptance, delete tests or substitute fakes to meet a budget.
- Disjoint worktrees/fixtures; one Git custodian. Agents NEVER use `git stash` and NEVER run `git worktree prune`. Preserve dirty/user work; stage explicit paths. Do not delete unfinished worktrees at batch boundaries.

## Load details only for the decision at hand

- A specific verification risk: search [verification.md](references/verification.md) for the matching law/section; do not read the incident catalog routinely.
- Shared Git custody or mounted filesystems: [git-custody.md](references/git-custody.md).
- Research fleets or blind evaluations: relevant section of [research.md](references/research.md).
- Production runbooks, detached Hermes or sandbox limitations: relevant section of [operations.md](references/operations.md).
- Cortana/WaiveLabs work-breakdown or Linear decisions: the matching route in `cortana-vault/projects/claude-skills/claude-skills--development-sdlc.md`; not the entire linked playbook library.
- Efficiency evaluation: [efficiency-case-study.md](references/efficiency-case-study.md). Historical provenance: [changelog.md](references/changelog.md). Neither belongs in worker prompts.

## Improving this skill

Change rules only from evidence. Stage a candidate in an isolated Cortana inbox batch; compare registry, relevant prior staging and loaded harness copies. Append the dated provenance to the changelog, test executable changes, publish reviewed bytes through `bin/publish-skill.sh` under existing user authority, and verify harness links. Preserve old staging. Report measured reductions separately from modeled savings and end-to-end outcomes. Do not add another generic efficiency checklist.
