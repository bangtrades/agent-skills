# Engagement Lifecycle — P0 Signal → P8 Graduate

The single spine behind every WaiveLabs engagement. Each phase has an owner-agent, inputs,
outputs, and a hard exit gate. Motions (Enterprise · Partner · SMB/DTC) parameterize the
spine; they don't change it. Timelines are targets, not promises — they compress as models
improve (SF ran signal→signed in ~12 weeks; the demo sprint alone in 10 days).

## P0 — Signal & Qualification (Days 0–2)
- **Trigger:** inbound interest, outbound reply, referral, or deliberate target selection.
- **Do:** log the prospect (WaiveBoard `prospects` if available); run the Phase-0
  qualification scorecard (`~/Projects/agency/phase0-intake-qualification-onboarding.md`)
  → RED/YELLOW/GREEN; pick the motion; create the client manifest + Linear project
  (SKILL.md Steps 1–2).
- **Exit gate:** GREEN/YELLOW verdict · motion selected · named human decision-maker
  identified · manifest exists.

## P1 — Recon (Days 1–4, parallel with P0)
- **Do:** run the **brand-recon** skill → structured dossier + `{client}-brand` skill.
  Enterprise motion adds exec-persona research: transcribe the decision-maker's public
  content (interviews, podcasts, testimony) and extract their stated priorities *verbatim*
  (Varian: 4 Peter Shen interviews → the whole thesis).
- **Outputs:** dossier · `{client}-brand` skill · tech-stack hypothesis · champion map ·
  competitive scan · the client's #1 objection (this drives the demo's objection surface).
- **Exit gate:** brand skill renders a test artifact on-brand; top 3–5 decision-maker
  priorities documented in their own words. *(Autonomous — no human review required; errors
  here surface at G1 anyway because everything downstream renders through the brand skill.)*

## P2 — Positioning (Days 3–6)
- **Do:** design the thesis to map **1:1 to the decision-maker's stated priorities**. Draft
  the narrative arc: *quantified burden → why now → what the system is → domains/agents →
  trust & governance → flagship → market → the ask*. Define the flagship "wow" surface and
  the #1 objection to answer visually (Varian: PHI-local GPU console; SF: brand-authentic
  decision system).
- **Outputs:** one-page positioning memo a stranger could pitch from · demo spec (surface
  list, flagship, objection-answer, calibration targets, brand tokens).
- **Exit gate:** thesis + demo spec staged for bang. This is a **G2-adjacent** checkpoint:
  proceed with the demo build autonomously, but the thesis must be approved before anything
  built on it is *sent* (G1) or *priced* (G2).

## P3 — Demo Sprint (Days 5–14, target ≤7 days)
- **Do:** execute `demo-doctrine.md`. Parallel coding agents build surfaces against a shared
  synthetic simulation engine (`data-simulation.md`); wrap in Next.js; gate via
  waivelabs-secure-demo; QA screenshots archived for deck reuse.
- **Benchmarks:** SF 10 days end-to-end · Varian shipped with 3 agents in parallel.
- **Exit gate:** demo live on gated `{client}.waivelabs.ai` · doctrine ship-checklist passes
  · screenshots in `demo/deck-qa/`. Deploy is autonomous; *issuing viewer codes to the
  client is G1.*

## P4 — Pitch Package (Days 10–16)
- **Do:** run **client-pitch** + `{client}-brand`. Programmatic deck (pptxgenjs, follow the
  `build_vail_deck.js` pattern) following the P2 arc with P3 screenshots; strategic
  framework doc (full + lean); **3-tier pricing** (converts yes/no into "which tier");
  one-sheet.
- **Pricing anchors (defaults, G2 to change):** SMB 90-day $42k/$63k/$84k · growth-desk
  ~$21k/mo (60 hrs/mo @ $350) · Enterprise tiered $1.8M–$7M · Partner retainer + %.
- **Exit gate:** deck PDF renders on-brand · pricing tiers approved (**G2**) · package staged
  → bang sends/presents (**G1**).

## P5 — Legal & Close (Days 14–30)
- **Do:** NDA screen FIRST on any enterprise paper (see `proposal-legal.md`). Generate the
  4-doc set (Proposal → Engagement Letter → SOW → Services Agreement) or the lean vendor
  proposal for RFP responses. SOW must include the **demo→production bridge** line item and
  pre-agreed success/abort criteria.
- **Follow-up cadence (post-pitch):** +2d value-add insight → +7d second artifact (mini
  analysis of their market/data) → +14d direct close ask → +30d park to nurture. Never an
  empty "checking in." Drafts staged; sends are G1.
- **Exit gate:** signed engagement letter + first payment. Signature is bang's alone.

## P6 — Discovery & Onboarding (Week 0–1 post-signature)
- **Do:** intake questionnaire · Week-0 baseline (top-5 manual tasks + hrs/wk, reporting
  lag, source count, AI-literacy rating — the before-picture for ROI proof) · tech-stack
  audit · access provisioning · DPA if regulated data · kickoff scheduled · client folders +
  vault records created.
- **Exit gate:** contract signed · access granted · baseline captured · kickoff scheduled.

## P7 — Build: the Agentic OS (Weeks 1–10)
1. **Data foundation:** land sources into Supabase (client project via Supabase MCP), RLS +
   PII classification + security baseline.
2. **Visibility:** flagship Next.js app (auth, roles, charts, action surfaces) on Vercel.
3. **Agents:** control plane (Railway langgraph + agent inbox pattern, validated
   2026-07-02); 4 starter specialists (Data/Insights, Sales & Marketing, Ops, Engineering)
   with memory schema, tools, approval gates on write/spend/send; audit logging.
4. **Apps & autonomy:** AI-assisted dev loop with the client; native mobile if scoped.
- **The bridge:** Week 1 explicitly swaps the demo's simulation engine for real connectors —
  this is the paid SOW line item, never an assumed freebie.
- **Exit gate per sub-phase:** success metrics + abort triggers agreed BEFORE build starts
  (accuracy floor, adoption floor, safety incidents = 0).

## P8 — Deliver, Train, Graduate, Retain (Weeks 8–13)
- **Do:** curriculum sessions (8 modules; the SF AI Academy — in-product curriculum + AI
  Coach + per-learner progress — is the reference pattern and a proven upsell) ·
  Power-User Scorecard pre/post · handoff pack (architecture diagram, schema docs,
  agent/tool reference, runbooks, kill-switch) · case study + testimonial · retainer
  proposal (~10–20 hrs/mo, framed as "co-pilot for what you build next").
- **Exit gate:** handoff accepted · scorecard delta documented · retainer decision ·
  **run-log entry appended + skill diffs proposed** (SKILL.md Step 5).

---

## Motion parameterization

| Parameter | Enterprise (Varian) | Partner (Solugenix) | SMB / DTC (SF, CopperJoint) |
|---|---|---|---|
| P1 emphasis | Exec persona + org intel | Partner's clients + compliance regime | brand-recon dossier |
| P3 proof | Cinematic multi-console demo | Discovery instruments ARE the demo (no bespoke build) | Gated growth-desk demo |
| P4 pricing | Tiered build plan $1.8–7M | Retainer + % | $42/63/84k or ~$21k/mo |
| P5 paper | Their NDA/MSA (redline hard) | MSA + white-label terms | WaiveLabs 4-doc set / lean proposal |
| P7 scale | Pilot domain, phased | Behind partner brand | Full 90-day OS |

## Where the human sits

Bang holds exactly: **G1** (anything transmitted to the client, incl. presenting the pitch
and issuing demo codes), **G2** (legal content + every commercial figure + signature), and
the client relationship itself. Everything else — recon, brand skill, positioning drafts,
demo build, deploy, DNS, database provisioning, proposal/legal drafting, follow-up drafting —
runs without waiting.
