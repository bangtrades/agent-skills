"""read-file skill handler.

Two tools: `read_file(path, limit, offset)` and
`list_directory(path, include_hidden)`. Stdlib-only.

The shim does not exec this module yet — the LLM provider is the
runtime through S10D-2. The handler is the authoritative behaviour
spec: when the tool-execution dispatcher lands (S10D-3 or later), it
will route `tool_use` content blocks here. The test suite pins the
behaviour today so the spec doesn't drift.

Workspace scoping rules (see SKILL.md for the full table):
  - Paths are resolved with `os.path.realpath` before any check.
  - If the resolved path is not a descendant of `workspace_root`,
    the handler refuses with `path_outside_workspace` UNLESS the
    agent holds the `filesystem_outside_workspace` capability.
  - Defense-in-depth: certain paths are refused regardless of
    capability state (see ALWAYS_BLOCKED_FRAGMENTS).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Iterable


ALWAYS_BLOCKED_FRAGMENTS = (
    "/Users/nolan/Documents",
    "/Users/Nolan/Documents",
    "/.ssh/",
    "/.aws/",
    "/credentials/",
)
# S10F-2B — the on-disk filesystem is case-insensitive on macOS, so a
# capital-N spelling resolves to the same directory as a lowercase-n
# one. Fold both fragment AND resolved path to lower-case at compare
# time so any case variant of `/Users/Nolan/Documents` is refused.
_ALWAYS_BLOCKED_LOWER = tuple(frag.lower() for frag in ALWAYS_BLOCKED_FRAGMENTS)

TEXT_EXTENSIONS = frozenset({
    ".txt", ".md", ".json", ".yaml", ".yml", ".toml", ".ini",
    ".py", ".js", ".ts", ".tsx", ".jsx", ".sh", ".sql", ".html",
    ".css", ".rs", ".go", ".rb", ".log", ".jsonl",
})


@dataclass(frozen=True)
class HandlerContext:
    workspace_root: str
    capabilities: frozenset


def _refuse(code: str, message: str) -> dict:
    return {"ok": False, "error": code, "message": message}


def _resolve_and_check(ctx: HandlerContext, raw_path: str) -> tuple[bool, str, dict | None]:
    """Resolve `raw_path` and apply scope + always-blocked checks.

    Returns (allowed, resolved_path, refusal). On refusal, `refusal`
    is the dict to return to the caller; otherwise None.
    """
    if not isinstance(raw_path, str) or not raw_path:
        return False, "", _refuse("path_invalid", "path must be a non-empty string")

    if os.path.isabs(raw_path):
        candidate = raw_path
    else:
        candidate = os.path.join(ctx.workspace_root, raw_path)

    resolved = os.path.realpath(candidate)

    resolved_lower = resolved.lower()
    for frag in _ALWAYS_BLOCKED_LOWER:
        if frag in resolved_lower:
            return False, resolved, _refuse(
                "path_blocked_always",
                f"path contains always-blocked fragment {frag!r}; refused regardless of capability state",
            )

    workspace_real = os.path.realpath(ctx.workspace_root)
    inside = resolved == workspace_real or resolved.startswith(workspace_real + os.sep)
    if not inside and "filesystem_outside_workspace" not in ctx.capabilities:
        return False, resolved, _refuse(
            "path_outside_workspace",
            f"resolved path {resolved!r} is outside workspace {workspace_real!r} and the agent does not hold filesystem_outside_workspace",
        )

    return True, resolved, None


def _looks_textual(sample: bytes, ext: str) -> bool:
    if ext.lower() in TEXT_EXTENSIONS:
        return True
    return all(b == 0x09 or b == 0x0A or b == 0x0D or 0x20 <= b <= 0x7E for b in sample)


def read_file(ctx: HandlerContext, *, path: str, limit: int = 200, offset: int = 0) -> dict:
    if not isinstance(limit, int) or limit < 1 or limit > 2000:
        return _refuse("input_invalid", "limit must be an integer in [1, 2000]")
    if not isinstance(offset, int) or offset < 0:
        return _refuse("input_invalid", "offset must be a non-negative integer")

    allowed, resolved, refusal = _resolve_and_check(ctx, path)
    if not allowed:
        return refusal

    if not os.path.exists(resolved):
        return _refuse("path_not_found", f"no such path: {resolved}")
    if os.path.isdir(resolved):
        return _refuse("path_not_a_file", f"{resolved} is a directory; use list_directory")

    try:
        with open(resolved, "rb") as fh:
            sample = fh.read(4096)
    except (OSError, PermissionError) as exc:
        return _refuse("read_failure", f"{type(exc).__name__}: {exc}")

    ext = os.path.splitext(resolved)[1]
    if not _looks_textual(sample, ext):
        return _refuse("binary_content", f"{resolved} appears to be binary; refused")

    try:
        with open(resolved, "r", encoding="utf-8", errors="replace") as fh:
            all_lines = fh.readlines()
    except (OSError, PermissionError) as exc:
        return _refuse("read_failure", f"{type(exc).__name__}: {exc}")

    selected = all_lines[offset:offset + limit]
    rendered = "".join(
        f"{offset + i + 1}\t{line if line.endswith(chr(10)) else line + chr(10)}"
        for i, line in enumerate(selected)
    )
    return {
        "ok": True,
        "path": resolved,
        "line_count": len(all_lines),
        "lines_returned": len(selected),
        "offset": offset,
        "content": rendered,
    }


def list_directory(ctx: HandlerContext, *, path: str, include_hidden: bool = False) -> dict:
    allowed, resolved, refusal = _resolve_and_check(ctx, path)
    if not allowed:
        return refusal

    if not os.path.exists(resolved):
        return _refuse("path_not_found", f"no such path: {resolved}")
    if not os.path.isdir(resolved):
        return _refuse("path_not_a_directory", f"{resolved} is not a directory; use read_file")

    try:
        names = sorted(os.listdir(resolved))
    except (OSError, PermissionError) as exc:
        return _refuse("read_failure", f"{type(exc).__name__}: {exc}")

    entries = []
    for name in names:
        if not include_hidden and name.startswith("."):
            continue
        full = os.path.join(resolved, name)
        try:
            if os.path.isdir(full):
                entry_count = len(os.listdir(full))
                entries.append({"name": name, "type": "directory", "entry_count": entry_count})
            else:
                size = os.path.getsize(full)
                entries.append({"name": name, "type": "file", "size_bytes": size})
        except (OSError, PermissionError):
            entries.append({"name": name, "type": "unknown"})

    return {"ok": True, "path": resolved, "entries": entries}


def handle(ctx: HandlerContext, tool_name: str, arguments: dict) -> dict:
    """Single dispatcher entry point used by the future tool-execution layer."""
    if tool_name == "read_file":
        return read_file(ctx, **arguments)
    if tool_name == "list_directory":
        return list_directory(ctx, **arguments)
    return _refuse("unknown_tool", f"read-file skill has no tool named {tool_name!r}")
