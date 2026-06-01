#!/usr/bin/env python3
"""
Cortana Vault — Automatic File Ingestion Watcher

Watches the inbox/ folder for new files, processes them through LM Studio
(via OpenAI-compatible API), and integrates them into the wiki following
vault naming conventions.

Usage:
    python vault-watcher.py                                    # Watch mode (default)
    python vault-watcher.py --process-once                     # Process inbox once and exit
    python vault-watcher.py --model google_gemma-4-26b-a4b-it  # Use a specific model
    python vault-watcher.py --api-base http://host:1234/v1     # Custom LM Studio endpoint
    python vault-watcher.py --api-key lms-...                  # LM Studio API key

Requirements:
    pip install watchdog requests PyPDF2 python-frontmatter
"""

import os
import sys
import json
import time
import shutil
import hashlib
import logging
import argparse
import re
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional

# Third-party
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("Missing dependency: pip install watchdog")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("Missing dependency: pip install requests")
    sys.exit(1)

try:
    import frontmatter
except ImportError:
    frontmatter = None  # Optional — we can write frontmatter manually

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

VAULT_ROOT = Path(__file__).resolve().parent.parent
INBOX_DIR = VAULT_ROOT / "inbox"
RAW_DIR = VAULT_ROOT / "raw" / "ingested"
PROJECTS_DIR = VAULT_ROOT / "projects"
RESEARCH_DIR = VAULT_ROOT / "research"
YOUTUBE_DIR = VAULT_ROOT / "youtube"
LOG_FILE = VAULT_ROOT / "log.md"
INDEX_FILE = VAULT_ROOT / "index.md"
SCHEMA_FILE = VAULT_ROOT / "SCHEMA.md"
PROCESSED_LOG = VAULT_ROOT / "scripts" / ".processed"

# LM Studio — OpenAI-compatible API via LM Link
LMSTUDIO_API_BASE = os.environ.get("LMSTUDIO_API_BASE", "http://localhost:1234/v1")
LMSTUDIO_API_KEY = os.environ.get("LMSTUDIO_API_KEY", "lms-default")
DEFAULT_MODEL = "google_gemma-4-26b-a4b-it"

# File extensions we can process
SUPPORTED_TEXT = {".md", ".txt", ".csv", ".json", ".py", ".js", ".ts", ".html", ".css", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".sh", ".bash", ".zsh", ".pine", ".sql", ".r", ".jsx", ".tsx"}
SUPPORTED_PDF = {".pdf"}
SUPPORTED_IMAGE = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
SUPPORTED_OFFICE = {".docx", ".xlsx", ".pptx"}

SETTLE_TIME = 2  # seconds to wait after last file event before processing

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("vault-watcher")


# ---------------------------------------------------------------------------
# LM Studio helpers (OpenAI-compatible API)
# ---------------------------------------------------------------------------

def lmstudio_available(api_base: str = LMSTUDIO_API_BASE, api_key: str = LMSTUDIO_API_KEY) -> bool:
    """Check if LM Studio server is reachable and has models loaded."""
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        r = requests.get(f"{api_base}/models", headers=headers, timeout=5)
        return r.status_code == 200
    except Exception:
        return False


def lmstudio_chat(prompt: str, model: str = DEFAULT_MODEL, system: str = "",
                  api_base: str = LMSTUDIO_API_BASE, api_key: str = LMSTUDIO_API_KEY) -> str:
    """Call LM Studio's OpenAI-compatible chat completions endpoint."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 4096,
        "stream": False,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    try:
        r = requests.post(
            f"{api_base}/chat/completions",
            json=payload,
            headers=headers,
            timeout=180,
        )
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"].strip()
    except requests.exceptions.ConnectionError:
        log.error(f"Cannot connect to LM Studio at {api_base}")
        log.error("Make sure LM Studio is running with the local server started.")
        return ""
    except requests.exceptions.HTTPError as e:
        log.error(f"LM Studio HTTP error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            log.error(f"  Response: {e.response.text[:500]}")
        return ""
    except (KeyError, IndexError) as e:
        log.error(f"Unexpected LM Studio response format: {e}")
        return ""
    except Exception as e:
        log.error(f"LM Studio error: {e}")
        return ""


# ---------------------------------------------------------------------------
# Content extraction
# ---------------------------------------------------------------------------

def extract_content(filepath: Path) -> tuple[str, str]:
    """
    Extract text content from a file.
    Returns (content, file_type) where file_type is 'text', 'pdf', 'image', 'office', 'unknown'.
    """
    ext = filepath.suffix.lower()

    if ext in SUPPORTED_TEXT:
        try:
            text = filepath.read_text(encoding="utf-8", errors="replace")
            return text[:50000], "text"  # Cap at 50k chars for LLM context
        except Exception as e:
            log.warning(f"Could not read {filepath}: {e}")
            return "", "text"

    if ext in SUPPORTED_PDF:
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(str(filepath))
            pages = []
            for page in reader.pages[:30]:  # Cap at 30 pages
                pages.append(page.extract_text() or "")
            return "\n\n---\n\n".join(pages)[:50000], "pdf"
        except ImportError:
            log.warning("PyPDF2 not installed — skipping PDF extraction. pip install PyPDF2")
            return f"[PDF file: {filepath.name}, could not extract — install PyPDF2]", "pdf"
        except Exception as e:
            log.warning(f"PDF extraction failed for {filepath}: {e}")
            return f"[PDF file: {filepath.name}, extraction error: {e}]", "pdf"

    if ext in SUPPORTED_IMAGE:
        return f"[Image file: {filepath.name}]", "image"

    if ext in SUPPORTED_OFFICE:
        return f"[Office file: {filepath.name} — manual processing recommended]", "office"

    return f"[Unsupported file type: {ext}]", "unknown"


# ---------------------------------------------------------------------------
# Wiki page generation
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    """Convert text to a vault-safe filename slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')[:80]


def get_existing_projects() -> dict[str, str]:
    """Return a map of project_slug -> project display name from existing vault."""
    projects = {}
    for proj_dir in PROJECTS_DIR.iterdir():
        if proj_dir.is_dir() and not proj_dir.name.startswith('.'):
            overview = proj_dir / f"{proj_dir.name}.md"
            if overview.exists():
                # Extract title from frontmatter
                text = overview.read_text(encoding="utf-8", errors="replace")
                title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', text, re.MULTILINE)
                display = title_match.group(1) if title_match else proj_dir.name
                projects[proj_dir.name] = display
    return projects


SYSTEM_PROMPT = """You are a wiki librarian for a trader and AI engineer named bang.
You categorize and summarize incoming files for an Obsidian knowledge vault.

The vault has these existing project categories:
{projects}

And these domains:
- Trading & Markets: NQ futures, scalping, indicators, backtesting, market data
- Wick App: Trading platform development
- Platform / Infrastructure: Agent platforms, memory systems, Claude skills
- Business / Consulting: SouthbayAI, client work, competitive analysis
- Research: Learning materials, technical topics
- Finance / Admin: Tax, budgeting, email

You MUST respond in valid JSON only. No markdown, no explanation outside the JSON."""


def classify_file(filename: str, content: str, model: str, api_base: str = LMSTUDIO_API_BASE, api_key: str = LMSTUDIO_API_KEY) -> dict:
    """Use LM Studio to classify a file and generate a wiki summary."""
    existing = get_existing_projects()
    proj_list = "\n".join(f"- {slug}: {name}" for slug, name in existing.items())

    system = SYSTEM_PROMPT.format(projects=proj_list)

    # Truncate content for classification prompt
    content_preview = content[:8000]

    prompt = f"""Analyze this file and return a JSON object with the following fields:

{{
  "title": "A clear, descriptive title for this content",
  "summary": "2-3 sentence summary of what this file contains and why it matters",
  "category": "one of: trading | platform | business | research | finance | youtube",
  "project_slug": "existing project slug from the list above, or a NEW slug if it doesn't fit any (lowercase-with-hyphens)",
  "project_name": "human-readable project name",
  "is_new_project": true/false,
  "tags": ["tag1", "tag2", "tag3"],
  "key_insights": ["insight 1", "insight 2", "insight 3"],
  "related_projects": ["project-slug-1", "project-slug-2"],
  "relevance_to_trading": "Brief note on how this connects to bang's trading work, or 'none' if unrelated"
}}

Filename: {filename}

Content:
{content_preview}

Respond with ONLY the JSON object, nothing else."""

    response = lmstudio_chat(prompt, model=model, system=system, api_base=api_base, api_key=api_key)

    # Parse JSON from response
    try:
        # Try to find JSON in the response
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            return json.loads(json_match.group())
    except json.JSONDecodeError:
        pass

    # Fallback classification
    log.warning(f"LLM classification failed, using fallback for {filename}")
    return {
        "title": filename,
        "summary": "Auto-ingested file — needs manual review.",
        "category": "research",
        "project_slug": "uncategorized",
        "project_name": "Uncategorized",
        "is_new_project": True,
        "tags": ["auto-ingested", "needs-review"],
        "key_insights": [],
        "related_projects": [],
        "relevance_to_trading": "unknown",
    }


def generate_wiki_page(filename: str, content: str, classification: dict, model: str,
                       api_base: str = LMSTUDIO_API_BASE, api_key: str = LMSTUDIO_API_KEY) -> str:
    """Use LM Studio to generate a full wiki page for the ingested file."""
    content_preview = content[:12000]

    prompt = f"""Write an Obsidian wiki page for this ingested file. Use this classification:

Title: {classification['title']}
Summary: {classification['summary']}
Category: {classification['category']}
Tags: {', '.join(classification.get('tags', []))}

The page should have these sections:
1. Summary (2-3 paragraphs)
2. Key Takeaways (bullet points)
3. Technical Details (if applicable)
4. Relevance to Trading & AI Work
5. Action Items (if any)
6. Related Topics (use [[wikilink]] format for connections)

Use Obsidian callouts where appropriate:
- > [!tip] for actionable insights
- > [!warning] for risks or concerns
- > [!question] for open questions

Content to summarize:
{content_preview}

Write the wiki page body ONLY (no frontmatter — I'll add that separately). Use [[wikilinks]] for any concept, tool, or project that might have its own page."""

    return lmstudio_chat(prompt, model=model, api_base=api_base, api_key=api_key)


def create_wiki_page(filepath: Path, classification: dict, wiki_body: str) -> Path:
    """Create the actual .md file in the vault following naming conventions."""
    today = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(classification["title"])
    project_slug = classification["project_slug"]
    category = classification["category"]

    # Determine target directory
    if category == "youtube":
        target_dir = YOUTUBE_DIR / "transcripts"
        page_name = f"{slug}.md"
    elif category == "research":
        target_dir = RESEARCH_DIR / "topics"
        page_name = f"{slug}.md"
    else:
        # Project-based file
        target_dir = PROJECTS_DIR / project_slug
        target_dir.mkdir(parents=True, exist_ok=True)

        # If this is a new project, create the overview page
        if classification.get("is_new_project"):
            create_project_overview(project_slug, classification, today)

        # Session/source pages go in the project root (not sessions/ — that's for Cowork sessions)
        page_name = f"{project_slug}--{slug}.md"

    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / page_name

    # Avoid overwriting
    if target_path.exists():
        base = page_name.replace(".md", "")
        target_path = target_dir / f"{base}-{int(time.time())}.md"

    # Build frontmatter
    fm = f"""---
title: "{classification['title']}"
type: source
created: {today}
updated: {today}
tags: [{', '.join(classification.get('tags', []))}]
status: active
source_file: "{filepath.name}"
project: "[[projects/{project_slug}/{project_slug}|{classification['project_name']}]]"
related: [{', '.join(f'"[[projects/{r}/{r}]]"' for r in classification.get('related_projects', []))}]
relevance: "{classification.get('relevance_to_trading', 'unknown')}"
---

# {classification['title']}

> **Source:** `{filepath.name}` | **Ingested:** {today}

"""

    target_path.write_text(fm + wiki_body, encoding="utf-8")
    log.info(f"  Created wiki page: {target_path.relative_to(VAULT_ROOT)}")
    return target_path


def create_project_overview(project_slug: str, classification: dict, today: str):
    """Create a new project overview page if it doesn't exist."""
    proj_dir = PROJECTS_DIR / project_slug
    proj_dir.mkdir(parents=True, exist_ok=True)
    overview_path = proj_dir / f"{project_slug}.md"

    if overview_path.exists():
        return

    content = f"""---
title: "{classification['project_name']}"
type: project
created: {today}
updated: {today}
tags: [{', '.join(classification.get('tags', []))}]
status: active
sources: []
related: [{', '.join(f'"[[projects/{r}/{r}]]"' for r in classification.get('related_projects', []))}]
---

# {classification['project_name']}

## Summary

{classification['summary']}

## Key Topics

{chr(10).join(f"- {insight}" for insight in classification.get('key_insights', []))}

## Source Files

<!-- Auto-updated by vault-watcher -->

## Session History

<!-- Links to related session summaries -->
"""
    overview_path.write_text(content, encoding="utf-8")
    log.info(f"  Created new project: {overview_path.relative_to(VAULT_ROOT)}")


# ---------------------------------------------------------------------------
# Index and log updates
# ---------------------------------------------------------------------------

def append_to_log(filepath: Path, classification: dict, wiki_page: Path):
    """Append an entry to log.md."""
    today = datetime.now().strftime("%Y-%m-%d")
    wiki_rel = str(wiki_page.relative_to(VAULT_ROOT)).replace(".md", "")

    entry = f"""
## [{today}] ingest | {classification['title']}

- **type**: ingest
- **source**: `{filepath.name}`
- **category**: {classification['category']}
- **project**: [[projects/{classification['project_slug']}/{classification['project_slug']}|{classification['project_name']}]]
- **details**: {classification['summary']}
- **pages touched**: [[{wiki_rel}]]
"""

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)
    log.info(f"  Updated log.md")


# ---------------------------------------------------------------------------
# Processing pipeline
# ---------------------------------------------------------------------------

def load_processed() -> set:
    """Load the set of already-processed file hashes."""
    if PROCESSED_LOG.exists():
        return set(PROCESSED_LOG.read_text().strip().split("\n"))
    return set()


def save_processed(hashes: set):
    """Save the processed file hashes."""
    PROCESSED_LOG.parent.mkdir(parents=True, exist_ok=True)
    PROCESSED_LOG.write_text("\n".join(sorted(hashes)))


def file_hash(filepath: Path) -> str:
    """Quick hash of filename + size + mtime for dedup."""
    stat = filepath.stat()
    key = f"{filepath.name}:{stat.st_size}:{stat.st_mtime}"
    return hashlib.md5(key.encode()).hexdigest()


def process_file(filepath: Path, model: str, api_base: str = LMSTUDIO_API_BASE, api_key: str = LMSTUDIO_API_KEY) -> bool:
    """Process a single file through the ingestion pipeline."""
    log.info(f"Processing: {filepath.name}")

    # 1. Extract content
    content, file_type = extract_content(filepath)
    if not content or content.startswith("[Unsupported"):
        log.warning(f"  Skipping {filepath.name} — unsupported or empty")
        return False

    if file_type == "image":
        log.info(f"  Image file — archiving to raw/ (no LLM processing)")
        dest = RAW_DIR / filepath.name
        shutil.copy2(filepath, dest)
        return True

    # 2. Classify with LLM
    log.info(f"  Classifying with {model}...")
    classification = classify_file(filepath.name, content, model, api_base=api_base, api_key=api_key)
    log.info(f"  -> Category: {classification['category']}, Project: {classification['project_slug']}")

    # 3. Generate wiki page
    log.info(f"  Generating wiki page...")
    wiki_body = generate_wiki_page(filepath.name, content, classification, model, api_base=api_base, api_key=api_key)
    if not wiki_body:
        log.warning(f"  LLM returned empty wiki page — using summary only")
        wiki_body = f"## Summary\n\n{classification['summary']}\n\n## Key Insights\n\n"
        wiki_body += "\n".join(f"- {i}" for i in classification.get("key_insights", []))

    # 4. Create wiki page
    wiki_page = create_wiki_page(filepath, classification, wiki_body)

    # 5. Archive raw file
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    raw_dest = RAW_DIR / filepath.name
    if raw_dest.exists():
        raw_dest = RAW_DIR / f"{filepath.stem}-{int(time.time())}{filepath.suffix}"
    shutil.copy2(filepath, raw_dest)
    log.info(f"  Archived to raw/ingested/{raw_dest.name}")

    # 6. Update log
    append_to_log(filepath, classification, wiki_page)

    # 7. Remove from inbox
    filepath.unlink()
    log.info(f"  Removed from inbox/")

    return True


def process_inbox(model: str, api_base: str = LMSTUDIO_API_BASE, api_key: str = LMSTUDIO_API_KEY):
    """Process all files and directories currently in the inbox."""
    if not INBOX_DIR.exists():
        return

    # Separate files and directories
    entries = [f for f in INBOX_DIR.iterdir()
               if not f.name.startswith('.') and f.name != "README.md"]

    dirs = [f for f in entries if f.is_dir()]
    files = [f for f in entries if f.is_file()]

    if not files and not dirs:
        return

    # Process directories first — they get flattened into individual files
    for dirpath in sorted(dirs):
        log.info(f"Found directory in inbox: {dirpath.name}/")
        process_directory(dirpath, model, api_base=api_base, api_key=api_key)

    # Now process any individual files (including those flattened from directories)
    files = [f for f in INBOX_DIR.iterdir()
             if f.is_file() and not f.name.startswith('.') and f.name != "README.md"]

    processed = load_processed()
    new_count = 0

    for filepath in sorted(files):
        fhash = file_hash(filepath)
        if fhash in processed:
            log.info(f"Skipping {filepath.name} — already processed")
            continue

        success = process_file(filepath, model, api_base=api_base, api_key=api_key)
        if success:
            processed.add(fhash)
            new_count += 1

    save_processed(processed)

    if new_count > 0:
        log.info(f"\nProcessed {new_count} new file(s)")


# ---------------------------------------------------------------------------
# Directory scanning / sampling
# ---------------------------------------------------------------------------

def scan_directory(dirpath: Path) -> dict:
    """
    Scan a directory and produce structured metadata for LLM summarization.
    Returns dict with tree structure, file counts, sample content, etc.
    """
    all_files = [f for f in dirpath.rglob("*") if f.is_file() and not f.name.startswith('.')]
    total_files = len(all_files)

    # File extension breakdown
    ext_counts: dict[str, int] = {}
    for f in all_files:
        ext = f.suffix.lower() or "(no ext)"
        ext_counts[ext] = ext_counts.get(ext, 0) + 1
    ext_summary = sorted(ext_counts.items(), key=lambda x: -x[1])

    # Top-level subdirectories
    subdirs = sorted([d.name for d in dirpath.iterdir()
                      if d.is_dir() and not d.name.startswith('.')])

    # Sample up to 20 representative files (spread across subdirs)
    samples = []
    sample_budget = 20
    if subdirs:
        per_subdir = max(1, sample_budget // len(subdirs))
        for sd in subdirs:
            sd_files = sorted(
                [f for f in (dirpath / sd).rglob("*")
                 if f.is_file() and not f.name.startswith('.')],
                key=lambda f: f.name
            )
            for f in sd_files[:per_subdir]:
                if len(samples) >= sample_budget:
                    break
                content, ftype = extract_content(f)
                samples.append({
                    "path": str(f.relative_to(dirpath)),
                    "size": f.stat().st_size,
                    "preview": content[:2000] if content else "",
                })
    else:
        for f in sorted(all_files, key=lambda f: f.name)[:sample_budget]:
            content, ftype = extract_content(f)
            samples.append({
                "path": str(f.relative_to(dirpath)),
                "size": f.stat().st_size,
                "preview": content[:2000] if content else "",
            })

    # Build a compact directory tree (max 3 levels deep)
    tree_lines = [f"{dirpath.name}/"]
    def _tree(path: Path, prefix: str, depth: int):
        if depth > 2:
            return
        entries = sorted(path.iterdir(), key=lambda e: (not e.is_dir(), e.name))
        dirs_here = [e for e in entries if e.is_dir() and not e.name.startswith('.')]
        files_here = [e for e in entries if e.is_file() and not e.name.startswith('.')]
        # Show dirs + first 5 files per level
        for d in dirs_here:
            child_count = sum(1 for _ in d.rglob("*") if _.is_file())
            tree_lines.append(f"{prefix}├── {d.name}/ ({child_count} files)")
            _tree(d, prefix + "│   ", depth + 1)
        for f in files_here[:5]:
            tree_lines.append(f"{prefix}├── {f.name}")
        if len(files_here) > 5:
            tree_lines.append(f"{prefix}└── ... +{len(files_here) - 5} more files")
    _tree(dirpath, "  ", 0)
    tree_str = "\n".join(tree_lines[:100])  # cap at 100 lines

    return {
        "name": dirpath.name,
        "total_files": total_files,
        "subdirectories": subdirs,
        "extensions": ext_summary,
        "tree": tree_str,
        "samples": samples,
    }


# ---------------------------------------------------------------------------
# Two-tier directory ingestion
# ---------------------------------------------------------------------------

DIR_SUMMARY_SYSTEM = """You are a wiki librarian for a trader and AI engineer named bang.
You produce concise, searchable overviews of large directories dropped into an Obsidian vault.

bang works in: NQ futures trading, scalping strategies, AI agent platforms, Claude skill development, and consulting.

Your job is to write a compact overview that lets bang:
1. Remember what this directory contains months later
2. Search for specific tools/files/concepts via Obsidian search
3. Decide whether to deep-dive into any section

You MUST respond in valid JSON only."""


def summarize_directory(scan: dict, model: str,
                        api_base: str = LMSTUDIO_API_BASE,
                        api_key: str = LMSTUDIO_API_KEY) -> dict:
    """
    Send directory scan data to LLM and get a structured summary.
    Returns dict with overview, categories, highlights, and trading relevance.
    """
    # Build the sample content block
    sample_text = ""
    for s in scan["samples"]:
        sample_text += f"\n--- {s['path']} ({s['size']} bytes) ---\n"
        sample_text += s["preview"][:1500] + "\n"

    ext_str = ", ".join(f"{ext}: {count}" for ext, count in scan["extensions"][:15])

    prompt = f"""Analyze this directory and produce a JSON summary for a wiki page.

DIRECTORY: {scan['name']}
TOTAL FILES: {scan['total_files']}
SUBDIRECTORIES: {', '.join(scan['subdirectories'][:30]) or 'none (flat)'}
FILE TYPES: {ext_str}

DIRECTORY TREE:
{scan['tree']}

SAMPLE FILE CONTENTS:
{sample_text[:12000]}

Return a JSON object:
{{
  "title": "Human-readable title for this collection",
  "one_liner": "One sentence — what IS this directory?",
  "summary": "2-4 paragraph overview. What's in here, how it's organized, what's notable.",
  "categories": [
    {{"name": "category name", "description": "what's in this category", "file_count": N, "standout_items": ["item1", "item2"]}}
  ],
  "highlights": ["The 5-8 most interesting/useful items in this collection, with brief why"],
  "relevance_to_trading": "How this connects to bang's trading/AI work, or 'general reference' if indirect",
  "search_keywords": ["15-20 keywords someone might search for to find content in this directory"],
  "tags": ["tag1", "tag2", "tag3"],
  "recommended_deep_dives": ["Specific items/sections worth materializing into full wiki pages"]
}}

Respond with ONLY the JSON object."""

    response = lmstudio_chat(prompt, model=model, system=DIR_SUMMARY_SYSTEM,
                             api_base=api_base, api_key=api_key)

    try:
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            return json.loads(json_match.group())
    except json.JSONDecodeError:
        pass

    # Fallback
    log.warning(f"LLM summary failed for {scan['name']}, using fallback")
    return {
        "title": scan["name"],
        "one_liner": f"Directory with {scan['total_files']} files.",
        "summary": f"Auto-ingested directory `{scan['name']}` containing {scan['total_files']} files across {len(scan['subdirectories'])} subdirectories. Needs manual review.",
        "categories": [{"name": sd, "description": "auto-detected subdirectory", "file_count": 0, "standout_items": []} for sd in scan["subdirectories"][:10]],
        "highlights": [],
        "relevance_to_trading": "unknown",
        "search_keywords": [scan["name"]],
        "tags": ["auto-ingested", "needs-review"],
        "recommended_deep_dives": [],
    }


def write_directory_overview(scan: dict, summary: dict) -> Path:
    """
    Write the compact wiki overview page for a directory.
    This is the ONLY page created for a directory drop (Tier 1).
    The raw archive in raw/ingested/ preserves everything for on-demand deep dives.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(summary.get("title", scan["name"]))
    project_dir = PROJECTS_DIR / slug
    project_dir.mkdir(parents=True, exist_ok=True)

    overview_path = project_dir / f"{slug}.md"

    # Build category sections
    cat_sections = ""
    for cat in summary.get("categories", []):
        standouts = ", ".join(cat.get("standout_items", [])[:5])
        cat_sections += f"- **{cat['name']}** ({cat.get('file_count', '?')} items)"
        if standouts:
            cat_sections += f" — {standouts}"
        cat_sections += "\n"

    # Build highlights
    highlights = "\n".join(f"- {h}" for h in summary.get("highlights", []))

    # Build deep dive suggestions
    deep_dives = "\n".join(f"- {d}" for d in summary.get("recommended_deep_dives", []))

    # Search keywords as inline tags for Obsidian search
    keywords = ", ".join(summary.get("search_keywords", []))

    tags_str = ", ".join(summary.get("tags", ["auto-ingested"]))

    content = f"""---
title: "{summary.get('title', scan['name'])}"
type: project
created: {today}
updated: {today}
tags: [{tags_str}]
status: active
source_dir: "{scan['name']}"
total_files: {scan['total_files']}
archive: "raw/ingested/{scan['name']}"
sources: ["{scan['name']}"]
related: []
---

# {summary.get('title', scan['name'])}

> {summary.get('one_liner', '')}

**Source:** `inbox/{scan['name']}/` ({scan['total_files']} files) | **Archived:** `raw/ingested/{scan['name']}/` | **Ingested:** {today}

## Overview

{summary.get('summary', '')}

## Categories

{cat_sections}
## Highlights

{highlights}

## Relevance

{summary.get('relevance_to_trading', 'unknown')}

## Recommended Deep Dives

{deep_dives}

> [!tip] On-demand deep dives
> The full source is archived at `raw/ingested/{scan['name']}/`. To materialize a detailed page for any item:
> ```bash
> python scripts/deep-dive.py "{scan['name']}" "item-name-or-path"
> ```

## Directory Structure

```
{scan['tree']}
```

## Search Keywords

{keywords}
"""

    overview_path.write_text(content, encoding="utf-8")
    log.info(f"  Created overview: {overview_path.relative_to(VAULT_ROOT)}")
    return overview_path


def process_directory(dirpath: Path, model: str,
                      api_base: str = LMSTUDIO_API_BASE,
                      api_key: str = LMSTUDIO_API_KEY):
    """
    Two-tier directory ingestion:
      Tier 1 (auto): Scan → LLM summary → single compact overview page
      Tier 2 (on-demand): deep-dive.py materializes individual pages from archive

    The raw directory is archived to raw/ingested/ for future deep dives.
    Only ONE wiki page is created per directory drop.
    """
    log.info(f"Processing directory: {dirpath.name}/")

    # 1. Scan the directory
    log.info(f"  Scanning structure...")
    scan = scan_directory(dirpath)
    log.info(f"  Found {scan['total_files']} files across {len(scan['subdirectories'])} subdirectories")

    # 2. Summarize with LLM
    log.info(f"  Generating LLM overview with {model}...")
    summary = summarize_directory(scan, model, api_base=api_base, api_key=api_key)
    log.info(f"  Title: {summary.get('title', dirpath.name)}")

    # 3. Write the overview page
    overview_path = write_directory_overview(scan, summary)

    # 4. Archive raw directory
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    archive_dest = RAW_DIR / dirpath.name
    if archive_dest.exists():
        archive_dest = RAW_DIR / f"{dirpath.name}-{int(time.time())}"
    shutil.copytree(dirpath, archive_dest)
    log.info(f"  Archived to raw/ingested/{archive_dest.name}/")

    # 5. Remove from inbox
    shutil.rmtree(dirpath)
    log.info(f"  Removed from inbox/")

    # 6. Log it
    today = datetime.now().strftime("%Y-%m-%d")
    wiki_rel = str(overview_path.relative_to(VAULT_ROOT)).replace(".md", "")
    slug = overview_path.parent.name

    log_entry = f"""
## [{today}] ingest | {summary.get('title', dirpath.name)}

- **type**: ingest (directory → compact overview)
- **source**: `{dirpath.name}/` ({scan['total_files']} files)
- **details**: {summary.get('one_liner', 'Directory ingested')}
- **pages created**: 1 overview page
- **archive**: `raw/ingested/{archive_dest.name}/`
- **pages touched**: [[{wiki_rel}]]
"""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)

    log.info(f"  Done — 1 overview page created (full source in raw/ingested/ for deep dives)")


# ---------------------------------------------------------------------------
# File watcher
# ---------------------------------------------------------------------------

class InboxHandler(FileSystemEventHandler):
    """Watches inbox/ for new files and directories."""

    def __init__(self, model: str, api_base: str, api_key: str):
        super().__init__()
        self.model = model
        self.api_base = api_base
        self.api_key = api_key
        self._pending = {}

    def on_created(self, event):
        path = Path(event.src_path)

        # Skip hidden files and README
        if path.name.startswith('.') or path.name == "README.md":
            return

        # Record event time — we'll wait for SETTLE_TIME before processing
        self._pending[str(path)] = time.time()

    def on_modified(self, event):
        path = Path(event.src_path)
        if path.name.startswith('.') or path.name == "README.md":
            return
        self._pending[str(path)] = time.time()

    def check_pending(self):
        """Check if any pending files have settled (no changes for SETTLE_TIME seconds)."""
        now = time.time()
        ready = []

        for path_str, last_event in list(self._pending.items()):
            if now - last_event >= SETTLE_TIME:
                ready.append(path_str)
                del self._pending[path_str]

        for path_str in ready:
            path = Path(path_str)
            if not path.exists():
                continue

            if path.is_dir():
                process_directory(path, self.model, api_base=self.api_base, api_key=self.api_key)
            elif path.is_file():
                process_file(path, self.model, api_base=self.api_base, api_key=self.api_key)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Cortana Vault — Auto-Ingestion Watcher")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"LM Studio model to use (default: {DEFAULT_MODEL})")
    parser.add_argument("--api-base", default=LMSTUDIO_API_BASE, help=f"LM Studio API base URL (default: {LMSTUDIO_API_BASE})")
    parser.add_argument("--api-key", default=LMSTUDIO_API_KEY, help="LM Studio API key (default: from LMSTUDIO_API_KEY env var)")
    parser.add_argument("--process-once", action="store_true", help="Process inbox once and exit")
    parser.add_argument("--vault", type=str, help="Override vault root path")
    args = parser.parse_args()

    global VAULT_ROOT, INBOX_DIR, RAW_DIR, PROJECTS_DIR, RESEARCH_DIR, YOUTUBE_DIR, LOG_FILE, INDEX_FILE, SCHEMA_FILE, PROCESSED_LOG

    if args.vault:
        VAULT_ROOT = Path(args.vault)
        INBOX_DIR = VAULT_ROOT / "inbox"
        RAW_DIR = VAULT_ROOT / "raw" / "ingested"
        PROJECTS_DIR = VAULT_ROOT / "projects"
        RESEARCH_DIR = VAULT_ROOT / "research"
        YOUTUBE_DIR = VAULT_ROOT / "youtube"
        LOG_FILE = VAULT_ROOT / "log.md"
        INDEX_FILE = VAULT_ROOT / "index.md"
        SCHEMA_FILE = VAULT_ROOT / "SCHEMA.md"
        PROCESSED_LOG = VAULT_ROOT / "scripts" / ".processed"

    # Ensure inbox exists
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    # Check LM Studio
    if not lmstudio_available(api_base=args.api_base, api_key=args.api_key):
        log.error(f"Cannot connect to LM Studio at {args.api_base}")
        log.error("Make sure:")
        log.error("  1. LM Studio is open on this machine")
        log.error("  2. LM Link is connected to Symbas-Mac-mini.local")
        log.error(f"  3. Model '{args.model}' is loaded on the Mac Mini via LM Link")
        log.error("  4. Local server is STARTED (Developer > Local Server > Start)")
        log.error("     The local server proxies API calls to the remote model.")
        sys.exit(1)

    log.info(f"Vault:    {VAULT_ROOT}")
    log.info(f"Model:    {args.model}")
    log.info(f"API base: {args.api_base}")
    log.info(f"Inbox:    {INBOX_DIR}")

    if args.process_once:
        log.info("Processing inbox (one-shot mode)...")
        process_inbox(args.model, api_base=args.api_base, api_key=args.api_key)
        log.info("Done.")
        return

    # Watch mode
    log.info("Starting file watcher... (Ctrl+C to stop)")
    log.info(f"Drop files into: {INBOX_DIR}/")

    handler = InboxHandler(model=args.model, api_base=args.api_base, api_key=args.api_key)
    observer = Observer()
    observer.schedule(handler, str(INBOX_DIR), recursive=True)
    observer.start()

    try:
        while True:
            handler.check_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        log.info("Stopping watcher...")
        observer.stop()
    observer.join()
    log.info("Watcher stopped.")


if __name__ == "__main__":
    main()
