# Program design

Use this reference to convert a target into a bounded research program. The ontology and tracks must reflect the target; the execution mechanics remain stable.

## 1. Frame the mission

Write a project brief that answers:

- What real decisions, client work, software, controls, or operating changes will this graph support?
- What would a builder need to know without further foundational research?
- What counts as the target, and what is explicitly out of scope?
- Which geographies, legal entities, products, business units, user roles, and time periods matter?
- Which claims require public evidence, internal evidence, interviews, system exports, or counsel/auditor validation?
- What are the consequences of a wrong answer?

Translate the downstream purpose into 3–7 operating surfaces such as research, sales, service delivery, underwriting, operations, finance, compliance, customer support, product, or strategy. Every entity should help at least one surface.

## 2. Choose the anchor model

### Company target

Anchor on the company and the ecosystem that constrains it:

- legal entities, business units, products, and key roles;
- customers, suppliers, partners, competitors, regulators, auditors, and critical vendors;
- end-to-end value streams and high-consequence decisions;
- systems of record, data flows, interfaces, and control ownership.

Do not turn a company graph into an industry survey. Use industry evidence to explain the company boundary and unresolved variance.

### Industry target

Build a representative organization universe first. Define inclusion, exclusion, geography, scale, business model, regulatory posture, and evidence thresholds. Select organizations that expose meaningful variation rather than only the most visible brands.

The universe should include:

- representative operators;
- regulators and standard setters;
- critical vendors and infrastructure providers;
- customers or counterparties where their requirements shape operations;
- boundary cases that test the scope definition.

### Domain target

Anchor on authoritative standards and real instantiations of the domain. Map roles, decisions, processes, artifacts, data, systems, metrics, controls, and failure modes. Use named organizations as evidence anchors, not as the object of the whole graph.

## 3. Derive the track map

Tracks are ownership partitions, not ontology types. A useful default is:

| Concern | Typical track | Owns |
|---|---|---|
| Anchor universe | `organizations` | Companies, agencies, products, key people, boundary cases |
| Market and economics | `market` | Value chain, business models, strategy, incentives, economics |
| Stakeholders | `stakeholders` | Customers, users, counterparties, channels, networks |
| Operations | `operations` | Value streams, workflows, decisions, roles, handoffs |
| Artifacts and methods | `artifacts` | Documents, records, analytical methods, decision packages |
| Technology and data | `technology` | Systems, APIs, integrations, data objects, data sources, cloud |
| Measurement | `measurement` | KPIs, quality standards, benchmarks, outcomes, evaluation |
| Governance | `governance` | Regulation, security, privacy, controls, risks, assurance |
| Opportunity | `opportunity` | Derived product, automation, agent, and transformation targets |

Merge tracks for a focused company; split high-volume tracks for a broad industry. Keep each track internally coherent, roughly balanced, and owned by one writer at a time. Record the final tracks in `graph-config.json` before dispatch.

## 4. Run phases in order

### Phase 0 — Bootstrap

- Create scope, config, authoring contract, directories, compiler, and reservation registry.
- Prove an empty compile works.
- Define acceptance thresholds and source rules before research begins.

### Phase 1 — Anchor universe

- Build and verify anchor organizations, standards, or business units.
- Reserve immutable IDs.
- Record ambiguity instead of silently including or excluding boundary cases.

### Phase 2 — Parallel evidence collection

- Dispatch one owner per track when authorized.
- Give each worker the complete contract, anchors, source strategy, and output boundary.
- Require workers to reserve IDs before writing and report blocked/retrieval failures.

### Phase 3 — Reconciliation

- Compile, deduplicate, canonicalize aliases, resolve targets, repair relations, and deepen thin entities.
- Examine hubs and under-connected entities for ontology errors.
- Re-check load-bearing claims with primary or independent evidence.

### Phase 4 — Synthesis and opportunity derivation

- Derive opportunities only from the researched graph.
- Write synthesis after structural defects are resolved.
- Produce product/data/cloud and control-readiness views from the same evidence base.

### Phase 5 — Enterprise readiness review

- Partition public, internal, confidential, and restricted evidence.
- Map control objectives, control owners, evidence, gaps, and required assurance.
- Validate permissions, lineage, retention, deterministic calculations, human gates, and recovery paths.

### Phase 6 — Acceptance and handoff

- Run strict compiler and offline checks.
- Publish exact pass/fail evidence, open questions, and permissioned follow-up needs.
- Wire outputs into the destination knowledge system without changing unrelated content.

## 5. Fleet sizing and routing

Choose agent count from independent work, not from a fixed ritual. Use one worker per substantial track, combine tracks with fewer than roughly 15 expected entities, and split tracks that require materially different sources or expertise. Keep shared compiler, ontology, synthesis, and acceptance work with the lead.

Use frontier-quality reasoning for ontology, reconciliation, regulated controls, synthesis, and verification. Faster models may execute bounded source collection and entity authoring when the schema, directory boundary, and validation loop are explicit. Never lower the verification standard merely because execution was parallelized.

## 6. Lessons preserved from the reference build

- Anchor-first research prevents generic consultancy prose.
- A compiler written before the fleet prevents incompatible dialects.
- A reservation registry and one-writer-per-track rule prevent most merge defects.
- Capability, adoption, effectiveness, and contractual access require separate evidence.
- Structural green is not enough; adversarial review must catch mirrored edges, weak relation semantics, universalized workflows, and unsupported firm observations.
- The largest residual gap is often permissioned deployment reality: installed modules, API rights, lineage, decision records, and real operating cohorts.
- Checker-first, read-only opportunities usually earn enterprise trust before action-taking agents.
