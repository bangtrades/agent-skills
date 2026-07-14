#!/usr/bin/env python3
"""
new_sprint.py — scaffold a new docs/SPRINT-N-tracker.md.

Usage:
  python new_sprint.py --n 11 --goal "Polish and hardening" \
      --velocity 75 --start 2026-05-13 --duration 14 \
      [--theme "Polish"] [--carry-in "S10-05, S10-08"] [--repo-root PATH]

Outputs the skeleton to docs/SPRINT-N-tracker.md under --repo-root (or cwd-walked repo).
Fails fast if the file already exists — we don't silently overwrite a tracker.

The skeleton is intentionally minimal — Claude fills in epic tables and story
rows after the file is created. The script only handles the mechanical framing
(meta block, section headers, empty summary table).
"""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import sys
import textwrap


def find_repo_root(start: pathlib.Path) -> pathlib.Path:
    p = start.resolve()
    for candidate in [p, *p.parents]:
        if (candidate / ".git").exists():
            return candidate
    raise SystemExit(f"no .git ancestor found from {start}")


def render(args) -> str:
    start = dt.date.fromisoformat(args.start)
    end = start + dt.timedelta(days=args.duration)
    theme = args.theme or args.goal.split(".")[0].strip()

    out = textwrap.dedent(
        f"""\
        # Sprint {args.n} Tracker — {theme}

        **Sprint dates:** {start.isoformat()} → {end.isoformat()}
        **Goal:** {args.goal}
        **Velocity target:** {args.velocity} pts
        **Status:** 🟡 Open
        """
    )

    if args.carry_in:
        out += textwrap.dedent(
            f"""
            ## Carry-in from Sprint {args.n - 1}

            {args.carry_in}
            """
        )

    out += textwrap.dedent(
        f"""
        ## TBD Epic — Placeholder ({args.velocity} pts)

        | ID | Story | Pts | Status | Notes |
        |----|-------|-----|--------|-------|
        | S{args.n}-01 | _fill in_ | _?_ | ⏸ Pending | _fill in_ |

        **TBD: 0/{args.velocity} pts — OPEN**

        ## Sprint Summary

        | Epic | Points | Complete | Pending |
        |------|--------|----------|---------|
        | TBD | {args.velocity} | 0 | {args.velocity} |
        | **Total** | **{args.velocity}** | **0** | **{args.velocity}** |

        **Completion: 0% — Sprint in progress.**

        ## Key Decisions

        <!-- Append numbered entries as decisions land. Each entry: brief statement, then "why X over Y" rationale. -->

        ## Files Changed

        <!-- Append per-story sections as stories close. -->

        ## Run Summaries

        <!-- One line per closed story, linking to docs/sprint-runs/S{args.n}-XX-<slug>.md -->
        """
    )
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, required=True, help="Sprint number")
    ap.add_argument("--goal", required=True, help="Goal statement")
    ap.add_argument("--velocity", type=int, required=True, help="Velocity target in pts")
    ap.add_argument("--start", required=True, help="Start date YYYY-MM-DD")
    ap.add_argument("--duration", type=int, default=14, help="Duration in days (default 14)")
    ap.add_argument("--theme", default=None, help="Sprint theme (default: first sentence of goal)")
    ap.add_argument("--carry-in", default=None, help="Carry-in debt description")
    ap.add_argument("--repo-root", default=None, help="Repo root (default: auto-detect)")
    args = ap.parse_args()

    repo_root = pathlib.Path(args.repo_root) if args.repo_root else find_repo_root(pathlib.Path.cwd())
    docs_dir = repo_root / "docs"
    docs_dir.mkdir(exist_ok=True)

    target = docs_dir / f"SPRINT-{args.n}-tracker.md"
    if target.exists():
        print(f"refusing to overwrite existing tracker: {target}", file=sys.stderr)
        return 2

    target.write_text(render(args), encoding="utf-8")
    print(f"wrote {target}")
    print()
    print("next: fill in epic tables + story rows in the tracker.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
