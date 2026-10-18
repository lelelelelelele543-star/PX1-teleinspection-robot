"""Offline smoke tests for the PX1 process-level parallel Codex runner.

No model calls. Uses an intentionally fake local codex executable in a
temporary disposable Git repository. On GitHub Actions this runs in Linux.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SOURCE_ROOT = Path(__file__).resolve().parents[1]


def cmd(argv: list[str], cwd: Path, env: dict | None = None):
    return subprocess.run(argv, cwd=cwd, env=env, capture_output=True,
                          text=True, encoding="utf-8", errors="replace",
                          check=False, timeout=50)


FAKE_CODEX = r'''#!/usr/bin/env python3
import pathlib
import re
import sys
import time
prompt = sys.stdin.read()
dest = pathlib.Path(sys.argv[sys.argv.index("--output-last-message") + 1])
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text("fake codex only\n", encoding="utf-8")
if "PX1 isolated specialist:" in prompt:
    role = re.search(r"PX1 isolated specialist: ([a-z_]+)", prompt).group(1)
    folder = pathlib.Path.cwd() / "autonomy" / "team_work" / role
    folder.mkdir(parents=True, exist_ok=True)
    time.sleep(0.20)
    (folder / "REPORT.md").write_text(
        "role = " + role + "\nPASS: fake test only\n", encoding="utf-8")
else:
    progress = pathlib.Path.cwd() / "autonomy" / "PX1_TEAM_PROGRESS.md"
    progress.write_text("STATUS: IN_PROGRESS\nThree mock reports integrated\n",
                        encoding="utf-8")
    (pathlib.Path.cwd() / "autonomy" / "PX1_WORK_PACKAGES.json").write_text(
        '{"reference":"recheck reference","tether":"recheck tether","qa":"recheck QA"}\n',
        encoding="utf-8")
'''


@unittest.skipUnless(os.name == "posix", "Fake Codex executable uses POSIX shebang")
class ParallelRunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="px1-team-test-")
        self.root = Path(self.temp.name) / "project"
        self.root.mkdir()
        (self.root / "tools").mkdir()
        (self.root / "autonomy").mkdir()
        (self.root / "current").mkdir()
        shutil.copy2(SOURCE_ROOT / "tools" / "px1_parallel.py",
                     self.root / "tools" / "px1_parallel.py")
        (self.root / "AGENTS.md").write_text("Test repo\n", encoding="utf-8")
        (self.root / "autonomy" / "PX1_TEAM_BRIEF.md").write_text(
            "Test team brief\n", encoding="utf-8")
        (self.root / "autonomy" / "PX1_TEAM_PROGRESS.md").write_text(
            "STATUS: IN_PROGRESS\n", encoding="utf-8")
        (self.root / "current" / "README.md").write_text("Test\n", encoding="utf-8")
        (self.root / "current" / "HOLD_REGISTER.json").write_text(
            "[]\n", encoding="utf-8")
        (self.root / "autonomy" / "PX1_WORK_PACKAGES.json").write_text(
            '{"reference":"test reference","tether":"test tether","qa":"test qa"}\n',
            encoding="utf-8")
        (self.root / ".gitignore").write_text(
            ".px1-agent/\n__pycache__/\n", encoding="utf-8")
        for a in [
            ["git", "init"],
            ["git", "config", "user.email", "px1-tests@example.invalid"],
            ["git", "config", "user.name", "PX1 Test"],
            ["git", "add", "."],
            ["git", "commit", "-m", "isolated fixture"],
        ]:
            result = cmd(a, self.root)
            self.assertEqual(result.returncode, 0, result.stderr)
        bin_dir = Path(self.temp.name) / "bin"
        bin_dir.mkdir()
        fake = bin_dir / "codex"
        fake.write_text(FAKE_CODEX, encoding="utf-8")
        fake.chmod(0o755)
        self.env = os.environ.copy()
        self.env["PATH"] = str(bin_dir) + os.pathsep + self.env.get("PATH", "")
        self.run_script = [sys.executable, str(self.root / "tools" / "px1_parallel.py")]

    def tearDown(self):
        self.temp.cleanup()

    def test_dry_run_has_no_writes(self):
        result = cmd(self.run_script + ["--dry-run"], self.root, self.env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("DRY RUN OK", result.stdout)
        self.assertFalse((self.root / ".px1-agent").exists())
        self.assertFalse((self.root / "autonomy" / "team_work").exists())

    def test_three_isolated_workers_and_coordinator(self):
        result = cmd(self.run_script + ["--rounds", "1", "--timeout", "60"],
                     self.root, self.env)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        for role in ["reference", "tether", "qa"]:
            path = self.root / "autonomy" / "team_work" / role / "REPORT.md"
            self.assertTrue(path.is_file(), f"Missing {path}")
            self.assertIn(role, path.read_text(encoding="utf-8"))
        runs = list((self.root / ".px1-agent" / "parallel").glob("*/round-01/results.json"))
        self.assertEqual(len(runs), 1)
        meta = json.loads(runs[0].read_text(encoding="utf-8"))
        self.assertEqual(len(meta["roles"]), 3)
        self.assertEqual(meta["coordinator"]["return_code"], 0)
        self.assertTrue(all(row["return_code"] == 0 for row in meta["roles"]))
        self.assertEqual(
            "IN_PROGRESS",
            (self.root / "autonomy" / "PX1_TEAM_PROGRESS.md")
            .read_text(encoding="utf-8").splitlines()[0].split()[-1],
        )
        active = cmd(["git", "worktree", "list", "--porcelain"], self.root)
        self.assertEqual(active.returncode, 0, active.stderr)
        self.assertEqual(active.stdout.count("worktree "), 1,
                         "Temporary engineering worktrees leaked")

    def test_dirty_repo_requires_explicit_opt_in(self):
        (self.root / "AGENTS.md").write_text("Locally edited\n", encoding="utf-8")
        result = cmd(self.run_script + ["--rounds", "1", "--timeout", "60"],
                     self.root, self.env)
        self.assertEqual(result.returncode, 2)
        self.assertIn("--allow-dirty", result.stderr)
        self.assertFalse((self.root / ".px1-agent").exists())

    def test_invalid_work_package_rejected(self):
        (self.root / "autonomy" / "PX1_WORK_PACKAGES.json").write_text(
            '{"qa": 42}', encoding="utf-8")
        result = cmd(self.run_script + ["--dry-run"], self.root, self.env)
        self.assertEqual(result.returncode, 2)
        self.assertIn("Invalid role work packages", result.stderr)


if __name__ == "__main__":
    unittest.main()
