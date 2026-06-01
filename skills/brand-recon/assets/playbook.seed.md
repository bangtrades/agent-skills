# brand-recon Playbook

Lessons accumulated across every investigation. Append-only.

**Total runs:** 1
**Last run:** 2026-05-27 (copperjoint)

---

## How to use this file

- Read top-to-bottom before each new run to inherit prior lessons
- Skim the most recent 3 entries for blocked-source updates
- Search by entity-slug or category for prior comparable runs

---

## 2026-05-27 — copperjoint (BOOTSTRAP)

**Entity:** CopperJoint, LLC (https://www.copperjoint.com)
**Run length:** ~20 minutes
**Phases completed:** 14/15 (no schedule step)

### What worked unusually well
- The firecrawl `branding` format on the homepage returns a COMPLETE design system in ONE call (colors, fonts, button styles, logo URL, even inferred design framework). This is the single highest-leverage call in the entire investigation. Always run it first.
- openPR is gold for press release histories — scraping one release also surfaces a "More Releases for X" panel with the full press timeline at the bottom of the page. One scrape = many releases captured for free.
- The `/agents.md` probe (cost: one cheap firecrawl call) revealed CopperJoint is implementing the Universal Commerce Protocol with an MCP endpoint. This single signal changed the strategic narrative from "small DTC needs AI 101" to "AI-native owner, here's what to build on top." Always probe `/agents.md`, `/llms.txt`, and `/.well-known/ucp`.
- The Amazon brand storefront still uses the entity's LEGACY voice (pre-relaunch). The on-site voice has been deliberately upgraded but the marketplace presence hasn't caught up. This brand-coherence-across-channels diagnostic is one of the highest-leverage findings the dossier can surface, and is likely common across recently-relaunched DTC brands.

### What was blocked / low-yield
- Firecrawl is BLOCKED on Facebook, Instagram, and Pinterest. Don't waste calls retrying — escalate to Claude in Chrome MCP immediately. If Chrome isn't connected, fall back to WebSearch for approximate follower bands and document the degraded data quality in the dossier.
- ZoomInfo / RocketReach / Crunchbase public shells gave very little — revenue estimates are wildly off for small DTC brands (RocketReach said $1M when the actual Amazon footprint implies multi-million). Use as a floor, not as truth.
- Firecrawl_search with `site:reddit.com` returned EMPTY for this entity — small brand, low Reddit presence. Fall back to direct WebSearch with site: filter.

### Novel techniques discovered
- The two-stage scrape pattern: `firecrawl_scrape(homepage, formats:[markdown, branding, links])` + `firecrawl_map(domain)` in PARALLEL as the first move. Saves a full round-trip vs. sequential.
- The "press cadence" observation — counting press releases per quarter is a proxy for how aggressively the brand is in a reinvention/relaunch phase. CopperJoint had 6 releases in 4 months, which signaled "active brand transformation" → which set up the entire dossier framing.
- For credentialed advisors (doctors, scientists), check their personal site + US News profile + Doximity to validate credentials independently of the brand's marketing. CopperJoint's Dr. Strasser is a real, board-certified, Vanderbilt-affiliated surgeon — and the dossier said so with confidence because of the independent validation.

### Updates to the source catalog
- Added Meta-blocked status for FB/IG/Pinterest in source-catalog.md
- Added /agents.md, /llms.txt, /.well-known/ucp as standard Phase 11 probes
- Added openPR "More Releases for X" sibling-panel harvest pattern

### Updates to the dossier template
- Section 10 (AI/Tech Posture) should ALWAYS check for and prominently surface agents.md / UCP / MCP signals when present. These are not edge cases anymore in 2026.
- Section 2 (Brand Identity) should include a mandatory "voice drift across channels" diagnostic — almost every entity has SOME coherence gap, and this is one of the most actionable findings.

### Lessons for the next run
- Start every run with the homepage + branding + map parallel call. It anchors everything.
- Probe /agents.md unconditionally — the cost is negligible and the upside is "the entire strategic narrative changes."
- For DTC entities, scrape the Amazon brand store specifically to check for voice drift against the new site.
- Don't waste effort on Meta socials with firecrawl — go straight to Chrome MCP or WebSearch fallback.
