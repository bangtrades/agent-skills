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

## Keeping agent harnesses synchronized

This repository is the only place shared skills should be created or edited.
Claude uses a direct link to `skills/`, while Codex keeps per-skill links so
its harness-managed folders (such as `.system`) remain intact. Thus changes to
an existing skill are immediately visible to both harnesses.

Run this after adding or removing a skill directory, especially before the
change is committed:

```bash
/Users/nolan/Cortana/cortana-skill-registry/sync-skills.sh
```

The repository's Git hooks also run the same command after commits, checkouts,
rewrites, and merges. The sync only replaces or removes links that point into
this registry; unrelated harness-provided skills are preserved. New skills
must be committed and pushed from this repository to reach other machines.

### Skills in this registry

As of the consolidation, this registry holds **175 skills** merged from the Codex, Claude/Cowork, and Hermes harness skill sets (de-duplicated by skill id; Hermes folded in full, including its bundled library).


**Trading & markets**

| Skill id | Purpose |
| --- | --- |
| `backtest-run` | Use when running, analyzing, or validating a trading strategy backtest — preparing data, executing a backtest, |
| `backtest-expert` | Expert guidance for systematic backtesting of trading strategies. |
| `indicator-build` | Use when building, porting, or debugging a trading indicator or charting study — Pine Script (TradingView), or |
| `markets-research` | Use when researching a market, ticker, sector, or trading signal — gathering news, sentiment, macro context, o |
| `risk-rules` | Use when sizing a position, checking risk before a trade, or enforcing drawdown / exposure limits — position s |
| `data-fetch` | Use when retrieving market data — OHLCV bars, quotes, fundamentals, or on-chain data from an exchange or data  |
| `nq-snapshot` | Capture an MTF deep-analysis snapshot of MNQ/NQ futures from live TradingView via the tradingview MCP, applyin |
| `crystal-ball` | - Capture and analyze bang's Crystal Ball (CB) fib-expansion tool on a TradingView NQ/MNQ chart — decode the T |
| `pine-script` | Use this skill whenever the user wants to write, debug, optimize, or understand Pine Script for TradingView. |
| `pre-trade-intel` | - Query bang's structured trade history before entering a new NQ/MNQ trade and return a pre-trade intelligence |
| `trade-capture` | - Convert a natural-language trade description into a fully populated structured trade file in `projects/nq-tr |
| `bt-equity` | Produce a BT Stock Report — bang's institutional-tier (Druckenmiller-style) equity research dossier on a singl |
| `stock-market-pro` | - Yahoo Finance (yfinance) powered stock analysis skill: quotes, fundamentals, ASCII trends, high-resolution c |
| `polymarket` | Query Polymarket: markets, prices, orderbooks, history. |
| `polymarketodds` | Query Polymarket prediction markets - check odds, trending markets, search events, track prices and momentum. |


**Research & recon**

| Skill id | Purpose |
| --- | --- |
| `brand-recon` | Investigate a brand or company end-to-end and emit a structured dossier + a reusable per-entity brand skill in |
| `obsidian` | Cortana knowledge engine — manages bang's Obsidian vault (`cortana-vault/`) and the parallel Reports/ output l |
| `obsidian-review` | Run a comprehensive health review of the Cortana vault — audit frontmatter, tag hygiene, link density, orphan  |
| `yt` | Process a YouTube video into a Cortana vault wiki page. |
| `rag-architect` | Use when the user asks to design RAG pipelines, optimize retrieval strategies, choose embedding models, implem |
| `product-strategist` | Strategic product leadership toolkit for Head of Product covering OKR cascade generation, quarterly planning,  |
| `arxiv` | Search arXiv papers by keyword, author, category, or ID. |
| `blogwatcher` | Monitor blogs and RSS/Atom feeds via blogwatcher-cli tool. |
| `llm-wiki` | Karpathy's LLM Wiki: build/query interlinked markdown KB. |
| `research-paper-writing` | Write ML papers for NeurIPS/ICML/ICLR: design→submit. |
| `tavily-search` | AI-optimized web search via Tavily API. |


**Agents & autonomy**

| Skill id | Purpose |
| --- | --- |
| `adversarial-reviewer` | Adversarial code review that breaks the self-review monoculture. |
| `agent-designer` | Use when the user asks to design multi-agent systems, create agent architectures, define agent communication p |
| `agent-workflow-designer` | Agent Workflow Designer |
| `self-improving` | Corrections become improvements. |
| `self-improving-agent` | Curate Claude Code's auto-memory into durable project knowledge. |
| `agent-context-reconstruction` | Reconstruct context from a legacy/previous agent home directory without leaking secrets. |
| `chief-of-staff` | C-suite orchestration layer. |
| `orchestration` | This skill should be used when the user asks to "orchestrate agents", "give me agent slices", "coordinate a co |
| `skill-creator` | Create new skills, modify and improve existing skills, and measure skill performance. |
| `consolidate-memory` | Reflective pass over your memory files — merge duplicates, fix stale facts, prune the index. |
| `claude-code` | Delegate coding to Claude Code CLI (features, PRs). |
| `codex` | Delegate coding to OpenAI Codex CLI (features, PRs). |
| `opencode` | Delegate coding to OpenCode CLI (features, PR review). |
| `hermes-agent` | Configure, extend, or contribute to Hermes Agent. |
| `hermes-agent-skill-authoring` | Author in-repo SKILL.md: frontmatter, validator, structure. |
| `kanban-codex-lane` | Use when a Hermes Kanban worker wants to run Codex CLI as an isolated implementation lane while Hermes keeps o |
| `kanban-orchestrator` | Decomposition playbook + anti-temptation rules for an orchestrator profile routing work through Kanban. |
| `kanban-worker` | Pitfalls, examples, and edge cases for Hermes Kanban workers. |
| `godmode` | Jailbreak LLMs: Parseltongue, GODMODE, ULTRAPLINIAN. |
| `native-mcp` | MCP client: connect servers, register tools (stdio/HTTP). |
| `dogfood` | Exploratory QA of web apps: find bugs, evidence, reports. |


**Cortana platform**

| Skill id | Purpose |
| --- | --- |
| `cortana-memory` | Cortana platform memory pillar — spec, contracts, operations, troubleshooting, and upgrade ceremonies. |
| `cortana-troubleshooting` | This skill should be used when the user asks to "debug Cortana", "troubleshoot Paperclip", "check the router", |
| `paperclip-triage` | This skill should be used when the user asks to "triage Paperclip", "debug Paperclip", "troubleshoot Cortana a |
| `read-file` | Read text files and list directories from the agent's workspace. |
| `paperclip-cortana-operations` | Operate and triage Cortana-on-Paperclip agency stacks: handoff review, roster activation, agent runtime readin |
| `hermes-s6-container-supervision` | Modify, debug, or extend the s6-overlay supervision tree inside the Hermes Agent Docker image — adding new ser |
| `debugging-hermes-tui-commands` | Debug Hermes TUI slash commands: Python, gateway, Ink UI. |
| `webhook-subscriptions` | Webhook subscriptions: event-driven agent runs. |


**Delivery & PM**

| Skill id | Purpose |
| --- | --- |
| `sprint-audit` | This skill should be used when the user asks to "run a sprint audit", "audit the sprint plan", "review agent s |
| `sprint-runner` | Track solo indie sprints — scaffold sprint trackers, compose per-story run summaries from git log + test outpu |
| `schedule` | Create or update a scheduled task that runs automatically. |
| `setup-cowork` | Guided Cowork setup — install role-matched plugins, connect your tools, try a skill. |
| `scrum-master` | Advanced Scrum Master skill for data-driven agile team analysis and coaching. |
| `senior-pm` | Senior Project Manager for enterprise software, SaaS, and digital transformation projects. |
| `jira-expert` | Atlassian Jira expert for creating and managing projects, planning, product discovery, JQL queries, workflows, |
| `linear` | Linear: manage issues, projects, teams via GraphQL + curl. |
| `plan` | Plan mode: write markdown plan to .hermes/plans/, no exec. |
| `writing-plans` | Write implementation plans: bite-sized tasks, paths, code. |
| `spike` | Throwaway experiments to validate an idea before build. |


**Software engineering**

| Skill id | Purpose |
| --- | --- |
| `code-review` | Use when reviewing a pull request, diff, or change set — checking correctness, security, style, and test cover |
| `code-reviewer` | Comprehensive code review skill for TypeScript, JavaScript, Python, Swift, Kotlin, Go. |
| `requesting-code-review` | Pre-commit review: security scan, quality gates, auto-fix. |
| `test-runner` | Use when running a test or smoke harness, interpreting failures, or wiring tests into a workflow — unit, integ |
| `test-driven-development` | TDD: enforce RED-GREEN-REFACTOR, tests before code. |
| `systematic-debugging` | 4-phase root cause debugging: understand bugs before fixing. |
| `subagent-driven-development` | Execute plans via delegate_task subagents (2-stage review). |
| `python-debugpy` | Debug Python: pdb REPL + debugpy remote (DAP). |
| `node-inspect-debugger` | Debug Node.js via --inspect + Chrome DevTools Protocol CLI. |
| `senior-backend` | Comprehensive backend development skill for building scalable backend systems using NodeJS, Express, Go, Pytho |
| `senior-frontend` | Comprehensive frontend development skill for building modern, performant web applications using ReactJS, NextJ |
| `senior-fullstack` | Comprehensive fullstack development skill for building complete web applications with React, Next.js, Node.js, |
| `senior-devops` | Comprehensive DevOps skill for CI/CD, infrastructure automation, containerization, and cloud platforms (AWS, G |
| `senior-data-engineer` | World-class data engineering skill for building scalable data pipelines, ETL/ELT systems, and data infrastruct |
| `senior-data-scientist` | World-class senior data scientist skill specialising in statistical modeling, experiment design, causal infere |
| `senior-qa` | Generates unit tests, integration tests, and E2E tests for React/Next.js applications. |
| `senior-prompt-engineer` | World-class prompt engineering skill for LLM optimization, prompt patterns, structured outputs, and AI product |
| `security-pen-testing` | Use when the user asks to perform security audits, penetration testing, vulnerability scanning, OWASP Top 10 c |
| `tech-stack-evaluator` | Technology stack evaluation and comparison with TCO analysis, security assessment, and ecosystem health scorin |
| `webapp-testing` | Toolkit for interacting with and testing local web applications using Playwright. |
| `pso-optimizer` | Particle Swarm Optimization (PSO) skill for algorithm design, implementation, parameter tuning, convergence an |
| `api-gateway` | | Connect to 100+ APIs (Google Workspace, Microsoft 365, Notion, Slack, Airtable, HubSpot, etc.) with managed  |
| `codebase-inspection` | Inspect codebases w/ pygount: LOC, languages, ratios. |


**GitHub ops**

| Skill id | Purpose |
| --- | --- |
| `github` | Interact with GitHub using the `gh` CLI. |
| `github-auth` | GitHub auth setup: HTTPS tokens, SSH keys, gh CLI login. |
| `github-issues` | Create, triage, label, assign GitHub issues via gh or REST. |
| `github-pr-workflow` | GitHub PR lifecycle: branch, commit, open, CI, merge. |
| `github-code-review` | Review PRs: diffs, inline comments via gh or REST. |
| `github-repo-management` | Clone/create/fork repos; manage remotes, releases. |


**Apple / Swift / devices**

| Skill id | Purpose |
| --- | --- |
| `senior-swift` | Senior Swift/SwiftUI engineering skill for writing, debugging, and fixing iOS/macOS code. |
| `swift-concurrency` | 'Diagnose data races, convert callback-based code to async/await, implement actor isolation patterns, resolve  |
| `swift-security-expert` | Use when working with iOS/macOS Keychain Services (SecItem queries, kSecClass, OSStatus errors), biometric aut |
| `swiftui-pro` | Comprehensively reviews SwiftUI code for best practices on modern APIs, maintainability, and performance. |
| `swiftui-performance-audit` | Audit and improve SwiftUI runtime performance from code review and architecture. |
| `ios-accessibility` | 'Expert guidance on iOS accessibility best practices, patterns, and implementation. |
| `swift-nova` | This skill should be used when the user asks to work on the Novai, NovaKids, NovaCompanion, or Nova v2 classro |
| `apple-notes` | Manage Apple Notes via memo CLI: create, search, edit. |
| `apple-reminders` | Apple Reminders via remindctl: add, list, complete. |
| `imessage` | Send and receive iMessages/SMS via the imsg CLI on macOS. |
| `findmy` | Track Apple devices/AirTags via FindMy.app on macOS. |
| `macos-computer-use` | | Drive the macOS desktop in the background — screenshots, mouse, keyboard, scroll, drag — without stealing th |
| `openhue` | Control Philips Hue lights, scenes, rooms via OpenHue CLI. |
| `maps` | Geocode, POIs, routes, timezones via OpenStreetMap/OSRM. |


**MLOps & models**

| Skill id | Purpose |
| --- | --- |
| `dspy` | DSPy: declarative LM programs, auto-optimize prompts, RAG. |
| `huggingface-hub` | HuggingFace hf CLI: search/download/upload models, datasets. |
| `audiocraft` | AudioCraft: MusicGen text-to-music, AudioGen text-to-sound. |
| `segment-anything` | SAM: zero-shot image segmentation via points, boxes, masks. |
| `vllm` | vLLM: high-throughput LLM serving, OpenAI API, quantization. |
| `obliteratus` | OBLITERATUS: abliterate LLM refusals (diff-in-means). |
| `llama-cpp` | llama.cpp local GGUF inference + HF Hub model discovery. |
| `lm-evaluation-harness` | lm-eval-harness: benchmark LLMs (MMLU, GSM8K, etc.). |
| `weights-and-biases` | W&B: log ML experiments, sweeps, model registry, dashboards. |
| `jupyter-live-kernel` | Iterative Python via live Jupyter kernel (hamelnb). |


**Creative & generative**

| Skill id | Purpose |
| --- | --- |
| `canvas-design` | Create beautiful visual art in .png and .pdf documents using design philosophy. |
| `frontend-design` | Create distinctive, production-grade frontend interfaces with high design quality. |
| `epic-design` | Build immersive, cinematic 2.5D interactive websites using scroll storytelling, parallax depth, text animation |
| `ui-design-system` | UI design system toolkit for Senior UI Designer including design token generation, component documentation, re |
| `nova-design` | This skill should be used when the user asks for Novai or NovaKids design, classroom UI, 2.5D art direction, a |
| `ghibli-photo` | Transform real photos into cohesive, warm, hand-painted storybook illustrations inspired by classic Japanese a |
| `superdesign` | Expert frontend design guidelines for creating beautiful, modern UIs. |
| `claude-design` | Design one-off HTML artifacts (landing, deck, prototype). |
| `design-md` | Author/validate/export Google's DESIGN.md token spec files. |
| `architecture-diagram` | Dark-themed SVG architecture/cloud/infra diagrams as HTML. |
| `excalidraw` | Hand-drawn Excalidraw JSON diagrams (arch, flow, seq). |
| `sketch` | Throwaway HTML mockups: 2-3 design variants to compare. |
| `ascii-art` | ASCII art: pyfiglet, cowsay, boxes, image-to-ascii. |
| `ascii-video` | ASCII video: convert video/audio to colored ASCII MP4/GIF. |
| `pixel-art` | Pixel art w/ era palettes (NES, Game Boy, PICO-8). |
| `p5js` | p5.js sketches: gen art, shaders, interactive, 3D. |
| `manim-video` | Manim CE animations: 3Blue1Brown math/algo videos. |
| `pretext` | Use when building creative browser demos with @chenglou/pretext — DOM-free text layout for ASCII art, typograp |
| `comfyui` | Generate images, video, and audio with ComfyUI — install, launch, manage nodes/models, run workflows with para |
| `touchdesigner-mcp` | Control a running TouchDesigner instance via twozero MCP — create operators, set parameters, wire connections, |
| `popular-web-designs` | 54 real design systems (Stripe, Linear, Vercel) as HTML/CSS. |
| `baoyu-comic` | Knowledge comics (知识漫画): educational, biography, tutorial. |
| `baoyu-infographic` | Infographics: 21 layouts x 21 styles (信息图, 可视化). |
| `baoyu-article-illustrator` | Article illustrations: type × style × palette consistency. |
| `humanizer` | Humanize text: strip AI-isms and add real voice. |
| `creative-ideation` | Generate project ideas via creative constraints. |
| `songwriting-and-ai-music` | Songwriting craft and Suno AI music prompts. |
| `nano-banana-pro` | Generate/edit images with Nano Banana Pro (Gemini 3 Pro Image). |


**Docs & productivity**

| Skill id | Purpose |
| --- | --- |
| `docx` | Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). |
| `pdf` | Use this skill whenever the user wants to do anything with PDF files. |
| `pptx` | Use this skill any time a .pptx file is involved in any way — as input, output, or both. |
| `xlsx` | Use this skill any time a spreadsheet file is the primary input or output. |
| `client-pitch` | Create client-specific AI/agentic transformation pitch packages with branded PowerPoint and matching PDF outpu |
| `powerpoint` | Create, read, edit .pptx decks, slides, notes, templates. |
| `google-workspace` | Gmail, Calendar, Drive, Docs, Sheets via gws CLI or Python. |
| `airtable` | Airtable REST API via curl. |
| `notion` | Notion API + ntn CLI: pages, databases, markdown, Workers. |
| `nano-pdf` | Edit PDF text/typos/titles via nano-pdf CLI (NL prompts). |
| `ocr-and-documents` | Extract text from PDFs/scans (pymupdf, marker-pdf). |
| `teams-meeting-pipeline` | Operate the Teams meeting summary pipeline via Hermes CLI — summarize meetings, inspect pipeline status, repla |
| `himalaya` | Himalaya CLI: IMAP/SMTP email from terminal. |


**Media & social**

| Skill id | Purpose |
| --- | --- |
| `youtube-content` | YouTube transcripts to summaries, threads, blogs. |
| `spotify` | Spotify: play, search, queue, manage playlists and devices. |
| `songsee` | Audio spectrograms/features (mel, chroma, MFCC) via CLI. |
| `heartmula` | HeartMuLa: Suno-like song generation from lyrics + tags. |
| `gif-search` | Search/download GIFs from Tenor via curl + jq. |
| `xurl` | X/Twitter via xurl CLI: post, search, DM, media, v2 API. |


**Gaming**

| Skill id | Purpose |
| --- | --- |
| `minecraft-modpack-server` | Host modded Minecraft servers (CurseForge, Modrinth). |
| `pokemon-player` | Play Pokemon via headless emulator + RAM reads. |


**Brand kits**

| Skill id | Purpose |
| --- | --- |
| `copperjoint-brand` | CopperJoint brand guide for generating consistent, on-brand documents and digital deliverables. |
| `hbef-brand` | Hermosa Beach Education Foundation (HBEF) brand guide for generating consistent, on-brand documents. |
| `hbef-fb-voice` | HBEF Facebook (and Instagram caption) voice guide — generate posts that match Hermosa Beach Education Foundati |
| `hbef-surf-report` | HBEF Surf Report voice and format guide — write HBEF's contributions to the weekly HVPTO Surf Report newslette |
| `sf-brand` | Summer Fridays brand guide for generating consistent, on-brand documents and deliverables. |
| `varian-brand` | Siemens Healthineers / Varian brand guide for generating consistent, on-brand documents and presentations. |


**Other**

| Skill id | Purpose |
| --- | --- |
| `yuanbao` | Yuanbao (元宝) groups: @mention users, query info/members. |

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
- **Hermes** harness skills folded in full (100 added) — your custom additions
  (`backtest-expert`, `stock-market-pro`, `polymarketodds`, `superdesign`, `tavily-search`,
  `nano-banana-pro`, `api-gateway`, …) plus Hermes's bundled library (apple/creative/
  mlops/productivity/media/gaming/github-ops/etc.). Hermes keeps its own curator;
  the shared set is mirrored back to it via top-level symlinks.

De-duplication is by **skill id** (directory name). The only collision was
`paperclip-triage`, where the richer registry copy (v0.2.0, four reference docs)
was kept over the Claude/Cowork copy (v0.1.0). Hermes contributes no distinct
skill content of its own — its agents draw from this shared registry, so linking
Hermes means pointing it at this repo (see `HARNESS-LINKING.md`).

Vendor/marketplace plugin caches that happened to live under the Codex home
(Vercel, Supabase, Box, etc.) were intentionally **excluded** — those are
third-party plugins, not bang's authored skills.
