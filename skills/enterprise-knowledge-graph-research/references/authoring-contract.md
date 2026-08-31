# Authoring contract

Use this as the default project schema, then specialize the closed vocabularies in `graph-config.json`. Do not weaken provenance, sensitivity, relation, or uncertainty requirements to make authoring easier.

## File and identity rules

- Path: `context/<track>/<id>.md`.
- Filename equals `id`; IDs are lowercase kebab-case, globally unique, and stable.
- One entity per file.
- Recommended body length: 200–700 words. Change only when the project brief justifies it.
- Reserve an ID before writing. Retired IDs map to canonical IDs through aliases; do not reuse them for a different concept.

## Default entity frontmatter

```yaml
---
id: customer-onboarding
name: Customer Onboarding
type: process
track: operations
summary: The controlled workflow that moves an approved customer into active service.
relations:
  - {predicate: consumes, target: signed-customer-agreement}
  - {predicate: uses, target: customer-master-record}
  - {predicate: governed_by, target: customer-access-control}
  - {predicate: measured_by, target: onboarding-cycle-time}
sources:
  - title: "Exact source title"
    uri: "https://authoritative.example/source"
    accessed: 2026-08-31
    source_class: primary
    sensitivity: public
confidence: high
evidence_class: primary
sensitivity: internal
anchors_observed: [example-organization]
status: reviewed
---
```

Use opaque authorized references such as `client://system/document-id` for internal sources. Do not place secrets, credentials, sensitive query strings, or unauthorized local paths in source URIs.

## Default closed type set

Start with these and remove unused types rather than adding near-synonyms:

- `organization`, `person`, `role`, `stakeholder`;
- `offering`, `market`, `strategy`, `value-stream`;
- `process`, `decision`, `artifact`, `method`, `event`;
- `data-object`, `data-source`, `tool`, `integration`, `platform`;
- `metric`, `standard`, `regulation`, `control`, `risk`, `pattern`;
- `opportunity` for graph-derived product, automation, or agent targets.

## Default predicates

Use a closed directed vocabulary. A useful starting set is:

`part_of` · `owned_by` · `performed_by` · `serves` · `uses` · `consumes` · `produces` · `produced_by` · `governed_by` · `implemented_by` · `sources_from` · `stored_in` · `integrates_with` · `triggers` · `precedes` · `validates` · `approves` · `maps_to` · `alternative_to` · `competes_with` · `measured_by` · `mitigates` · `constrains` · `depends_on` · `references` · `automates`

Declare each edge once. Never mirror an edge merely to make both entities appear connected. Use the direction that answers the operational question. The compiler rejects exact mirrors and the `produces`/`produced_by` semantic inverse pair when both are declared.

## Evidence classes

| Class | Meaning |
|---|---|
| `primary` | Original regulator, standard, contract, filing, client-controlled record, system export, or organization-authored source |
| `practitioner` | A named practitioner describing their own work |
| `vendor` | A vendor describing its product or service |
| `secondary` | Journalism, analyst research, academic synthesis, or industry survey |
| `inferred` | A conclusion reasoned from indirect evidence |

Vendor evidence may establish product capability, not customer adoption or effectiveness. Inferred evidence cannot be high confidence. Interviews and internal documents need source ownership, date, authorization, sensitivity, and retention handling even when they are primary.

## Sensitivity

Default values are `public`, `internal`, `confidential`, and `restricted`. The entity sensitivity is the highest classification of content stored in the entity, not the sensitivity of the topic in the abstract. Source classification and retrieval authorization must be enforced before content reaches a model or shared graph.

Do not collapse restricted evidence into a public summary if the summary itself reveals protected facts. Use separate graph partitions or redacted derived facts with recorded approval.

## Body structure

```markdown
# <name>

<What it is and where it sits in the operating system.>

## Operational reality
<Inputs, sequence, outputs, timing, cost, responsible roles, decisions, and exceptions.>

## Systems and data
<Systems of record, interfaces, data objects, provenance, permissions, and manual seams.>

## Decision rights and controls
<Who proposes, reviews, approves, executes, monitors, and can override.>

## Why it matters to the build
<Data model, retrieval boundary, tool calls, deterministic logic, human gate, and evaluation signal.>

## Key facts
- <Atomic, independently supportable facts.>

## Variance and contradictions
<How practice differs across anchors, conditions, or time; separate claim from observation.>

## Open questions
- <What remains unverified, who should answer it, and what evidence would resolve it.>
```

Every entity needs substantive open questions. A well-bounded unknown is more useful than a confident generalization.

## Opportunity entity contract

An opportunity is derived from researched entities and must state:

- workflow augmented or replaced;
- explicit capability boundary and prohibited actions;
- input data and systems, including access reality;
- output artifact or state change;
- required integrations and whether the interface is verified;
- accountable human gate and why it exists;
- failure mode, affected parties, and controls;
- named success metric and rollback or stop signal;
- data availability, implementation difficulty, regulatory friction, and defensibility;
- smallest read-only or checker-first experiment.

An unsourced opportunity must relate to at least three distinct sourced, non-opportunity entities and at least one live metric. Graph grounding does not prove ROI or deployment readiness.

## Compiler invariants

At minimum enforce:

- frontmatter shape, filename/ID identity, unique IDs, and closed vocabularies;
- source required fields, URI validity, accessed dates, and sensitivity values;
- word range, substantive open questions, and evidence/confidence rules;
- relation shape, target resolution, duplicates, self-edges, mirrors, and selected type constraints;
- minimum distinct grounded outgoing relations;
- opportunity grounding, metric, and human-gate requirements;
- dangling targets, orphans, unsourced researched entities, and acceptance thresholds in strict mode.
