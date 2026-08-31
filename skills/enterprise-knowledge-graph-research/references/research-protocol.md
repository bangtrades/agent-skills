# Research and retrieval protocol

Use this protocol for public web research and authorized internal evidence. The research tool is replaceable; provenance, authorization, and claim discipline are not.

## Source priority

Prefer, in order:

1. controlling law, regulator, standard setter, official registry, court, or government data;
2. signed agreement, approved policy, audit evidence, system export, or client-controlled source;
3. organization-authored filings, documentation, product pages, technical docs, and statements;
4. named practitioners describing their own work;
5. independent academic, investigative, or industry evidence;
6. vendor claims and broad secondary summaries for discovery or capability context;
7. inference, clearly labeled and capped at medium confidence.

Priority is claim-specific. A vendor is primary for its API documentation but not for customer adoption or business outcomes.

## Firecrawl routing

When Firecrawl is available and authorized:

| Need | Preferred surface |
|---|---|
| Discover unknown URLs | Search with precise document-language queries |
| Inventory a site | Map before crawling |
| Retrieve a known page | Scrape |
| Extract repeated fields | Scrape with a reusable JSON schema |
| Collect a bounded documentation set | Crawl with path filters, depth, and page caps |
| Parse PDF or office documents | Parse with page limits where appropriate |
| Open-ended multi-source investigation | Asynchronous agent, then poll to terminal state |

Use search results to locate evidence, not as the final evidence when the underlying page is available. Map before crawling. Prefer bounded retrieval over whole-site collection.

## Query design

Search for the language used by the source author:

- exact artifact, filing, policy, job title, system, standard, API, or meeting name;
- organization plus vendor, workflow, role, or document type;
- regulator docket, rule number, form, implementation guide, enforcement action, or audit criterion;
- file types and likely site paths for policies, manuals, developer docs, board packets, and reports.

Run multiple distinct query frames for load-bearing questions. Repeated near-identical queries create false confidence.

## Repeated extraction

For an organization universe or recurring source type:

1. define the extraction schema first;
2. include evidence locator, date/as-of, unit/basis, and missing-value reason;
3. reuse the schema across the population;
4. preserve raw retrieval metadata separately from normalized fields;
5. sample and manually verify extraction quality before scaling.

Do not infer missing values to make a table complete.

## Claim ledger

For every load-bearing claim, preserve:

- claim text or normalized fact;
- supporting and conflicting source IDs;
- source date, retrieval date, and temporal validity;
- evidence class and confidence;
- scope/population and quantitative basis;
- permission, license, sensitivity, and allowed downstream use;
- reviewer disposition and later corrections.

Differentiate these states:

- **capability:** a product or rule permits something;
- **adoption:** the target uses it;
- **implementation:** it is configured and operating;
- **effectiveness:** it produces a measured result;
- **entitlement:** the specific client contract permits access, export, storage, or model use.

Never use one state as evidence for another without explicit support.

## Internal and sensitive sources

- Confirm authorization before retrieval.
- Minimize collection to the research purpose.
- Keep public, internal, confidential, and restricted partitions separate.
- Use opaque source references; do not place credentials or sensitive URLs in notes.
- Record system of record, owner, retention, permitted use, and deletion requirement.
- Do not persist raw regulated content when a source reference and approved derived fact are sufficient.
- Treat interviews as evidence with speaker role, date, scope, consent, and potential bias; do not launder recollection into verified system behavior.

## Failures and stopping conditions

On retrieval failure, retry once with a materially appropriate method or bounded alternative. Then record:

- URL or source reference;
- failure type and date;
- why it matters;
- best authorized alternative;
- owner or permission needed to resolve it.

Stop or escalate on authorization ambiguity, paywall or robots restriction, sensitive-data scope expansion, uncertain redistribution rights, repeated quota failure, or evidence that contradicts the project boundary.

## Evidence quality review

Before synthesis, sample every track and all high-degree hubs. Re-retrieve or independently verify:

- quantitative claims;
- regulatory requirements and effective dates;
- product API, export, authentication, and retention claims;
- named organizational adoption;
- workflow timing, conversion, cost, and outcome claims;
- statements used to justify product ranking or automation.

Record freshness and known source limitations. Current web content cannot prove historical state without archived or dated evidence.
