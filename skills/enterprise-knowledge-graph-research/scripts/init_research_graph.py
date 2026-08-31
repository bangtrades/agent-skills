#!/usr/bin/env python3
"""Initialize a compiler-enforced enterprise research graph without overwriting work."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


TRACKS = [
    "organizations",
    "market",
    "stakeholders",
    "operations",
    "artifacts",
    "technology",
    "measurement",
    "governance",
    "opportunity",
]

TYPES = [
    "organization", "person", "role", "stakeholder", "offering", "market",
    "strategy", "value-stream", "process", "decision", "artifact", "method",
    "event", "data-object", "data-source", "tool", "integration", "platform",
    "metric", "standard", "regulation", "control", "risk", "pattern", "opportunity",
]

PREDICATES = [
    "part_of", "owned_by", "performed_by", "serves", "uses", "consumes",
    "produces", "produced_by", "governed_by", "implemented_by", "sources_from",
    "stored_in", "integrates_with", "triggers", "precedes", "validates", "approves",
    "maps_to", "alternative_to", "competes_with", "measured_by", "mitigates",
    "constrains", "depends_on", "references", "automates",
]

PROFILES = {
    "company": {"entities": 150, "edges": 450, "sources": 250, "domains": 60, "opportunities": 15},
    "domain": {"entities": 200, "edges": 650, "sources": 350, "domains": 100, "opportunities": 15},
    "industry": {"entities": 250, "edges": 900, "sources": 450, "domains": 150, "opportunities": 20},
}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not slug:
        raise ValueError("target does not produce a usable slug")
    return slug


def write_new(path: Path, text: str) -> None:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def config_for(target: str, title: str, kind: str, tracks: list[str]) -> dict:
    profile = PROFILES[kind]
    return {
        "project": {
            "slug": slugify(target),
            "title": title,
            "target": target,
            "target_kind": kind,
            "created": dt.date.today().isoformat(),
        },
        "tracks": tracks,
        "types": TYPES,
        "predicates": PREDICATES,
        "evidence_classes": ["primary", "practitioner", "vendor", "secondary", "inferred"],
        "confidences": ["high", "medium", "low"],
        "statuses": ["draft", "reviewed"],
        "sensitivities": ["public", "internal", "confidential", "restricted"],
        "allowed_source_schemes": ["http", "https", "client", "urn", "file", "s3", "gs", "azure", "sharepoint", "notion", "gdrive", "slack"],
        "source_required_fields": ["title", "uri", "accessed", "source_class", "sensitivity"],
        "word_range": [200, 700],
        "minimum_outgoing_relations": 3,
        "anchor_track": tracks[0],
        "anchor_types": ["organization"],
        "vendor_high_confidence_tracks": ["technology"],
        "aliases": {},
        "opportunity": {
            "track": "opportunity" if "opportunity" in tracks else None,
            "type": "opportunity",
            "minimum_grounded_targets": 3,
            "metric_predicate": "measured_by",
            "metric_type": "metric",
            "human_gate_heading": "Human gate",
        },
        "predicate_target_types": {
            "measured_by": ["metric"],
            "produced_by": ["process"],
            "produces": ["artifact", "data-object", "metric", "event"],
            "implemented_by": ["tool", "integration", "platform", "control", "process"],
        },
        "predicate_source_types": {"produced_by": ["artifact"]},
        "acceptance": {
            "minimum_entities": profile["entities"],
            "minimum_edges": profile["edges"],
            "minimum_distinct_sources": profile["sources"],
            "minimum_distinct_public_domains": profile["domains"],
            "minimum_opportunities": profile["opportunities"],
            "minimum_primary_share": 0.35,
            "minimum_high_confidence_share": 0.55,
        },
    }


def schema_text(config: dict) -> str:
    return f"""# {config['project']['title']} — Graph authoring contract

This contract is enforced by `scripts/build_graph.py` and configured by `graph-config.json`.

## Entity files

- Store one entity in `context/<track>/<id>.md`.
- Filename equals a stable lowercase kebab-case `id`.
- Use only configured tracks, types, predicates, evidence classes, confidence values, statuses, and sensitivities.
- Write {config['word_range'][0]}–{config['word_range'][1]} body words and at least {config['minimum_outgoing_relations']} distinct grounded outgoing relations.
- Every researched entity has sources and substantive `## Open questions`.

## Required frontmatter

```yaml
---
id: example-entity
name: Example Entity
type: process
track: operations
summary: One declarative sentence describing the entity.
relations:
  - {{predicate: uses, target: another-entity}}
sources:
  - title: "Exact source title"
    uri: "https://authoritative.example/source"
    accessed: {dt.date.today().isoformat()}
    source_class: primary
    sensitivity: public
confidence: high
evidence_class: primary
sensitivity: public
anchors_observed: []
status: draft
---
```

Use `client://` or `urn:` opaque references for authorized internal evidence. Never store credentials or sensitive query strings.

## Body headings

`Operational reality` · `Systems and data` · `Decision rights and controls` · `Why it matters to the build` · `Key facts` · `Variance and contradictions` · `Open questions`

## Evidence boundaries

Separate capability, adoption, implementation, effectiveness, and entitlement. Inferred evidence cannot be high confidence. Vendor evidence may verify product capability but not organizational adoption or effectiveness. Preserve contradictions and date every source.

## Opportunity entities

Opportunity entities are graph-derived. They must name workflow, inputs, output, tools, human gate, failure risk, controls, success metric, and smallest safe experiment. An unsourced opportunity must resolve to the configured minimum number of sourced non-opportunity entities and a live metric.
"""


def brief_text(config: dict) -> str:
    project = config["project"]
    return f"""# {project['title']} — Project brief

## Target

- Target: {project['target']}
- Kind: {project['target_kind']}
- Created: {project['created']}

## Downstream purpose

Record the client, product, operating, security, compliance, and decision uses this graph must support before dispatching research.

## Scope and exclusions

Define organizations, products, geographies, time horizon, regulated activities, and explicit exclusions. Boundary cases must be recorded rather than silently normalized.

## Enterprise boundary

Record users, environments, data classes, systems, authorization, retention, residency, legal or contractual restrictions, and required assurance.

## Authorized evidence and tools

List public sources, permissioned internal sources, interviews, repositories, connectors, retrieval tools, and any time or spend limits.

## Operating surfaces

Name the 3–7 workflows or decision surfaces the graph must support.

## Acceptance profile

This scaffold uses the `{project['target_kind']}` profile. Edit thresholds in `graph-config.json` before the fleet begins if the documented scope requires a different contract.
"""


def readme_text(config: dict) -> str:
    title = config["project"]["title"]
    return f"""# {title}

Compiler-enforced enterprise research graph.

## Loading order

1. `PROJECT-BRIEF.md`
2. `SCHEMA.md`
3. `UNIVERSE.md` when created
4. `context/graph/manifest.json`
5. `SYNTHESIS.md` and supporting deliverables when completed

## Build

```sh
python3 scripts/build_graph.py --root .
python3 scripts/build_graph.py --root . --strict
python3 scripts/build_graph_viz.py --root .
```

Strict mode enforces the acceptance profile in `graph-config.json`. A passing compiler validates structure and configured thresholds; it does not certify regulatory compliance, SOC 2 conformity, business accuracy, or production readiness.
"""


def reservations_text() -> str:
    return """# Entity reservations

Append one row before writing an entity. IDs are immutable after completion.

| id | track | owner | status | note |
|---|---|---|---|---|
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--target", required=True)
    parser.add_argument("--title")
    parser.add_argument("--target-kind", choices=sorted(PROFILES), required=True)
    parser.add_argument("--tracks", help="comma-separated ownership tracks")
    args = parser.parse_args(argv)

    output = args.output.expanduser().resolve()
    if output.exists() and any(output.iterdir()):
        parser.error(f"output is not empty; refusing to overwrite: {output}")
    output.mkdir(parents=True, exist_ok=True)

    tracks = [x.strip() for x in args.tracks.split(",") if x.strip()] if args.tracks else list(TRACKS)
    if len(tracks) != len(set(tracks)) or any(not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", x) for x in tracks):
        parser.error("tracks must be unique lowercase kebab-case names")
    title = args.title or f"{args.target} Enterprise Knowledge Graph"
    config = config_for(args.target, title, args.target_kind, tracks)

    for track in tracks:
        (output / "context" / track).mkdir(parents=True, exist_ok=True)
    (output / "context" / "graph").mkdir(parents=True, exist_ok=True)
    (output / "outputs").mkdir(parents=True, exist_ok=True)
    (output / "scripts").mkdir(parents=True, exist_ok=True)

    write_new(output / "graph-config.json", json.dumps(config, indent=2) + "\n")
    write_new(output / "PROJECT-BRIEF.md", brief_text(config))
    write_new(output / "SCHEMA.md", schema_text(config))
    write_new(output / "README.md", readme_text(config))
    write_new(output / "context" / "graph" / "RESERVATIONS.md", reservations_text())

    here = Path(__file__).resolve().parent
    for name in ("build_graph.py", "build_graph_viz.py"):
        source = here / name
        if not source.exists():
            raise FileNotFoundError(f"missing companion script: {source}")
        shutil.copy2(source, output / "scripts" / name)

    probe = subprocess.run(
        [sys.executable, str(output / "scripts" / "build_graph.py"), "--root", str(output)],
        text=True,
        capture_output=True,
        check=False,
    )
    if probe.returncode:
        print(probe.stdout, end="")
        print(probe.stderr, end="", file=sys.stderr)
        return probe.returncode
    print(f"Initialized {output}")
    print(probe.stdout.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
