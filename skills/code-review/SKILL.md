---
name: code-review
description: Use when reviewing a pull request, diff, or change set — checking correctness, security, style, and test coverage against the team's standards. Trigger on "review this PR", "review my changes", "check this diff", "is this ready to merge", or pre-merge quality gating.
required: false
version: 0.1.0
---

# Code Review

> **Stub skill.** The owning agent (dev / QA) fills in `scripts/` and expands the
> checklist as it masters the skill. The frontmatter above is the
> Paperclip-discoverable manifest.

Review changes against a consistent quality and security bar.

## When to use this skill

- Reviewing a PR or diff before merge.
- Sanity-checking your own change set before requesting review.
- Producing a structured review report.

## Usage

1. **Understand** — read the diff and the intent. Don't review code you don't
   understand; ask or read the surrounding context first.
2. **Checklist** — correctness, edge cases, security (injection, authz, secrets),
   error handling at boundaries, test coverage, and clarity. Flag scope creep.
3. **Prioritize** — separate blocking issues from nits. Lead with the blockers.
4. **Report** — file-and-line references, a clear merge/no-merge call, and the
   reasoning.

## Scripts

`scripts/` is a placeholder. Intended helpers (filled in later): diff summarizer,
checklist runner, review-report templater.

## Mastery notes

This agent's accumulated preferences live in its vault at
`skill-mastery/code-review.md` (STEP-49 §2.1), not in this file.
