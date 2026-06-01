#!/usr/bin/env python3
"""
Extract YouTube video metadata and transcript.

Usage:
    python yt_extract.py "https://www.youtube.com/watch?v=VIDEO_ID" --output-dir /path/to/dir

Outputs two files in output-dir:
    metadata.json   — title, channel, duration, upload_date, views, description, url
    transcript.txt  — timestamped transcript lines: [MM:SS] text

Requires: yt-dlp (pip install yt-dlp)
"""

import argparse
import json
import subprocess
import sys
import re
from pathlib import Path


def get_metadata(url: str) -> dict:
    """Pull video metadata via yt-dlp --dump-json."""
    result = subprocess.run(
        [sys.executable, "-m", "yt_dlp", "--dump-json", "--skip-download", url],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        print(f"Error getting metadata: {result.stderr[:500]}", file=sys.stderr)
        return {}

    data = json.loads(result.stdout)
    duration = data.get("duration", 0)
    return {
        "title": data.get("title", "Unknown"),
        "channel": data.get("channel", data.get("uploader", "Unknown")),
        "duration": f"{duration // 3600}:{(duration % 3600) // 60:02d}:{duration % 60:02d}" if duration >= 3600
                    else f"{duration // 60}:{duration % 60:02d}",
        "duration_seconds": duration,
        "upload_date": data.get("upload_date", ""),
        "views": data.get("view_count", 0),
        "description": data.get("description", "")[:1000],
        "url": url,
        "video_id": data.get("id", ""),
    }


def get_transcript(url: str, output_dir: Path) -> str:
    """Pull auto-generated subtitles and parse into timestamped text."""
    video_id = re.search(r'(?:v=|youtu\.be/)([^&?#]+)', url)
    vid = video_id.group(1) if video_id else "video"
    sub_path = output_dir / f"yt-{vid}"

    # Download subtitles as JSON3
    subprocess.run(
        [sys.executable, "-m", "yt_dlp",
         "--write-auto-sub", "--sub-lang", "en", "--skip-download",
         "--sub-format", "json3", "-o", str(sub_path), url],
        capture_output=True, text=True, timeout=60
    )

    # Find the subtitle file
    json3_file = None
    for candidate in [
        sub_path.with_suffix(".en.json3"),
        Path(f"{sub_path}.en.json3"),
    ]:
        if candidate.exists():
            json3_file = candidate
            break

    if not json3_file:
        # Try glob
        matches = list(output_dir.glob(f"yt-{vid}*.json3"))
        if matches:
            json3_file = matches[0]

    if not json3_file:
        print("No subtitle file found", file=sys.stderr)
        return ""

    # Parse JSON3 into timestamped lines
    with open(json3_file) as f:
        data = json.load(f)

    lines = []
    for event in data.get("events", []):
        segs = event.get("segs", [])
        text = "".join(s.get("utf8", "") for s in segs).strip()
        if text and text != "\n":
            ts = event.get("tStartMs", 0) / 1000
            mins = int(ts // 60)
            secs = int(ts % 60)
            lines.append(f"[{mins:02d}:{secs:02d}] {text}")

    # Clean up subtitle file
    try:
        json3_file.unlink()
    except Exception:
        pass

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Extract YouTube metadata and transcript")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--output-dir", default=".", help="Directory for output files")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Fetching metadata...", file=sys.stderr)
    metadata = get_metadata(args.url)
    if not metadata:
        print("Failed to get metadata", file=sys.stderr)
        sys.exit(1)

    print(f"Title: {metadata['title']}", file=sys.stderr)
    print(f"Channel: {metadata['channel']}", file=sys.stderr)
    print(f"Duration: {metadata['duration']}", file=sys.stderr)

    print("Fetching transcript...", file=sys.stderr)
    transcript = get_transcript(args.url, output_dir)
    line_count = len(transcript.split("\n")) if transcript else 0
    print(f"Transcript: {line_count} lines", file=sys.stderr)

    # Write outputs
    meta_path = output_dir / "metadata.json"
    meta_path.write_text(json.dumps(metadata, indent=2))

    trans_path = output_dir / "transcript.txt"
    trans_path.write_text(transcript)

    # Also print metadata as JSON to stdout for piping
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
