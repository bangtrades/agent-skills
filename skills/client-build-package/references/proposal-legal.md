# Proposal & Legal — from RFP to signed SOW

Everything here is **G2 territory**: no figure is final and nothing is sent (G1) without
bang. Agents draft, generate, redline, and verify; bang approves and signs.

## The lean proposal (RFP response) — use the `waive-proposal` skill

Source of the house style: SF proposal went from 16 pages of governance prose to **6 pages**,
and the 6-page version is the one that got sent.

- **Structure = Requirements → Plan → Timeline → Cost.** Everything else supports.
- **Scope & ownership up front:** what WaiveLabs owns vs. what the client/client IT owns
  (SF: WaiveLabs owns the Growth Desk app + agents; client IT owns the Fabric data
  platform). Ambiguity here is the #1 way an IT reviewer stalls a deal.
- **Tables over prose.** Coverage maps (requirement ↔ our plan, clause-for-clause against
  their RFP), capability plans, timelines, commercials — all tables.
- **Honesty as a feature:** name exceptions and dependencies up front; commit that AI
  recommendations are labeled and never presented as validated fact.
- **No callout boxes, no cover subtitle paragraph, no footer tagline.** Lean wins.
- Build via the bundled ReportLab system (`waive-proposal` skill: `wlstyle.py` +
  template; Sora/Inter, Ocean Blue #317FF5 / Sunset Orange #E65100, "Ride the Waive.").
  Bump the cover version each iteration (V0.1 → V0.2 …). Verify by extracting PDF text.

## Proposal ↔ demo alignment check (do this before G1)

The SF near-miss: proposal committed to the client's mandated platform (Microsoft Fabric);
the demo ran Next.js/Vercel/Supabase/synthetic. Run an explicit gap analysis
(SF reference: `Proposal_Review_and_Demo_Alignment_2026-06-15.md`):

1. Does the proposal mirror the RFP clause-for-clause (every deliverable, capability,
   governance rule, production gate)?
2. Does the demo showcase the capabilities the proposal leads with? (SF's demo was missing
   its two hero capabilities until this check caught it — they were added as new views.)
3. Is the stack mismatch addressed in writing? Frame the demo as a *vision prototype* and
   map each demo screen → required platform capability.
4. Does the agent inventory in the proposal match what the demo shows?
5. Any placeholder claims (security certs!) that must be reconciled to the real posture?

## The 4-doc legal set (WaiveLabs paper — SMB/DTC default)

Generate via `~/Projects/agency/_templates/engagement-docs/` (`gen_proposal.js`,
`gen_legal.js`); executed reference: the CopperJoint set.

Proposal → Engagement Letter → SOW → Services Agreement. Locked stances:
- **Entity:** Jam Sessions, LLC (DE) d/b/a WaiveLabs; CA law; liability capped at fees
  (12-month cap pattern).
- **IP:** client owns their deliverables/data/instance on full payment; **WaiveLabs retains
  the reusable Kit** (skills, templates, generators, patterns).
- **SOW must contain:** milestone schedule; the **demo→production bridge** as an explicit
  paid line item; success metrics + abort criteria agreed before build; client-furnished
  items (LLM API subscriptions, DB, credentials, SME time); payment schedule
  (deposit / monthly / closure pattern, net-15).

## Enterprise paper (their NDA/MSA — redline hard)

NDA screen FIRST, before anything else is exchanged:
- **Kill feedback-clause IP grabs** — clauses that silently assign consulting output via
  "feedback" definitions (caught in the Siemens NDA; it would have assigned the work).
- **Kill "arising from / relating to" IP language** — scope IP assignment to deliverables
  specifically defined in a SOW.
- **Flag personal liability** — SF's NDA bound the founder personally, jointly & severally
  (pierces the LLC shield). If accepted consciously, confirm E&O + Cyber coverage and note
  the exclusions (willful breach, injunctive relief, contractual liability).
- **Approved-tools schedule pattern (SF innovation, reuse it):** attach a Schedule listing
  the AI tools that may process Confidential Information, each with its data posture
  (zero-retention / no-training), approvable by email reply. It converts a vague AI-risk
  conversation into a signable artifact.
- Term sanity: 3-year confidentiality typical; perpetual only for trade secrets/PII/
  credentials.

## Commercial figure discipline

The SF drift: proposal v0.4 said $63,000 ($10.5k/$21k/$21k/$10.5k); the signed SOW said
$60,000 ($10k/$20k/$20k/$10k). Nobody decided that twice — it drifted.

- Figures live in the **client manifest** and nowhere else. Every document build reads them
  from there.
- Any figure change = manifest edit (G2, bang only) + regenerate affected docs + a Linear
  comment on the `commercial` issue noting old → new.
- If the SOW intentionally supersedes proposal commercials, say so in the SOW explicitly.

## Version & folder hygiene

- One authoritative legal folder: `legal/final/` holds exactly the signable/signed set;
  drafts and redlines live in `legal/drafts/`. (SF ended with MSA/, MSA_final/,
  MSA_SOW_final/ + a stray redline — don't repeat it.)
- Keep every proposal version PDF; never overwrite. The version history is the negotiation
  record.

## Follow-up cadence (post-pitch, pre-signature)

+2 days: value-add follow-up (a new insight from the dossier, not "checking in") →
+7 days: second artifact (mini-analysis using their market/data) →
+14 days: direct close ask →
+30 days: park to nurture.
Draft all four at pitch time (S6); each send is a G1.
