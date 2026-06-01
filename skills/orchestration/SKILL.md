---
name: orchestration
description: This skill should be used when the user asks to "orchestrate agents", "give me agent slices", "coordinate a complex build", "plan parallel dev work", "manage implementation slices", "turn a roadmap into agent prompts", "recover a stuck project", "sequence next engineering work", or asks how to coordinate multiple agents, reports, gates, tests, commits, or release decisions for any software project.
version: 0.1.0
---

# Orchestration

Use this skill to coordinate complex software work across multiple agents, contributors, or implementation slices. The purpose is to convert a messy project state into clear parallel work, truth-based reporting, and a release path that does not confuse activity with progress.

Keep the skill project-agnostic. Discover the repository, sprint plan, local instructions, test gates, issue tracker conventions, and report format from the active working context. Do not assume any specific product, agent platform, or memory system.

## Core Rule

Orchestrate from evidence, not optimism. A slice is not complete because an agent says it is complete; it is complete when code, tests, gates, logs, issue state, or an explicit operator result prove it against the acceptance criteria.

## Safety

- Read local project instructions first when present: `AGENTS.md`, `CLAUDE.md`, repo docs, or equivalent.
- Preserve user changes. Do not revert unrelated work.
- Use `rg` / `rg --files` for discovery.
- Keep slice ownership disjoint when multiple agents may edit files.
- Do not run destructive commands.
- Separate live, offline, simulated, historical, and operator-provided evidence.
- Avoid paid or mutating reruns until the failing layer is understood.

## When To Orchestrate

Use orchestration when work has any of these traits:

- More than one credible implementation lane exists.
- The user has multiple agents ready and needs prompts.
- Gates or reports disagree about status.
- The project is stuck in repeated small fixes or reruns.
- A sprint plan needs translation into executable dev slices.
- A release decision requires code, docs, tests, and operator evidence to line up.

When the user is angry, blocked, or repeating failed tests, shift from normal task execution into triage-first orchestration: stop generating more slices until the actual failing layer is named.

## Workflow

### Session-Derived Patterns

Apply these patterns from prior complex build orchestration:

- Use triage before new slices when the team is looping on live tests. Repeated reruns usually mean the failing layer has not been isolated.
- Separate “system worked” from “reporting said it worked.” A canonical log, audit row, database record, or test result can prove execution even when an issue, UI, or final model response misclassifies it.
- Create slices around ownership boundaries, not around vague topics. Good slices own a classifier, a gate, a runtime module, a runbook, or a release ledger.
- Keep one slice responsible for truth reconciliation. This prevents implementation agents from marking their own work done without independent evidence.
- Require report paths up front. A report that lands in a predictable location becomes part of the sprint ledger instead of disappearing into chat history.
- Promote repeated troubleshooting lessons into skills. When a failure pattern recurs, add it to a triage or orchestration skill before the next rerun.

### 1. Stabilize Context

Identify the current state before assigning work:

- Repo root, branch, dirty files, and nested worktrees.
- Active sprint or roadmap docs.
- Existing agent report paths and naming conventions.
- Current blockers, gate classifications, issue ids, and timestamps.
- Recent operator commands and their final classifications.
- Local safety constraints.

If the worktree is dirty, explicitly protect unrelated changes. When proposing commits, name the exact files that belong in the commit.

### 2. Decide Whether To Triage First

Invoke troubleshooting methods before slice planning when:

- A gate says `NO_GO`, `BLOCKED`, `WAITING`, or has contradictory pass/fail tallies.
- The team has rerun the same smoke/test repeatedly.
- A tool executed but the UI or issue lifecycle says it failed.
- A model response, agent report, or screenshot conflicts with logs or audit rows.
- A stale or pre-fix artifact is being treated as current.

Triage by layer:

- Static/config readiness.
- Runtime/container/service health.
- Prompt/task delivery.
- Tool visibility and execution lifecycle.
- Canonical audit/log evidence.
- Semantic final response.
- Gate/reporting truth.
- Release decision.

Patch only the layer proven defective. If a verifier misreports true execution as failure, fix the verifier or reporting surface separately from the runtime.

### 3. Build The Work Ledger

Convert the goal into a ledger with:

- Outcome.
- Evidence required.
- Owner or agent.
- Write scope.
- Read-only dependencies.
- Tests/gates to run.
- Report path.
- Definition of done.

Use the ledger to avoid duplicate work. If two agents need the same file, split sequentially or make one read-only.

### 4. Create Agent Slices

Each agent prompt must be self-contained and concrete. Include:

- Context in 3-6 sentences.
- Goal.
- Primary ownership paths.
- Explicit non-ownership paths or coordination constraints.
- Safety rules.
- Tasks in execution order.
- Required tests/gates.
- Required report path.
- Expected final report contents.

Prefer four slices when the work naturally separates into implementation, verification, docs/release, and adversarial/truth review. Prefer fewer slices when ownership cannot be separated cleanly.

Use `references/slice-templates.md` for reusable prompt skeletons.

### 5. Sequence And Coordinate

Assign work by dependency:

- Parallel: independent file ownership or read-only audits.
- Sequential: shared classifier/reason-code contracts, schema changes, migrations, public API changes, release notes that depend on final gate names.
- Sidecar: docs, ledger updates, and verification harnesses can often start while implementation runs, but must reconcile after code lands.

Name dependencies directly. Example: “Agent 3 starts after Agent 1 chooses the reason-code contract.”

### 6. Reconcile Reports

When agent reports return:

- Compare claims to git status and diffs.
- Check that tests actually ran and are current.
- Re-run focused gates when cheap and local.
- Mark stale, missing, or simulated evidence explicitly.
- Identify contradictions between reports, issue state, UI, logs, and gates.

If a report says done but no evidence exists, classify it as a reporting gap, not completion.

### 7. Decide Commit And Release Scope

Before commit or release:

- Confirm final classifications and exit codes.
- Confirm blockers are empty or intentionally deferred.
- Confirm docs/ledger reflect current truth.
- Stage only files belonging to the accepted slice.
- Leave unrelated dirty files untouched.
- Produce a clear release verdict: ship, commit-only, hold, or re-triage.

## Reporting Format

For orchestration updates, use:

1. **Current Verdict** — what is true now.
2. **Evidence** — commands, reports, gates, logs, issue ids.
3. **Slices** — agent prompts or active ownership matrix.
4. **Dependencies** — what can run now vs later.
5. **Risks** — likely misreports, stale evidence, shared file conflicts.
6. **Next Action** — the smallest useful move.

Keep agent prompts copy-ready. Avoid vague instructions like “investigate thoroughly” unless paired with exact files, questions, and output requirements.

## Anti-Patterns

- Do not create more agents to compensate for unclear root cause.
- Do not let every agent edit the same shared classifier or config.
- Do not accept screenshots or agent comments without log/gate corroboration when release truth matters.
- Do not re-run expensive live tests before checking whether the last run already contains canonical proof.
- Do not mix runtime fixes, gate truth fixes, docs, and release commits without naming the scope.
- Do not bury “remaining defect” under a green headline.

## End-of-Run Skill Improvement

End every orchestration session with a short process review:

1. What actually moved the project forward?
2. Which slices were well-scoped or poorly scoped?
3. Which reports, gates, or logs were misleading?
4. Which dependency should have been sequenced differently?
5. What should this skill do better next time?

Then run this improvement command as a prompt in the current assistant session:

```text
Use the orchestration skill to review the orchestration run we just completed. Compare the planned slices, agent reports, code changes, tests, gates, commits, and remaining blockers. Recommend one concrete improvement to /Users/nolan/.codex/skills/orchestration/SKILL.md or its references, and patch it if the improvement is small and clearly correct.
```

Prefer adding one crisp rule, checklist item, or template refinement over long narrative.

## References

- `references/slice-templates.md` — reusable agent prompt skeletons and report formats.
