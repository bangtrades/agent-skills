# Sprint Audit Truth Taxonomy

Use these classifications to keep development reporting honest.

## Verified Done

Use only when:

- Acceptance criteria are explicit or clearly inferred.
- Code/artifact changes are present.
- Tests, gates, logs, or issue evidence are current.
- No known blocker contradicts the claim.

Do not use if the only proof is a contributor summary.

## Done, Verification Gap

Use when implementation appears complete but one of these is missing:

- Current test or gate output.
- Fresh issue/log evidence.
- Exact artifact path.
- Reproducible command.
- Review of generated output.

Next action should be a bounded verification step, not more feature work.

## Partially Done

Use when some scope landed but:

- Acceptance criteria are incomplete.
- Integration is missing.
- UI/status surfaces are stale.
- Tests only cover part of the behavior.
- Follow-up slices are required for release.

## Blocked

Use when progress depends on:

- Quota, credentials, approvals, or subscription limits.
- Environment/runtime availability.
- External reviewer or operator action.
- Failing upstream gate.
- Missing design/product decision.

Name the blocker and the unblock action.

## Stale / Superseded

Use when evidence was valid earlier but is no longer the current truth:

- Older issue failed before a fix.
- Gate reads old classification after a newer canonical pass.
- Sprint row still says offline when live evidence exists.
- Agent report predates a later patch.

Stale evidence should not block release unless the stale signal is still used by active gates.

## No Evidence

Use when a claim has no supporting artifact:

- No diff.
- No test output.
- No issue/comment/log.
- No acceptance criteria.
- No reproducible command.

Do not soften this label. It is the reporting system telling the team where proof is missing.

## Evidence Hierarchy

Prefer newer and more direct evidence:

1. Current gate/test exit code and classification.
2. Fresh issue/run/audit/log rows inside the relevant time window.
3. Code diff plus focused regression test.
4. Operator-provided output pasted in the session.
5. Agent report.
6. Plan or intent text.

When evidence conflicts, name the conflict and prefer the source closest to runtime truth.
