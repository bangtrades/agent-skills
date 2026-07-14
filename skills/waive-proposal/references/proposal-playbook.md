# WaiveLabs Proposal Playbook — the lean structure

Read this before drafting. It encodes the proven section order and what each holds. The worked
example is the Summer Fridays v0.4 in `templates/build_proposal_template.py`.

## Canonical section order (lean default — ~5–7 pages)

1. **Engagement Summary** — 2 short paragraphs. What WaiveLabs will deliver, and the one-line
   scope boundary (what we own vs. what the client owns). Mention an accompanying live demo in a
   single clause if one exists. No mission statements, no "how to read this."
2. **Scope & Ownership** — a table: Area | Owner | Notes. The most important section for IT.
   Make the WaiveLabs / client / client-IT split unambiguous. Add one plain sentence on what
   WaiveLabs does NOT do.
3. **The Plan / Capabilities** — a compact table mapping each client requirement (or capability)
   to what WaiveLabs delivers, plus the responsible agent and the phase. One row per capability.
   Note the shared time-period/filter spine once, not per row.
4. **AI Agents & Governance** *(include when agents are in scope)* — an agent inventory table
   (agent | purpose | audience) and a controls table mapping each of the client's AI rules to a
   WaiveLabs control. Commit to: approved-sources-only, respects permissions, source traceability,
   flags incomplete data, no invented metrics, prompt-injection protection, recommendations
   visibly labeled vs. fact.
5. **Timeline** — phased table: Phase | Focus | Depends on. Pace by client dependencies (data
   access, approvals). Prefer phases over hard day-counts when a single resource or external
   dependencies make dates fragile. Put the client's most urgent item first.
6. **Required Deliverables — Coverage & Ownership** — answer the RFP's deliverable list directly:
   deliverable | owner (WaiveLabs / Client IT / Shared) | where/how. This is the "did you read our
   requirements" checkbox; keep it factual.
7. **Commercial** — table. See commercial patterns below.
8. **What We Need & Next Steps** — short numbered table: step | outcome.
   End with one line: "This proposal is a working draft prepared for discussion."

Add depth-only sections (architecture, validation, detailed security) **only if the client's RFP
explicitly demands them as vendor deliverables AND they're in WaiveLabs' scope.** Otherwise cite
that the client owns them, or reference a companion document — don't restate.

## Commercial patterns

- **Hourly retainer:** "$RATE / hour", "N hours per month", "$MONTHLY / month (N × $RATE)".
- **Payment schedule (explicit beats prose):** render as a single schedule line, e.g.
  "$X deposit at signing · $Y end of Month 1 · $Y end of Month 2 · $Z on successful closure —
  **$TOTAL over an N-month initial term**." Confirm the exact split with the user; verify the
  arithmetic (deposit + installments + closure = months × monthly).
- **Term must match the payment structure.** A signing deposit + closure payment implies a
  committed initial term — say so ("N-month initial engagement; continues monthly thereafter by
  agreement"), don't leave it "monthly / cancellable."
- **Assumptions row:** what the client provides (platform, data access, stakeholder time, that
  third-party data licenses stay in the client's name).
- **Personnel disclosure:** honor the user's choice; default to "personnel detail not disclosed
  at proposal stage" unless told otherwise.

## Voice

- Plain, confident, specific. Short sentences. Numbers over adjectives.
- Name dependencies and exceptions up front; reviewers trust honesty.
- WaiveLabs method (prototype → spec → build-from-zero in the client's environment) shows through
  the scope split — don't write a section selling the method.

## Anti-patterns (cut these — they bloated earlier drafts)

- ❌ Cover subtitle paragraph restating the RFP; footer taglines.
- ❌ "How to read the demo / this document" boxes.
- ❌ "Companion documents" / "what this references" boxes — just cite inline if needed.
- ❌ A "How We Work / Why Us / methodology" section — overkill for a vendor proposal.
- ❌ `callout()` quote boxes scattered per page. The helper exists; default to not using it.
- ❌ Restating something the table already says in a paragraph.
- ❌ Governance prose beyond what the RFP asks for and what's in scope.
- ❌ Hard day-by-day milestones the resourcing can't honor.
