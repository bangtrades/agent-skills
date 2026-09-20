# Slice Templates

Use these templates when generating copy-ready agent prompts. Keep ownership paths disjoint and make the evidence requirements explicit.

## Implementation Slice

```text
You are Agent N for <slice-id>.

Context:
<3-6 sentences describing current state, current verified truth, and why this slice exists. Include issue/gate ids and timestamps if relevant.>

Goal:
<One concrete outcome.>

Primary ownership:
- <file or module path>
- <file or module path>

Non-ownership / coordination:
- Do not edit <shared file> unless required. (Shared config files — package
  manifests, lockfiles — have exactly ONE owning slice; name it.)
- PINNED CONTRACT with <other slice> (paste the identical signature + data
  shape in both prompts; consumer lazy-imports with a fallback so both
  slices test standalone).
- Do not revert unrelated work.

Environment (paste facts, don't make the agent rediscover them):
- Working directory + branch: <path>, <branch>.
- Test command: <exact command with absolute venv/tool path>.
- Lint command: <exact command>.
- Key installed versions the code must target: <pkg==ver, ...>.
- Do NOT run version-control commands — the orchestrator commits.

Rules:
- Read local project instructions first.
- Preserve user changes.
- Keep the patch narrow.
- Add regression coverage at the layer being changed.
- Write code before tests before report, so a mid-run kill leaves
  salvageable work in that order.

Tasks:
1. Inspect <specific files>.
2. Identify <specific contract or bug>.
3. Implement <specific behavior>.
4. Add tests for <case A>, <case B>, <case C>.
5. Run <focused command>.
6. Write report at <report path>.

Report must include:
- Files changed.
- Tests run and exact results.
- Evidence that acceptance criteria are met.
- Remaining risks or follow-up slices.
```

## Verification / Gate Slice

```text
You are Agent N for <slice-id>.

Context:
<State which implementation or behavior needs independent verification.>

Goal:
Create or update a read-only verifier that reports current truth without mutating state.

Primary ownership:
- <script path>
- <test path, if applicable>

Rules:
- The verifier must be read-only by composition.
- Separate stale/historical evidence from fresh evidence.
- Final classification, exit code, blockers, and evidence must agree.

Tasks:
1. Inspect existing verifier style and JSON conventions.
2. Define canonical classifications.
3. Implement the verifier.
4. Add offline classifier tests where possible.
5. Run verifier against the current repo state.
6. Write report at <report path>.

Report must include:
- Classification matrix.
- Commands run.
- Current result.
- Any misleading prior signal corrected by the verifier.
```

## Triage Slice

```text
You are Agent N for <slice-id>.

Context:
<Describe the repeated failure, contradictory signal, or user-visible blocked state.>

Goal:
Find the failing layer and produce a patch recommendation or minimal fix.

Primary ownership:
- Read-only by default unless root cause is proven.

Rules:
- Do not patch before identifying the layer.
- Inspect source-of-truth records, logs, and gates.
- Do not rerun live/paid workflows unless explicitly approved.

Questions to answer:
1. What did the system claim happened?
2. What actually happened according to canonical logs/audit?
3. Which layer misreported or failed?
4. What is the smallest durable fix?
5. What regression test should prevent recurrence?

Report must include:
- Root cause.
- False leads eliminated.
- Evidence path.
- Recommended implementation slice.
```

## Docs / Release Slice

```text
You are Agent N for <slice-id>.

Context:
<State verified implementation status and any open defects.>

Goal:
Update sprint/release docs so project truth matches current evidence.

Primary ownership:
- <sprint doc>
- <runbook/report path>

Rules:
- Do not claim deferred work is complete.
- Distinguish implementation complete, verified complete, audit-only complete, and release blocked.
- Include issue ids, gate names, and dates when relevant.

Tasks:
1. Read current roadmap/sprint docs and reports.
2. Add or update ledger rows.
3. State completed, open, and deferred lanes.
4. Recommend next order of work.
5. Write report at <report path>.
```

## Research Slice

```text
You are Agent N for <slice-id>.

Context:
<Question, frozen research contract (hash of thresholds/schema/reservations), and the
ledger path every citation must join.>

Goal:
<One evidence deliverable: cards, graph nodes, a section draft.>

Primary ownership:
- <output folder or page paths>
- NO-GO: the frozen contract, shared builders, other slices' pages.

Retrieval:
- Capability matrix result pasted in (search / scrape / map / parse / agent /
  firecrawl_research_*), with cost per surface and the cheap corroboration route.
- Per-call cost ceiling: <n credits>. Expensive surfaces by name: <x.com scrape, ...>.
- Paper-class claims: yes/no. If yes: firecrawl_research_search_papers →
  related_papers (≥1 expansion pass, pool size recorded) → read_paper for every
  quoted number; cite arxiv:/pmid:/pmcid:/doi: with the operation class;
  budget k ≤ 20 search · ≤ 6 read · ≤ 20 related.
- Numeric thresholds carry their convention (<multi-day average / ±tolerance>).
- Quote `column → value` pairs from wide tables; record each source's own caveat
  sentence verbatim before scoring; distinguish full text from query extract.
- Search forms: read field names and try one URL-constructed GET before filing
  "undrivable".

Vault page contract (when writing into cortana-vault):
- Read `cortana-vault/scripts/vault-contract.json` first. `type:` is a declared
  type (never a `legacy_types` value; under research/ it is almost always
  `topic`); first `tags:` element is exactly one declared emoji, no other emoji;
  `title`, `type`, `created`, `updated`, `tags`, `status` first. No fit → closest
  declared value plus a `## Frontmatter note` line; never invent a value.
- Any template you author is contract-checked before a page is written from it.
- Cross-page references cite heading text or anchor, never a section number.
- Every asserted timestamp traces to a machine-readable stamp inside a cited
  document; mtime and headings are not evidence.

Tasks:
1. <retrieve> 2. <inspect originals> 3. <write output first, incrementally>
4. Run `scripts/vault-lint.py` scoped to your folder (legacy-* warnings on your
   pages are failures). 5. Write report at <report path>.

Report must include:
- Citations with ledger joins and operation class; suppressed candidates.
- Contradictions with other slices' facts you noticed.
- What could not be retrieved, per surface, and the fallback used.
```

Wave close (orchestrator, before declaring a research wave complete): append a
`## <Wave title> — <YYYY-MM-DD>` section to `research/research-hub.md` in the house
form (wikilink row: folder index · brief · QA gate; numbers produced; standing
quoting caveat), add the hub to the wave folder index's `related:`, bump the hub's
`updated:`.

## Slice Quality Checklist

- The prompt is copy-ready.
- The goal is singular.
- Ownership paths are explicit.
- Tests are named.
- Report path is named.
- Dependencies are explicit.
- The agent knows what not to touch.
- The slice can be judged from evidence, not vibes.
- Cross-slice contracts are pinned verbatim in every prompt that touches them.
- Every shared config file has exactly one owning slice, named in all prompts.
- Environment facts (venv path, exact test/lint commands, versions) are pasted in.
- The prompt forbids version-control commands; the orchestrator commits.
- The slice survives a mid-run kill: work products land on disk incrementally,
  and the orchestrator can judge them from diffs + gates without the report.
