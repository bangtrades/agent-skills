---
name: orchestration
description: This skill should be used when the user asks to "orchestrate agents", "give me agent slices", "coordinate a complex build", "plan parallel dev work", "manage implementation slices", "turn a roadmap into agent prompts", "recover a stuck project", "sequence next engineering work", or asks how to coordinate multiple agents, reports, gates, tests, commits, or release decisions for any software project.
version: 0.2.0
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
- Probe tool boundaries before dispatching agents across them. Deploy tools, external APIs, and browser automation have capability ceilings (payload size, auth state, platform/arch) that a ≤60-second orchestrator probe reveals; an agent discovers the same ceiling only after an expensive grind. One probe beats one retry-agent, every time. Deeper mechanism, confirmed across model tiers: NO model can hand-transcribe large
  byte-exact payloads (~50KB+) into a tool-call parameter — emission degrades to placeholders
  or truncation regardless of tier. Inline-content tools are therefore bounded by model
  transcription reliability, not just by the tool's own limits. For large payloads, always
  prefer a channel that reads bytes from disk directly (browser file-input upload, CLI, git)
  over any inline tool parameter; escalating model tier does NOT fix transcription.
- Budget every dispatched agent and give it an abort clause: state the effort budget and instruct "if blocked by auth, a capability ceiling, or a policy gate — stop and report the exact blocker and what you verified." Treat a precise blocker report as a SUCCESSFUL run. Unbudgeted agents fail heroically (encoding detours, web-UI workarounds) and burn 5–10× a productive slice's tokens producing nothing shippable.
- Own the contract, parallelize the surfaces: when multiple agents build against one artifact, the ORCHESTRATOR writes the shared kernel (shell/API/data module) and documents the interface in the kernel's file header; slices get disjoint file ownership plus the header as their spec. Assign shared-state seeding to exactly one slice. This pattern has produced zero-conflict first-merge integration across parallel coding agents.
- Verify with the cheapest sufficient evidence, in a ladder: static/syntax check → stub or dry-run against real data → real runtime (headless browser / live endpoint, console + screenshots) → human-eyeball of the highest-stakes surfaces. Climb only until the gate's question is answered; never accept a lower rung as proof of a higher rung's property.

Patterns from multi-agent parallel waves (2026-07, MetaCortex M2/M4 — agents killed mid-wave by provider credit exhaustion and by a session restart):

- **Update the issue tracker per slice at verification time, never batched at wave end.** Batched close-out is the root cause of stale boards: agents finish the code, die before the paperwork, and the tracker lags reality for hours. Verify a slice → immediately move its issue with an evidence comment.
- **Reports are advisory; diffs + gate runs are the record.** Accept work whose report never landed if the diff exists and the focused gate passes (two of five M4 slices shipped this way). Refuse "done" claims with no matching diff. Never order re-work to recover missing paperwork.
- **Agents die silently — plan the wave to be salvageable.** Background agents are killed by session restarts, credit exhaustion, and user stops, usually AFTER writing code and BEFORE tests/reports. On any resume: inventory disk first (`git status` + focused gates), classify each slice `complete-unverified` / `partial` / `zero-output`, then accept / resume-from-transcript / re-dispatch respectively. Resuming a partial agent with a one-message "here is what landed, finish only X" is far cheaper than a redo.
- **Pin cross-slice contracts verbatim in BOTH prompts.** When slice B consumes slice C's API, put the identical signature + data shape in both prompts and require the consumer to lazy-import with a fallback, so neither slice blocks the other and tests pass standalone. (Held twice with zero coordination traffic.)
- **Exactly one slice owns each shared config file** (pyproject/package manifests/lockfiles), named explicitly in every prompt ("you are the ONLY slice allowed to edit X"). The orchestrator pre-creates shared package `__init__` files before dispatch so no two agents invent them.
- **Prompts carry the environment facts:** absolute venv/tool paths, the exact test + lint commands, installed dependency versions, and "do NOT run version-control commands — the orchestrator commits." Each agent rediscovering the environment wastes its context; agents committing in a shared worktree corrupts the index.
- **Focused gates while the wave runs; the full gate only at reconcile.** Mid-wave, other agents' half-written files pollute a full-suite run — verify a completing slice against its own tests + lint, and run the whole suite once when the wave settles (and again after any merge).
- **Identify operator-gated actions before dispatch.** Permission classifiers refuse some actions regardless of agent intent (creating repos, pushing to new remotes, weakening branch protection, applying migrations). Don't assign these to agents or burn retries — stage everything, then hand the operator exact copy-paste commands and record the handoff on the tracker item.
- **Model tiering works:** orchestrator on the premium model doing assignment/verification only; complex slices (graph/pipeline/stateful logic) on the strong builder model; mechanical slices (renderers, registries, tool wrappers) on the fast model. Verification effort concentrates where correctness is subtle, not evenly.

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
- Effort budget and abort clause (what "blocked" means and the exact stop-and-report rule).
- The verified-passable path for any tool boundary the slice must cross (the orchestrator's probe result), or an explicit statement that the slice must NOT attempt that boundary.

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
- For a new CI workflow, validate command ordering from a clean checkout or identify generated-file prerequisites; a local pass after a prior build is not CI evidence.
- Mark stale, missing, or simulated evidence explicitly.
- Identify contradictions between reports, issue state, UI, logs, and gates.

If a report says done but no evidence exists, classify it as a reporting gap, not completion.

Log each agent's cost (tokens / tool-uses / wall time) next to its outcome in the ledger. Cost-per-shipped-artifact is the metric that exposes silent failure modes — a run can be "all green" while half its spend produced nothing.

The inverse also holds: if the diff exists and the focused gate passes but the report is missing (agent killed mid-run), accept the work on direct evidence and record "report missing, verified by orchestrator" — do not re-dispatch to recover paperwork.

### 6b. Recover A Broken Wave

When agents die mid-wave (session restart, provider credit exhaustion, user stop):

1. Inventory disk before anything else: `git status` + the file list each slice owned.
2. Classify every slice: `complete-unverified` (diff present, run its focused gate), `partial` (some owned files missing — usually tests or reports), `zero-output`.
3. Accept complete-unverified slices on gate evidence. Resume partial agents from their saved transcript with a one-message delta ("here is what landed and verifies; finish only X"). Re-dispatch only zero-output slices, noting in the new prompt that a prior attempt left empty artifacts.
4. Sweep the issue tracker to match the classification immediately — a broken wave's worst symptom is a board that lies for hours.
5. Do not treat pre-existing scaffold files in an agent's ownership area as its work product; check `git ls-files` provenance before crediting output.

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
- Do not dispatch a retry-agent for a failed slice before naming the failing layer — the retry inherits the same wall plus fresh ignorance of it.
- Do not let an agent cross an authentication wall "creatively" (web-UI logins, signups, alternate upload endpoints). Auth walls are stop-and-report events by definition.
- Do not schedule work whose single stage exceeds the execution environment's hard caps (shell timeouts, no surviving background processes); split into sub-cap stages with file-based state handoff.

## End-of-Run Skill Improvement

End every orchestration session with a short process review:

1. What actually moved the project forward?
2. Which slices were well-scoped or poorly scoped?
3. Which reports, gates, or logs were misleading?
4. Which dependency should have been sequenced differently?
5. What should this skill do better next time?

Then run this improvement command as a prompt in the current assistant session:

```text
Use the orchestration skill to review the orchestration run we just completed. Compare the planned slices, agent reports, code changes, tests, gates, commits, and remaining blockers. Recommend one concrete improvement to /Users/nolan/.claude/skills/orchestration/SKILL.md or its references, and patch it if the improvement is small and clearly correct.
```

Prefer adding one crisp rule, checklist item, or template refinement over long narrative.

## References

- `references/slice-templates.md` — reusable agent prompt skeletons and report formats.
