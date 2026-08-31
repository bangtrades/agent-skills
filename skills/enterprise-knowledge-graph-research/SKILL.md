---
name: enterprise-knowledge-graph-research
description: Build a compiler-enforced, deeply sourced operating knowledge graph for a company, industry, client, or complex domain. Use when the output must ground enterprise product design, client management, regulated workflows, security controls, data architecture, or agent opportunities; do not use for quick market scans or ordinary web research.
---

# Enterprise Knowledge Graph Research

Build an auditable operating model that a product, engineering, security, compliance, or client team can use without repeating the foundational research. The result is not a market map. It reconstructs how the target actually works: actors, workflows, decisions, artifacts, systems, data, metrics, regulations, controls, risks, and buildable opportunities, with every material claim traceable to evidence.

## Invocation contract

Accept a company, industry, organization, ecosystem, or domain as the target. Also use any supplied client files, scope notes, repositories, source systems, or regulatory perimeter.

Before execution, establish and record:

- target and target kind: `company`, `industry`, or `domain`;
- downstream purpose and the decisions or systems the graph must support;
- geography, organization boundary, time horizon, and explicit exclusions;
- deployment lane, users, data classes, and regulated activities;
- authorized sources, tools, repositories, connectors, and write location;
- research depth, time or spend limits, and whether parallel agents are authorized;
- output consumers and required delivery format.

Infer these from supplied context when safe. Ask only when a missing choice would materially change scope, authority, confidentiality, or cost. Invocation does not authorize access to private systems, external communication, purchases, or production changes.

## Choose the operating mode

- **Plan:** design the scope, track map, ontology, source strategy, fleet, controls, and acceptance gates without performing the research.
- **Execute:** run the full program and produce the graph and deliverables.
- **Resume:** inspect existing artifacts and compiler state, then continue from the first incomplete gate without rebuilding finished work.
- **Audit:** evaluate an existing corpus against its schema, evidence rules, enterprise controls, and acceptance contract. Do not expand the research unless asked.

If the user supplies only a target while explicitly invoking this skill, default to **Execute**. If they ask to review, design, or audit, respect that narrower mode.

## Design the research program

Read [program-design.md](references/program-design.md) before planning or executing. Derive tracks from the target instead of reusing an industry-specific taxonomy. Every full program must cover these concerns, whether as separate tracks or deliberate combinations:

1. anchor organizations, products, people, and stakeholders;
2. market structure, value chain, strategy, and economics;
3. end-to-end operations, workflows, decisions, and artifacts;
4. customers, counterparties, channels, and relationship networks;
5. data objects, sources, software, APIs, integrations, and cloud infrastructure;
6. metrics, quality standards, benchmarks, and outcome measurement;
7. regulation, security, privacy, governance, controls, and failure risks;
8. derived product, automation, agent, and transformation opportunities.

For a single company, anchor the graph on the company and its real ecosystem. For an industry, construct a representative and explicitly bounded organization universe before researching abstract practices. For a domain, anchor on authoritative standards, real operating organizations, and the decisions and artifacts that instantiate the domain.

## Bootstrap before parallel work

When executing a new program:

1. Create a project brief with scope, exclusions, downstream purpose, enterprise boundary, and acceptance profile.
2. Create the directory layout and `graph-config.json`. Use `scripts/init_research_graph.py` when practical.
3. Write the authoring contract and prove the compiler succeeds on the empty graph.
4. Build the anchor universe and reserve immutable IDs.
5. Create a checkpoint before a fleet writes to the workspace when the repository contract requires it.

Do not dispatch abstract track research before anchors exist. Do not let multiple agents write the same track. Do not begin synthesis before the researched graph compiles.

## Research and evidence rules

Read [research-protocol.md](references/research-protocol.md) before source collection.

- Prefer primary and permissioned first-party evidence. Record practitioner, vendor, secondary, and inferred evidence distinctly.
- Separate product capability, claimed organizational practice, verified adoption, and measured effectiveness. They are different claims.
- Every number carries its definition, population, date, and basis.
- Preserve contradictions and changed facts; do not silently reconcile them into a cleaner story.
- Unverified material becomes an open question, not an invented fact.
- Never bypass a paywall, robots restriction, authorization boundary, retention rule, or contractual data-use limit.
- Do not collect secrets, personal data beyond the authorized purpose, or regulated/confidential content into a public graph.
- Record retrieval failures and evidence gaps after one bounded retry. Do not grind low-yield sources.

Prefer Firecrawl search, map, scrape, crawl, parse, and asynchronous research when available and authorized. Use approved alternatives when Firecrawl is unavailable. Tool choice never changes the evidence contract.

## Fleet execution

When parallel agents are authorized, assign one owner per track and give each worker:

- the project brief and complete authoring contract;
- the anchor universe and reservation registry;
- its exact directory boundary and entity target;
- source priorities and evidence restrictions;
- the enterprise data-classification rules;
- the required return report: entities, sources, domains, findings, gaps, requested IDs, and failures.

Workers may propose cross-track IDs and relations but must not write outside their owned track. The lead owns shared files, reconciliation, synthesis, compiler changes, aliases, and final acceptance. Use strong independent review for load-bearing claims and final verification; do not treat worker completion as proof of correctness.

## Authoring and graph contract

Read [authoring-contract.md](references/authoring-contract.md) before writing entities or changing the ontology.

- One entity per file with a stable, globally unique ID.
- Closed, project-specific vocabularies for tracks, types, predicates, evidence classes, confidence, status, and sensitivity.
- Directed relations declared once. No self-edges, duplicate edges, or semantic mirror pairs.
- Every researched entity has sources, substantive open questions, and at least three grounded outgoing relations unless the project brief documents a stricter or justified alternative.
- Derived opportunity entities may cite the graph rather than external sources, but must point to researched entities and name the workflow, inputs, output, tools, human gate, failure risk, controls, and success metric.
- The compiler, not prose review, enforces the structural contract.

Use `scripts/build_graph.py --root <project-root>` throughout reconciliation and add `--strict` for the final acceptance run. Use `scripts/build_graph_viz.py --root <project-root>` to emit a self-contained offline explorer.

## Enterprise and regulated-industry requirements

Read [enterprise-controls.md](references/enterprise-controls.md) for any client, regulated, confidential, or production-oriented program.

Treat identity, authorization, evidence lineage, deterministic calculation, workflow state, certification, audit, retention, incident response, vendor risk, continuity, and model governance as product requirements—not an appendix.

Never state that a company, product, or architecture is “SOC 2 compliant,” certified, legally compliant, safe, or production-ready solely because this research was completed. Produce a control and evidence map, identify inherited and missing controls, name accountable owners, and distinguish:

- observed control design;
- observed implementation evidence;
- operating-effectiveness evidence;
- proposed target-state control;
- unresolved assurance or legal judgment.

Certification belongs to the scoped organization and its independent auditor. Legal interpretation belongs to qualified counsel and named accountable owners.

## Required deliverables

Read [deliverables-and-acceptance.md](references/deliverables-and-acceptance.md) before setting thresholds or closing the program. A comprehensive execution normally produces:

- project brief, scope/universe, authoring schema, and loader README;
- compiler-enforced entity graph, edge list, manifest, reservation registry, and validation report;
- master operating synthesis;
- product, application, API, data-source, and integration landscape;
- data and cloud reference architecture with lineage and security boundaries;
- regulatory, security, privacy, SOC 2 control, risk, and evidence map;
- ranked product/automation/agent opportunity map with human gates and evaluation metrics;
- open-question and permissioned-evidence register with owners;
- self-contained offline graph explorer;
- acceptance report with failures and candid self-audit.

Adapt names to the destination repository, but preserve these functions.

## Reconciliation and review

After track work:

1. Compile and fix malformed records, invalid vocabularies, duplicate IDs, and relation defects.
2. Canonicalize aliases and retire duplicates without breaking inbound references.
3. Drive dangling targets, orphans, thin entities, unsourced researched entities, and placeholder questions to zero.
4. Audit source diversity, primary-evidence share, confidence calibration, temporal freshness, and domain coverage.
5. Verify that every synthesis claim resolves to supporting entities and that every opportunity resolves to workflows, evidence, controls, and metrics.
6. Run adversarial review for capability-versus-adoption confusion, false universality, regulatory overclaiming, sensitive-data leakage, weak human gates, and attractive but inaccessible integrations.
7. Validate the offline explorer without network access and run the final compiler in strict mode.

## Completion standard

Report what was built, exact compiler and acceptance results, source and domain counts, primary and high-confidence shares, unresolved failures, permissioned evidence still needed, and the next highest-value validation step. A failed gate reported accurately is useful. A passed gate without reproducible evidence is a defect.

Finish repository-specific wiring, validation, and logs required by the destination workspace. Do not publish, install, deploy, or communicate externally unless explicitly authorized.
