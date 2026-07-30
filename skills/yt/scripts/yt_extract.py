#!/usr/bin/env python3
"""
Extract YouTube video metadata and transcript — rung 1 of the yt skill's tool ladder.

Usage
-----
  # Normal extraction (rung 1)
  python yt_extract.py "https://www.youtube.com/watch?v=VIDEO_ID" --output-dir /tmp/yt-ingest

  # Normalize a pasted / Chrome-scraped transcript (rung 3-4) into canonical [MM:SS] lines
  python yt_extract.py --normalize raw.txt --url "URL" --output-dir /tmp/yt-ingest

  # Merge Firecrawl-derived metadata (rung 2) into the output
  python yt_extract.py --url "URL" --metadata-json fc.json --output-dir /tmp/yt-ingest

Outputs (in --output-dir)
-------------------------
  metadata.json   title, channel, duration, upload_date, views, description, url, video_id
  transcript.txt  timestamped lines: [MM:SS] text
  status.json     {metadata_ok, transcript_ok, reason, video_id, rung}

Exit codes — the agent uses these to decide whether to climb the ladder
----------------------------------------------------------------------
  0   metadata + transcript both OK
  10  metadata OK, transcript MISSING  -> climb to rung 2 (Firecrawl two-hop)
  20  metadata FAILED (likely bot-block) -> use Firecrawl for metadata, then climb
  1   usage / unexpected error

Requires: yt-dlp (pip install yt-dlp --break-system-packages)
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_NO_TRANSCRIPT = 10
EXIT_NO_METADATA = 20
EXIT_USAGE = 1

BOT_BLOCK_MARKERS = (
    "sign in to confirm",
    "not a bot",
    "requestblocked",
    "http error 429",
    "video unavailable",
)


def extract_video_id(url: str) -> str:
    m = re.search(r"(?:v=|youtu\.be/|/shorts/|/embed/)([A-Za-z0-9_-]{11})", url or "")
    return m.group(1) if m else ""


def fmt_duration(seconds: int) -> str:
    seconds = int(seconds or 0)
    if seconds >= 3600:
        return f"{seconds // 3600}:{(seconds % 3600) // 60:02d}:{seconds % 60:02d}"
    return f"{seconds // 60}:{seconds % 60:02d}"


def get_metadata(url: str) -> tuple[dict, str]:
    """Pull video metadata via yt-dlp. Returns (metadata, failure_reason)."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "yt_dlp", "--dump-json", "--skip-download", url],
            capture_output=True, text=True, timeout=90,
        )
    except subprocess.TimeoutExpired:
        return {}, "yt-dlp metadata timed out"
    except Exception as exc:  # noqa: BLE001
        return {}, f"yt-dlp not runnable: {exc}"

    if result.returncode != 0:
        err = (result.stderr or "")[:600]
        low = err.lower()
        reason = "bot-blocked" if any(m in low for m in BOT_BLOCK_MARKERS) else "yt-dlp metadata failed"
        return {}, f"{reason}: {err.strip()}"

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {}, "yt-dlp returned unparseable JSON"

    duration = data.get("duration", 0) or 0
    return {
        "title": data.get("title", "Unknown"),
        "channel": data.get("channel", data.get("uploader", "Unknown")),
        "duration": fmt_duration(duration),
        "duration_seconds": duration,
        "upload_date": data.get("upload_date", ""),
        "views": data.get("view_count", 0),
        "description": (data.get("description") or "")[:2000],
        "url": url,
        "video_id": data.get("id", "") or extract_video_id(url),
        "metadata_source": "yt-dlp",
    }, ""


def get_transcript(url: str, output_dir: Path) -> tuple[str, str]:
    """Pull auto-generated subtitles. Returns (transcript, failure_reason)."""
    vid = extract_video_id(url) or "video"
    sub_path = output_dir / f"yt-{vid}"

    try:
        proc = subprocess.run(
            [sys.executable, "-m", "yt_dlp",
             "--write-auto-sub", "--write-sub", "--sub-lang", "en.*",
             "--skip-download", "--sub-format", "json3", "-o", str(sub_path), url],
            capture_output=True, text=True, timeout=120,
        )
    except subprocess.TimeoutExpired:
        return "", "subtitle download timed out"
    except Exception as exc:  # noqa: BLE001
        return "", f"subtitle download not runnable: {exc}"

    matches = sorted(output_dir.glob(f"yt-{vid}*.json3"))
    if not matches:
        err = (proc.stderr or "")[:400].strip()
        low = err.lower()
        if any(m in low for m in BOT_BLOCK_MARKERS):
            return "", f"bot-blocked: {err}"
        return "", f"no subtitle track found{': ' + err if err else ''}"

    try:
        data = json.loads(matches[0].read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return "", f"subtitle file unparseable: {exc}"

    lines, seen_last = [], None
    for event in data.get("events", []):
        text = "".join(s.get("utf8", "") for s in event.get("segs", [])).strip()
        if not text or text == "\n" or text == seen_last:
            continue
        seen_last = text
        ts = (event.get("tStartMs", 0) or 0) / 1000
        lines.append(f"[{int(ts // 60):02d}:{int(ts % 60):02d}] {text}")

    for f in matches:
        try:
            f.unlink()
        except OSError:
            pass

    if not lines:
        return "", "subtitle track was empty"
    return "\n".join(lines), ""


# Matches a bare timestamp on its own line: "0:00", "12:34", "1:02:03"
TS_LINE = re.compile(r"^\s*(?:(\d+):)?(\d{1,2}):(\d{2})\s*$")
# Matches "0:00 some text" on one line
TS_INLINE = re.compile(r"^\s*(?:(\d+):)?(\d{1,2}):(\d{2})\s+(.*\S)\s*$")


def normalize_transcript(raw: str) -> str:
    """Convert a pasted YouTube transcript into canonical [MM:SS] text lines.

    Handles both YouTube paste shapes:
      "0:00\\ntext\\n0:04\\ntext"   (timestamp on its own line)
      "0:00 text\\n0:04 text"       (timestamp inline)
    Lines already in [MM:SS] form pass through untouched.
    """
    out, pending_ts = [], None
    for line in raw.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("[") and "]" in s[:12]:      # already canonical
            out.append(s)
            pending_ts = None
            continue
        m = TS_LINE.match(s)
        if m:
            h, mm, ss = m.groups()
            total = int(h or 0) * 3600 + int(mm) * 60 + int(ss)
            pending_ts = f"[{total // 60:02d}:{total % 60:02d}]"
            continue
        m = TS_INLINE.match(s)
        if m:
            h, mm, ss, text = m.groups()
            total = int(h or 0) * 3600 + int(mm) * 60 + int(ss)
            out.append(f"[{total // 60:02d}:{total % 60:02d}] {text}")
            pending_ts = None
            continue
        if pending_ts:
            out.append(f"{pending_ts} {s}")
            pending_ts = None
        else:
            out.append(s)
    return "\n".join(out)


def write_outputs(output_dir: Path, metadata: dict, transcript: str,
                  reason: str, rung: str) -> None:
    (output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    (output_dir / "transcript.txt").write_text(
        transcript + "\n" if transcript and not transcript.endswith("\n") else transcript,
        encoding="utf-8",
    )
    status = {
        "metadata_ok": bool(metadata.get("title")),
        "transcript_ok": bool(transcript.strip()),
        "transcript_lines": len(transcript.splitlines()) if transcript.strip() else 0,
        "reason": reason,
        "video_id": metadata.get("video_id", ""),
        "rung": rung,
    }
    (output_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps({"metadata": metadata, "status": status}, indent=2))


def main() -> int:
    p = argparse.ArgumentParser(description="Extract YouTube metadata and transcript")
    p.add_argument("url_pos", nargs="?", help="YouTube video URL (positional)")
    p.add_argument("--url", help="YouTube video URL")
    p.add_argument("--output-dir", default=".", help="Directory for output files")
    p.add_argument("--normalize", metavar="FILE",
                   help="Normalize a pasted/scraped transcript file into [MM:SS] lines")
    p.add_argument("--metadata-json", metavar="FILE",
                   help="Merge externally-sourced (e.g. Firecrawl) metadata JSON")
    args = p.parse_args()

    url = args.url or args.url_pos or ""
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # ---- external metadata (Firecrawl rung) --------------------------------
    external = {}
    if args.metadata_json:
        try:
            external = json.loads(Path(args.metadata_json).read_text(encoding="utf-8"))
            external.setdefault("metadata_source", "firecrawl")
        except Exception as exc:  # noqa: BLE001
            print(f"Could not read --metadata-json: {exc}", file=sys.stderr)
            return EXIT_USAGE

    # ---- normalize mode (rungs 3-4) ----------------------------------------
    if args.normalize:
        try:
            raw = Path(args.normalize).read_text(encoding="utf-8", errors="replace")
        except Exception as exc:  # noqa: BLE001
            print(f"Could not read {args.normalize}: {exc}", file=sys.stderr)
            return EXIT_USAGE
        transcript = normalize_transcript(raw)
        metadata = external or {"url": url, "video_id": extract_video_id(url),
                                "metadata_source": "external"}
        metadata.setdefault("video_id", extract_video_id(url))
        metadata.setdefault("url", url)
        print(f"Normalized {len(transcript.splitlines())} lines", file=sys.stderr)
        write_outputs(output_dir, metadata, transcript, "normalized from file", "normalize")
        return EXIT_OK if transcript.strip() else EXIT_NO_TRANSCRIPT

    if not url:
        print("A URL is required (positional or --url)", file=sys.stderr)
        return EXIT_USAGE

    # ---- rung 1: yt-dlp ----------------------------------------------------
    print("Fetching metadata...", file=sys.stderr)
    metadata, meta_reason = get_metadata(url)
    if external:
        metadata = {**metadata, **external} if metadata else external
        metadata.setdefault("video_id", extract_video_id(url))
        metadata.setdefault("url", url)
        meta_reason = ""

    if metadata.get("title"):
        print(f"Title:    {metadata.get('title')}", file=sys.stderr)
        print(f"Channel:  {metadata.get('channel')}", file=sys.stderr)
        print(f"Duration: {metadata.get('duration')}", file=sys.stderr)
    else:
        print(f"Metadata unavailable — {meta_reason}", file=sys.stderr)
        print("  -> climb to rung 2: firecrawl_scrape the watch URL for metadata",
              file=sys.stderr)

    print("Fetching transcript...", file=sys.stderr)
    transcript, trans_reason = get_transcript(url, output_dir)
    if transcript:
        print(f"Transcript: {len(transcript.splitlines())} lines", file=sys.stderr)
    else:
        print(f"Transcript unavailable — {trans_reason}", file=sys.stderr)
        print("  -> climb the ladder: rung 2 Firecrawl two-hop (rawHtml -> captionTracks "
              "baseUrl), rung 3 Chrome MCP, rung 4 ask bang to paste", file=sys.stderr)

    reason = "; ".join(r for r in (meta_reason, trans_reason) if r)
    if not metadata.get("title"):
        metadata = metadata or {"url": url, "video_id": extract_video_id(url)}
    write_outputs(output_dir, metadata, transcript, reason, "yt-dlp")

    if not metadata.get("title"):
        return EXIT_NO_METADATA
    if not transcript.strip():
        return EXIT_NO_TRANSCRIPT
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
