---
name: orchestration
description: "Use when coordinating authorized multi-agent engineering or research: bounded batches, compact task contracts, independent verification, integration and tracker closeout. Also use to improve orchestration from measured run evidence."
---

# Orchestration

Deliver verified outcomes with bounded context and coordination. User instructions and required acceptance gates prevail. Delegation, publication and spending require existing authority; this skill does not grant them.

## Execution contract

1. **Choose one deliverable batch, at most two independent slices.** Own the actual caller and its implementation together. Read only the selected requirements and dependencies; keep the remaining backlog as IDs and one-line dependency summaries. New incidental findings enter the backlog, not the current batch unless they block acceptance. Reserve a QA slot; on capacity refusal, wait for a state change instead of retrying or changing models.
2. **Set a measured envelope before dispatch.** Honor explicit user limits across root and workers. Without them, start with the configurable planning defaults in `references/budget-policy.json`: 60 minutes, 5M processed tokens including cached input, 100K output, 120 responses across the batch, and 20% reserved for verification/closeout. These are conservative replan triggers, not evidence that a task fits, permission to stop unfinished work, or permission to spend money. Override an unsuitable default before dispatch with a concrete estimate and recorded reason; never silently raise it after overspending. Do not automatically start unlimited batches to evade a run limit.
3. **Keep the controller thin.** Root selects, dispatches, reads bounded returns, verifies identities and integrates. Producers own investigation, edits and scoped tests; QA owns independent reproduction. Root does not duplicate their full reviews or rerun unchanged suites. Use scripts for counts, manifests, hashes and repetitive checks. Follow the user's model policy; a cheaper model reduces dollars, not necessarily tokens. Do not switch the current task's model silently.
4. **Use fresh, task-specific contexts.** No full-history fork by default. Brief: goal, acceptance, exact base, owned caller/paths, dependencies, prohibitions, required commands, budget and return format; target 400 words. Do not tell workers to load this entire coordinator skill. Include relevant safety rules verbatim. Reuse a producer only for the same bounded repair; fresh context for unrelated work. At first compaction or 24K input growth above that task's first-response baseline, checkpoint and renew context at a safe boundary. Fixed harness overhead cannot be removed by a skill. If root renewal is unavailable, state that limitation; never claim a summary cleared its context.
5. **Coordinate on events.** Worker messages are only `BLOCKED`, `READY_FOR_QA`, `FAILED_GATE` or `DONE`, with evidence pointers and the needed decision. Batch routine questions; decide reversible implementation details locally within the contract. No progress ping-pong or replies to acknowledgements. Use native completion/wait facilities, bounded by host responsiveness rules. A timeout without new evidence does not justify source rereads, another status request or a board sweep. User-facing progress remains timely and concise.
6. **One independent review, two dimensions.** QA checks requirements and implementation quality together, through the real mounted caller, on frozen source. Separate reviewers only for a user/repository requirement, private holdout isolation or a distinct specialist risk. Reproduce findings before repair; allow one coherent repair and delta review. A second failure of the same invariant triggers diagnosis and rescoping, not another unchanged retry. Preserve unresolved work and all required gates.
7. **Integrate once, close once.** Reuse evidence only while relevant code, inputs, toolchain, configuration and rubric identities match. Run required final integration checks and one real-seam smoke. Root verifies candidate/receipt identity and acceptance coverage; a second full review needs a named unresolved risk. Update the tracker at dispatch, material blocker and accepted closeout, not on timer-only board sweeps. Stop at the authorized completion condition; unfinished work is never marked accepted.

## Observable guard

Before a dispatch or repair, measure the current batch using `scripts/usage_guard.py`; read [usage.md](references/usage.md) once for the tool contract. It consumes explicit scoped usage files and includes compaction responses. At 80% of the envelope, stop admitting new implementation and spend the reserve on QA/closeout. If exhausted, preserve state and replan the affected work. Continue authorized work only within a revised viable plan and remaining user limit; do not keep redispatching the same approach. Missing telemetry is unknown, never zero: use response/event counts and elapsed checkpoints while restoring measurement.

The script denies admission when invoked. It cannot intercept native tools, terminate agents, enforce provider billing caps or reclaim already loaded context. Do not represent this as a host-enforced hard limit. See [task-contract.md](references/task-contract.md) for the compact manifest and completion packet.

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
