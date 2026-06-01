---
name: sprint-audit
description: This skill should be used when the user asks to "run a sprint audit", "audit the sprint plan", "review agent slice work", "assess sprint progress", "check development reporting truth", "compare agent reports to the active sprint", "prepare a sprint status review", or asks what the team should do next based on current repo, issue, gate, test, or agent-slice evidence.
version: 0.1.0
---

# Sprint Audit

Use this skill to perform an evidence-based sprint review for any software project in the current working context. The goal is to answer: what was planned, what agents or contributors claimed, what actually changed, what is verified, what is blocked, and what should happen next.

The audit must be project-agnostic. Do not assume Cortana, Wick, Nova, or any other specific system. Discover the active sprint plan, local conventions, gates, test scripts, issue artifacts, and agent reports from the repo.

## Core Rule

Do not accept status labels at face value. Treat every claim as unverified until it is linked to concrete evidence: code diff, test output, gate classification, issue state, artifact path, log row, commit, or operator-confirmed result.

## Safety

- Read local project instructions first when present: `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, repo README, or equivalent.
- Preserve user changes. Do not revert unrelated work.
- Use `rg` / `rg --files` for discovery.
- Do not mutate project state unless the user explicitly asks for fixes.
- Do not run destructive commands.
- Treat external dashboards, issue trackers, and paid agent runs as operator-controlled unless suitable tools are available and the user asked to use them.

## Audit Workflow

### 1. Establish Context

Identify:

- Repo root and active branch.
- Relevant local instructions.
- Active sprint/roadmap/plan files.
- Agent report locations.
- Issue/task identifiers mentioned in recent work.
- Gate/test scripts used for release or readiness.
- Current date and timezone when interpreting “today,” “latest,” or stale evidence.

Use commands like:

```bash
git status --short
git branch --show-current
rg --files -g '*sprint*' -g '*plan*' -g '*roadmap*' -g '*release*' -g '*agent-report*' -g '*gate*'
rg -n 'TODO|BLOCKED|NO_GO|GO_|PASS|FAIL|Done|verified|offline|agent' docs .github scripts 2>/dev/null
```

Adjust paths to the repo. If the project uses a nested workspace or submodule, audit parent and nested worktrees separately.

### 2. Build the Sprint Ledger

Extract active sprint items from the plan. For each item, capture:

- Slice/story id.
- Owner/agent.
- Intended outcome.
- Claimed status.
- Acceptance criteria.
- Linked reports or artifacts.
- Dependencies.

If no explicit sprint plan exists, infer a provisional ledger from issue titles, agent reports, branch names, recent commits, and changed files. Label the ledger as inferred.

### 3. Review Agent Slice Work

For each agent report or contributor slice:

- Summarize the claim in one sentence.
- Identify files allegedly touched.
- Compare report claims to actual git status/diff.
- Check whether acceptance criteria were addressed.
- Check whether tests/gates were run and whether outputs were pasted, logged, or reproducible.
- Mark missing evidence explicitly.

Use the truth taxonomy from `references/truth-taxonomy.md`.

### 4. Verify Current Evidence

Run safe read-only checks appropriate to the repo:

- `git status --short`
- `git diff --check`
- focused tests or gate scripts that are local and low-risk
- existing release/readiness scripts
- lint/typecheck only when cheap or already expected by the project

Do not overrun user budget. If tests are expensive, list them as recommended verification instead of running them.

### 5. Reconcile Truth

Classify each sprint item:

- `Verified Done`: acceptance criteria met and evidence is current.
- `Done, Verification Gap`: implementation likely complete but proof is missing, stale, or indirect.
- `Partially Done`: meaningful implementation landed, but criteria remain open.
- `Blocked`: external dependency, quota, environment, approval, failing gate, or missing input.
- `Stale / Superseded`: old report or issue no longer reflects current code or gate truth.
- `No Evidence`: claim exists but cannot be tied to code, tests, logs, or issue state.

Prefer precise reasons over generic labels.

### 6. Audit Reporting Quality

Assess development reporting truth:

- Are statuses consistent across sprint plan, issue tracker, agent reports, gates, and git?
- Are “done” claims backed by current evidence?
- Are stale failures still surfacing after later passes?
- Are offline, live, and simulated results clearly distinguished?
- Are blockers specific enough for action?
- Are issue identifiers and timestamps included?
- Are gates aligned with the latest architecture?

Flag any misleading reporting surface as a product/process bug, not just documentation drift.

### 7. Recommend Next Steps

Return a short ranked plan:

1. Release blockers that must be fixed before commit/push.
2. Verification gaps that can be closed quickly.
3. Commit slicing recommendations.
4. Sprint ledger updates.
5. Follow-up stories for stale gates, reporting UX, or automation.

Keep the recommendations action-oriented and assignable.

## Output Format

Use this structure unless the user asks for a different format:

1. **Executive Verdict**
   - Overall sprint health.
   - Ship/commit readiness.
   - Biggest risk.

2. **Evidence Reviewed**
   - Commands run or files inspected.
   - Important gate/test results.
   - Relevant issue/report identifiers.

3. **Sprint Item Matrix**
   - Item, claim, evidence, classification, next action.

4. **Reporting Truth Gaps**
   - Contradictions, stale gates, unverifiable claims, missing timestamps, or misleading status labels.

5. **Recommended Next Steps**
   - Ordered and scoped.

6. **Skill Improvement Note**
   - One improvement to make future sprint audits more reliable.
   - If small and clearly useful, patch this skill or its references.

For a detailed report template, see `references/audit-template.md`.

## Anti-Patterns

- Do not report “all green” when one gate is green but another current release gate is stale or failing.
- Do not equate “agent said TASK_COMPLETE” with verified completion.
- Do not hide dirty worktree scope.
- Do not collapse live, offline, simulated, and historical evidence.
- Do not rerun expensive tests just to look thorough.
- Do not produce a giant status dump without ranking next actions.

## References

- `references/truth-taxonomy.md` — status classifications and evidence rules.
- `references/audit-template.md` — reusable sprint audit report format.
