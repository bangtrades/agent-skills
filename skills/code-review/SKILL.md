---
name: code-review
description: Use when reviewing a PR or change set for concrete correctness, security, regression, and maintainability issues. Return supported file-and-line findings and verification limits.
required: false
version: 0.1.1
---

# Evidence-based code review

## Cortana SDLC and delivery playbooks

For Cortana/WaiveLabs software work, read the **review and verification** route in `cortana-vault/projects/claude-skills/claude-skills--development-sdlc.md` from the accessible Cortana root (local default `~/Cortana`) or approved project export before making the corresponding decisions. It links the maintained SDLC starter and MetaCortex playbooks. If unavailable, name the missing context and proceed from supplied evidence only where the next decision does not depend on it.

Check the affected requirement/ADR, real callers, data/trust boundaries and acceptance evidence. Report exact-candidate findings and verification limits; keep independent review separate from permission to merge, release or mark work accepted.


Read repository instructions, the change intent, the exact diff, surrounding implementations, and affected callers. Fix the comparison base before reviewing; preserve a dirty working tree and never use shared-repository stash as a baseline mechanism.

1. Trace changed behavior to inputs, state, side effects, consumers, and error paths.
2. Check correctness, authorization, data boundaries, compatibility, concurrency, migrations, and meaningful tests relevant to the change.
3. Use actual project checks when appropriate. Do not equate tool completion or empty findings with a clean review. The older `code-reviewer` analyzers are scaffolds and provide no review evidence.
4. Report each actionable finding with severity, exact file/line, triggering condition, consequence, and a specific correction. Distinguish confirmed defects from uncertain questions.
5. Deduplicate findings and state checks run, checks omitted, and residual limits. Zero findings is valid; do not manufacture a quota.

Use `github-pr-workflow` for requested PR logistics or `github-code-review` for the GitHub-specific review procedure. Choose `mp-code-review` as an alternative when its standards workflow fits. Use independent `adversarial-reviewer` only when authorized or required by applicable instructions. Review never implies permission to post, approve, merge, or deploy.

## Runtime and maintenance

Read the current project hub and applicable local instructions. Discover available tools and verify their input schema; skill names do not prove an API exists. Record what was executed, what was checked, and what remains unverified. Stage skill improvements in Cortana’s inbox; never rewrite the installed registry.
