---
name: research-paper-writing
title: Research Paper Writing Pipeline
description: Use when designing experiments, drafting or revising a research paper, or preparing verified submission materials. Load only the relevant phase of the detailed handbook.
version: 1.1.1
author: Orchestra Research
license: MIT
dependencies:
- semanticscholar
- arxiv
- habanero
- requests
- scipy
- numpy
- matplotlib
- SciencePlots
platforms:
- linux
- macos
metadata:
  hermes:
    tags:
    - Research
    - Paper Writing
    - Experiments
    - ML
    - AI
    - NeurIPS
    - ICML
    - ICLR
    - ACL
    - AAAI
    - COLM
    - LaTeX
    - Citations
    - Statistical Analysis
    category: research
    related_skills:
    - arxiv
    - ml-paper-writing
    - subagent-driven-development
    - plan
    requires_toolsets:
    - terminal
    - files
---

# Research paper workflow

Establish the contribution, paper type, current evidence, target audience, and requested phase. Treat all citations, results, numbers, and venue requirements as claims requiring source verification. Separate proposed experiments from executed experiments and observed results.

Read [HANDBOOK.md](HANDBOOK.md) only at the section needed for this task; do not load the full handbook by default. It stays at the package root so its existing relative resource links remain valid. The handbook preserves imported guidance, including dated/tool-specific examples that must be checked against the actual runtime.

1. Inventory the existing project, datasets, code, claims, and artifact locations.
2. Verify literature through `arxiv` or other available primary-source retrieval. Never invent citations; flag missing evidence.
3. Define experiments tied to claims, baselines, held-out data, uncertainty, seeds, costs, and reproducibility before execution.
4. Run only authorized experiments; keep configs and results auditable. Draft an accurate paper from what the evidence establishes.
5. Check claim-to-evidence coverage, citations, figures, limitations, and venue rules. Report compile/validation status separately from scientific validity.
6. Preserve authorship, submission authority, and project constraints. Submission, external communication, or parallel delegation requires applicable authorization.

Use `enterprise-knowledge-graph-research` for an operational company/industry corpus and `brand-recon` for a company dossier. Neither requires a paper lifecycle.

## Handbook navigation

- Phase 0: Project Setup
- Phase 1: Literature Review
- Phase 2: Experiment Design
- Phase 3: Experiment Execution & Monitoring
- Phase 4: Result Analysis
- Phase 5: Paper Drafting
- Phase 6: Self-Review & Revision
- Phase 7: Submission Preparation
- Citation
- Phase 8: Post-Acceptance Deliverables
- Paper Types Beyond Empirical ML
- Common Issues and Solutions
