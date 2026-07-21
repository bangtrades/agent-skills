---
name: client-build-package
description: >-
  Orchestrate the full WaiveLabs client-build motion — take any brand or company
  from "new prospect showed interest" to "elite gated demo + executive pitch +
  proposal + legal set, ready to present" in one agentic loop, then through
  signature into delivery. Client-agnostic (DTC, enterprise, white-label).
  Creates the Linear project, dispatches research agents (brand-recon → dossier
  + brand skill), parallel demo agents, data-simulation agents, infra agents
  (Supabase, Vercel, gated deploy), and document agents (pitch, proposal, legal)
  — human gates ONLY on client-facing sends and legal/commercial approvals.
  Trigger aggressively on "new client/prospect X", "we signed X", "launch X",
  "run the machine on X", "kick off X", "client-build X", or any company named
  with intent to pitch, demo, close, or onboard. Also for partial
  runs: "build the demo for X", "prep the pitch package", "generate the legal
  docs", "onboard X". SUPERSEDES client-launch. Not for pure research
  (brand-recon) or WaiveLabs-internal product work.
---

# Client Build Package — the WaiveLabs engagement engine

You are running the WaiveLabs client-build motion. One loop, proven across four live
engagements (Varian enterprise, Solugenix partner, Summer Fridays DTC, CopperJoint SMB):

```
P0 Signal → P1 Recon → P2 Position → P3 Demo Sprint → P4 Pitch → P5 Close →
P6 Discovery → P7 Build (Agentic OS) → P8 Deliver/Graduate/Retain
                        ↑______ run-log feedback → this skill improves ______|
```

The variation between clients is parameterization, not process. Your job is to move the
engagement through phases as autonomously as possible, stopping ONLY at the two human gates.

**This skill supersedes `client-launch`.** If you find both installed, use this one.

## The two human gates (everything else is autonomous)

| Gate | What stops | Why |
|---|---|---|
| **G1 — Client-facing** | Nothing is SENT to the client — no email, proposal PDF, pitch deck, demo link, or access code leaves the building — without bang's explicit sign-off. Drafting, building, and deploying are all autonomous; transmission is not. | The SF proposal took 8 versions before final. Bang owns the relationship. |
| **G2 — Legal & commercials** | NDA/MSA/SOW content and ANY pricing number require bang's approval before they are treated as final. Also: bang signs everything; agents sign nothing. | SF drifted $63k (proposal) vs $60k (signed SOW). Figures live in ONE place (the manifest) and only bang changes them. |

Deploys, DNS, database provisioning, demo builds, research, and drafting run autonomously on
standing WaiveLabs infrastructure (Vercel, Supabase `waivelabs`, existing subscriptions).
Net-new recurring spend (a paid capacity, a new SaaS seat) isn't a blocking gate, but file it
as a Linear issue tagged `commercial` so bang sees it — it's a commercial fact.

## Step 0 — Load context

1. Read `references/lifecycle.md` — the P0–P8 spine, exit gates, motion parameterization.
2. Read `references/task-slices.md` — the S1–S12 slice briefs you will dispatch, and the
   Linear mapping.
3. If the run includes a demo: `references/demo-doctrine.md` and `references/data-simulation.md`.
4. If the run includes proposal/legal work: `references/proposal-legal.md`.
5. If deploying or provisioning: `references/infrastructure.md`.
6. If `~/Projects/agency/` exists, also read `~/Projects/agency/MISSION.md` and skim
   `~/Projects/agency/playbook/00-retrospective-2026-07.md` for run-log lessons newer than
   this skill.
7. Load the client's existing material if any: dossier + `{client}-brand` skill (vault or
   `~/Projects/{Client}/research/brand-recon/`). Missing → S1 runs first.

## Step 1 — Intake: create the client manifest

Copy `templates/client-manifest.md` to `~/Projects/{Client}/00_context/client-manifest.md`
(create the folder scaffold: `00_context/ research/ demo/ proposal/ legal/ pitch/ data/`).
Fill what you know; ask bang (AskUserQuestion) ONLY for what you cannot infer:

- **Motion:** Enterprise co-dev · White-label partner · SMB/DTC. This parameterizes
  everything downstream (see lifecycle.md table).
- **Entry phase & scope:** full pre-signature loop (default), post-signature delivery, or
  named slices.
- **Decision-maker:** name + role. Recon will mine their public statements.
- **Product naming:** lock the deliverable's name NOW (SF churned "AI Director" →
  "Agent Director" across duplicate decks). One name, recorded in the manifest.

The manifest is the **single source of truth** for the slug, naming, commercial figures, and
gate status. Every document agent reads figures from it; no agent invents a number.

## Step 2 — Create the Linear project

Set up tracking before dispatching anything (full spec: `references/task-slices.md` §Linear):

- Project **"{Client} — Client Build"** in the WaiveLabs team; description = one-line thesis
  + manifest path.
- Milestones = phases (P1 Recon … P5 Close; add P6–P8 post-signature).
- One issue per slice (S1–S12), titled `S3c — Flagship surface`, labeled by phase, with the
  slice brief pasted into the description and dependencies set as blocking relations.
- Gate issues assigned to bang: `G1 — Approve send: proposal`, `G2 — Approve commercials`,
  etc. These are the only issues a human must touch.

If the Linear MCP is not authenticated, tell bang once (connector settings), then fall back
to the local task list plus a `RUN_TRACKER.md` in the client folder mirroring the same
structure — do not stall the run on tooling.

## Step 3 — Dispatch the slice graph

Launch agents per `references/task-slices.md`, in dependency order, independent slices in
parallel. Every dispatched agent prompt contains: the slice brief verbatim, the client slug +
folder paths, the motion, the manifest path, and the standing rules (below).

**Board leads the work.** Move each slice's Linear issue to **In Progress the moment you start
it — BEFORE the agent runs or the inline build begins**, with a one-line "dispatching" comment.
Never let an issue jump created→Done; the operator watches the board to see what is being worked
*now*. Mark Done only when the exit artifact verifiably exists (Step 4).

**Inline-first for the single-file demo.** The static-first demo (demo-doctrine.md) is one HTML
build whose surfaces share a single token sheet and one chart/UI kit — that is *coupled* work.
Build it **inline and sequentially**, not by fanning out an agent per surface: sibling agents
collide on the shared kit, and mid-turn operator messages kill in-flight subagents. Fan out only
for genuinely file-disjoint work (e.g. the vendor-export estate, the legal doc set). If a
dispatch wave returns dead/junk twice, go inline immediately (orchestration.md → Dispatch
Discipline). This is the biggest wall-clock lever in the whole motion.

The pre-signature default ("full parity" — what Summer Fridays got):

```
S1 Recon+brand skill → S2 Positioning+demo spec → S3a sim engine+shell
  → S3b/c/d/e parallel surfaces → S3f calibration → S3g gated deploy → S3h QA+screenshots
  → S4 pitch package → [G1+G2: bang approves + presents] → S6 follow-up cadence
S5 proposal + legal set runs parallel from S2 → [G2] → [signature]
```

## Step 4 — Enforce exit gates

A phase is done when its exit artifact EXISTS — verify files on disk, deploys via HTTP, Linear
via API. Never accept an agent's claim without the artifact. Verification ladder
(cheapest-sufficient first, stop when the gate's question is answered): syntax/static check →
stub-render or dry-run against the real data contract → real headless browser or live endpoint
(console errors + screenshots) → orchestrator visually inspects at minimum the flagship and
landing screenshots before S3 is called done. Never skip straight to the expensive rung; never
accept the cheap rung as proof of visual/brand quality. Before anything is staged for a
G1 send: rendered through `{client}-brand` + `brand-waive`, numbers match the manifest, and
the honesty rules below hold.

## Step 5 — Retrospective (MANDATORY at every demo-complete AND engagement-close)

**This is a hard trigger, not optional cleanup — the equal of brand-recon's Phase 14.** The
moment the demo passes its ship checklist (and again at engagement close), stop and run a
retrospective before starting anything new. bang's standing instruction: *every completed build
launches a retro and improves the process.* A build that ships without a retro is unfinished.

Produce `~/Projects/{Client}/00_context/RETRO_{date}.md` from `templates/retro-template.md`:

1. **Timeline table** — phase-by-phase wall-clock from hard evidence (Linear
   `startedAt`/`completedAt`, artifact mtimes, commit times), planned vs actual. bang measures
   the run in wall-clock; measure it the same way. To make this cheap, **instrument as you go**:
   stamp each phase's start/end in `RUN_TRACKER.md` (or rely on Linear transitions if the board
   led the work — which, per Step 3, it now does).
2. **What compounded** — the reusable wins to keep/strengthen (evidence-based tie-outs, the vault
   schema-library hits, contract-first, per-checkpoint commits).
3. **What slowed it** — root-caused, with the wall-clock cost of each (dispatch thrash,
   post-hoc calibration tuning, recurring build gotchas). Name the single biggest lever.
4. **Board-discipline self-check** — did every issue move to In Progress *before* its work
   started? List any that jumped created→Done. (Fix the habit, not just the record.)
5. **Skill diffs across EVERY skill the engagement used** — brand-recon, data-simulator,
   client-build-package, orchestration. New patterns in, disproven guidance out. If the installed
   skill is writable, patch it in-session and note it; if read-only, write the diffs to
   `00_context/skill-patches/` with an `INSTALL.md` and tell bang to fold them in.
6. **Run-log entry** — append the dated summary to
   `~/Projects/agency/playbook/00-retrospective-2026-07.md` if it exists, else `RUN_LOG.md`
   beside the manifest.

Open a Linear issue for the retro itself (`Retro — {date} build → skill patches`), moved to
In Progress before you start it — the retro obeys its own board rule. The playbook only compounds
if every run writes back.

## Standing rules (every agent, every slice)

1. **Never contact the client.** Draft everything; send nothing. G1 is bang's.
2. **No real client data pre-contract.** Synthetic-but-calibrated only (data-simulation.md).
3. **Honesty is load-bearing.** The demo is a synthetic prototype and is framed as such; the
   demo→production bridge is a paid SOW line item. Never imply live wiring to client systems.
   Never ship a security/governance doc with placeholder certifications — state the real
   posture. Never claim "nothing leaves the platform" — the honest line is "minimized,
   aggregated slice; no-train / zero-retention."
4. **Secrets discipline.** Tokens never in chat or committed files; use the gitignored
   `.deploy-secrets.local.md` pattern; rotate anything exposed (infrastructure.md).
5. **Brand or nothing.** Client-facing output renders through `{client}-brand`; WaiveLabs
   docs through `brand-waive`. Slogan: **"Ride the Waive."**
6. **Figures come from the manifest.** If a commercial number isn't there, it doesn't exist
   yet — raise a G2 issue.
7. **Missing template? Build it generically first**, then apply it to this client, and note
   it in the run log. The Kit compounds.
8. Close every slice with a 5-line summary: what shipped, where, what surprised you, what
   should change in this skill.
9. **Every dispatched agent gets a budget and an abort clause.** The dispatch prompt states
   a step/effort budget and: "If you hit an authentication wall, a tool capability ceiling
   (payload size, rate limit, unsupported platform/arch), or any G1/G2 boundary — STOP and
   report the exact blocker and what you verified. Do not improvise around it (no encoding
   detours, no web-UI signup/login flows, no alternate upload endpoints)." A precise blocker
   report is a successful agent run; a heroic multi-hour failure is not.
10. **Probe before dispatch.** Before sending any agent across a tool boundary (deploy
    tools, external APIs, browser automation), the orchestrator runs a ≤60-second capability
    probe itself: smallest possible payload through the same tool, auth state check,
    platform/arch check. Only dispatch once the path is proven passable.
11. **One gated surface, no strays.** A demo is not "deployed" until exactly one URL is gated AND every
    earlier/duplicate deploy is neutralized or deleted — verified UNAUTHENTICATED. On Vercel Pro there is
    no production Vercel-auth to hide a leak; the custom gate (or deletion) is the only close. Deploy via
    the Vercel CLI + token (the MCP can't carry a real demo), disable the project's Vercel
    deployment-protection so the gate is the front door, and never ship the operator's WIP branch when
    redeploying a git-connected project.
12. **Board leads work.** Every tracked issue moves to In Progress *before* its work begins and
    Done only on verified artifact — never created→Done. The board is a live picture of what is
    being worked now, not an after-the-fact log.
13. **Retro every build.** Demo-complete and engagement-close each trigger Step 5's mandatory
    retrospective before any new work starts. No exceptions.

## The Kit (reusable assets on bang's machine)

| Asset | Location | Used in |
|---|---|---|
| brand-recon skill | installed | S1 |
| client-pitch skill | installed | S4 |
| waive-proposal skill | `~/Projects/agency/WaiveLabs/skills/waive-proposal/` (bundled ReportLab system) | S5 |
| waivelabs-secure-demo skill | installed / `~/Projects/agency/WaiveLabs/skills/` | S3g |
| brand-waive + {client}-brand skills | installed | all |
| Legal generators (4-doc set) | `~/Projects/agency/_templates/engagement-docs/` (`gen_proposal.js`, `gen_legal.js`) | S5 |
| Deck generator pattern | `~/Projects/HCE/Healthcare Context Engine/deck/build_vail_deck.js` | S4 |
| Data simulation reference | `~/Projects/Summer Fridays/Fabric_Simulation/` (`generate_data.py`, `generate_sources_tier1.py`) | S3, data-simulation.md |
| Intake questionnaire + Phase-0 scorecard | `~/Projects/agency/` | P0, S7 |
| Worked examples | `~/Projects/Summer Fridays/` (DTC), `~/Projects/Varian/`+`~/Projects/HCE/` (enterprise), `~/Projects/Solugenix/` (partner), CopperJoint docs in `~/Projects/agency/` (SMB legal) | all |

If a Kit path is missing in the current environment, the references contain enough detail to
rebuild the asset generically (rule 7).
