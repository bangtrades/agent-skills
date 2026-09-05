---
name: waive-proposal
description: Use when drafting a WaiveLabs client proposal, scope of work, or RFP response with requirements, plan, timeline, and commercial terms. Pair with brand-waive and the current approved client context; verify unresolved brand variants before output.
version: 0.2.0
---

# WaiveLabs Proposal

Turn a client's requirements into a **lean, branded vendor proposal PDF** that an executive and an
IT reviewer can both say yes to quickly. This skill encodes the WaiveLabs proposal house style,
the section structure, the commercial patterns, and a working ReportLab build system.

> [!tip] The one rule that matters most
> **Lean wins.** Executives want: the requirements, our plan to meet them, the timeline, and the
> cost. They do not want explainer paragraphs, "how to read this" boxes, or redundant quote
> callouts. If a sentence isn't a requirement, a plan, a date, or a number, question it. The
> proven SF proposal went from 16 pages of governance prose to **6 pages** — and the 6-page
> version is the one that got sent.

## House style — non-negotiables

- **Structure = Requirements → Plan → Timeline → Cost.** Everything else is supporting.
- **No callout/quote boxes, no cover subtitle paragraph, no footer tagline.** (The `callout()`
  helper exists but default to NOT using it — see anti-patterns in the playbook.)
- **Scope & ownership up front.** State plainly what WaiveLabs owns vs. what the client / client
  IT owns. Ambiguity here is the #1 way an IT reviewer stalls a deal.
- **Tables over prose.** Coverage maps, capability plans, timelines, and commercials are tables.
- **Honesty as a feature.** Name exceptions and dependencies up front (e.g., "this needs client
  data access first," "this component runs outside their platform"). Reviewers trust it.
- **Recommendations vs. fact.** Anywhere AI output is described, commit that recommendations are
  labeled and never presented as validated fact.
- **WaiveLabs method, shown not told.** Prototype → agree spec → build from zero in the client's
  environment. Let the scope/ownership split carry this; don't write a meta-section about it.
- **Brand:** read `brand-waive` and the current approved project brand source. This package previously used `#317FF5` and "Ride the Waive." while the registry brand guide carries `#3179F5` and "Ride the AI wave." Treat the discrepancy as unresolved until dated operator/project authority establishes the variant. Do not silently mix variants; inspect renderer constants and the final artifact.

## Workflow

1. **Gather inputs.** The client's requirements/RFP document (read it fully — every required
   deliverable, every capability, every governance rule, every production-readiness gate), the
   client name, and any accompanying demo (see `waivelabs-secure-demo`).
2. **Confirm scope & commercials with the user BEFORE drafting** (these change the whole doc):
   - What does WaiveLabs own vs. the client / client IT? (e.g., app + AI agents vs. data platform)
   - Resource model + whether personnel are disclosed.
   - Rate, monthly hours, term, and payment schedule (deposit? milestone billing? closure payment?).
   Use AskUserQuestion if any are unclear. Confirm any non-obvious commercial wording before writing it.
3. **Draft to the canonical structure** in `references/proposal-playbook.md`. Lean prose; tables.
4. **Build the branded PDF** with the bundled system — see `references/build-system.md`. Bump the
   draft version on the cover each iteration (V0.1 → V0.2 …).
5. **Verify**: extract the PDF text, confirm page count is tight, the cover/version/slogan are
   right, commercials read correctly, and no stray explainer boxes crept in.
6. **Iterate** with the user. Keep cutting; never add bulk.
7. **Log to the vault** (use the `obsidian` skill: a session note under the client's project +
   a `log.md` entry) and **run the self-improvement step below.**

## Build system (bundled, self-contained)

- `templates/wlstyle.py` — the WaiveLabs ReportLab design system (fonts, palette, cover,
  header/footer, and helpers: `section`, `data_table`, `field_table`, `bullets`, `callout`).
  Per-engagement cover/header text is in the `CLIENT` + `COVER` config, overridden by the build
  script.
- `templates/build_proposal_template.py` — a runnable **worked example** (the SF v0.4 proposal).
  Copy it, edit the CONFIG block + section content, run.
- `assets/fonts/` — Sora, Inter (+ Montserrat/Jost spares) and `wl-logo-clean.png`.

Quick build (see `references/build-system.md` for detail):
```bash
mkdir -p /tmp/fonts && cp assets/fonts/* /tmp/fonts/      # wlstyle expects /tmp/fonts
cp templates/wlstyle.py templates/build_proposal_template.py /build-dir/
cd /build-dir && python3 build_proposal_template.py        # edit CONFIG + OUT first
```
Use an isolated environment or the runtime’s bundled reportlab/pypdf dependencies.

## References
- `references/proposal-playbook.md` — the canonical lean section structure, what each section
  holds, voice rules, and anti-patterns (what to cut).
- `references/build-system.md` — how to run/extend the ReportLab build; helper API; gotchas.
- `IMPROVEMENTS.md` — the running log of lessons; read it before drafting.

## Reference engagement
First use: **Summer Fridays** — "AI Growth Desk" vendor proposal, sent 2026-06-16. v0.4, 6pp.
Scope: WaiveLabs owns the AI Growth Desk (dashboards + agents); client IT owns the Microsoft
Fabric data platform. 60 hrs/mo @ $350; $63k over a 3-month initial term with a deposit +
closure schedule. Source: `~/Projects/Summer Fridays/outputs/proposal_build/`.

---

## Self-improvement protocol

Capture only reusable, evidence-backed lessons from the proposal. Stage changes to `IMPROVEMENTS.md`, the playbook, or the skill under `cortana-vault/_inbox/skills/waive-proposal/`, preserving other staged edits. Record source evidence and the proposed rule. Installed-package writability does not authorize editing it; the operator publishes reviewed changes. Keep old evidence through version history or reversible archival rather than deletion.

## Changelog

- 2026-09-05: Expose tagline/palette discrepancy; resolve from dated approved brand evidence before rendering.
