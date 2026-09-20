---
title: "Orchestration retro — DetailAI WAI-548"
type: analysis
created: 2026-09-06
updated: 2026-09-07
tags: [🤖, orchestration, detailai, verification]
status: completed
deployment: both
related:
  - "[[Reports/software-dev/2026-09-06-detailai-wai548-development-report]]"
  - "[[cortana-vault/projects/detailai/detailai]]"
---

# DetailAI WAI-548 orchestration retro

Run `wai548-20260906-01` used GPT-5.6 Sol agents for disjoint database, account-routing and
provider slices, followed by fresh independent Sol QA and original-owner repairs. Root owned
the integration branch, events/reconciliation, runtime import and final verification.
WaiveBoard and MetaCortex product work stayed outside the scope.

## What changed in the verification practice

- **Database permissions belong to the migration artifact.** A test harness that grants all
  privileges after applying a migration can conceal a missing runtime grant. When grants are
  narrowed correctly, fixture INSERTs must use the permitted account birth and binding path
  or explicit administrator bootstrap; failing fixture setup is not a passed runtime probe.
- **Paid-operation history must be durable against all reachable writes.** Independent QA
  deleted an ambiguous journal row as the application role and obtained a fresh create claim.
  Removing DELETE/TRUNCATE and identity-column writes, then checking legal state transitions
  and legitimate tenant deletion, closed the actual boundary. Method-level retry tests alone
  had not established durability.
- **Provider fixtures must preserve real variants.** Changing an event type on a happy-path
  payload retained a campaign SID that real number-deregistration success omits. Fresh QA
  used the genuine shape and found a rejecting parser. A generic reconciler also had to keep
  Sole Proprietor mobile verification and independent profile/trust approval gates intact.
- **Build and start the packaged runtime.** Both images built, but worker startup initially
  failed because its Calendar workspace was missing. Root also removed a new database-to-API
  source import that the worker image could not resolve. Unit and type checks over the whole
  checkout do not establish the deployment source closure.
- **Mutation survivors are test defects worth fixing.** Two account tests did not isolate
  tenant-only or AccountSid-only substitution. The original owner reproduced each mutant,
  added precise negative cases and verified failure with the guard removed.
- **Copy commit identities from Git.** A developer incorrectly expanded a short SHA into an
  invented full hash. `git log` exposed the mismatch before integration; future reports use
  exact command output. A plausible hash is not a verified commit.

- **Read the actual list wire contract and crash boundary.** The provider returns campaign
  collections as `compliance` and use-case identifiers as `code`; display-name mocks concealed
  both mismatches. A completed phone binding also changes the database selector precondition,
  so recovery must resume after persisted PN ownership instead of rerunning fresh selection.
- **RLS does not imply relational ownership.** The two-shop calendar test found that a
  tenant-owned booking hold and message could reference another tenant's thread through a single-column
  foreign key. Cross-tenant reference substitution needs its own negative test and composite
  ownership constraint, even when both tables already have correct RLS policies. Changing the inserted row's tenant only tests RLS; retain the caller tenant and substitute the parent ID to test the foreign key.

## Evidence boundaries

Actual local PostgreSQL used a role with `rolsuper=false` and `rolbypassrls=false`. Provider
HTTP responses and external model responses in local tests were injected fixtures. These
prove caller wiring and isolation, not real registration, paid side effects, physical handset
receipt or production readiness. Requested real shop records, consent evidence, exact numbers
and purchase limits were not supplied during local implementation.

## Publication

The loaded account path resolves to the registry source. The staged copy contained a newer
September 7 framework-build addendum, which was preserved during the three-way comparison.
A pre-existing lineage hold named missing DetailAI retros. The maintained mirror source was read directly through Git, and six historical entries were restored as a byte-preserving addition to the staged copy. The hold note records this resolution and its source receipt. The registry was not edited. The updated package remains staged for operator review:

```sh
/Users/nolan/Cortana/cortana-skill-registry/bin/publish-skill.sh orchestration
```
