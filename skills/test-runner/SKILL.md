---
name: test-runner
description: Use when running a test or smoke harness, interpreting failures, or wiring tests into a workflow — unit, integration, and smoke runs across the project's frameworks. Trigger on "run the tests", "run a smoke test", "why is this test failing", "set up the test harness", or pre-merge verification.
required: false
version: 0.1.0
---

# Test Runner

> **Stub skill.** The owning agent (QA) fills in `scripts/` and expands the
> harness as it masters the skill. The frontmatter above is the
> Paperclip-discoverable manifest.

Run tests and smoke checks, and turn failures into actionable findings.

## When to use this skill

- Running a project's unit / integration / smoke suite.
- Diagnosing a failing test (real bug vs flaky vs environment).
- Wiring a smoke harness into a verification gate.

## Usage

1. **Select** — the right suite for the change; prefer the fastest suite that
   can falsify the change.
2. **Run** — execute with a clean, recorded environment. Capture full output.
3. **Interpret** — distinguish a real failure from a flake or env issue. Ground
   the verdict in the actual output, not the runner's exit summary alone.
4. **Report** — pass/fail per suite, the failing output verbatim, and a
   suspected cause.

> Pairs with `paperclip-triage` when a failure is in the Paperclip/Cortana
> platform itself rather than application code.

## Scripts

`scripts/` is a placeholder. Intended helpers (filled in later): suite runners,
flaky-test detector, smoke-gate wrapper.

## Mastery notes

This agent's accumulated preferences live in its vault at
`skill-mastery/test-runner.md` (STEP-49 §2.1), not in this file.
