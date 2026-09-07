---
name: software-architecture
description: Use when turning a PRD or product requirements into an application architecture, reviewing a system design, choosing component boundaries, or preparing ADRs and an implementation handoff. Applies Cortana's SDLC and MetaCortex development playbooks when available; use architecture-diagram for visualization alone.
---

# Software architecture from requirements

Produce a reviewable architecture for the smallest useful release and its next likely changes. A well-made application is usable, correct, secure, private, performant under its stated workload, maintainable and straightforward to deploy and recover. Choose complexity only when an actual requirement or demonstrated constraint justifies it.

## Load Cortana's SDLC before design decisions

For Cortana/WaiveLabs work, resolve and read the **architecture and stack** route in `cortana-vault/projects/claude-skills/claude-skills--development-sdlc.md` from the accessible Cortana root (local default `~/Cortana`) or approved project export. This is the maintained entry point to the project starter, architecture template, decision research, applicability profiles and MetaCortex development playbook. Read the current project and repository instructions first.

Load only sources relevant to the decision. Recover MetaCortex's current context, effective execution standard and existing roadmap only when MetaCortex is the selected execution lane or the system being designed. A future possibility is an owned portability question; it does not trigger a factory-roadmap load or import factory backlog into the product design. A personal vault is not a worker mount or an enterprise authority layer. If Cortana context is unavailable, name the missing record and affected decisions; use the supplied PRD and the portable workflow below without claiming compliance with unseen guidance. Continue independent work and ask for missing information only where necessary.

## Design and challenge the system

1. **Recover intent and evidence.** Identify the target user, critical workflow, MVP boundary, existing PRD/architecture versions, actual repository state, constraints and prior decisions. Preserve approved choices unless changed evidence requires an explicit revision. Do not regenerate adequate supplied documents just to match a template.
2. **Make requirements testable.** Give functional and nonfunctional requirements stable IDs and observable acceptance. Capture workload, latency/resource/cost budgets, availability/recovery needs, supported devices/input methods, data categories and legal/region applicability. Label assumptions and unresolved decisions with owners; never invent a benchmark or legal conclusion.
3. **Choose the simplest viable architecture.** Compare credible alternatives against those requirements, team/runtime constraints, operating cost and a removal/replacement path. Start from a small deployable system when appropriate; split services only for a concrete isolation, scaling, ownership or operational need. Use bounded spikes for uncertain integrations or performance. Verify changing vendor capabilities and entitlements from current primary sources before relying on them. If retrieval is unavailable, keep the comparison provisional or vendor-neutral, name the evidence needed, and defer only the dependent vendor commitment; continue independent architecture work.
4. **Describe actual boundaries.** Show system context, runtime components, trust and tenant boundaries, data flows/retention, API and persistence contracts, failure paths, dependencies and deployment/recovery topology. Distinguish current, proposed and externally controlled parts. Diagram only what the evidence and declared proposal support.
5. **Record decisions and traceability.** For each material ADR, record context, requirement IDs, options, decision/status/owner, tradeoffs, validation method and conditions for reconsideration. Trace requirements through the relevant component and real caller to implementation work and verification. Every shared seam has an owner.
6. **Plan coherent increments.** Define the first end-to-end usable workflow and dependency-ordered implementation/verification slices. Preserve existing issue identities where work already exists; proposed task mappings are not native blockers. Include bootstrap, real integration, user/error states, migration, observability and rollback in the appropriate increment.
7. **Challenge before handoff.** Review whether the design can meet its acceptance under the declared roles, data shape and failure conditions. Specify independent checks, intended-role allow/deny cases and representative user-journey validation proportional to risk. Leave unexecuted experiments unverified. A backend candidate is not a user-facing MVP when the promise includes a UI.

## Deliverable and stopping point

For substantial design work, produce an architecture document plus ADRs/diagrams as needed, a requirement-to-decision-to-work-to-verification trace, deployment/recovery and quality plans, and an owned decision/risk register. Record source versions and verification limits so another agent can reproduce the reasoning. For a focused review or small change, update only the affected decisions, seams and evidence.

Keep document acceptance, implementation, independent verification, merge, release and user acceptance separate. A schema-valid package, source-graph confidence, or successful diagram render does not prove runtime behavior or authorize a release. Product feedback returns to a versioned requirement/architecture change; do not silently rewrite the active acceptance criteria.

Hand off the next scoped action under existing authorization. Designing an architecture does not itself create live issues, change repository settings, deploy software or start autonomous workers. Use the current runtime's permissions and tool schemas for any separately authorized effect.
