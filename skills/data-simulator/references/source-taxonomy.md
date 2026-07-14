# Source Taxonomy — what data a company generates, by business model

Use this checklist in Phase 1 so no source category gets missed. The dossier names specific vendors; this list catches the categories a dossier might gloss over. For each category: identify the brand's actual vendor if known, else the category-default as `assumed: true`.

## Universal (every brand)

| category | what it holds | common vendors |
|---|---|---|
| web analytics | sessions, traffic sources, conversion | GA4 (default assume), Adobe |
| paid media | campaign spend/attribution per platform | Meta, Google, TikTok, Pinterest, Snap |
| ESP (email) | campaigns, flows, list growth | Klaviyo, Braze, Iterable, Mailchimp |
| SMS | campaign performance | Attentive, Postscript |
| internal docs | plan-vs-actual, budget trackers, calendars | XLSX/Sheets (always exists) |
| support/CX | tickets, CSAT, contact reasons | Kustomer, Gorgias, Zendesk |
| reviews/UGC | ratings, review text | Yotpo, Okendo, Bazaarvoice |

## DTC / consumer brand

| category | what it holds | common vendors |
|---|---|---|
| commerce platform | orders, sales-over-time (the DTC ledger) | Shopify (Plus), BigCommerce, Salesforce CC |
| marketplace | ordered sales, traffic, ads, settlements | Amazon Seller/Vendor Central + Amazon Ads |
| social commerce | GMV, LIVE/video/card split | TikTok Shop |
| retail portals | sell-through by door, bestseller ranks, retail media | Sephora, Ulta, Target Partners Online, Walmart Luminate |
| affiliate/creator | creator performance, commissions | LTK, ShopMy, Impact, CreatorIQ |
| third-party panels | modeled sales estimates (±error BY DESIGN) | Stackline, YipitData, Circana, FastMoss |
| loyalty/retention | members, redemption, cohorts | Yotpo Loyalty, Rivo, Smile |
| returns | RMA, reasons, refund value | Redo, Loop, Happy Returns |
| social listening/SoV | mentions, sentiment, share-of-voice | Dash Hudson, Tribe Dynamics, Tubular |
| AI visibility | LLM share-of-voice, citation tracking | emerging category — simulate weekly SoV vs competitor set (strong WaiveLabs pitch angle) |
| 3PL/ops | inventory snapshots, fulfillment SLA | ShipBob, NetSuite WMS, internal DCs |

## SaaS / B2B software

product analytics (Amplitude/Mixpanel/PostHog), CRM pipeline (Salesforce/HubSpot), billing & MRR (Stripe/Chargebee), marketing automation (HubSpot/Marketo), ads (Google/LinkedIn), support (Zendesk/Intercom), data warehouse exports, NPS. Ledger = MRR movements (new/expansion/contraction/churn) instead of daily net sales; cohorts = logo retention + NRR.

## B2B services / agency

CRM pipeline, time-tracking/utilization (Harvest/Kantata), invoicing (QuickBooks/Xero), project delivery (Asana/Jira/Linear), payroll cost. Ledger = billed revenue by client × month; the "channel mix" analogue = service line mix.

## Marketplace / platform

GMV ledger (buyer side), take-rate revenue, supply-side metrics (listings, sellers, fill rate), payments (Stripe Connect), trust/safety. Two-sided cohorts.

## Notes

- **The ledger concept adapts, the architecture doesn't.** Pick the business model's canonical value stream (daily net sales, MRR movements, billed hours, GMV), make it the ledger, and derive every source view from it with the distortion model.
- **Panels and scrapers exist for most consumer categories** — include at least one estimate-grade source per consumer brand; the "panel vs actual" gap is a reliable demo lesson.
- **Always include internal XLSX docs.** Every company has them; they make unstructured-ingest demos honest and they're cheap to generate.
- When the brand runs something unusual (e.g., a live UCP/MCP agent-commerce endpoint, a custom subscription engine, an in-house app), simulate its data too — the unusual source is often the pitch's sharpest hook.
