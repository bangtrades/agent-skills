# Cortana Skill Registry

The shared skill library for the Cortana agency. This repo is the canonical
source of the skills Cortana agents draw on — trading skills, dev skills, and
the two platform skills (`cortana-memory`, `paperclip-triage`).

It is a **standalone git repo**, checked out and mounted **read-only** into the
Paperclip container. Skills load via Paperclip's standard skill discovery — no
Paperclip source-tree modification (STEP-48).

## Why it is its own repo

The registry is operator-managed and version-controlled independently of the
platform tree so it can be shared, imported via a GitHub URL, and updated
without touching `platform-v2/`. Per the operator's decision it lives in a
**private** GitHub repo. Creation + push is operator-gated (GitHub auth is
theirs); this tree is scaffolded ready for `git init`.

## Structure

```
cortana-skill-registry/
  README.md              ← this file
  .gitignore
  skills/
    <skill-id>/
      SKILL.md           ← the manifest + skill body (see "Manifest format")
      scripts/           ← skill helper scripts (filled in by agents over time)
      references/        ← optional deep-dive docs (carry-overs use these)
```

Each immediate subdirectory of `skills/` that contains a `SKILL.md` is one
discoverable skill. The directory name is the skill id.

### Skills in this registry

As of the consolidation, this registry holds **75 skills** merged from the Codex, Claude/Cowork, and Hermes harness skill sets (de-duplicated by skill id).


**Trading & markets**

| Skill id | Purpose |
| --- | --- |
| `backtest-run` | Use when running, analyzing, or validating a trading strategy backtest — preparing data, executing a backtest, and  |
| `indicator-build` | Use when building, porting, or debugging a trading indicator or charting study — Pine Script (TradingView), or indi |
| `markets-research` | Use when researching a market, ticker, sector, or trading signal — gathering news, sentiment, macro context, on-cha |
| `risk-rules` | Use when sizing a position, checking risk before a trade, or enforcing drawdown / exposure limits — position sizing |
| `data-fetch` | Use when retrieving market data — OHLCV bars, quotes, fundamentals, or on-chain data from an exchange or data provi |
| `nq-snapshot` | Capture an MTF deep-analysis snapshot of MNQ/NQ futures from live TradingView via the tradingview MCP, applying ban |
| `crystal-ball` | - Capture and analyze bang's Crystal Ball (CB) fib-expansion tool on a TradingView NQ/MNQ chart — decode the T1–T5  |
| `pine-script` | Use this skill whenever the user wants to write, debug, optimize, or understand Pine Script for TradingView. |
| `pre-trade-intel` | - Query bang's structured trade history before entering a new NQ/MNQ trade and return a pre-trade intelligence brie |
| `trade-capture` | - Convert a natural-language trade description into a fully populated structured trade file in `projects/nq-trading |
| `bt-equity` | Produce a BT Stock Report — bang's institutional-tier (Druckenmiller-style) equity research dossier on a single tic |


**Research & recon**

| Skill id | Purpose |
| --- | --- |
| `brand-recon` | Investigate a brand or company end-to-end and emit a structured dossier + a reusable per-entity brand skill into th |
| `obsidian` | Cortana knowledge engine — manages bang's Obsidian vault (`cortana-vault/`) and the parallel Reports/ output layer  |
| `obsidian-review` | Run a comprehensive health review of the Cortana vault — audit frontmatter, tag hygiene, link density, orphan pages |
| `yt` | Process a YouTube video into a Cortana vault wiki page. |
| `rag-architect` | Use when the user asks to design RAG pipelines, optimize retrieval strategies, choose embedding models, implement v |
| `product-strategist` | Strategic product leadership toolkit for Head of Product covering OKR cascade generation, quarterly planning, compe |


**Agent design & ops**

| Skill id | Purpose |
| --- | --- |
| `adversarial-reviewer` | Adversarial code review that breaks the self-review monoculture. |
| `agent-designer` | Use when the user asks to design multi-agent systems, create agent architectures, define agent communication patter |
| `agent-workflow-designer` | Agent Workflow Designer |
| `self-improving-agent` | Curate Claude Code's auto-memory into durable project knowledge. |
| `chief-of-staff` | C-suite orchestration layer. |
| `orchestration` | This skill should be used when the user asks to "orchestrate agents", "give me agent slices", "coordinate a complex |
| `skill-creator` | Create new skills, modify and improve existing skills, and measure skill performance. |
| `consolidate-memory` | Reflective pass over your memory files — merge duplicates, fix stale facts, prune the index. |


**Cortana platform**

| Skill id | Purpose |
| --- | --- |
| `cortana-memory` | Cortana platform memory pillar — spec, contracts, operations, troubleshooting, and upgrade ceremonies. |
| `cortana-troubleshooting` | This skill should be used when the user asks to "debug Cortana", "troubleshoot Paperclip", "check the router", "inv |
| `paperclip-triage` | This skill should be used when the user asks to "triage Paperclip", "debug Paperclip", "troubleshoot Cortana agents |
| `read-file` | Read text files and list directories from the agent's workspace. |


**Delivery & PM**

| Skill id | Purpose |
| --- | --- |
| `sprint-audit` | This skill should be used when the user asks to "run a sprint audit", "audit the sprint plan", "review agent slice  |
| `sprint-runner` | Track solo indie sprints — scaffold sprint trackers, compose per-story run summaries from git log + test output, an |
| `schedule` | Create or update a scheduled task that runs automatically. |
| `setup-cowork` | Guided Cowork setup — install role-matched plugins, connect your tools, try a skill. |
| `scrum-master` | Advanced Scrum Master skill for data-driven agile team analysis and coaching. |
| `senior-pm` | Senior Project Manager for enterprise software, SaaS, and digital transformation projects. |
| `jira-expert` | Atlassian Jira expert for creating and managing projects, planning, product discovery, JQL queries, workflows, cust |


**Software engineering**

| Skill id | Purpose |
| --- | --- |
| `code-review` | Use when reviewing a pull request, diff, or change set — checking correctness, security, style, and test coverage a |
| `code-reviewer` | Comprehensive code review skill for TypeScript, JavaScript, Python, Swift, Kotlin, Go. |
| `test-runner` | Use when running a test or smoke harness, interpreting failures, or wiring tests into a workflow — unit, integratio |
| `senior-backend` | Comprehensive backend development skill for building scalable backend systems using NodeJS, Express, Go, Python, Po |
| `senior-frontend` | Comprehensive frontend development skill for building modern, performant web applications using ReactJS, NextJS, Ty |
| `senior-fullstack` | Comprehensive fullstack development skill for building complete web applications with React, Next.js, Node.js, Grap |
| `senior-devops` | Comprehensive DevOps skill for CI/CD, infrastructure automation, containerization, and cloud platforms (AWS, GCP, A |
| `senior-data-engineer` | World-class data engineering skill for building scalable data pipelines, ETL/ELT systems, and data infrastructure. |
| `senior-data-scientist` | World-class senior data scientist skill specialising in statistical modeling, experiment design, causal inference,  |
| `senior-qa` | Generates unit tests, integration tests, and E2E tests for React/Next.js applications. |
| `senior-prompt-engineer` | World-class prompt engineering skill for LLM optimization, prompt patterns, structured outputs, and AI product deve |
| `security-pen-testing` | Use when the user asks to perform security audits, penetration testing, vulnerability scanning, OWASP Top 10 checks |
| `tech-stack-evaluator` | Technology stack evaluation and comparison with TCO analysis, security assessment, and ecosystem health scoring. |
| `webapp-testing` | Toolkit for interacting with and testing local web applications using Playwright. |
| `pso-optimizer` | Particle Swarm Optimization (PSO) skill for algorithm design, implementation, parameter tuning, convergence analysi |


**Apple / Swift**

| Skill id | Purpose |
| --- | --- |
| `senior-swift` | Senior Swift/SwiftUI engineering skill for writing, debugging, and fixing iOS/macOS code. |
| `swift-concurrency` | 'Diagnose data races, convert callback-based code to async/await, implement actor isolation patterns, resolve Senda |
| `swift-security-expert` | Use when working with iOS/macOS Keychain Services (SecItem queries, kSecClass, OSStatus errors), biometric authenti |
| `swiftui-pro` | Comprehensively reviews SwiftUI code for best practices on modern APIs, maintainability, and performance. |
| `swiftui-performance-audit` | Audit and improve SwiftUI runtime performance from code review and architecture. |
| `ios-accessibility` | 'Expert guidance on iOS accessibility best practices, patterns, and implementation. |
| `swift-nova` | This skill should be used when the user asks to work on the Novai, NovaKids, NovaCompanion, or Nova v2 classroom Sw |


**Design & docs**

| Skill id | Purpose |
| --- | --- |
| `canvas-design` | Create beautiful visual art in .png and .pdf documents using design philosophy. |
| `frontend-design` | Create distinctive, production-grade frontend interfaces with high design quality. |
| `epic-design` | Build immersive, cinematic 2.5D interactive websites using scroll storytelling, parallax depth, text animations, an |
| `ui-design-system` | UI design system toolkit for Senior UI Designer including design token generation, component documentation, respons |
| `nova-design` | This skill should be used when the user asks for Novai or NovaKids design, classroom UI, 2.5D art direction, asset  |
| `ghibli-photo` | Transform real photos into cohesive, warm, hand-painted storybook illustrations inspired by classic Japanese animat |
| `docx` | Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). |
| `pdf` | Use this skill whenever the user wants to do anything with PDF files. |
| `pptx` | Use this skill any time a .pptx file is involved in any way — as input, output, or both. |
| `xlsx` | Use this skill any time a spreadsheet file is the primary input or output. |
| `client-pitch` | Create client-specific AI/agentic transformation pitch packages with branded PowerPoint and matching PDF outputs. |


**Brand kits**

| Skill id | Purpose |
| --- | --- |
| `copperjoint-brand` | CopperJoint brand guide for generating consistent, on-brand documents and digital deliverables. |
| `hbef-brand` | Hermosa Beach Education Foundation (HBEF) brand guide for generating consistent, on-brand documents. |
| `hbef-fb-voice` | HBEF Facebook (and Instagram caption) voice guide — generate posts that match Hermosa Beach Education Foundation's  |
| `hbef-surf-report` | HBEF Surf Report voice and format guide — write HBEF's contributions to the weekly HVPTO Surf Report newsletter, or |
| `sf-brand` | Summer Fridays brand guide for generating consistent, on-brand documents and deliverables. |
| `varian-brand` | Siemens Healthineers / Varian brand guide for generating consistent, on-brand documents and presentations. |

## Manifest format (what Paperclip actually discovers)

Paperclip discovers a skill by scanning `skills/` for any subdirectory
containing a `SKILL.md`. **The YAML frontmatter of `SKILL.md` is the manifest** —
there is no separate authoring `skill.json`. Verified against the v2 Paperclip
source: `listPaperclipSkillEntries` /
`packages/adapter-utils/src/server-utils.ts` reads `SKILL.md` frontmatter; the
`.paperclip-materialized-skill.json` file referenced internally is a runtime
sentinel Paperclip writes, not an authoring input.

> Note: STEP-48 §3.6 phrased this as `skills/<name>/skill.json`. That was
> aspirational shorthand; the implemented discovery contract is `SKILL.md`
> frontmatter. This registry follows the implemented contract.

Frontmatter fields:

| Field | Required | Meaning |
| --- | --- | --- |
| `name` | yes | Skill name; must match the directory id. |
| `description` | yes | Trigger-friendly summary — when the skill should fire. |
| `required` | no (default `true`) | `false` marks the skill optional (loaded on demand, not auto-injected). |
| `version` | no | Semantic version of the skill content. |

Minimal example:

```markdown
---
name: markets-research
description: Use when researching a market, ticker, or trading signal...
required: false
version: 0.1.0
---

# Markets Research
...usage...
```

## How skills are consumed

1. **Registry → company library.** The operator imports skills into the Cortana
   Paperclip company via the company-skills import surface, using this repo's
   GitHub URL (or `org/repo/skill-id` key form). Example:
   `POST /api/companies/$COMPANY_ID/skills/import` with
   `{"source": "https://github.com/<org>/cortana-skill-registry"}`.
2. **Company library → agent.** Skills are assigned to agents via
   `desiredSkills` at hire/create, or `POST /api/agents/<id>/skills/sync`.
3. **Read-only mount.** The repo is mounted read-only into the Paperclip
   container; agents read skills but never mutate the registry from inside a run.
   Registry edits go through git on the operator's side.

## Skill-mastery convention (STEP-49 §2.1)

A skill in this registry is *shared, static* knowledge. An agent's *fluency*
with a skill — its accumulated preferences, gotchas, and worked shortcuts — is
**agent-private** and lives in that agent's Cortana vault, not here:

```
state/cortana-memory/<agent-uuid>/skill-mastery/<skill-id>.md
```

- One mastery note per skill the agent has used repeatedly. The filename's
  `<skill-id>` matches the registry directory id (e.g. `backtest-run.md`).
- The note records *this agent's* learned specifics: preferred parameters,
  recurring pitfalls, links to its own past runs — not a copy of the SKILL.md.
- Mastery notes are part of the agent's portable identity (STEP-49 §2.1: the
  skill-mastery layer). On harness migration they travel with the soul + memory
  (STEP-49 §5 step 5); the registry itself does not move with the agent.
- The registry is the *what*; the mastery note is the *how this agent does it*.

This separation keeps the registry clean and shareable while letting each agent
build private fluency over the same shared skills.

## Consolidation provenance

This registry was consolidated on 2026-05-31 from the three Cortana agent
harnesses into a single source of truth:

- **Claude / Cowork** authored skill set (56 skills) — trading, research,
  engineering, Swift, design, document, and brand-kit skills.
- **Codex** harness authored skills not in the Claude set (8): `adversarial-reviewer`,
  `agent-designer`, `agent-workflow-designer`, `chief-of-staff`, `self-improving-agent`,
  `nova-design`, `swift-nova`, `ghibli-photo`.
- **Codex / Hermes (Paperclip)** platform skills — `cortana-memory`,
  `paperclip-triage`, `cortana-troubleshooting`, `read-file`, plus the original
  seven trading/dev registry stubs.

De-duplication is by **skill id** (directory name). The only collision was
`paperclip-triage`, where the richer registry copy (v0.2.0, four reference docs)
was kept over the Claude/Cowork copy (v0.1.0). Hermes contributes no distinct
skill content of its own — its agents draw from this shared registry, so linking
Hermes means pointing it at this repo (see `HARNESS-LINKING.md`).

Vendor/marketplace plugin caches that happened to live under the Codex home
(Vercel, Supabase, Box, etc.) were intentionally **excluded** — those are
third-party plugins, not bang's authored skills.
