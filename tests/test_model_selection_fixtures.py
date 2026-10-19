"""Verify selection assessment inputs expose real contract and tool failures."""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

FIXTURES = Path(__file__).resolve().parents[1] / "evals/fixtures/model-selection"


class ModelSelectionFixtureTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def copy_project(self, name: str) -> None:
        shutil.copytree(FIXTURES / name, self.root / "project")

    def run_python(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-B", *args],
            cwd=self.root / "project",
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )

    def check_contract(self) -> subprocess.CompletedProcess[str]:
        return self.run_python(str(FIXTURES / "checks.py"), str(self.root / "project"))

    def test_existing_starter_tests_pass_but_new_key_is_not_implemented(self) -> None:
        self.copy_project("starter")
        result = self.run_python("-m", "unittest", "discover", "-s", "tests")
        self.assertEqual(result.returncode, 0, result.stderr)
        contract = self.check_contract()
        self.assertNotEqual(contract.returncode, 0)
        self.assertIn("new client: expected", contract.stdout)
        self.assertIn("precedence: expected", contract.stdout)

    def test_passing_candidate_tests_do_not_establish_legacy_compatibility(
        self,
    ) -> None:
        self.copy_project("candidate")
        result = self.run_python("-m", "unittest", "discover", "-s", "tests")
        self.assertEqual(result.returncode, 0, result.stderr)
        contract = self.check_contract()
        self.assertEqual(contract.returncode, 1)
        self.assertIn("legacy client: expected", contract.stdout)
        self.assertEqual(len(contract.stdout.splitlines()), 1)

    def test_independent_checks_accept_both_keys_and_new_key_precedence(self) -> None:
        self.copy_project("candidate")
        (self.root / "project/configuration.py").write_text(
            "def resolve_url(config):\n"
            "    if 'service_url' in config:\n"
            "        return config['service_url']\n"
            "    if 'endpoint' in config:\n"
            "        return config['endpoint']\n"
            "    return 'https://default.invalid'\n"
        )
        contract = self.check_contract()
        self.assertEqual(contract.returncode, 0, contract.stdout)

    def test_tool_failure_is_non_mutating_and_separate_from_model_execution(
        self,
    ) -> None:
        self.copy_project("starter")
        before = {
            p.relative_to(self.root): p.read_bytes()
            for p in self.root.rglob("*")
            if p.is_file()
        }
        result = self.run_python(str(FIXTURES / "blocked_tool.py"))
        self.assertEqual(result.returncode, 77)
        error = json.loads(result.stderr)
        self.assertEqual(error["error"], "permission_denied")
        self.assertFalse(error["execution_started"])
        after = {
            p.relative_to(self.root): p.read_bytes()
            for p in self.root.rglob("*")
            if p.is_file()
        }
        self.assertEqual(after, before)


if __name__ == "__main__":
    unittest.main()
