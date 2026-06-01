# Source Catalog — Living Document

This is the canonical map of which sources to hit for which kind of intel. It is **updated by every investigation** via the self-improvement closeout (Phase 14).

The format is intentionally simple so the playbook can grow without becoming brittle.

## How to read this catalog

Each source has three properties that determine how to access it:

| Tag | Meaning |
|---|---|
| `firecrawl` | Reliably scrapable via firecrawl_scrape. Default to this. |
| `firecrawl-flaky` | Sometimes works, sometimes 403/blocked — retry with `proxy: "stealth"` or fall through. |
| `chrome` | Firecrawl blocked. Use Claude in Chrome MCP. |
| `search-only` | Only accessible via WebSearch summarization (no direct scrape). |
| `paywall` | Public shell only — capture what's visible, don't break paywalls. |

Each source also gets a `yield` rating set per-run by Phase 14:

| Yield | Meaning |
|---|---|
| `high` | Returns useful, unique intel in most investigations |
| `medium` | Sometimes useful, often duplicative |
| `low` | Rarely worth the round-trip |
| `noisy` | Returns data but mostly junk (template results, paid placement) |

---

## Phase 1 — Visual identity + URL discovery

| Source | Access | Yield | Notes |
|---|---|---|---|
| `{primary_url}` (homepage) | firecrawl | high | Always start here — `formats: ["markdown", "branding", "links"]` is the single most valuable call in the entire investigation |
| `{primary_url}/sitemap.xml` | firecrawl | medium | Use if firecrawl_map yields <50 URLs |
| Direct `firecrawl_map` of domain | firecrawl | high | Best path to URL inventory |

---

## Phase 2 — Critical pages

| Source | Access | Yield | Notes |
|---|---|---|---|
| `{domain}/pages/about-us` or `/about` or `/about-us` or `/our-story` | firecrawl | high | Voice + ownership + founder narrative |
| `{domain}/pages/faq` or `/faq` or `/help` | firecrawl | high | Voice + claim discipline + product policies |
| `{domain}/pages/contact` or `/press` | firecrawl | medium | Contact details + press kit if available |
| `{domain}/pages/education` or `/learn` | firecrawl | medium | Education content tells you about authority play |
| `{domain}/agents.md` | firecrawl | high if exists | Rare AI-readiness signal — always try, often 404s |
| `{domain}/llms.txt` | firecrawl | medium if exists | Newer AI-readiness signal — always try |
| `{domain}/.well-known/ucp` | firecrawl | high if exists | Universal Commerce Protocol — major signal |

---

## Phase 3 — Press releases & news

| Source | Access | Yield | Notes |
|---|---|---|---|
| openpr.com | firecrawl | high | Cleanest scrape, often has CopperJoint-style press history with archive of ABNewswire-syndicated releases |
| prnewswire.com | firecrawl | high | Major brand releases, usually accessible |
| businesswire.com | firecrawl | high | Same tier as PRNewswire |
| globenewswire.com | firecrawl | medium | Smaller volume |
| markets.financialcontent.com | firecrawl | medium | Syndication, often duplicates openPR |
| TechCrunch / The Information / Axios | firecrawl-flaky | high if found | Often paywalled but bylines are free |
| Local business journals (TBJ, BIJ, etc.) | firecrawl-flaky | medium | Sometimes paywalled |
| Founder/CEO interviews on podcast/YouTube | search-only | medium | WebSearch can surface; for actual content, use yt skill |

---

## Phase 4 — Company profile sources

| Source | Access | Yield | Notes |
|---|---|---|---|
| Crunchbase | paywall | medium | Public profile shell visible — funding rounds, founder, basic firmographics |
| ZoomInfo | paywall | medium | Public profile shell — employee count and revenue band |
| RocketReach | paywall | medium | Often has an estimated revenue and employee count |
| Owler | paywall | low | Mostly behind paywall, low yield |
| D&B (Dun & Bradstreet) | paywall | medium | Useful for corporate hierarchy |
| OpenCorporates | firecrawl | medium | LLC registration filings, jurisdiction |
| State SoS (WY, DE, etc.) | firecrawl | high if registered there | Direct registration filings — definitive on legal entity |
| LinkedIn company page | chrome | high | Real employee count, headcount trend, recent hires |
| LinkedIn People search | chrome | medium | Useful for surfacing named team members |
| SEC EDGAR | firecrawl | high if public | Definitive financial data for public entities |
| PitchBook | paywall | low | Almost always paywalled |
| AngelList / Wellfound | firecrawl | low | Useful for very early startups only |

---

## Phase 5 — Financial signals

| Source | Access | Yield | Notes |
|---|---|---|---|
| Amazon Storefront (`amazon.com/stores/{Brand}`) | firecrawl | high | Pulls ASIN-level data, ratings, review counts; rendered text often verbose but parseable |
| Specific Amazon product page (`/dp/{ASIN}`) | firecrawl | high | Review count, rating, A+ content copy, BSR sometimes visible |
| Keepa (BSR history) | search-only | medium | Free data is limited; subscription needed for deep history |
| Helium 10 / Jungle Scout dashboards | search-only | low | Subscription-gated |
| Glassdoor company page | firecrawl-flaky | medium | Employee count + culture signals + sometimes salary band |
| App Store listing | firecrawl-flaky | medium | Rating + review count + recent reviews |
| Google Play listing | firecrawl | medium | Similar to App Store |
| SimilarWeb (free tier) | search-only | medium | Traffic estimate, channel mix — often surfaced via WebSearch |
| Semrush / Ahrefs (free results) | search-only | medium | Keyword reach estimate via WebSearch surfacing |

---

## Phase 6 — Customer sentiment

| Source | Access | Yield | Notes |
|---|---|---|---|
| Trustpilot | firecrawl | high | Best aggregator of consumer reviews |
| BBB (Better Business Bureau) | firecrawl | medium | Complaints + accreditation status |
| ConsumerReports.org | firecrawl | medium | Editorial reviews (paywall on full reviews) |
| Reddit (`site:reddit.com {Entity}`) | firecrawl | high | Highest-signal customer voice — quote directly |
| CusRev | firecrawl | medium | Aggregates retailer reviews |
| Sitejabber | firecrawl | medium | Similar to Trustpilot, smaller scale |
| PissedConsumer | firecrawl | medium | Skewed negative — useful for failure-mode analysis |
| HighYa | firecrawl | low | Older, lower-signal |
| Wirecutter / NYT Recommends | firecrawl | high if mentioned | Editorial recommendation has SEO and trust weight |
| App Store + Google Play reviews | firecrawl | high | Mobile-only entities |
| Capterra / G2 / TrustRadius | firecrawl | high | SaaS entities |

---

## Phase 7 — Competitive landscape

| Source | Access | Yield | Notes |
|---|---|---|---|
| Comparison articles ("X vs Y vs Z") | search-only | high | WebSearch surfaces these well |
| Review aggregators ("best {category} 2026") | search-only | medium | Often SEO-optimized listicles |
| G2 / Capterra comparison views | firecrawl | high | SaaS |
| Crunchbase competitor sections | paywall | medium | Public shell shows top 5 |
| Direct competitor brand-recon dossiers in this vault | firecrawl | high if exists | Cross-link to existing dossiers |

---

## Phase 8 — Marketplace footprint

(Covered above — Amazon, G2, Capterra, App Store, Clutch, etc.)

---

## Phase 9 — Social media

| Platform | Access | Yield | Notes |
|---|---|---|---|
| **Facebook** | chrome | high via chrome / low via search-only | Firecrawl always blocked. Live follower count needs Chrome. WebSearch often surfaces approximate follower band. |
| **Instagram** | chrome | high via chrome / low via search-only | Firecrawl always blocked. Same fallback as FB. |
| **Pinterest** | chrome | high via chrome / low via search-only | Firecrawl always blocked. Often under-leveraged for wellness/health/home brands. |
| **TikTok** | firecrawl-flaky | medium | Sometimes works, often blocked. Chrome reliable. |
| **LinkedIn company page** | chrome | high | Firecrawl mostly blocked. Real employee count + activity cadence. |
| **YouTube channel** | firecrawl-flaky | medium | Often works. Combine with the yt skill for individual videos. |
| **X / Twitter** | firecrawl-flaky | low | Mostly blocked post-API-changes. Use Chrome. |
| **Threads** | chrome | medium | Meta property, blocked by firecrawl. |
| **Bluesky** | firecrawl | medium | Open protocol, usually works. |
| **Substack** | firecrawl | high if exists | Newsletter content is gold for brand voice |

---

## Phase 10 — People (founders, executives, advisors)

| Source | Access | Yield | Notes |
|---|---|---|---|
| LinkedIn personal profiles | chrome | high | Career history, role, current title — Chrome required |
| Personal websites (`{name}MD.com`, `{name}.io`) | firecrawl | high | Direct credentials + publications |
| US News Doctors profile | firecrawl | high for medical advisors | Verified credentials, board certs |
| Doximity | firecrawl | medium for physicians | Public profile available |
| Google Scholar | firecrawl | high for scientists | Citations, h-index, publication list |
| YouTube channels | search-only / yt skill | high if exists | Often the most authentic voice sample |
| Podcast appearances | search-only | medium | WebSearch surfaces; use yt skill for substantive ones |
| Personal Twitter/X | chrome | medium | Live activity signal |
| Wikipedia | firecrawl | medium | Validates major figures, low-signal for everyone else |

---

## Phase 11 — AI/tech posture

| Source | Access | Yield | Notes |
|---|---|---|---|
| `{domain}/agents.md` | firecrawl | very high if exists | The single most important AI-readiness signal of 2026 |
| `{domain}/llms.txt` | firecrawl | high if exists | Anthropic-promoted standard |
| `{domain}/.well-known/ucp` | firecrawl | very high if exists | Universal Commerce Protocol — built for agent commerce |
| `{domain}/robots.txt` | firecrawl | low (but cheap) | Sometimes reveals API hints |
| `{domain}/sitemap.xml` | firecrawl | medium | Quantifies content footprint |
| BuiltWith profile | search-only | medium | Public tier shows tech stack |
| Wappalyzer browser data | search-only | medium | Similar to BuiltWith |
| Page source inspection via firecrawl | firecrawl | high | Read the homepage source for Klaviyo / Recharge / Smile.io / Judge.me / Intercom signatures |

---

## Live source-quality entries (auto-updated)

> The self-improvement closeout appends entries below this line. The format is:
>
> `YYYY-MM-DD — {entity-slug} — {source-url} — access:{firecrawl|chrome|search|paywall} — yield:{high|medium|low|blocked} — notes:{short text}`

<!-- BEGIN AUTO-APPENDED ENTRIES -->

2026-05-27 — copperjoint — copperjoint.com homepage — access:firecrawl — yield:high — notes:branding format returned complete token set in one call (ink/copper/gold/chalk + Montserrat + Epilogue + component radii + button styles)

2026-05-27 — copperjoint — copperjoint.com/agents.md — access:firecrawl — yield:high — notes:exposes UCP + MCP endpoint, major AI-posture signal — confirm this probe is part of every Phase 11

2026-05-27 — copperjoint — facebook.com/copperjoint — access:firecrawl — yield:blocked — notes:firecrawl returns "we do not support this site" — escalate to Chrome MCP next time

2026-05-27 — copperjoint — instagram.com/officialcopperjoint — access:firecrawl — yield:blocked — notes:same as Facebook — Chrome MCP required

2026-05-27 — copperjoint — pinterest.com/copperjoint — access:firecrawl — yield:blocked — notes:same — Chrome MCP required

2026-05-27 — copperjoint — openpr.com — access:firecrawl — yield:high — notes:six press releases between Sept 2025 and Jan 2026 — also surfaces sibling press in the "More Releases for X" panel — scrape ONE release and harvest the sibling panel for free

2026-05-27 — copperjoint — amazon.com/stores/{Brand} — access:firecrawl — yield:high — notes:returns A+ content copy and individual product carousels including ratings and review counts — verbose but parseable

2026-05-27 — copperjoint — zoominfo.com/c/{slug} — access:paywall — yield:low — notes:public shell shows only company name and basic address — no revenue or employee data visible

2026-05-27 — copperjoint — rocketreach.co/{profile} — access:paywall — yield:medium — notes:surfaced via WebSearch and gave revenue estimate ($1M) and HQ — number was likely understated for the entity but useful as a floor

2026-05-27 — copperjoint — Reddit search via firecrawl_search — access:firecrawl — yield:low — notes:no Reddit results surfaced for this entity — small brand, low Reddit presence — try direct WebSearch with site:reddit.com if firecrawl_search returns empty

2026-05-27 — copperjoint — usnews health/doctors — access:firecrawl — yield:high — notes:validates physician credentials cleanly — use for any medical-advisor entity

<!-- END AUTO-APPENDED ENTRIES -->
