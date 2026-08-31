#!/usr/bin/env python3
"""Compile and validate a config-driven Markdown enterprise knowledge graph."""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse


def load_yaml(text: str) -> dict:
    try:
        import yaml  # type: ignore
    except ModuleNotFoundError:
        yaml = None
    if yaml is not None:
        value = yaml.safe_load(text)
    else:
        ruby = (
            "require 'yaml'; require 'json'; require 'date'; "
            "v=YAML.safe_load(STDIN.read, permitted_classes:[Date], aliases:false); "
            "STDOUT.write(JSON.generate(v))"
        )
        proc = subprocess.run(["ruby", "-e", ruby], input=text, text=True, capture_output=True, check=False)
        if proc.returncode:
            raise ValueError(f"YAML parser unavailable or malformed YAML: {proc.stderr.strip()}")
        value = json.loads(proc.stdout)
    if not isinstance(value, dict):
        raise ValueError("frontmatter must be a mapping")
    return value


def parse_markdown(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", text, re.S)
    if not match:
        raise ValueError("missing or malformed YAML frontmatter")
    frontmatter, body = match.groups()
    return load_yaml(frontmatter), body.strip()


def body_word_count(body: str) -> int:
    prose = re.sub(r"https?://\S+|\[\[|\]\]|[`#*_>|{}\[\]()]", " ", body)
    return len(re.findall(r"\b[\w'-]+\b", prose))


def substantive_section(body: str, heading: str, minimum_words: int = 4) -> bool:
    pattern = rf"^##+\s+{re.escape(heading)}\s*$\n(.*?)(?=^##+\s|\Z)"
    match = re.search(pattern, body, re.M | re.S | re.I)
    if not match:
        return False
    text = re.sub(r"^\s*[-*+]\s+", "", match.group(1), flags=re.M).strip()
    placeholders = {"", "none", "n/a", "na", "tbd", "todo", "unknown", "-", "?"}
    return text.lower().strip(". ") not in placeholders and len(re.findall(r"\w+", text)) >= minimum_words


def canonical(entity_id: str, aliases: dict[str, str]) -> str:
    seen: set[str] = set()
    while entity_id in aliases:
        if entity_id in seen:
            return entity_id
        seen.add(entity_id)
        entity_id = aliases[entity_id]
    return entity_id


def source_domain(uri: str) -> str:
    parsed = urlparse(uri)
    if parsed.scheme not in {"http", "https"}:
        return ""
    host = (parsed.hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def iso_date(value: object) -> bool:
    try:
        dt.date.fromisoformat(str(value))
        return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(value)))
    except ValueError:
        return False


def load_config(root: Path) -> dict:
    path = root / "graph-config.json"
    if not path.exists():
        raise FileNotFoundError(f"missing {path}")
    config = json.loads(path.read_text(encoding="utf-8"))
    required = ["tracks", "types", "predicates", "evidence_classes", "confidences", "statuses", "sensitivities", "word_range", "acceptance"]
    missing = [key for key in required if key not in config]
    if missing:
        raise ValueError(f"graph-config.json missing keys: {', '.join(missing)}")
    return config


def compile_graph(root: Path, strict: bool = False) -> tuple[int, list[str]]:
    config = load_config(root)
    graph = root / "context" / "graph"
    graph.mkdir(parents=True, exist_ok=True)
    tracks = set(config["tracks"])
    types = set(config["types"])
    predicates = set(config["predicates"])
    evidence_classes = set(config["evidence_classes"])
    confidences = set(config["confidences"])
    statuses = set(config["statuses"])
    sensitivities = set(config["sensitivities"])
    source_fields = list(config.get("source_required_fields", ["title", "uri", "accessed", "source_class", "sensitivity"]))
    schemes = set(config.get("allowed_source_schemes", ["http", "https", "client", "urn"]))
    minimum_relations = int(config.get("minimum_outgoing_relations", 3))
    low_words, high_words = map(int, config.get("word_range", [200, 700]))
    aliases = dict(config.get("aliases", {}))

    paths = sorted(
        path for path in (root / "context").glob("*/*.md")
        if path.parent != graph and path.name not in {"SCHEMA.md", "README.md", "_index.md"}
    )
    errors: list[str] = []
    records: list[dict] = []
    raw_ids: set[str] = set()

    for path in paths:
        rel = path.relative_to(root).as_posix()
        try:
            front, body = parse_markdown(path)
        except Exception as exc:
            errors.append(f"{rel}: {exc}")
            continue
        entity_id = front.get("id")
        if not isinstance(entity_id, str) or not entity_id:
            errors.append(f"{rel}: missing non-empty string id")
            entity_id = path.stem
        if entity_id != path.stem:
            errors.append(f"{rel}: id {entity_id!r} does not equal filename stem {path.stem!r}")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", entity_id):
            errors.append(f"{rel}: id is not lowercase kebab-case: {entity_id!r}")
        if entity_id in raw_ids:
            errors.append(f"{rel}: duplicate id {entity_id!r}")
        raw_ids.add(entity_id)

        track = front.get("track")
        entity_type = front.get("type")
        if track not in tracks:
            errors.append(f"{rel}: invalid track {track!r}")
        if track != path.parent.name:
            errors.append(f"{rel}: track {track!r} does not match parent {path.parent.name!r}")
        if entity_type not in types:
            errors.append(f"{rel}: invalid type {entity_type!r}")
        if front.get("evidence_class") not in evidence_classes:
            errors.append(f"{rel}: invalid evidence_class {front.get('evidence_class')!r}")
        if front.get("confidence") not in confidences:
            errors.append(f"{rel}: invalid confidence {front.get('confidence')!r}")
        if front.get("status") not in statuses:
            errors.append(f"{rel}: invalid status {front.get('status')!r}")
        if front.get("sensitivity") not in sensitivities:
            errors.append(f"{rel}: invalid sensitivity {front.get('sensitivity')!r}")
        for field in ("name", "summary"):
            if not isinstance(front.get(field), str) or not front[field].strip():
                errors.append(f"{rel}: missing non-empty {field}")

        clean_relations: list[dict] = []
        relations = front.get("relations")
        if not isinstance(relations, list):
            errors.append(f"{rel}: relations must be a list")
            relations = []
        for index, relation in enumerate(relations):
            if not isinstance(relation, dict) or set(relation) != {"predicate", "target"}:
                errors.append(f"{rel}: relation[{index}] must contain only predicate and target")
                continue
            predicate, target = relation.get("predicate"), relation.get("target")
            if predicate not in predicates:
                errors.append(f"{rel}: relation[{index}] invalid predicate {predicate!r}")
            if not isinstance(target, str) or not target:
                errors.append(f"{rel}: relation[{index}] target must be a non-empty string")
                continue
            clean_relations.append({"predicate": predicate, "target": target, "index": index})

        clean_sources: list[dict] = []
        sources = front.get("sources")
        if not isinstance(sources, list):
            errors.append(f"{rel}: sources must be a list")
            sources = []
        for index, source in enumerate(sources):
            if not isinstance(source, dict):
                errors.append(f"{rel}: source[{index}] must be a mapping")
                continue
            missing = [field for field in source_fields if source.get(field) in {None, ""}]
            if missing:
                errors.append(f"{rel}: source[{index}] missing {', '.join(missing)}")
                continue
            uri = str(source["uri"])
            parsed = urlparse(uri)
            if parsed.scheme not in schemes:
                errors.append(f"{rel}: source[{index}] uses disallowed or missing URI scheme: {parsed.scheme!r}")
            if parsed.scheme in {"http", "https"} and not parsed.netloc:
                errors.append(f"{rel}: source[{index}] is not a valid HTTP(S) URI")
            if not iso_date(source["accessed"]):
                errors.append(f"{rel}: source[{index}] accessed must be YYYY-MM-DD")
            if source.get("source_class") not in evidence_classes:
                errors.append(f"{rel}: source[{index}] invalid source_class {source.get('source_class')!r}")
            if source.get("sensitivity") not in sensitivities:
                errors.append(f"{rel}: source[{index}] invalid sensitivity {source.get('sensitivity')!r}")
            clean_sources.append({key: str(value) for key, value in source.items()})

        anchors = front.get("anchors_observed", [])
        if not isinstance(anchors, list) or any(not isinstance(value, str) for value in anchors):
            errors.append(f"{rel}: anchors_observed must be a list of ids")
            anchors = []
        count = body_word_count(body)
        if not low_words <= count <= high_words:
            errors.append(f"{rel}: body word count {count} is outside required {low_words}–{high_words} range")
        if not substantive_section(body, "Open questions"):
            errors.append(f"{rel}: Open questions must contain substantive content")
        if front.get("evidence_class") == "inferred" and front.get("confidence") == "high":
            errors.append(f"{rel}: inferred evidence cannot have high confidence")
        vendor_tracks = set(config.get("vendor_high_confidence_tracks", []))
        if front.get("evidence_class") == "vendor" and track not in vendor_tracks and front.get("confidence") == "high":
            errors.append(f"{rel}: vendor evidence outside configured capability tracks cannot have high confidence")

        front.update({"relations": clean_relations, "sources": clean_sources, "anchors_observed": anchors})
        records.append({**front, "raw_id": entity_id, "body": body, "file": rel, "word_count": count})

    for key, target in aliases.items():
        if not isinstance(key, str) or not isinstance(target, str) or not key or not target:
            errors.append(f"aliases: keys and targets must be non-empty strings: {key!r} -> {target!r}")
            continue
        if key in raw_ids:
            errors.append(f"aliases: retired id {key!r} is still a live entity")
        seen: set[str] = set()
        current = key
        while current in aliases:
            if current in seen:
                errors.append(f"aliases: cycle involving {current!r}")
                break
            seen.add(current)
            current = aliases[current]
        if current not in raw_ids:
            errors.append(f"aliases: target for {key!r} does not resolve: {current!r}")

    aliases_safe = {} if any(error.startswith("aliases: cycle") for error in errors) else aliases
    for record in records:
        record["id"] = canonical(record.pop("raw_id"), aliases_safe)
        record["anchors_observed"] = [canonical(value, aliases_safe) for value in record["anchors_observed"]]
        for relation in record["relations"]:
            relation["target"] = canonical(relation["target"], aliases_safe)

    for entity_id, count in collections.Counter(record["id"] for record in records).items():
        if count > 1:
            errors.append(f"canonical id collision after aliases: {entity_id}")
    by_id = {record["id"]: record for record in records}
    id_set = set(by_id)

    anchor_track = config.get("anchor_track")
    anchor_types = set(config.get("anchor_types", []))
    anchor_ids = {
        record["id"] for record in records
        if record.get("track") == anchor_track and (not anchor_types or record.get("type") in anchor_types)
    }
    for record in records:
        for anchor in record["anchors_observed"]:
            if anchor not in anchor_ids:
                errors.append(f"{record['file']}: anchors_observed target does not resolve to an anchor: {anchor}")

    edges: list[dict] = []
    for record in records:
        seen: dict[tuple[str, str], int] = {}
        for relation in record["relations"]:
            key = (relation["predicate"], relation["target"])
            if key in seen:
                errors.append(f"{record['file']}: duplicate relation[{seen[key]}] and relation[{relation['index']}]")
            seen[key] = relation["index"]
            if relation["target"] == record["id"]:
                errors.append(f"{record['file']}: self-edge relation[{relation['index']}]")
            edges.append({"source": record["id"], "predicate": relation["predicate"], "target": relation["target"], "file": record["file"], "index": relation["index"]})
        valid = {(edge["predicate"], edge["target"]) for edge in record["relations"] if edge["target"] in id_set and edge["target"] != record["id"]}
        if len(valid) < minimum_relations:
            errors.append(f"{record['file']}: requires at least {minimum_relations} valid distinct outgoing relations; found {len(valid)}")

    edge_map = {(edge["source"], edge["predicate"], edge["target"]): edge for edge in edges}
    mirrored: set[tuple] = set()
    for edge in edges:
        candidates = [(edge["target"], edge["predicate"], edge["source"])]
        if edge["predicate"] == "produces":
            candidates.append((edge["target"], "produced_by", edge["source"]))
        if edge["predicate"] == "produced_by":
            candidates.append((edge["target"], "produces", edge["source"]))
        for candidate in candidates:
            other = edge_map.get(candidate)
            if other:
                pair = tuple(sorted(((edge["file"], edge["index"]), (other["file"], other["index"]))))
                if pair not in mirrored:
                    mirrored.add(pair)
                    errors.append(f"prohibited mirrored edges: {edge['source']} --{edge['predicate']}--> {edge['target']}")

    target_rules = config.get("predicate_target_types", {})
    source_rules = config.get("predicate_source_types", {})
    for edge in edges:
        source, target = by_id.get(edge["source"]), by_id.get(edge["target"])
        if target and edge["predicate"] in target_rules and target.get("type") not in set(target_rules[edge["predicate"]]):
            errors.append(f"{edge['file']}: {edge['predicate']} target {target['id']!r} has invalid type {target.get('type')!r}")
        if source and edge["predicate"] in source_rules and source.get("type") not in set(source_rules[edge["predicate"]]):
            errors.append(f"{edge['file']}: {edge['predicate']} source {source['id']!r} has invalid type {source.get('type')!r}")

    opportunity_cfg = config.get("opportunity", {})
    opportunity_track = opportunity_cfg.get("track")
    opportunity_type = opportunity_cfg.get("type", "opportunity")
    opportunity_ids: list[str] = []
    for record in records:
        if not opportunity_track or record.get("track") != opportunity_track:
            continue
        opportunity_ids.append(record["id"])
        if record.get("type") != opportunity_type:
            errors.append(f"{record['file']}: opportunity track requires type {opportunity_type!r}")
        if record.get("evidence_class") != "inferred":
            errors.append(f"{record['file']}: opportunity entities must use evidence_class inferred")
        heading = opportunity_cfg.get("human_gate_heading", "Human gate")
        if not substantive_section(record["body"], heading, minimum_words=6):
            errors.append(f"{record['file']}: opportunity requires substantive ## {heading}")
        metric_predicate = opportunity_cfg.get("metric_predicate", "measured_by")
        metric_type = opportunity_cfg.get("metric_type", "metric")
        if not any(
            relation["predicate"] == metric_predicate
            and relation["target"] in by_id
            and by_id[relation["target"]].get("type") == metric_type
            for relation in record["relations"]
        ):
            errors.append(f"{record['file']}: opportunity requires a {metric_predicate} relation to type {metric_type}")
        if not record["sources"]:
            grounded = {
                relation["target"] for relation in record["relations"]
                if relation["target"] in by_id
                and by_id[relation["target"]].get("track") != opportunity_track
                and by_id[relation["target"]].get("sources")
            }
            minimum = int(opportunity_cfg.get("minimum_grounded_targets", 3))
            if len(grounded) < minimum:
                errors.append(f"{record['file']}: unsourced opportunity requires {minimum} distinct sourced non-opportunity targets; found {len(grounded)}")

    dangling = sorted({edge["target"] for edge in edges if edge["target"] not in id_set})
    connected = {edge["source"] for edge in edges} | {edge["target"] for edge in edges if edge["target"] in id_set}
    orphans = sorted(id_set - connected)
    unsourced = sorted(
        record["id"] for record in records
        if not record["sources"] and record.get("track") != opportunity_track
    )
    missing_questions = sorted(record["id"] for record in records if not substantive_section(record["body"], "Open questions"))
    out_of_range = sorted(record["id"] for record in records if not low_words <= record["word_count"] <= high_words)
    all_uris = sorted({source["uri"] for record in records for source in record["sources"]})
    domains = sorted({domain for uri in all_uris if (domain := source_domain(uri))})
    by_track = collections.Counter(record.get("track", "<missing>") for record in records)
    by_type = collections.Counter(record.get("type", "<missing>") for record in records)
    by_evidence = collections.Counter(record.get("evidence_class", "<missing>") for record in records)
    by_confidence = collections.Counter(record.get("confidence", "<missing>") for record in records)
    indegree = collections.Counter(edge["target"] for edge in edges if edge["target"] in id_set)

    acceptance = config.get("acceptance", {})
    primary_share = by_evidence.get("primary", 0) / len(records) if records else 0.0
    high_share = by_confidence.get("high", 0) / len(records) if records else 0.0
    checks = [
        ("entities", len(records), int(acceptance.get("minimum_entities", 0)), ">="),
        ("edges", len(edges), int(acceptance.get("minimum_edges", 0)), ">="),
        ("distinct sources", len(all_uris), int(acceptance.get("minimum_distinct_sources", 0)), ">="),
        ("distinct public domains", len(domains), int(acceptance.get("minimum_distinct_public_domains", 0)), ">="),
        ("opportunities", len(opportunity_ids), int(acceptance.get("minimum_opportunities", 0)), ">="),
        ("primary share", primary_share, float(acceptance.get("minimum_primary_share", 0)), ">="),
        ("high-confidence share", high_share, float(acceptance.get("minimum_high_confidence_share", 0)), ">="),
    ]
    acceptance_failures = [f"acceptance: {name} {actual:.3g} is below {threshold:.3g}" for name, actual, threshold, _ in checks if actual < threshold]
    if strict:
        errors.extend(f"strict: dangling target {item}" for item in dangling)
        errors.extend(f"strict: orphan entity {item}" for item in orphans)
        errors.extend(f"strict: unsourced researched entity {item}" for item in unsourced)
        errors.extend(acceptance_failures)

    clean_edges = [{key: edge[key] for key in ("source", "predicate", "target")} for edge in edges]
    entities = {}
    for record in sorted(records, key=lambda item: item["id"]):
        emitted = {key: value for key, value in record.items() if key != "relations"}
        emitted["relations"] = [{key: relation[key] for key in ("predicate", "target")} for relation in record["relations"]]
        entities[record["id"]] = emitted
    manifest = {
        record["id"]: {key: record.get(key) for key in ("name", "type", "track", "summary", "sensitivity", "file")}
        for record in sorted(records, key=lambda item: item["id"])
    }
    (graph / "entities.json").write_text(json.dumps(entities, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (graph / "edges.json").write_text(json.dumps(clean_edges, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (graph / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def bullets(items: list[str]) -> str:
        return "\n".join(f"- `{item}`" for item in items) if items else "- None"

    def table(counter: collections.Counter) -> str:
        return "\n".join(f"| {key} | {value} |" for key, value in sorted(counter.items())) or "| — | 0 |"

    check_rows = []
    for name, actual, threshold, operator in checks:
        display_actual = f"{actual:.1%}" if "share" in name else str(actual)
        display_threshold = f"{threshold:.1%}" if "share" in name else str(threshold)
        check_rows.append(f"| {name} | {operator} {display_threshold} | {display_actual} | {'PASS' if actual >= threshold else 'FAIL'} |")
    report = f"""# Knowledge graph validation report

Generated {dt.datetime.now(dt.timezone.utc).isoformat()} by `scripts/build_graph.py`.

## Summary

- Entities: **{len(records)}**
- Directed edges: **{len(edges)}**
- Distinct source records: **{len(all_uris)}**
- Distinct public domains: **{len(domains)}**
- Primary evidence share: **{primary_share:.1%}**
- High-confidence share: **{high_share:.1%}**
- Structural errors: **{len(errors)}**
- Dangling targets: **{len(dangling)}**
- Orphans: **{len(orphans)}**
- Unsourced researched entities: **{len(unsourced)}**
- Missing substantive open questions: **{len(missing_questions)}**
- Entities outside {low_words}–{high_words} words: **{len(out_of_range)}**

## Acceptance profile

| Gate | Threshold | Actual | Result |
|---|---:|---:|:---:|
{chr(10).join(check_rows)}

## Errors

{bullets(sorted(set(errors)))}

## Dangling targets

{bullets(dangling)}

## Orphans

{bullets(orphans)}

## Counts by track

| Track | Count |
|---|---:|
{table(by_track)}

## Counts by type

| Type | Count |
|---|---:|
{table(by_type)}

## Counts by evidence class

| Evidence class | Count |
|---|---:|
{table(by_evidence)}

## Counts by confidence

| Confidence | Count |
|---|---:|
{table(by_confidence)}

## Top graph hubs by in-degree

| Entity | In-degree |
|---|---:|
{table(collections.Counter(dict(indegree.most_common(20))))}
"""
    (graph / "REPORT.md").write_text(report, encoding="utf-8")

    unique_errors = sorted(set(errors))
    if unique_errors:
        print(f"FAIL: {len(unique_errors)} violation(s); see {graph / 'REPORT.md'}", file=sys.stderr)
        return 1, unique_errors
    mode = "strict" if strict else "iterative"
    print(f"PASS {mode}: {len(records)} entities, {len(edges)} edges, {len(all_uris)} sources; acceptance gaps: {len(acceptance_failures)}")
    return 0, []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)
    try:
        return compile_graph(args.root.expanduser().resolve(), strict=args.strict)[0]
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
