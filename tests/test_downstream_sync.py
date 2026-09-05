#!/usr/bin/env python3
"""Test downstream publication against disposable local repositories only."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1]/'bin/sync-downstream.sh'


class DownstreamTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='cortana-downstream-test-')
        self.base = Path(self.temp.name)
        self.reg = self.base/'registry'
        self.mirror = self.base/'mirror'
        self.reg_remote = self.base/'registry.git'
        self.mirror_remote = self.base/'mirror.git'
        for root, remote in [(self.reg, self.reg_remote), (self.mirror, self.mirror_remote)]:
            self.git(self.base, 'init', '-q', '--bare', str(remote))
            self.git(self.base, 'init', '-q', '-b', 'main', str(root))
            self.git(root, 'config', 'user.name', 'Fixture')
            self.git(root, 'config', 'user.email', 'fixture@example.invalid')
            self.git(root, 'config', 'core.hooksPath', '.git/hooks')
            self.git(root, 'remote', 'add', 'origin', str(remote))
            (root/'skills'/'alpha').mkdir(parents=True)
            (root/'skills'/'alpha'/'SKILL.md').write_text('published' if root == self.reg else 'previous')
        (self.mirror/'skills'/'retired').mkdir()
        (self.mirror/'skills'/'retired'/'SKILL.md').write_text('preserve me')
        (self.reg/'bin').mkdir()
        shutil.copy2(SOURCE, self.reg/'bin'/'sync-downstream.sh')
        for root in [self.reg, self.mirror]:
            self.git(root, 'add', '.')
            self.git(root, 'commit', '-qm', 'fixture baseline')
            self.git(root, 'push', '-q', 'origin', 'main')
        self.before = self.git(self.mirror_remote, 'rev-parse', 'refs/heads/main').strip()

    def tearDown(self):
        self.temp.cleanup()

    def git(self, root, *args):
        return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.STDOUT, text=True)

    def run_sync(self):
        env = dict(os.environ, SKILL_MIRROR=str(self.mirror), TMPDIR=str(self.base))
        return subprocess.run(['bash', str(self.reg/'bin'/'sync-downstream.sh')], env=env, capture_output=True, text=True)

    def test_committed_snapshot_and_replacement_backup(self):
        (self.reg/'skills'/'alpha'/'SKILL.md').write_text('unpublished edit')
        (self.reg/'skills'/'unpublished').mkdir()
        (self.reg/'skills'/'unpublished'/'SKILL.md').write_text('unpublished addition')
        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertEqual((self.mirror/'skills'/'alpha'/'SKILL.md').read_text(), 'published')
        self.assertFalse((self.mirror/'skills'/'unpublished').exists())
        backups = list((self.base/'.trash').glob('**/SKILL.md'))
        self.assertEqual({p.read_text() for p in backups}, {'previous', 'preserve me'})
        self.assertEqual(self.git(self.mirror_remote, 'show', 'main:skills/alpha/SKILL.md'), 'published')

    def test_dirty_mirror_is_untouched(self):
        (self.mirror/'skills'/'alpha'/'SKILL.md').write_text('operator edit')
        self.git(self.mirror, 'add', 'skills/alpha/SKILL.md')
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('mirror has existing changes', result.stdout)
        self.assertEqual((self.mirror/'skills'/'alpha'/'SKILL.md').read_text(), 'operator edit')
        self.assertEqual(self.git(self.mirror, 'show', ':skills/alpha/SKILL.md'), 'operator edit')
        self.assertEqual(self.git(self.mirror_remote, 'rev-parse', 'refs/heads/main').strip(), self.before)

    def test_failed_commit_never_pushes(self):
        hook = self.mirror/'.git'/'hooks'/'pre-commit'
        hook.write_text('#!/bin/sh\nexit 1\n')
        hook.chmod(0o755)
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('mirror push skipped', result.stdout)
        self.assertEqual(self.git(self.mirror_remote, 'rev-parse', 'refs/heads/main').strip(), self.before)
        self.assertNotEqual(self.git(self.mirror, 'diff', '--cached', '--name-only').strip(), '')


if __name__ == '__main__':
    unittest.main()
