#!/usr/bin/env python3
"""
run_summary.py — generate a draft run summary from git log + diff stat.

Usage:
  python run_summary.py --story S10-12 --from f5f304e --to f16186a \
      [--title "Skill-engine wiring"] [--sprint 10] [--pts 8] \
      [--slug skill-engine-s10-12] [--repo-root PATH] \
      [--has-ui] [--has-http-api] [--has-flags] \
      [--retires "S9-11"] [--out <path>]

What it does:
  1. Runs `git log --oneline` between the refs (inclusive of --to, exclusive of --from).
  2. Runs `git diff --numstat` to collect per-file LOC deltas.
  3. Renders the run-summary template with prose placeholders (<!-- FILL: ... -->).
  4. Writes to docs/sprint-runs/S{N}-{XX}-{slug}.md (or --out).

It does NOT fill in prose. That's Claude's job after reading the draft.
It does NOT overwrite an existing run summary without --force.

The output is intentionally "structured skeleton" — meta block complete, files
changed list populated, prose sections left as <!-- FILL --> comments for the
model to replace with actual technical narrative.
"""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import re
import subprocess
import sys
import textwrap


def find_repo_root(start: pathlib.Path) -> pathlib.Path:
    p = start.resolve()
    for candidate in [p, *p.parents]:
        if (candidate / ".git").exists():
            return candidate
    raise SystemExit(f"no .git ancestor found from {start}")


def git(repo: pathlib.Path, *args: str) -> str:
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed:\n{r.stderr}")
    return r.stdout


def collect_commits(repo: pathlib.Path, from_sha: str, to_sha: str) -> list[tuple[str, str]]:
    out = git(repo, "log", "--pretty=%h %s", f"{from_sha}..{to_sha}")
    lines = [ln for ln in out.strip().splitlines() if ln.strip()]
    commits = []
    for ln in lines:
        parts = ln.split(" ", 1)
        if len(parts) == 2:
            commits.append((parts[0], parts[1]))
    return commits


def collect_numstat(repo: pathlib.Path, from_sha: str, to_sha: str) -> list[tuple[str, int, int]]:
    out = git(repo, "diff", "--numstat", f"{from_sha}..{to_sha}")
    rows = []
    for ln in out.strip().splitlines():
        parts = ln.split("\t")
        if len(parts) != 3:
            continue
        add, rm, path = parts
        try:
            adds = int(add)
            rms = int(rm)
        except ValueError:
            # binary file
            adds = rms = 0
        rows.append((path, adds, rms))
    return rows


def file_status(repo: pathlib.Path, from_sha: str, to_sha: str) -> dict[str, str]:
    """Map path → 'new' | 'edited' | 'deleted' | 'renamed'."""
    out = git(repo, "diff", "--name-status", f"{from_sha}..{to_sha}")
    result: dict[str, str] = {}
    for ln in out.strip().splitlines():
        parts = ln.split("\t")
        if not parts:
            continue
        code = parts[0][0] if parts[0] else "M"
        status = {
            "A": "new",
            "M": "edited",
            "D": "deleted",
            "R": "renamed",
            "C": "copied",
        }.get(code, "edited")
        path = parts[-1]
        result[path] = status
    return result


def slugify(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s or "run"


def parse_story_id(story: str) -> tuple[int, int]:
    m = re.match(r"S(\d+)-(\d+)", story)
    if not m:
        raise SystemExit(f"story id must look like S10-12, got {story!r}")
    return int(m.group(1)), int(m.group(2))


def render(
    *,
    story: str,
    title: str,
    sprint_n: int,
    pts: str,
    retires: str | None,
    files: list[tuple[str, str, int, int]],
    commits: list[tuple[str, str]],
    loc_total: int,
    from_sha: str,
    to_sha: str,
    has_ui: bool,
    has_http_api: bool,
    has_flags: bool,
    landed: str,
) -> str:
    meta = [f"**Sprint:** {sprint_n}", f"**Story:** {story} ({pts} pts)"]
    if retires:
        meta.append(f"**Retires:** {retires}")
    meta.append(f"**Landed:** {landed}")
    meta.append(f"**Status:** ✅ Done")

    shipped_lines = []
    for path, status, adds, rms in files:
        delta = f"+{adds}/-{rms}" if (adds or rms) else "binary"
        shipped_lines.append(f"- `{path}` ({status}, {delta})")
    shipped_block = "\n".join(shipped_lines) if shipped_lines else "- _no file changes detected in range_"

    commit_block = "\n".join(f"- `{sha}` {msg}" for sha, msg in commits) or "- _no commits in range_"

    out = [f"# {story} — {title} Run Summary", ""]
    out.append("\n".join(meta))
    out.append("")
    out.append(
        "<!-- FILL: Opening paragraph — 2–4 sentences. What's the context? "
        "What prior runs does this build on? Why did this story matter to the sprint goal? "
        f"Link prior runs as `[S{sprint_n}-XX](./SN-XX-slug.md)`. -->"
    )
    out.append("")
    out.append("## What shipped")
    out.append("")
    out.append(shipped_block)
    out.append("")
    out.append(
        "<!-- FILL: 1–2 sentences per cluster of files. Group by module if there are more than ~8 files. "
        "Call out any file that's new and any test file with its test-count delta like (+7 tests, 23 → 30). -->"
    )
    out.append("")
    out.append("## Architectural decisions")
    out.append("")
    out.append(
        "<!-- FILL: Numbered list. Every decision must answer \"why X over Y\". "
        "If there are no non-trivial decisions (rare), delete this section entirely rather than padding it. -->"
    )
    out.append("")
    out.append("## Quick-start runbook (bang's Mac)")
    out.append("")
    out.append("```bash")
    out.append("# FILL: numbered steps with `# expect:` annotations")
    out.append("```")
    out.append("")
    out.append("## Validation matrix")
    out.append("")
    out.append("| Check | Where | Status | Notes |")
    out.append("|-------|-------|--------|-------|")
    out.append("| _fill in_ | sandbox | ✅ | _what ran here_ |")
    out.append("| _fill in_ | bang's Mac | 🟡 | _requires local validation_ |")
    out.append("")
    out.append("### Prerequisites bang must run on his Mac")
    out.append("")
    out.append("```bash")
    out.append("# FILL: bash block for anything that couldn't run in the sandbox")
    out.append("```")
    out.append("")
    if has_ui:
        out.append("## End-to-end Dev Console walkthrough")
        out.append("")
        out.append(
            "<!-- FILL: Numbered steps a tester would follow in the Dev Console UI. "
            "Include expected state transitions and any gotchas. -->"
        )
        out.append("")
    if has_http_api:
        out.append("## curl cheat sheet")
        out.append("")
        out.append("```bash")
        out.append("# FILL: real curl commands piped through jq with # expected: annotations")
        out.append("```")
        out.append("")
    if has_flags:
        out.append("## Feature-flag matrix")
        out.append("")
        out.append("| Flag | Default | Effect when on | Effect when off |")
        out.append("|------|---------|----------------|-----------------|")
        out.append("| _fill in_ | off | _..._ | _..._ |")
        out.append("")
    if retires:
        out.append("## Debt retired")
        out.append("")
        out.append(
            f"<!-- FILL: For each of {retires}, a short section: "
            "### S?-XX — <Title> / 1–2 sentences on what was wrong and how this run fixed it. -->"
        )
        out.append("")
    out.append("## What's next")
    out.append("")
    out.append(
        "<!-- FILL: 1–3 bullets on the next logical step. Don't over-commit — "
        "this is a preview, not a plan. -->"
    )
    out.append("")
    out.append("## Cross-references")
    out.append("")
    out.append(
        "<!-- FILL: Links to prior run summaries, related ADRs, external docs. -->"
    )
    out.append("")
    out.append("## Commits in this range")
    out.append("")
    out.append(commit_block)
    out.append("")
    out.append("---")
    out.append("")
    out.append(
        f"*Generated by sprint-runner skill. Git range: `{from_sha}..{to_sha}` "
        f"({len(commits)} commits, {loc_total} LOC).*"
    )
    out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--story", required=True, help="Story ID like S10-12")
    ap.add_argument("--from", dest="from_sha", required=True, help="Starting git ref (exclusive)")
    ap.add_argument("--to", dest="to_sha", default="HEAD", help="Ending git ref (default HEAD)")
    ap.add_argument("--title", default=None, help="Human-readable title; default derived from story ID")
    ap.add_argument("--sprint", type=int, default=None, help="Sprint number; default inferred from story")
    ap.add_argument("--pts", default="?", help="Story points")
    ap.add_argument("--slug", default=None, help="Filename slug; default from title")
    ap.add_argument("--retires", default=None, help="Comma-separated list of carry-in stories retired")
    ap.add_argument("--has-ui", action="store_true", help="Include Dev Console walkthrough section")
    ap.add_argument("--has-http-api", action="store_true", help="Include curl cheat sheet section")
    ap.add_argument("--has-flags", action="store_true", help="Include feature-flag matrix section")
    ap.add_argument("--repo-root", default=None, help="Repo root (default: auto-detect)")
    ap.add_argument("--out", default=None, help="Output path override")
    ap.add_argument("--force", action="store_true", help="Overwrite existing summary")
    args = ap.parse_args()

    repo = pathlib.Path(args.repo_root) if args.repo_root else find_repo_root(pathlib.Path.cwd())
    sprint_n, story_num = parse_story_id(args.story)
    sprint_n = args.sprint or sprint_n
    title = args.title or f"{args.story} delivery"
    slug = args.slug or slugify(title)
    landed = dt.date.today().isoformat()

    commits = collect_commits(repo, args.from_sha, args.to_sha)
    numstat = collect_numstat(repo, args.from_sha, args.to_sha)
    status_map = file_status(repo, args.from_sha, args.to_sha)
    files = [(p, status_map.get(p, "edited"), a, r) for (p, a, r) in numstat]
    loc_total = sum(a + r for _, a, r in numstat)

    body = render(
        story=args.story,
        title=title,
        sprint_n=sprint_n,
        pts=args.pts,
        retires=args.retires,
        files=files,
        commits=commits,
        loc_total=loc_total,
        from_sha=args.from_sha,
        to_sha=args.to_sha,
        has_ui=args.has_ui,
        has_http_api=args.has_http_api,
        has_flags=args.has_flags,
        landed=landed,
    )

    if args.out:
        target = pathlib.Path(args.out)
    else:
        runs_dir = repo / "docs" / "sprint-runs"
        runs_dir.mkdir(parents=True, exist_ok=True)
        target = runs_dir / f"{args.story}-{slug}.md"

    if target.exists() and not args.force:
        print(f"refusing to overwrite existing summary: {target} (use --force)", file=sys.stderr)
        return 2

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body, encoding="utf-8")
    print(f"wrote {target}")
    print()
    print(f"  commits: {len(commits)}")
    print(f"  files changed: {len(files)}")
    print(f"  LOC delta: {loc_total}")
    print()
    print("next: replace <!-- FILL --> placeholders with technical narrative.")
    print("      read references/run-summary-shape.md for section-by-section voice guidance.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
