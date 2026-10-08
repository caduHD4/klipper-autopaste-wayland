# SPDX-License-Identifier: GPL-2.0-or-later
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BuildGuardTest(unittest.TestCase):
    def run_guard(self, version, *args):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            pacman = path / 'pacman'
            pacman.write_text('#!/bin/sh\nprintf "%s\\n" "plasma-workspace ' + version + '"\n')
            pacman.chmod(0o755)
            makepkg = path / 'makepkg'
            makepkg.write_text('#!/bin/sh\necho "unexpected package build" >&2\nexit 93\n')
            makepkg.chmod(0o755)
            return subprocess.run(['/bin/bash', str(ROOT / 'build-package.sh'), *args],
                                  env=dict(os.environ, PATH=str(path) + ':' + os.environ['PATH']),
                                  capture_output=True, text=True)

    def test_matching_upstream_accepts_different_package_releases_without_build(self):
        for version in ('6.7.4-3.1', '6.7.4-3.2', '6.7.4-3.3'):
            result = self.run_guard(version, '--check')
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_newer_upstream_refuses_before_build_or_downgrade(self):
        result = self.run_guard('6.7.5-1.1')
        self.assertEqual(result.returncode, 1)
        self.assertIn('Refusing', result.stderr)
        self.assertNotIn('unexpected package build', result.stderr)

    def test_unknown_arguments_refuse(self):
        self.assertEqual(self.run_guard('6.7.4-3.2', '--force').returncode, 2)
