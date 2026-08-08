# PATCH — nq-snapshot: scalar-only frontmatter (2026-08-08)

**Staged for operator.** Fold into the `nq-snapshot` skill via `bin/publish-skill.sh`.
Companion migration (already applied to the 61 bloated historical files):
`cortana-vault/scripts/migrations/migrate-frontmatter-bloat-2026-08.py`.

## Problem

The skill's report template emitted essay-length YAML: `title:` held a
~1,500-word session thesis; `session_bias` / `bias_confidence` / `archetype` /
`key_observation` held multi-thousand-word prose as YAML scalars; tags included
~45 hyper-specific single-use markers (`gamma-flip-706`, `iv-rank-43`).
Worst case measured 40,339 B of YAML (69% of the file); 61 files carried
>10 KB of frontmatter (~1.32 MB of YAML total). Frontmatter is a metadata
index — Bases/Dataview only query scalars usefully — not a document body.

## Template change (the rule)

1. **Frontmatter emits scalars only.** No value may exceed ~200 characters.
   Bias is an enum, confidence is 0–100, archetype is a slug, tags ≤ 8.
2. **All prose goes to body sections** (`## Session thesis`, `## Session bias`,
   `## Bias & confidence`, `## Key observation`, …) — same content, same
   depth, just in the body where it belongs.
3. **Single-use / per-session data** (gamma flip strike, IV rank, P/C ratio,
   walls, max pain, o/n range) goes to a `## Session metrics` table in the
   body — NOT into tags and NOT into frontmatter.
4. **Tags:** emoji lead tag + reusable taxonomy tags only (a tag must be
   plausibly reusable across ≥3 sessions). Never mint value-bearing tags
   like `gamma-flip-706`.

## New frontmatter template (quote literally into the skill)

```yaml
---
title: "NQ Morning Review — {{YYYY-MM-DD}}"
type: report
report_class: macro-regime
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: active
session_date: {{YYYY-MM-DD}}
review_time_et: "{{HH:MM}}"
bias: {{long|short|neutral}}
confidence: {{0-100}}
archetype: "{{slug, e.g. a3-a4-vol-expansion-down}}"
day_type: {{trend|range|event}}
spot: {{number}}
vwap: {{number}}
gamma_regime: {{positive|negative|flip}}
tags: [🎯, nq-trading, morning-review, nq, {{up-to-4-more-reusable-tags}}]
related: ["[[{{vault-companion-wikilink}}]]"]
---
```

Hard budget: rendered frontmatter ≤ 2,000 bytes (2,500 hard cap). Omit any
field that is not cleanly determinable — never pad, never fabricate.

## New body skeleton (prose lands here)

```markdown
# NQ Morning Review — {{YYYY-MM-DD}} ({{weekday}} — {{short headline, one line}})

## Session thesis
{{the full narrative thesis that previously lived in title:}}

## Session bias
{{the full session_bias essay}}

## Bias & confidence
{{the full bias_confidence essay}}

## Key observation
{{the full key_observation essay}}

## Session metrics
| Metric | Value |
|---|---|
| Gamma flip (QQQ / NQ equiv) | {{...}} |
| Call wall / put wall | {{...}} |
| Max pain | {{...}} |
| P/C OI | {{...}} |
| IV rank | {{...}} |
| O/N range (O/H/L/last) | {{...}} |
```

## Acceptance checks for the patched skill

- `yaml.safe_load` parses the emitted frontmatter; size ≤ 2,000 B.
- No frontmatter string value > 200 chars; no list item > 200 chars.
- ≤ 8 tags, emoji first, no digits-bearing single-use tags.
- Every prose element present in the body; `## Session metrics` table present.
