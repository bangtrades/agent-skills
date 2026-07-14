---
name: waive-proposal
description: Produce a WaiveLabs client vendor proposal — a lean, branded PDF that maps a client's requirements to WaiveLabs' plan, timeline, and cost. Trigger aggressively whenever the user asks to draft, write, revise, or iterate a client/vendor/engagement proposal, respond to an RFP or "vendor requirements" document, scope a client engagement with commercial terms, or build a branded WaiveLabs proposal PDF. Also trigger on "proposal for <client>", "respond to their RFP", "put together a SOW/proposal", "make the WaiveLabs proposal", or a client requirements PDF handed over with intent to bid. Produces a branded PDF via the bundled ReportLab build system (Sora/Inter, Ocean-Blue/Sunset-Orange, "Ride the Waive."). Pairs with the client's brand skill (for any client-styled collateral) and with waivelabs-secure-demo (the demo that accompanies a proposal). Self-improving — appends a lesson to IMPROVEMENTS.md after every run. Do NOT use for non-WaiveLabs documents or for the demo build itself (that is waivelabs-secure-demo).
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
- **Brand:** Sora headings, Inter body, Ocean Blue `#317FF5` + Sunset Orange `#E65100`, slogan
  **"Ride the Waive."** (never "Ride the AI wave").

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
`pip install reportlab pypdf --break-system-packages` if needed.

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

## Self-improvement protocol (run at the END of every use)

This skill is meant to get better with each proposal. After delivering (or iterating) a proposal:

1. **Reflect** on this run: What did the client/user push back on? What did you cut and why? What
   wording landed? What was missing from the playbook or build system? Any new commercial pattern?
2. **Append a dated entry to `IMPROVEMENTS.md`** (newest first) with: the engagement, what changed
   or was learned, and the concrete rule to apply next time. Keep entries short and actionable.
3. **Promote durable lessons** into the body: if a lesson will apply to every future proposal,
   edit `references/proposal-playbook.md` (or this SKILL.md) so it becomes default behavior — don't
   leave it buried in the log. Conversely, **delete or cut** any guidance a run proved wrong.
4. **Keep the skill lean too.** If the playbook is bloating, trim it. The skill should practice
   what it preaches. Note any structural change in the IMPROVEMENTS entry.

> [!warning] When this skill's source is a read-only cache
> If you're running where the installed skill is read-only, write the IMPROVEMENTS entry into the
> working copy and tell the user to fold it back into the source skill (Settings → Capabilities or
> their skill repo). Never silently drop a lesson.
