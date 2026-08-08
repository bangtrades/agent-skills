# Slice Templates

Use these templates when generating copy-ready agent prompts. Keep ownership paths disjoint and make the evidence requirements explicit.

## Implementation Slice

```text
You are Agent N for <slice-id>.

Context:
<3-6 sentences describing current state, current verified truth, and why this slice exists. Include issue/gate ids and timestamps if relevant.>

Goal:
<One concrete outcome.>

Primary ownership:
- <file or module path>
- <file or module path>

Non-ownership / coordination:
- Do not edit <shared file> unless required.
- Coordinate reason names/schema/API shape with <other slice>.
- Do not revert unrelated work.

Rules:
- Read local project instructions first.
- Preserve user changes.
- Keep the patch narrow.
- Add regression coverage at the layer being changed.

Tasks:
1. Inspect <specific files>.
2. Identify <specific contract or bug>.
3. Implement <specific behavior>.
4. Add tests for <case A>, <case B>, <case C>.
5. Run <focused command>.
6. Write report at <report path>.

Report must include:
- Files changed.
- Tests run and exact results.
- Evidence that acceptance criteria are met.
- Remaining risks or follow-up slices.
```

## Verification / Gate Slice

```text
You are Agent N for <slice-id>.

Context:
<State which implementation or behavior needs independent verification.>

Goal:
Create or update a read-only verifier that reports current truth without mutating state.

Primary ownership:
- <script path>
- <test path, if applicable>

Rules:
- The verifier must be read-only by composition.
- Separate stale/historical evidence from fresh evidence.
- Final classification, exit code, blockers, and evidence must agree.

Tasks:
1. Inspect existing verifier style and JSON conventions.
2. Define canonical classifications.
3. Implement the verifier.
4. Add offline classifier tests where possible.
5. Run verifier against the current repo state.
6. Write report at <report path>.

Report must include:
- Classification matrix.
- Commands run.
- Current result.
- Any misleading prior signal corrected by the verifier.
```

## Triage Slice

```text
You are Agent N for <slice-id>.

Context:
<Describe the repeated failure, contradictory signal, or user-visible blocked state.>

Goal:
Find the failing layer and produce a patch recommendation or minimal fix.

Primary ownership:
- Read-only by default unless root cause is proven.

Rules:
- Do not patch before identifying the layer.
- Inspect source-of-truth records, logs, and gates.
- Do not rerun live/paid workflows unless explicitly approved.

Questions to answer:
1. What did the system claim happened?
2. What actually happened according to canonical logs/audit?
3. Which layer misreported or failed?
4. What is the smallest durable fix?
5. What regression test should prevent recurrence?

Report must include:
- Root cause.
- False leads eliminated.
- Evidence path.
- Recommended implementation slice.
```

## Docs / Release Slice

```text
You are Agent N for <slice-id>.

Context:
<State verified implementation status and any open defects.>

Goal:
Update sprint/release docs so project truth matches current evidence.

Primary ownership:
- <sprint doc>
- <runbook/report path>

Rules:
- Do not claim deferred work is complete.
- Distinguish implementation complete, verified complete, audit-only complete, and release blocked.
- Include issue ids, gate names, and dates when relevant.

Tasks:
1. Read current roadmap/sprint docs and reports.
2. Add or update ledger rows.
3. State completed, open, and deferred lanes.
4. Recommend next order of work.
5. Write report at <report path>.
```

## Slice Quality Checklist

- The prompt is copy-ready.
- The goal is singular.
- Ownership paths are explicit.
- Tests are named.
- Report path is named.
- Dependencies are explicit.
- The agent knows what not to touch.
- The slice can be judged from evidence, not vibes.
