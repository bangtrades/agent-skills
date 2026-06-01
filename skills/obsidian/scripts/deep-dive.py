#!/usr/bin/env python3
"""
Cortana Vault — On-Demand Deep Dive

Materializes detailed wiki pages from archived directories.
Use after a directory has been ingested (Tier 1 overview exists).

Usage:
    # List what's in an archived directory
    python scripts/deep-dive.py claude-skills-main --list

    # Search for items matching a keyword
    python scripts/deep-dive.py claude-skills-main --search "agent"

    # Materialize a specific file or subdirectory into a wiki page
    python scripts/deep-dive.py claude-skills-main "engineering/agent-designer"

    # Materialize all items in a subdirectory
    python scripts/deep-dive.py claude-skills-main "engineering/" --all

    # Materialize with custom model/endpoint
    python scripts/deep-dive.py claude-skills-main "file.py" --model google_gemma-4-26b-a4b-it

Requirements:
    pip install requests python-frontmatter
"""

import os
import sys
import json
import re
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional

try:
    import requests
except ImportError:
    print("Missing dependency: pip install requests")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

VAULT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = VAULT_ROOT / "raw" / "ingested"
PROJECTS_DIR = VAULT_ROOT / "projects"
LOG_FILE = VAULT_ROOT / "log.md"

LMSTUDIO_API_BASE = os.environ.get("LMSTUDIO_API_BASE", "http://localhost:1234/v1")
LMSTUDIO_API_KEY = os.environ.get("LMSTUDIO_API_KEY", "lms-default")
DEFAULT_MODEL = "google_gemma-4-26b-a4b-it"

SUPPORTED_TEXT = {".md", ".txt", ".csv", ".json", ".py", ".js", ".ts", ".html",
                  ".css", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".sh", ".bash",
                  ".zsh", ".pine", ".sql", ".r", ".jsx", ".tsx"}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("deep-dive")


# ---------------------------------------------------------------------------
# LLM helper (same as vault-watcher)
# ---------------------------------------------------------------------------

def lmstudio_chat(prompt: str, model: str = DEFAULT_MODEL, system: str = "",
                  api_base: str = LMSTUDIO_API_BASE, api_key: str = LMSTUDIO_API_KEY) -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        r = requests.post(
            f"{api_base}/chat/completions",
            json={"model": model, "messages": messages, "temperature": 0.3,
                  "max_tokens": 4096, "stream": False},
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {api_key}"},
            timeout=180,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        log.error(f"LLM error: {e}")
        return ""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')[:80]


def extract_text(filepath: Path) -> str:
    ext = filepath.suffix.lower()
    if ext in SUPPORTED_TEXT:
        try:
            return filepath.read_text(encoding="utf-8", errors="replace")[:50000]
        except Exception:
            return ""
    if ext == ".pdf":
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(str(filepath))
            return "\n\n".join(p.extract_text() or "" for p in reader.pages[:20])[:50000]
        except Exception:
            return f"[PDF: {filepath.name}]"
    return f"[Binary: {filepath.name} ({ext})]"


def find_archive(name: str) -> Optional[Path]:
    """Find an archived directory by name."""
    exact = RAW_DIR / name
    if exact.exists() and exact.is_dir():
        return exact
    # Fuzzy match (name might have timestamp suffix)
    for d in RAW_DIR.iterdir():
        if d.is_dir() and d.name.startswith(name):
            return d
    return None


def find_project_dir(archive_name: str) -> Optional[Path]:
    """Find the project directory that was created from this archive."""
    for d in PROJECTS_DIR.iterdir():
        if not d.is_dir():
            continue
        overview = d / f"{d.name}.md"
        if overview.exists():
            text = overview.read_text(encoding="utf-8", errors="replace")
            if f'source_dir: "{archive_name}"' in text or f'archive: "raw/ingested/{archive_name}"' in text:
                return d
    return None


# ---------------------------------------------------------------------------
# Deep dive generation
# ---------------------------------------------------------------------------

DEEP_DIVE_SYSTEM = """You are a wiki page writer for a trader and AI engineer named bang.
You create detailed, searchable Obsidian wiki pages from source files.
Write in a way that maximizes future searchability and quick reference.
Focus on: what it does, how to use it, why it matters for trading/AI work."""


def materialize_file(filepath: Path, archive_path: Path, project_dir: Path,
                     model: str, api_base: str, api_key: str) -> Optional[Path]:
    """Create a detailed wiki page for a single archived file."""
    rel_path = filepath.relative_to(archive_path)
    content = extract_text(filepath)
    if not content or content.startswith("[Binary"):
        log.warning(f"  Skipping {rel_path} — unsupported format")
        return None

    # Generate the wiki page via LLM
    prompt = f"""Write a detailed Obsidian wiki page for this file.

FILE: {rel_path}
FROM ARCHIVE: {archive_path.name}

CONTENT:
{content[:15000]}

Write the page body (NO frontmatter). Include:
1. One-line summary of what this is
2. Detailed explanation of contents, purpose, and usage
3. Key takeaways or notable details
4. How it connects to trading, AI development, or tool building (if relevant)
5. Related concepts using [[wikilink]] syntax

Keep it concise but thorough. Use Obsidian callouts where appropriate."""

    wiki_body = lmstudio_chat(prompt, model=model, system=DEEP_DIVE_SYSTEM,
                              api_base=api_base, api_key=api_key)
    if not wiki_body:
        # Fallback — just include content preview
        wiki_body = f"## Content Preview\n\n```\n{content[:3000]}\n```"

    # Determine page name: <project>--<slug>.md
    project_slug = project_dir.name
    item_slug = slugify(str(rel_path).replace("/", "-").replace(".", "-"))
    page_name = f"{project_slug}--{item_slug}.md"
    page_path = project_dir / page_name

    today = datetime.now().strftime("%Y-%m-%d")
    title = filepath.stem.replace("-", " ").replace("_", " ").title()

    frontmatter = f"""---
title: "{title}"
type: source
created: {today}
updated: {today}
tags: [deep-dive, {project_slug}]
status: active
source_file: "raw/ingested/{archive_path.name}/{rel_path}"
project: "[[projects/{project_slug}/{project_slug}|{project_slug}]]"
related: []
---

# {title}

> **Source:** `{rel_path}` from `{archive_path.name}/` | **Deep dive:** {today}

"""

    page_path.write_text(frontmatter + wiki_body, encoding="utf-8")
    log.info(f"  Created: {page_path.relative_to(VAULT_ROOT)}")
    return page_path


def materialize_subdir(subdir: Path, archive_path: Path, project_dir: Path,
                       model: str, api_base: str, api_key: str) -> list[Path]:
    """Materialize all readable files in a subdirectory."""
    files = sorted([f for f in subdir.rglob("*")
                    if f.is_file() and not f.name.startswith('.')])
    created = []
    for f in files:
        page = materialize_file(f, archive_path, project_dir, model, api_base, api_key)
        if page:
            created.append(page)
    return created


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_list(archive_path: Path):
    """List contents of an archived directory."""
    print(f"\nArchive: {archive_path.name}/")
    print(f"Location: {archive_path}\n")

    subdirs = sorted([d for d in archive_path.iterdir() if d.is_dir() and not d.name.startswith('.')])
    files = sorted([f for f in archive_path.iterdir() if f.is_file() and not f.name.startswith('.')])

    if subdirs:
        print("Subdirectories:")
        for d in subdirs:
            count = sum(1 for _ in d.rglob("*") if _.is_file())
            print(f"  {d.name}/ ({count} files)")

    if files:
        print(f"\nTop-level files ({len(files)}):")
        for f in files[:20]:
            print(f"  {f.name} ({f.stat().st_size:,} bytes)")
        if len(files) > 20:
            print(f"  ... +{len(files) - 20} more")

    total = sum(1 for _ in archive_path.rglob("*") if _.is_file())
    print(f"\nTotal: {total} files")


def cmd_search(archive_path: Path, query: str):
    """Search file names and content in an archived directory."""
    query_lower = query.lower()
    matches = []

    for f in archive_path.rglob("*"):
        if not f.is_file() or f.name.startswith('.'):
            continue
        rel = f.relative_to(archive_path)

        # Name match
        if query_lower in str(rel).lower():
            matches.append((str(rel), "name match"))
            continue

        # Content match (text files only)
        if f.suffix.lower() in SUPPORTED_TEXT:
            try:
                text = f.read_text(encoding="utf-8", errors="replace")[:10000]
                if query_lower in text.lower():
                    # Find context
                    idx = text.lower().index(query_lower)
                    start = max(0, idx - 50)
                    end = min(len(text), idx + len(query) + 50)
                    context = text[start:end].replace("\n", " ").strip()
                    matches.append((str(rel), f"...{context}..."))
            except Exception:
                pass

    print(f"\nSearch: '{query}' in {archive_path.name}/")
    print(f"Found {len(matches)} match(es):\n")

    for path, context in matches[:50]:
        print(f"  {path}")
        if context != "name match":
            print(f"    {context}")
    if len(matches) > 50:
        print(f"\n  ... +{len(matches) - 50} more matches")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Cortana Vault — On-Demand Deep Dive into archived directories",
        epilog="Examples:\n"
               "  python scripts/deep-dive.py claude-skills-main --list\n"
               "  python scripts/deep-dive.py claude-skills-main --search 'agent'\n"
               '  python scripts/deep-dive.py claude-skills-main "engineering/agent-designer"\n'
               '  python scripts/deep-dive.py claude-skills-main "engineering/" --all\n',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("archive", help="Name of the archived directory in raw/ingested/")
    parser.add_argument("target", nargs="?", help="File or subdirectory path to deep-dive into")
    parser.add_argument("--list", action="store_true", help="List archive contents")
    parser.add_argument("--search", type=str, help="Search archive by keyword")
    parser.add_argument("--all", action="store_true", help="Materialize all items in target subdirectory")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"LM Studio model (default: {DEFAULT_MODEL})")
    parser.add_argument("--api-base", default=LMSTUDIO_API_BASE, help="LM Studio API base URL")
    parser.add_argument("--api-key", default=LMSTUDIO_API_KEY, help="LM Studio API key")
    args = parser.parse_args()

    # Find the archive
    archive_path = find_archive(args.archive)
    if not archive_path:
        print(f"Archive not found: {args.archive}")
        print(f"Available archives in {RAW_DIR}:")
        for d in sorted(RAW_DIR.iterdir()):
            if d.is_dir():
                print(f"  {d.name}/")
        sys.exit(1)

    # List mode
    if args.list:
        cmd_list(archive_path)
        return

    # Search mode
    if args.search:
        cmd_search(archive_path, args.search)
        return

    # Deep dive mode — requires a target
    if not args.target:
        parser.print_help()
        print(f"\nTip: use --list to see what's in {archive_path.name}/")
        sys.exit(1)

    # Find the project directory for this archive
    project_dir = find_project_dir(archive_path.name)
    if not project_dir:
        # Create a new project dir from the archive name
        slug = slugify(archive_path.name)
        project_dir = PROJECTS_DIR / slug
        project_dir.mkdir(parents=True, exist_ok=True)
        log.warning(f"No existing project found — created {project_dir.name}/")

    # Resolve the target within the archive
    target = archive_path / args.target.rstrip("/")
    if not target.exists():
        # Try fuzzy match
        matches = list(archive_path.rglob(f"*{args.target}*"))
        if matches:
            print(f"Exact path not found. Did you mean one of these?")
            for m in matches[:10]:
                print(f"  {m.relative_to(archive_path)}")
            sys.exit(1)
        else:
            print(f"Not found in archive: {args.target}")
            sys.exit(1)

    # Process
    today = datetime.now().strftime("%Y-%m-%d")
    created_pages = []

    if target.is_dir():
        if args.all:
            log.info(f"Materializing all files in {target.relative_to(archive_path)}/")
            created_pages = materialize_subdir(
                target, archive_path, project_dir,
                args.model, args.api_base, args.api_key
            )
        else:
            print(f"'{args.target}' is a directory. Use --all to materialize all files inside it.")
            print(f"Contents:")
            for f in sorted(target.rglob("*")):
                if f.is_file() and not f.name.startswith('.'):
                    print(f"  {f.relative_to(archive_path)}")
            sys.exit(0)
    else:
        page = materialize_file(
            target, archive_path, project_dir,
            args.model, args.api_base, args.api_key
        )
        if page:
            created_pages.append(page)

    # Log
    if created_pages:
        page_links = ", ".join(
            f"[[{str(p.relative_to(VAULT_ROOT)).replace('.md', '')}]]"
            for p in created_pages[:10]
        )
        if len(created_pages) > 10:
            page_links += f" + {len(created_pages) - 10} more"

        log_entry = f"""
## [{today}] deep-dive | {archive_path.name}/{args.target}

- **type**: deep-dive
- **archive**: `raw/ingested/{archive_path.name}/`
- **target**: `{args.target}`
- **pages created**: {len(created_pages)}
- **pages touched**: {page_links}
"""
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)

        print(f"\nDone — created {len(created_pages)} wiki page(s)")
    else:
        print("No pages created.")


if __name__ == "__main__":
    main()
