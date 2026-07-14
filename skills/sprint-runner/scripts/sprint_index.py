#!/usr/bin/env python3
"""
sprint_index.py — regenerate docs/sprint-runs/index.md by scanning run summaries.

Usage:
  python sprint_index.py [--repo-root PATH] [--dry-run]

How it works:
  1. Scans docs/sprint-runs/ for files named S*.md (excluding index.md).
  2. Parses the meta block from each (**Sprint:**, **Story:**, **Landed:**, **Status:**).
  3. Extracts the first non-heading, non-meta paragraph as the one-line summary.
     Truncates at 140 chars for the table cell.
  4. Writes a sorted markdown table (newest Landed date first) to index.md.

The script is idempotent. It NEVER touches run summary files themselves — it
only regenerates the index. Re-run freely after any finish-sprint operation.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from typing import Optional


def find_repo_root(start: pathlib.Path) -> pathlib.Path:
    p = start.resolve()
    for candidate in [p, *p.parents]:
        if (candidate / ".git").exists():
            return candidate
    raise SystemExit(f"no .git ancestor found from {start}")


META_RE = re.compile(r"\*\*([A-Za-z][A-Za-z ]*):\*\*\s*(.+)")


def parse_entry(path: pathlib.Path) -> Optional[dict]:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    meta: dict[str, str] = {}
    story_id = None
    one_line = ""

    # Story ID from H1
    for ln in lines[:5]:
        m = re.match(r"#\s+(S\d+-\d+)\b\s*[—-]?\s*(.*?)(?:\s+Run Summary)?\s*$", ln.strip())
        if m:
            story_id = m.group(1)
            title_rest = m.group(2).strip(" —-")
            meta["_h1_title"] = title_rest
            break

    if not story_id:
        return None

    # Meta block — find all **Key:** value lines in first ~20 lines
    for ln in lines[:25]:
        m = META_RE.search(ln)
        if m:
            meta[m.group(1).strip().lower()] = m.group(2).strip()

    # One-line summary: first paragraph after meta that isn't a heading or HTML comment
    body_start = 0
    for i, ln in enumerate(lines):
        if META_RE.search(ln) and i < 25:
            body_start = i + 1
    for ln in lines[body_start:]:
        s = ln.strip()
        if not s:
            continue
        if s.startswith("#"):
            continue
        if s.startswith("<!--"):
            continue
        if s.startswith("**"):
            continue
        one_line = s
        break

    if len(one_line) > 140:
        one_line = one_line[:137].rstrip() + "…"

    return {
        "id": story_id,
        "filename": path.name,
        "story_title": meta.get("_h1_title") or meta.get("story", story_id),
        "landed": meta.get("landed", ""),
        "status": meta.get("status", ""),
        "one_line": one_line or "—",
    }


PREAMBLE = """# Sprint Runs Index

Rolling ledger of every run summary under `docs/sprint-runs/`, sorted newest-first. Each entry is one story's worth of actually-shipped work — the backward-looking truth, distinct from the forward-looking plan in `docs/SPRINT-N-tracker.md`.

Scan this to find the last time a module was touched, or to cite prior work when writing a new run summary.

"""


def render_index(entries: list[dict]) -> str:
    # Sort by landed desc, then by id desc as tiebreaker
    def sort_key(e: dict) -> tuple:
        landed = e.get("landed") or "0000-00-00"
        return (landed, e["id"])

    entries_sorted = sorted(entries, key=sort_key, reverse=True)

    lines = [PREAMBLE.rstrip(), ""]
    lines.append("| Run | Story | Landed | Status | Summary |")
    lines.append("|-----|-------|--------|--------|---------|")
    for e in entries_sorted:
        cell_one_line = e["one_line"].replace("|", "\\|")
        cell_title = e["story_title"].replace("|", "\\|")
        lines.append(
            f"| [{e['id']}](./{e['filename']}) "
            f"| {cell_title} "
            f"| {e['landed']} "
            f"| {e['status']} "
            f"| {cell_one_line} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", default=None, help="Repo root (default: auto-detect)")
    ap.add_argument("--dry-run", action="store_true", help="Print to stdout instead of writing")
    args = ap.parse_args()

    repo = pathlib.Path(args.repo_root) if args.repo_root else find_repo_root(pathlib.Path.cwd())
    runs_dir = repo / "docs" / "sprint-runs"
    if not runs_dir.exists():
        print(f"no sprint-runs dir at {runs_dir}", file=sys.stderr)
        return 2

    entries: list[dict] = []
    for p in sorted(runs_dir.glob("S*.md")):
        if p.name == "index.md":
            continue
        parsed = parse_entry(p)
        if parsed:
            entries.append(parsed)
        else:
            print(f"  skip (no S?-?? H1 found): {p.name}", file=sys.stderr)

    content = render_index(entries)
    if args.dry_run:
        print(content)
    else:
        target = runs_dir / "index.md"
        target.write_text(content, encoding="utf-8")
        print(f"wrote {target} ({len(entries)} runs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
