# Novai Slice Reporting Reference

Every coding assignment to an external agent should require a slice report.

## Location

Use:

```text
/Users/nolan/Cortana/cortana-vault/projects/novai/slices/
```

Filename pattern:

```text
YYYY-MM-DD--novai-v2-classroom--agent-N--short-slice-name.md
```

Example:

```text
/Users/nolan/Cortana/cortana-vault/projects/novai/slices/2026-05-08--novai-v2-classroom--agent-1--lesson-audio-read-aloud-control.md
```

## Required Sections

```markdown
# Slice Name

## Summary

## Files Changed

## Sprint Plan Alignment

## Acceptance Criteria

## Validation

## Risks / Follow-Up
```

## Prompt Rule

Agent prompts must state:

- Which skill to use.
- Exact ownership/files or area.
- That the agent is not alone in the codebase and must not revert others' changes.
- The required slice report path.
- Build/test command expected.
- Explicit cut line for what to skip if time runs out.
