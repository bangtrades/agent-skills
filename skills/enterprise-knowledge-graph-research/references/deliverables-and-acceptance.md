# Deliverables and acceptance

Set the acceptance contract during bootstrap. Counts are scope controls, not substitutes for substance. Adjust the profile when justified and record the change before the fleet begins.

## Deliverable set

### Loader and scope

- `README.md`: loading order, graph counts, track map, rebuild commands, evidence boundary.
- `PROJECT-BRIEF.md`: target, purpose, scope, exclusions, consumers, regulated perimeter, source authority, acceptance profile.
- `UNIVERSE.md`: anchors, inclusion/exclusion, boundary cases, and selection evidence.
- `SCHEMA.md`: standalone authoring contract and closed vocabularies.

### Evidence graph

- `context/<track>/<id>.md`: one evidence-backed entity per file.
- `context/<track>/_index.md`: exact links to every track entity.
- `context/graph/RESERVATIONS.md`: immutable ID ownership and status.
- `context/graph/entities.json`, `edges.json`, `manifest.json`, and `REPORT.md`.

### Executive and builder views

- `SYNTHESIS.md`: the target's shape, operating loop, real differentiators, system reality, measures, constraints, broken work, and unknowns.
- `PRODUCT-AND-DATA-STACK.md`: applications, APIs, data sources, auth, export, integration, cost/contract visibility, build-versus-buy, and adoption evidence.
- `DATA-CLOUD-ARCHITECTURE.md`: ingestion, canonical model, lineage, object store, warehouse/lakehouse, operational data, search/vector, queues, identity, secrets, observability, backup, and AI gateway.
- `CONTROL-AND-COMPLIANCE-MAP.md`: regulatory perimeter, SOC 2/control objectives, ownership, evidence, inherited controls, gaps, and assurance boundary.
- `OPPORTUNITY-MAP.md`: ranked product, workflow, automation, and agent targets with visible scoring, human gates, controls, experiments, and metrics.
- `OPEN-QUESTIONS.md`: all medium/low confidence and unretrieved or permissioned evidence, grouped with owners and resolution evidence.
- `ACCEPTANCE-REPORT.md`: gate table, verification evidence, residual limitations, and self-audit.
- `outputs/knowledge-graph.html`: self-contained offline explorer.

## Default scale profiles

Use these as starting floors, then adapt to the real scope:

| Gate | Company | Domain | Industry |
|---|---:|---:|---:|
| Entities | 150 | 200 | 250 |
| Directed edges | 450 | 650 | 900 |
| Distinct source records | 250 | 350 | 450 |
| Distinct public domains | 60 | 100 | 150 |
| Opportunity entities | 15 | 15 | 20 |

For internal company work, a lower public-domain count may be appropriate when permissioned primary evidence is richer. Never compensate for weak evidence by padding entities or sources.

## Mandatory quality gates

Regardless of profile:

- hard compiler violations: 0;
- dangling relation targets: 0;
- orphan entities: 0;
- entities outside the configured word range: 0;
- researched entities without sources: 0;
- entities without substantive open questions: 0;
- every entity has the configured minimum grounded relations;
- inferred evidence with high confidence: 0;
- primary-evidence share: default at least 35%;
- high-confidence share: default at least 55%, with every medium/low entity in the open-question register;
- every opportunity names workflow, inputs, output, tools, human gate, risk, controls, metric, and smallest experiment;
- every sensitive source has classification and authorized reference handling;
- offline graph opens without a network dependency;
- repository wiring and operation log are complete.

Primary and high-confidence targets are not quotas to game. If the domain cannot support them, fail the gate honestly and explain the permissioned or longitudinal evidence required.

## Synthesis quality

Every substantive synthesis paragraph should resolve to graph entities. The narrative must distinguish:

- observed fact from synthesized operating model;
- common pattern from universal practice;
- current state from target architecture;
- vendor capability from adoption, entitlement, and effectiveness;
- control design from implementation and operating effectiveness;
- proposed opportunity from proven ROI.

## Opportunity scoring

Use a visible formula. A useful default is:

`priority = value × data availability × defensibility × reversibility ÷ build difficulty ÷ regulatory friction`

Score definitions must be included. Ties favor testability, checker-first boundaries, reusable evidence, and low-consequence rollback.

## Final self-audit

Answer in plain language:

1. What would a working operator, client owner, security leader, or regulator say is wrong or over-normalized?
2. Which load-bearing entities rely on one source or one source class?
3. Where did the work infer rather than verify, and could a builder mistake it for current practice?
4. Which controls are only proposed, which are evidenced as implemented, and which have operating-effectiveness evidence?
5. What is the biggest missing permissioned or longitudinal dataset?
6. Which product/API assumptions remain contract-specific or untested?
7. What is the narrowest next validation that would reduce the most risk?
8. If another full run were funded, where should the research budget go?
