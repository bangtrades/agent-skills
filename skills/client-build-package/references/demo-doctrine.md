# Demo Doctrine — astonishing demos, fast

Demos closed or advanced every engagement that had one. Target: **concept → gated live demo
in ≤7 days** (SF benchmark: 10 days; Varian shipped with 3 parallel agents; compress as
models improve).

## The ten principles

1. **A decision system, not a dashboard.** Every surface answers "what should I do?" Agents
   visibly **detect → explain → recommend**, with human approval gates on screen. Dashboards
   inform; decision systems astonish.
2. **Make the agents visible.** Live event stream of agent actions, an agent-fleet roster,
   KPI cards that move. Agentic AI is abstract until an exec watches agents work.
3. **Brand-authentic or nothing.** UI renders through `{client}-brand`. The demo should look
   like the client's own internal innovation team built it.
4. **Synthetic but calibrated.** Never real client data pre-contract. Seed the simulation to
   their public reality (SF: ±0.1% of the modeled run rate and exact channel mix). Believable
   numbers are what make execs lean in. Method: `data-simulation.md`.
5. **One shared simulation engine.** A single state/event engine drives all surfaces — a
   coherent world, and the contract parallel agents build against.
6. **One flagship "wow" surface.** Something the client has never seen a vendor do (Hospital
   Digital Twin; SF's 11-source Daily Flash auto-assemble). Everything else supports it.
7. **Answer the #1 objection visually.** Find the blocking fear in the dossier and build its
   answer into the demo (Varian feared data sovereignty → PHI-local GPU console on screen;
   SF governance → approval queues on every agent action).
8. **Depth via drilldowns.** Click-to-inspect everywhere (SF: 54 drilldown targets). The
   presenter can follow the exec's curiosity anywhere — that's what makes it feel real.
9. **Cinematic entry.** The landing moment sets the credibility budget in five seconds
   (dark command-center aesthetic, motion, typography per epic-design/frontend-design).
10. **Gated, watermarked, revocable.** Deploy via waivelabs-secure-demo to
    `{client}.waivelabs.ai`: per-person codes, identity watermark, instant revoke.
    URL-obscurity is not a strategy.

## The build recipe (agent-parallel — maps to slices S3a–S3h)

- **Day 0 — Spec (from S2):** surface list, flagship, objection-answer, calibration targets,
  brand tokens. One page.
- **Day 1 — S3a Skeleton:** simulation engine (entities, event stream, KPI state) + app
  shell (Next.js 14+, theme from `{client}-brand`) + routing for all surfaces.
- **Days 2–5 — S3b–S3e parallel surface builds:** one coding agent per surface. Every demo
  ships an **approval queue and audit ledger** — governance surfaces are part of the wow.
- **Day 5 — S3f integration + calibration:** one agent reconciles all surfaces against the
  sim engine; verify seeded numbers against the dossier.
- **Day 6 — S3g wrap + gate:** secure-demo gate, watermark, codes staged (issuing = G1).
- **Day 7 — S3h QA + capture:** click every drilldown; screenshot every surface into
  `demo/deck-qa/`; rehearse the 10-minute path: *landing → command center → flagship →
  objection-answer → approval/audit → the ask.*

## Two demo modes (from the SF build)

- **Static-first (fastest to wow):** vanilla HTML/JS single-page app with rich modules —
  demo runs anywhere, zero build step. Wrap in Next.js for the gated deploy afterward
  (`public/desk.html` byte-identical + watermark injection). This is the SF pattern.
- **Next.js-native:** when the demo will become the production app shell (enterprise).

**Live-agent option:** a local broker (`server.mjs` pattern, SF `agent/` folder) that holds
the model credential server-side so no key reaches the browser — MOCK mode as stage
insurance, real model via API key. Pitch it as "the governance layer, live." Every action
human-gated: agent proposes, human approves.

**Static-first QA recipe (proven):** run the demo from a trivial local HTTP server (browser
extensions cannot navigate file:// URLs), then: (1) syntax-check every module; (2) jsdom/stub
smoke — render every tab and exercise the approval/state flow; (3) headless-browser pass —
screenshot every surface into `demo/deck-qa/`, assert zero console errors; (4) the
orchestrator personally views flagship + landing screenshots for brand fidelity. On arm64
sandboxes without root: playwright chromium + PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=true,
extracting any missing system libs via `apt-get download <pkg> && dpkg -x` onto
LD_LIBRARY_PATH (x86-64 serverless-chromium builds do not run on arm). Sandbox stages must
each finish inside the shell's execution cap — background processes do not survive between
calls; sequence stages through files on disk.

## Ship checklist (all must pass before S3 is done)

- [ ] Renders through `{client}-brand`; zero default-Tailwind-slop surfaces
- [ ] Agents visibly act (event stream + fleet + recommendations w/ approval gates)
- [ ] Numbers calibrated to dossier; no lorem-ipsum data anywhere
- [ ] Flagship surface demo-able in <90 seconds
- [ ] #1 objection answered on-screen
- [ ] Every KPI/entity click-to-inspects
- [ ] Approval queue + audit ledger present
- [ ] Gated + watermarked + revocable; codes staged per named viewer
- [ ] QA screenshots archived to `demo/deck-qa/`
- [ ] 10-minute demo path rehearsed; nothing 404s off it
- [ ] `DEMO_SCRIPT.md` written: timed beats, talking points, honest framing lines

## The demo script

Always write `DEMO_SCRIPT.md` (SF reference: ~12 min, 7 timed beats). Include honest talking
points verbatim: data is synthetic and calibrated; actions route through approval queues;
external writes stay gated until data-rights clearance. The script feeds bang's live
delivery AND the deck's demo-walkthrough slides.

## Honesty rule

The demo is a synthetic proof of concept and is framed as such. The bridge to the client's
real stack is a scoped, paid SOW line item. Never let a prospect believe the demo is wired
to their systems. If the client mandates a specific platform (SF: Microsoft Fabric), frame
the demo explicitly as a *vision prototype* and map each demo screen to the required
platform capability in the proposal — the stack mismatch must be addressed in writing, not
discovered by their IT team.
