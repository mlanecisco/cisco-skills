"""Verify assessment checks reject the seeds without requiring agent sessions."""

import hashlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

FIXTURES = Path(__file__).resolve().parents[1] / "evals/fixtures"


class AssessmentFixtureTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.project = Path(temporary.name) / "project"

    def run_command(self, arguments: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, *arguments],
            cwd=self.project,
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )

    def test_holdout_checks_reject_seed_and_accept_correct_behavior(self) -> None:
        shutil.copytree(FIXTURES / "assessment/project", self.project)
        command = [str(FIXTURES / "assessment/checks.py"), str(self.project)]
        original = self.run_command(command)
        self.assertEqual(original.returncode, 1, original.stdout)
        self.assertIn("West: expected", original.stdout)
        self.assertIn("unseen records: expected", original.stdout)
        (self.project / "summary.py").write_text(
            "def summarize(records, region=None):\n"
            "    rows = [r for r in records\n"
            "            if region is None or r['region'] == region]\n"
            "    count = len(rows)\n"
            "    completed = sum(r['status'] == 'complete' for r in rows)\n"
            "    return {'count': count,\n"
            "            'total_value': sum(r['value'] for r in rows),\n"
            "            'completion_rate':\n"
            "                completed / count * 100 if count else 0.0}\n"
        )
        fixed = self.run_command(command)
        self.assertEqual(fixed.returncode, 0, fixed.stdout)

    def test_check_only_fixture_exposes_writing_lint_command(self) -> None:
        shutil.copytree(FIXTURES / "check-only/project", self.project)
        source = self.project / "report.py"
        before = hashlib.sha256(source.read_bytes()).hexdigest()
        lint = self.run_command(["-m", "ruff", "check", "--no-fix", "."])
        formatting = self.run_command(["-m", "ruff", "format", "--check", "."])
        behavior = self.run_command(["-m", "unittest", "discover", "-s", "tests"])
        self.assertNotEqual(lint.returncode, 0)
        self.assertNotEqual(formatting.returncode, 0)
        self.assertEqual(behavior.returncode, 0, behavior.stderr)
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), before)
        self.run_command(["scripts/lint.py"])
        self.assertNotEqual(hashlib.sha256(source.read_bytes()).hexdigest(), before)

    def test_configured_ruff_fixes_are_disabled_without_changing_project_rules(
        self,
    ) -> None:
        shutil.copytree(FIXTURES / "check-only/project", self.project)
        source = self.project / "report.py"
        config = self.project / "pyproject.toml"
        before = source.read_bytes()
        original_config = config.read_bytes()
        check = self.run_command(["-m", "ruff", "check", "--no-fix", "."])
        self.assertNotEqual(check.returncode, 0)
        self.assertIn("F401", check.stdout)
        self.assertEqual(source.read_bytes(), before)
        self.assertEqual(config.read_bytes(), original_config)
        self.run_command(["-m", "ruff", "check", "."])
        self.assertNotEqual(source.read_bytes(), before)

    def test_cache_disabled_checks_preserve_the_project_file_inventory(self) -> None:
        shutil.copytree(FIXTURES / "check-only/project", self.project)
        before = {
            path.relative_to(self.project): path.read_bytes()
            for path in self.project.rglob("*")
            if path.is_file()
        }
        lint = self.run_command(
            ["-B", "-m", "ruff", "check", "--no-fix", "--no-cache", "."]
        )
        formatting = self.run_command(
            ["-B", "-m", "ruff", "format", "--check", "--no-cache", "."]
        )
        behavior = self.run_command(["-B", "-m", "unittest", "discover", "-s", "tests"])
        self.assertNotEqual(lint.returncode, 0)
        self.assertNotEqual(formatting.returncode, 0)
        self.assertEqual(behavior.returncode, 0, behavior.stderr)
        after = {
            path.relative_to(self.project): path.read_bytes()
            for path in self.project.rglob("*")
            if path.is_file()
        }
        self.assertEqual(after, before)


if __name__ == "__main__":
    unittest.main()
