# Enterprise controls and regulated-industry overlay

Use this reference whenever the graph will support a major client, confidential data, production software, regulated activity, or assurance work.

## Assurance boundary

Research can map requirements, control design, and available evidence. It cannot certify SOC 2 compliance, give a legal opinion, prove operating effectiveness, or authorize production use.

For each control-related finding, label it as one of:

- observed requirement;
- observed control design;
- observed implementation evidence;
- observed operating-effectiveness evidence;
- proposed target-state control;
- gap requiring owner, counsel, security, privacy, compliance, auditor, or client validation.

Map applicable SOC 2 Trust Services Criteria—Security is mandatory for a SOC 2 examination; Availability, Processing Integrity, Confidentiality, and Privacy depend on scope. Do not claim coverage merely because a control is mentioned.

## Required control domains

### Scope and governance

- system and organization boundary;
- services, commitments, subservice organizations, and complementary user-entity controls;
- accountable owners, approval authorities, policies, exception process, and risk register;
- change, incident, problem, and evidence ownership.

### Identity and access

- workforce, service, customer, partner, and agent identities;
- SSO/MFA, provisioning/deprovisioning, role and attribute rules, privileged access, segregation of duties;
- object-, tenant-, matter-, deal-, patient-, account-, or case-level authorization as required;
- periodic review, emergency access, machine identity, secrets, and key rotation.

### Data governance

- canonical objects, systems of record, lineage, quality, certification, and restatement;
- classification, minimization, purpose limitation, retention, legal hold, deletion, export, and residency;
- encryption in transit and at rest, key custody, tokenization or de-identification where relevant;
- source entitlements and downstream rights for storage, embedding, model input, training, and cross-user display.

### Secure engineering and change

- approved architecture, threat model, dependency and vulnerability management;
- source control, review, testing, CI/CD, environment separation, release approval, rollback, and configuration management;
- infrastructure as code and drift detection where applicable;
- software and model supply-chain provenance.

### Logging, monitoring, and response

- immutable audit events for identity, retrieval, tool calls, approvals, state changes, exports, and administrative actions;
- security monitoring, anomaly detection, alert ownership, escalation, incident response, evidence preservation, and notification duties;
- time synchronization, log retention, access, and tamper resistance.

### Availability and continuity

- critical dependencies, capacity, backup scope, restore tests, RTO/RPO, regional failure assumptions, and degraded-mode operation;
- vendor outage and contract-termination export plans;
- business continuity ownership and tested recovery evidence.

### Vendor and subprocessor risk

- due diligence, contracts, DPAs/BAAs where applicable, subprocessors, data location, breach duties, audit reports, exceptions, and renewal review;
- API scope, write permissions, rate limits, deletion propagation, export completeness, and tested exit plan;
- shared-responsibility and inherited-control mapping.

### AI and agent controls

- use-case inventory, model/provider/version, allowed data, tools, prompts, retrieval, and prohibited actions;
- prompt-injection and tool-abuse defenses, least-privilege tool scopes, output validation, deterministic calculations, and sandboxing;
- capability-specific evaluations, human gates, override capture, incident thresholds, shutdown, rollback, and retirement;
- no cross-tenant or cross-matter memory by default;
- no autonomous legal interpretation, regulated decision, external communication, cash movement, trade, production write, or report release without explicit authority and control design.

## Control-map record

For each material requirement or control, capture:

| Field | Meaning |
|---|---|
| Control ID and objective | Stable reference and intended outcome |
| Requirement source | Law, contract, policy, standard, risk, or commitment |
| Scope | Entity, product, environment, data class, process, geography |
| Owner and approver | Accountable roles, not generic “human” |
| Preventive/detective/corrective | Control function |
| Frequency and trigger | Continuous, per event, daily, quarterly, release, incident |
| Implementation | System, workflow, configuration, manual step |
| Evidence | Log, ticket, report, review, test, attestation, export |
| Evidence location and retention | Authorized reference and required duration |
| Test method | Design or operating-effectiveness procedure |
| Exceptions and remediation | Open defects, compensating controls, owner, due date |
| Inherited or user control | Vendor, platform, client, or shared responsibility |

## Regulated overlays

Identify the actual perimeter before applying a framework. Examples include financial-services communications and books-and-records duties, HIPAA and healthcare security/privacy, PCI DSS, export controls, government contracting, education privacy, employment law, or jurisdiction-specific privacy rules. Use primary rule text and authoritative guidance; record effective dates and applicability assumptions.

The graph should show where a legal or compliance decision remains unresolved. Do not turn a generic framework mapping into a binding interpretation.

## Enterprise architecture order

The safest default dependency order is:

1. identity and canonical objects;
2. authorization and information partitions;
3. source rights and evidence lineage;
4. deterministic calculations and validations;
5. workflow state and immutable events;
6. certification and named approval;
7. distribution or action;
8. prospective evaluation before greater autonomy.

Recommend action-taking automation only after the preceding layers are evidenced. Prefer read-only retrieval, comparison, reconciliation, and draft generation as initial releases.
