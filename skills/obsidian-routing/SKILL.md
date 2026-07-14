---
name: obsidian-routing
description: >
  Routing/filing-decision-tree portion of the existing `obsidian` skill —
  frontmatter conventions, emoji tags, cross-linking, and log-entry format —
  scoped to vault-commons and the research-commons feed only.
kind: ability
risk_tier: medium
workspace_scope: [commons, internal]
model_invocable: true
version: 1.0.0
lane: [knowledge-ops]
owner: operator
depends_on: []
eval_suite: obsidian-routing-v1
tools:
  route.tag: medium
  vault.write: medium
---

## Status: PORT-PENDING — scope-limited subset

MC-004 §7's wave-1 port table is explicit about scope: "Port only the
routing/filing-decision-tree portion of the existing `obsidian` skill
(frontmatter conventions, emoji tags, cross-linking, log-entry format) as
it applies to `vault-commons` and the research-commons feed (MC-003 §6.2).
The full personal-Cortana-vault authoring surface of the original skill is
explicitly **not** ported — that skill continues to serve Cortana outside
MetaCortex entirely (wall #1)."

**Source (not yet ported, subset only):**
`~/Projects/agency/WaiveLabs/agent-skills/skills/obsidian/SKILL.md`
— note the source skill's name is `obsidian`, not `obsidian-routing`; this
registry entry is a deliberately narrower fork, not a 1:1 rename. Only the
routing/filing decision tree named above is in scope for the port; the rest
of that skill's surface (personal Cortana vault authoring) must not be
copied here, per wall #1 (charter §0, MC-000).

**Mechanical edits required on port (MC-004 §2.4):** write targets become
`MemoryClient.put(..., workspace=<resolved>)` calls against `vault-commons`;
`vault.write` at `commons` scope is only reachable via the promotion
pipeline in production (`governance/autonomy.yaml` labels
`vault_commons.write` as `high`, gated to `g-insight-promote-pipeline`) —
this skill's own declared `vault.write` tool is scoped to the `internal`
workspace_scope entry, not a backdoor into commons.
