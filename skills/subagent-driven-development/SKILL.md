---
name: subagent-driven-development
description: "Use when executing an approved implementation plan with fresh task-specific subagents and independent review. Uses the shared orchestration budget and evidence workflow."
version: 1.2.0
author: Hermes Agent (adapted from obra/superpowers)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [delegation, subagent, implementation, workflow]
    related_skills: [orchestration]
---

# Subagent-Driven Development

Use the available `orchestration` skill as the single execution controller. Resolve its registered path; read its entrypoint once, not in every worker. If unavailable, report the missing dependency and follow the user's supplied workflow without claiming its budget guard ran.

Select one bounded deliverable from the approved plan. Dispatch a fresh producer with the task's requirements, actual caller, exact base, owned paths, prohibitions and required tests. Do not extract the entire backlog into active context or fork the full transcript. Delegate only with applicable authority and a callable agent tool; do not assume a tool named `delegate_task` exists.

After producer checks pass, one independent reviewer evaluates both spec compliance and code quality against frozen source, including the actual application seam. Reproduce findings, perform one coherent repair and review the changed risk. Repeated failure of the same invariant requires diagnosis and replanning. Root verifies acceptance coverage and integration; it does not automatically commission another full review.

Separate specification and quality reviewers remain available when explicitly required by the user/repository or justified by a distinct mandate. Only then read [legacy-two-stage.md](references/legacy-two-stage.md); its historical unconditional retry language does not override orchestration budgets. Required tests, holdout privacy and independent review remain intact.

Use this adapter OR orchestration as the primary workflow, not two parallel coordinators. Existing context-budget and gate-taxonomy references are optional specialist material; do not load them routinely.
