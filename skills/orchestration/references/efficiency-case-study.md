# DetailAI: changing the execution model, September 23, 2026

The stopped run lasted 16h15m and processed 1,974,175,885 tokens in 13,905 responses. Input was 98.15% cached. The controller made 537 agent-message calls, 81 follow-up dispatches and 354 waits. Average response input was 141,509 tokens. Two developers were reused across unrelated tasks and compacted 102 times; controller/QA added another 31. Useful local code resulted, but no release was deployed. These are measured historical facts, not a general model benchmark.

## What changes the token equation

Total processed tokens are approximately response count × average input, plus output. Model substitution primarily changes cost, not this equation. The new workflow attacks both factors:

- Task-specific fresh contexts and 24K growth checkpoints reduce repeated input. Entry-point pruning helps but is insufficient alone.
- Producer-owned investigation and a single independent review reduce controller duplication.
- Event-only worker messages, compact manifests and scripted mechanical checks reduce response count.
- Caller tests before QA reduce avoidable repair loops.
- Batch admission and reserved QA capacity expose runaway scope before another dependency wave is started.

Old/new entrypoints, measured with tiktoken 0.12.0 `o200k_base` (a reproducible proxy, not a verified GPT-6 tokenizer): orchestration 9,965 → 1,483 tokens (85.12% reduction); subagent-driven-development 2,436 → 403 (83.46%). Conditional incident/research/operations instructions remain available as references; safety requirements stay in the entrypoint. Loading every reference would defeat the reduction.

Offline scenario on the same 13,905 recorded responses: cap each input at that agent's observed initial input +24K, retain all observed outputs and response counts → 926,884,387 tokens, 53.05% below baseline. Initial input was already about 35K for workers and 75K for the controller; a skill cannot remove host overhead. This scenario assumes relevant evidence fits and excludes renewal overhead. It is not a measured outcome of rerunning the work.

Hypothetically halving responses as well yields 463,442,194 tokens, 76.52% lower. This is a sensitivity calculation, not a promise that half the work was unnecessary. No same-quality delivery benchmark has yet demonstrated that reduction.

The default 5M batch envelope would have reached its 80% implementation-admission threshold after 54 responses, about 3m38s into the pathological trace. That proves detection, not equivalent work completed cheaply: it would require rescoping or a justified initial estimate. Never market the unexecuted remainder as saved productive work.

## Evaluation contract for the next authorized batch

Use a representative ticket with frozen acceptance and compare processed tokens per independently accepted deliverable, controller tokens, response count, repair count, missing requirements and elapsed time. Preserve required checks and privacy/authorization boundaries. Report fresh/cached input and output separately. Record context-renewal/setup overhead. Compare similar task complexity; don't divide a 31-ticket backlog by one simple fix.

Aim for at least 50% lower processed tokens per comparable accepted outcome; 70–80% is the stretch target if duplicated reads/coordination actually fall. If quality, critical caller coverage or acceptance completeness declines, the optimization fails regardless of token savings. If savings fall short, identify the remaining context floor or response source instead of silently weakening gates.

This skill change did not resume the stopped development run, deploy DetailAI, or prove live application accuracy. It installs a different workflow plus a tested admission tool. True host-enforced limits require runtime support; the script cannot intercept tool calls.

Local provenance: `/Users/nolan/Projects/DetailAI/audits/run-postmortem-20260923/postmortem.md`; measurements and reproducible benchmark: `/Users/nolan/Projects/DetailAI/audits/orchestration-optimization-20260923/benchmark.json` and `benchmark.py`.
