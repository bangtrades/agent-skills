# Task Slices — S1–S12, dependency graph, Linear mapping

Each slice is a self-contained brief a fresh agent can execute: inputs, skills, outputs,
done-when. Dependencies are explicit; everything else runs in parallel. Dispatch each slice
as an agent whose prompt contains the brief verbatim + client slug + folder paths + motion +
manifest path + SKILL.md standing rules.

**Founder-only (never delegated):** pitch delivery, contract signature, pricing decisions,
any transmission to the client (G1/G2).

---

## Pre-signature slices (P1–P5)

### S1 — Recon & Dossier
- **Skills:** brand-recon (Firecrawl primary, Chrome MCP fallback)
- **Inputs:** company name/URL, decision-maker name, motion
- **Outputs:** dossier; `{client}-brand` skill; tech-stack hypothesis; champion map; the
  client's #1 objection. Enterprise motion: decision-maker's public statements transcribed +
  verbatim priority list.
- **Done when:** brand skill renders a test artifact on-brand; top 3–5 decision-maker
  priorities documented in their own words.
- **Blocks:** S2, S3, S4, S5.

### S2 — Positioning Memo & Demo Spec
- **Inputs:** S1 dossier
- **Outputs:** one-page thesis mapped 1:1 to decision-maker priorities; narrative arc
  (burden → why now → what it is → domains → trust → flagship → market → ask); demo spec
  (surfaces, flagship, #1-objection answer, calibration targets, brand tokens); product
  name locked in the manifest.
- **Done when:** thesis + demo spec written and staged for bang. Build proceeds; nothing
  ships to the client until G1.
- **Blocks:** S3, S4.

### S3 — Demo Sprint (execute demo-doctrine.md)
Sub-slices, parallel after S3a:
- **S3a:** simulation engine (data-simulation.md) + Next.js app shell + routing — the
  contract all surface agents build against.
  *S3a is ORCHESTRATOR-OWNED:* the orchestrator (not a dispatched agent) writes the shell,
  core API module, theme, and the data module derived from the simulation contract, and
  documents the full tab/registration/state API in the core module's file HEADER so every
  surface agent learns the contract from one file. S3a also declares **state-seeding
  ownership**: exactly one slice owns seeding each shared store (approval queue, event
  stream); others consume only. Surface slices receive the contract header, stylesheet class
  inventory, exact data shapes, disjoint file-ownership lists, and the standing rules — and
  must verify with a syntax check plus a stub run against the real data module before
  reporting done. This is why parallel surfaces merge without conflicts.
- **S3b:** landing + command center (agent fleet, KPIs, live event stream)
- **S3c:** flagship "wow" surface
- **S3d:** operator consoles / drilldowns (click-to-inspect everywhere)
- **S3e:** objection-answer surface + approval queue + audit ledger
- **S3f:** integration + calibration pass — one agent reconciles all surfaces against the
  sim engine; verify seeded numbers against the dossier.
- **S3g:** gate via waivelabs-secure-demo (infrastructure.md): Supabase signed-cookie gate,
  watermark, subdomain, codes STAGED (issuing to client viewers = G1).
  *Deploy pre-flight is mandatory:* before dispatching S3g, probe the deploy tool with a
  one-file payload (MCP deploy tools commonly cap per-call payload far below a multi-file
  demo), confirm auth non-interactively (token in `.deploy-secrets.local.md` — never a web
  login flow), and confirm DNS prerequisites. If any probe fails: record the deploy as
  STAGED with the exact blocker and move on — the demo stays locally runnable by design
  (static-first mode), and a blocked deploy must never block S3h or S4.
- **S3h:** QA click-through + screenshots → `demo/deck-qa/` (feeds S4).
- **S3i:** package assembler — the "demo package" exit artifact. Bundle the S3f-passed demo,
  deck-qa screenshots, DEMO_SCRIPT.md, calibration-provenance note (window/seed/ladder-approval
  pointer), and gate-status snapshot into one `demo-package/` folder with a README a stranger
  could present from. Register it in the demo-board/registry if one is available; otherwise
  the folder IS the registry entry. Done when a person with zero run context can open the
  bundle and deliver the 10-minute path. This is the unit an autonomous loop outputs per
  prospect.
- **Done when:** demo-doctrine ship checklist passes; demo live on gated subdomain.

### S4 — Pitch Package
- **Skills:** client-pitch + `{client}-brand` + brand-waive + pptx/pdf
- **Outputs:** programmatic deck (pptxgenjs; `build_vail_deck.js` pattern) with S3h
  screenshots; strategic framework (full + lean); 3-tier pricing sheet (figures from
  manifest — G2 if absent); one-sheet.
- **Done when:** deck PDF renders on-brand; pricing approved (G2); package staged for G1.
- **Depends:** S2 (arc), S3h (screenshots).

### S5 — Proposal, Legal Screen & Doc Set
- **Skills:** waive-proposal (lean RFP-response proposal); legal:triage-nda,
  legal:review-contract; generators at `~/Projects/agency/_templates/engagement-docs/`.
  Full guidance: proposal-legal.md.
- **Outputs:** lean vendor proposal PDF (Requirements → Plan → Timeline → Cost) and/or the
  4-doc set; NDA/MSA redline memo; SOW with demo→production bridge + success/abort criteria.
- **Done when:** docs generated, redlines documented, figures match the manifest, bang has a
  signable set (G2 before any figure is final; G1 before anything is sent).
- **Parallel to S3/S4** (starts after S1).

### S6 — Follow-up Sequencer
- **Outputs:** post-pitch cadence drafted and scheduled (+2d value-add / +7d second artifact
  / +14d close ask / +30d park). Each touch contains a genuinely new insight from the
  dossier — never an empty nudge. Every send is G1.
- **Done when:** cadence scheduled + drafts staged in `proposal/followups/`.

## Post-signature slices (P6–P8)

### S7 — Onboarding & Baseline
- **Outputs:** intake questionnaire sent (G1) + parsed; Week-0 baseline captured; access
  provisioning checklist; DPA if regulated; kickoff scheduled; folders + vault + tracker
  records created.
- **Done when:** contract · access · baseline · kickoff. **Blocks S8–S12.**

### S8 — Data Foundation
- **Outputs:** dedicated Supabase project (Supabase MCP; see infrastructure.md) from base
  schema; sources connected; RLS + PII classification + security baseline green.

### S9 — Flagship App
- **Skills:** senior-frontend/fullstack, frontend-design, `{client}-brand`
- **Outputs:** production Next.js app (auth, roles, charts, action surfaces) on Vercel;
  demo simulation swapped for real connectors (**the paid bridge**). Depends: S8.

### S10 — Agent Plane
- **Outputs:** control plane (Railway langgraph + agent inbox, x-api-key); 4 starter
  specialists with memory schema, tools, approval gates on write/spend/send; audit logging.
  Depends: S8; integrates S9.

### S11 — Training & Curriculum
- **Outputs:** 8 curriculum modules delivered; consider the in-product AI Academy pattern
  (curriculum + AI Coach + progress tracking inside the flagship app — proven at SF);
  Power-User Scorecard pre/post. Runs alongside S9–S10.

### S12 — Graduation & Retention
- **Outputs:** handoff pack (architecture, schema docs, agent/tool reference, runbooks,
  kill-switch); case study + testimonial; retainer proposal; **run-log entry + skill diffs**
  (SKILL.md Step 5).

---

## Dependency graph

```
S1 ──► S2 ──► S3a ──► S3b/c/d/e ──► S3f ──► S3g ──► S3h ──► S4 (S3h ──► S3i) ──► [G1/G2: PITCH] ──► S6
 │      └────────────────────────────────────────────────────►S4
 └────► S5 (parallel) ──────────────────────────────► [G2] ──► [SIGNATURE]
[SIGNATURE] ──► S7 ──► S8 ──► S9 ──► S12
                        └───► S10 ──► S12
                 S7 ──► S11 ─────────► S12
```

---

## Linear mapping

Create the structure via the Linear MCP before dispatching S1. If the MCP isn't
authenticated, tell bang once (claude.ai connector settings), then mirror the same structure
in `RUN_TRACKER.md` + the local task list and keep moving.

- **Team:** WaiveLabs (or bang's default team — `list_teams` and pick).
- **Project:** `"{Client} — Client Build"`. Description: one-line thesis + manifest path +
  demo URL once live. Status updates at each phase transition (`save_status_update`).
- **Milestones:** `P1 Recon` · `P2 Position` · `P3 Demo` · `P4 Pitch` · `P5 Close` (+
  `P6 Discovery` · `P7 Build` · `P8 Graduate` post-signature).
- **Issues:** one per slice, titled `S3c — Flagship surface`, description = slice brief +
  done-when + output paths. Set blocking relations per the dependency graph. Labels:
  `phase:P3`, `client:{slug}`, plus `commercial` for anything touching figures.
- **Gate issues (assigned to bang, label `gate`):**
  - `G2 — Approve pricing tiers` (blocks S4 finalization)
  - `G2 — Approve legal set` (blocks signature staging)
  - `G1 — Send: proposal` · `G1 — Send: pitch/demo access` · `G1 — Send: follow-up #n`
  These are the ONLY issues requiring a human. Everything else the agents move themselves.
- **Agent hygiene:** move your issue to In Progress when you start, attach output paths in a
  comment when done, mark Done only when the exit artifact verifiably exists.
