# Vendored Upstreams

The registry has **two lanes**. Knowing which lane a skill is in tells you how to
change it.

| Lane | Lives in | Written by | To change it |
|---|---|---|---|
| **Authored** | `skills/<name>/` | `bin/publish-skill.sh` (operator-run, from the vault inbox) | Stage to `cortana-vault/_inbox/skills/<name>/`, operator publishes |
| **Vendored** | `skills/<prefix><name>/`, generated from `vendor/<repo>/src/` | `bin/sync-upstream.sh` | You don't. Bump the pin, or fork into the authored lane |

**Vendored skills are derived artifacts.** The entire generated set is deleted and
rebuilt on every sync, so a hand-edit survives exactly until the next upgrade.
Every generated `SKILL.md` carries an HTML provenance comment saying so.

---

## Current upstreams

| Vendor | Pin | Skills | Prefix | License |
|---|---|---|---|---|
| [mattpocock/skills](https://github.com/mattpocock/skills) | `v1.2.3` (`6acc160`, 2026-08-06) | 35 | `mp-` | MIT |

Run `bin/sync-upstream.sh --list` for the live pins.

---

## Upgrading

```bash
# 1. What would change? Writes nothing.
bin/sync-upstream.sh --check mattpocock-skills

# 2. Bump to the newest release (or --tag v1.3.0 for a specific one)
bin/sync-upstream.sh --latest mattpocock-skills

# 3. Review, then propagate to the harnesses
git -C ~/Cortana/cortana-skill-registry diff --stat
./sync-skills.sh
```

`--check` prints the upstream commit log between pins, the CHANGELOG head, and the
added/removed skill delta. **Read it before bumping** — upstream renames skills
(`to-prd` → `to-spec`, `to-plan` + `to-issues` → `to-tickets`), and a rename shows
up here as one addition plus one removal.

Pins are recorded in `vendor/<name>/.upstream.json`; the generated inventory with
per-skill checksums is in `vendor/<name>/MANIFEST.json`. Both are committed, so
`git log` on them is the upgrade history.

---

## Why generated copies, not symlinks

Three constraints in this repo force it:

1. **`sync-skills.sh` enumerates `skills/*/` — top-level only.** Nesting vendored
   skills under `skills/mattpocock/` would make them invisible to Codex and Hermes.
2. **`lint-skill.sh` fails on symlinks**, and fails when frontmatter `name` differs
   from the directory name.
3. **Namespacing has to reach the `name:` field**, because that is what the harness
   routes on — a directory prefix alone would leave `code-review` colliding with the
   authored `code-review`.

So: pristine upstream in `vendor/`, real generated directories in `skills/`.

### The three transforms

Applied by `bin/lib/vendor_generate.py`, all deterministic, everything else copied
byte-for-byte:

1. frontmatter `name:` → prefixed
2. sibling slash-command references → prefixed (`/grilling` → `/mp-grilling`), so
   the skill chain still resolves. File paths are left alone — the pattern refuses
   to match when preceded by a word char, `-`, `.` or `/`, which is what keeps
   `docs/agents/triage-labels.md` and `src/triage/handler.ts` intact.
3. `agents/openai.yaml` `display_name` → tagged `[MP] …`, so the Codex picker
   distinguishes a vendored skill from ours.

**Deliberately not transformed:** `disable-model-invocation`,
`policy.allow_implicit_invocation`, descriptions, and all body prose.

---

## Vendored content is exempt from the authoring lint

`bin/lint-skill.sh` is the gate for the **authored** lane. Vendored skills are run
through it for information only — we do not hold someone else's repo to our
authoring style, and rewriting their descriptions would have to be redone on every
upgrade.

At `v1.2.3`, 20 of 35 fail our lint. **All 20 failures are exactly the 20
user-invoked skills**, all on the same rule: *"description has no trigger cues."*

That correlation is not a coincidence, and it points at a bug on our side rather
than theirs. A skill with `disable-model-invocation: true` is **never model-routed** —
it is reachable only when the user types it. Trigger cues exist so the model can
decide when to reach for a skill, so requiring them on a user-invoked skill asks for
something that can never be read. The rule should be conditional on invocation mode.

This affects the authored lane too, and is tracked as an open item — see the
Agent-Engineering Patterns MOC, **P6**.

---

## Attribution

`mattpocock/skills` is MIT-licensed. The upstream `LICENSE` and copyright notice are
preserved verbatim at `vendor/mattpocock-skills/LICENSE`, the upstream `README.md`,
`CHANGELOG.md` and `CONTEXT.md` are kept alongside the payload, and every generated
skill names its upstream repo, tag and original skill name in a provenance comment.

Upstream also ships an official Claude Code plugin
(`claude plugins install mattpocock-skills`) which auto-updates and is read-only.
We vendor instead because the plugin reaches Claude Code only — the registry has to
feed **Codex and Hermes** as well, and client work needs skills we can adapt.
Per upstream's README, do not install both: you would get every skill twice.

---

## Adding another upstream

1. `mkdir -p vendor/<name>` and write `.upstream.json`:
   ```json
   {
     "name": "<name>",
     "repo": "https://github.com/owner/repo",
     "tag": "v0.0.0",
     "commit": "",
     "license": "MIT",
     "namespace_prefix": "xx-"
   }
   ```
2. `bin/sync-upstream.sh --latest <name>`
3. Pick a prefix that cannot collide with an authored skill, and add a row to the
   table above.

The generator assumes upstream keeps skills under `skills/**/SKILL.md`. A repo with
a different layout needs `SRC` adjusted in `bin/lib/vendor_generate.py`.
