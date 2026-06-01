"""Tests for the read-file skill handler.

Run from this directory:

    cd workspaces/cortana-skills/read-file
    python3 -m unittest test.test_handler
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Allow `from lib import handler` when running via `-m unittest test.test_handler`.
_HERE = Path(__file__).resolve().parent.parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from lib import handler  # noqa: E402


class _Workspace:
    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "hello.txt").write_text("hello\nworld\nthird\n", encoding="utf-8")
        (self.root / "sub").mkdir()
        (self.root / "sub" / "nested.md").write_text("# nested\n\nbody\n", encoding="utf-8")
        (self.root / "binary.bin").write_bytes(bytes(range(256)))
        (self.root / ".secret").write_text("hidden\n", encoding="utf-8")

    def cleanup(self):
        self.tmp.cleanup()


def _ctx(workspace_root: str, *caps: str) -> handler.HandlerContext:
    return handler.HandlerContext(
        workspace_root=workspace_root,
        capabilities=frozenset(caps),
    )


class ReadFileTests(unittest.TestCase):
    def setUp(self):
        self.ws = _Workspace()
        self.addCleanup(self.ws.cleanup)
        self.ctx = _ctx(str(self.ws.root))

    def test_read_relative_path(self):
        out = handler.read_file(self.ctx, path="hello.txt")
        self.assertTrue(out["ok"])
        self.assertEqual(out["line_count"], 3)
        self.assertIn("1\thello", out["content"])
        self.assertIn("2\tworld", out["content"])

    def test_read_absolute_path_inside_workspace(self):
        out = handler.read_file(self.ctx, path=str(self.ws.root / "hello.txt"))
        self.assertTrue(out["ok"])

    def test_read_offset_and_limit(self):
        out = handler.read_file(self.ctx, path="hello.txt", offset=1, limit=1)
        self.assertTrue(out["ok"])
        self.assertEqual(out["lines_returned"], 1)
        self.assertIn("2\tworld", out["content"])

    def test_read_path_not_found(self):
        out = handler.read_file(self.ctx, path="nope.txt")
        self.assertFalse(out["ok"])
        self.assertEqual(out["error"], "path_not_found")

    def test_read_directory_refused(self):
        out = handler.read_file(self.ctx, path="sub")
        self.assertEqual(out["error"], "path_not_a_file")

    def test_read_binary_refused(self):
        out = handler.read_file(self.ctx, path="binary.bin")
        self.assertEqual(out["error"], "binary_content")

    def test_read_invalid_limit(self):
        out = handler.read_file(self.ctx, path="hello.txt", limit=0)
        self.assertEqual(out["error"], "input_invalid")
        out = handler.read_file(self.ctx, path="hello.txt", limit=99999)
        self.assertEqual(out["error"], "input_invalid")

    def test_read_invalid_offset(self):
        out = handler.read_file(self.ctx, path="hello.txt", offset=-1)
        self.assertEqual(out["error"], "input_invalid")


class WorkspaceScopeTests(unittest.TestCase):
    def setUp(self):
        self.ws = _Workspace()
        self.outside = tempfile.TemporaryDirectory()
        (Path(self.outside.name) / "outside.txt").write_text("outside\n", encoding="utf-8")
        self.addCleanup(self.ws.cleanup)
        self.addCleanup(self.outside.cleanup)

    def test_outside_workspace_refused_without_capability(self):
        ctx = _ctx(str(self.ws.root))
        out = handler.read_file(ctx, path=str(Path(self.outside.name) / "outside.txt"))
        self.assertFalse(out["ok"])
        self.assertEqual(out["error"], "path_outside_workspace")

    def test_outside_workspace_admitted_with_capability(self):
        ctx = _ctx(str(self.ws.root), "filesystem_outside_workspace")
        out = handler.read_file(ctx, path=str(Path(self.outside.name) / "outside.txt"))
        self.assertTrue(out["ok"])
        self.assertIn("outside", out["content"])

    def test_documents_path_blocked_even_with_capability(self):
        # We can't actually create a file there in this test; we assert
        # the resolution path is refused without touching disk.
        ctx = _ctx(str(self.ws.root), "filesystem_outside_workspace")
        out = handler.read_file(ctx, path="/Users/nolan/Documents/anything.txt")
        self.assertFalse(out["ok"])
        self.assertEqual(out["error"], "path_blocked_always")

    def test_ssh_dir_blocked_even_with_capability(self):
        ctx = _ctx(str(self.ws.root), "filesystem_outside_workspace")
        out = handler.read_file(ctx, path="/Users/test/.ssh/id_rsa")
        self.assertEqual(out["error"], "path_blocked_always")


class ListDirectoryTests(unittest.TestCase):
    def setUp(self):
        self.ws = _Workspace()
        self.addCleanup(self.ws.cleanup)
        self.ctx = _ctx(str(self.ws.root))

    def test_list_workspace_root(self):
        out = handler.list_directory(self.ctx, path=".")
        self.assertTrue(out["ok"])
        names = [e["name"] for e in out["entries"]]
        self.assertIn("hello.txt", names)
        self.assertIn("sub", names)
        # Hidden by default.
        self.assertNotIn(".secret", names)

    def test_list_with_hidden(self):
        out = handler.list_directory(self.ctx, path=".", include_hidden=True)
        names = [e["name"] for e in out["entries"]]
        self.assertIn(".secret", names)

    def test_list_subdir(self):
        out = handler.list_directory(self.ctx, path="sub")
        self.assertTrue(out["ok"])
        names = [e["name"] for e in out["entries"]]
        self.assertEqual(names, ["nested.md"])

    def test_list_file_refused(self):
        out = handler.list_directory(self.ctx, path="hello.txt")
        self.assertEqual(out["error"], "path_not_a_directory")

    def test_list_path_not_found(self):
        out = handler.list_directory(self.ctx, path="nope")
        self.assertEqual(out["error"], "path_not_found")

    def test_entry_metadata_shape(self):
        out = handler.list_directory(self.ctx, path=".")
        for entry in out["entries"]:
            if entry["name"] == "hello.txt":
                self.assertEqual(entry["type"], "file")
                self.assertGreater(entry["size_bytes"], 0)
            if entry["name"] == "sub":
                self.assertEqual(entry["type"], "directory")
                self.assertEqual(entry["entry_count"], 1)


class HandleDispatchTests(unittest.TestCase):
    def setUp(self):
        self.ws = _Workspace()
        self.addCleanup(self.ws.cleanup)
        self.ctx = _ctx(str(self.ws.root))

    def test_handle_dispatches_read_file(self):
        out = handler.handle(self.ctx, "read_file", {"path": "hello.txt"})
        self.assertTrue(out["ok"])

    def test_handle_dispatches_list_directory(self):
        out = handler.handle(self.ctx, "list_directory", {"path": "."})
        self.assertTrue(out["ok"])

    def test_handle_unknown_tool(self):
        out = handler.handle(self.ctx, "frobnicate", {})
        self.assertEqual(out["error"], "unknown_tool")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
