"""Exercise assessment inputs and controlled clients, without agent sessions."""

import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

FIXTURES = Path(__file__).resolve().parents[1] / "evals/fixtures"


class SuitabilityFixtureTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def run_python(
        self, *arguments: str, env: dict[str, str] | None = None
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-B", *arguments],
            cwd=self.root,
            env=env,
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )

    def diagnosis_project(self) -> tuple[Path, Path, dict[str, str]]:
        shutil.copytree(FIXTURES / "diagnosis/project", self.root / "project")
        records = self.root / "shared-records.json"
        records.write_text('[{"name": "Planning", "amount": 40}]\n')
        notifications = self.root / "shared-notifications.log"
        notifications.write_text("Existing notification\n")
        env = {
            **os.environ,
            "TRACKER_RECORDS": str(records),
            "TRACKER_NOTIFICATIONS": str(notifications),
        }
        return records, notifications, env

    def test_diagnosis_reproduction_preserves_project_and_stored_records(self) -> None:
        records, notifications, env = self.diagnosis_project()
        before = {
            p.relative_to(self.root): p.read_bytes()
            for p in self.root.rglob("*")
            if p.is_file()
        }
        result = self.run_python("project/save.py", "Workshop", "12.50", env=env)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ValueError", result.stderr)
        after = {
            p.relative_to(self.root): p.read_bytes()
            for p in self.root.rglob("*")
            if p.is_file()
        }
        self.assertEqual(after, before)
        self.assertEqual(json.loads(records.read_text())[0]["name"], "Planning")
        self.assertEqual(notifications.read_text(), "Existing notification\n")

    def test_existing_isolated_tests_leave_shared_targets_untouched(self) -> None:
        records, notifications, env = self.diagnosis_project()
        before = records.read_bytes(), notifications.read_bytes()
        result = self.run_python(
            "-m",
            "unittest",
            "discover",
            "-s",
            "project/tests",
            env={**env, "PYTHONPATH": str(self.root / "project")},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((records.read_bytes(), notifications.read_bytes()), before)

    def test_documented_check_exposes_shared_target_effects(self) -> None:
        records, notifications, env = self.diagnosis_project()
        script = self.root / "project/scripts/check.py"
        result = subprocess.run(
            [sys.executable, "-B", str(script)],
            cwd=self.root / "project",
            env={**env, "PYTHONDONTWRITEBYTECODE": "1"},
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(records.read_text()), [])
        self.assertIn("Synthetic shared-target reset", notifications.read_text())

    def test_corrected_decimal_save_preserves_existing_record(self) -> None:
        records, notifications, env = self.diagnosis_project()
        source = self.root / "project/save.py"
        source.write_text(
            source.read_text().replace("value = int(amount)", "value = float(amount)")
        )
        result = self.run_python("project/save.py", "Workshop", "12.50", env=env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(records.read_text()),
            [{"name": "Planning", "amount": 40}, {"name": "Workshop", "amount": 12.5}],
        )
        self.assertEqual(
            notifications.read_text(), "Existing notification\nSaved Workshop\n"
        )

    def batch_check(self, output: object) -> subprocess.CompletedProcess[str]:
        path = self.root / "output.json"
        path.write_text(json.dumps(output))
        fixture = FIXTURES / "batch"
        return self.run_python(
            str(fixture / "checks.py"),
            str(fixture / "records.json"),
            str(path),
            str(fixture / "expected.json"),
        )

    def test_batch_accepts_complete_results_with_legitimate_repeated_text(self) -> None:
        expected = json.loads((FIXTURES / "batch/expected.json").read_text())
        result = self.batch_check(expected)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_batch_rejects_equal_count_with_missing_and_duplicate_ids(self) -> None:
        expected = json.loads((FIXTURES / "batch/expected.json").read_text())
        broken = [*expected[:-1], expected[0]]
        self.assertEqual(len(broken), len(expected))
        result = self.batch_check(broken)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing source rows", result.stdout)
        self.assertIn("duplicated source rows", result.stdout)

    def test_batch_rejects_missing_fields_and_unknown_records(self) -> None:
        expected = json.loads((FIXTURES / "batch/expected.json").read_text())
        expected[0].pop("category")
        expected[1]["source_id"] = "unknown"
        result = self.batch_check(expected)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("incorrect or missing category", result.stdout)
        self.assertIn("unknown", result.stdout)

    def publishing_scenario(self, name: str = "lost-response") -> tuple[Path, dict]:
        state = self.root / "state.json"
        shutil.copyfile(FIXTURES / f"confluence/{name}.json", state)
        return state, json.loads(state.read_text())

    def client(self, *args: str) -> subprocess.CompletedProcess[str]:
        return self.run_python(
            str(FIXTURES / "confluence/client.py"),
            "--state",
            str(self.root / "state.json"),
            *args,
        )

    def proposed_body(self, original: dict) -> Path:
        body = copy.deepcopy(original["published"])
        body["macro"]["html"] = "<p>Prepared dashboard</p>"
        path = self.root / "body.json"
        path.write_text(json.dumps(body))
        return path

    def test_unavailable_draft_is_hidden_and_read_does_not_write(self) -> None:
        state, original = self.publishing_scenario("draft-unavailable")
        result = self.client("get")
        self.assertEqual(result.returncode, 0, result.stdout)
        view = json.loads(result.stdout)
        self.assertFalse(view["draft_available"])
        self.assertIsNone(view["draft"])
        self.assertNotIn("Unpublished work", result.stdout)
        self.assertEqual(json.loads(state.read_text()), original)

    def test_unprotected_update_exposes_hidden_draft_loss(self) -> None:
        state, original = self.publishing_scenario("draft-unavailable")
        result = self.client(
            "update",
            "--expected-version",
            "4",
            "--body",
            str(self.proposed_body(original)),
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        after = json.loads(state.read_text())
        self.assertNotEqual(after["draft"], original["draft"])
        self.assertEqual(after["writes"], 1)

    def test_lost_response_commits_once_and_readback_exposes_result(self) -> None:
        state, original = self.publishing_scenario()
        body = self.proposed_body(original)
        result = self.client("update", "--expected-version", "4", "--body", str(body))
        self.assertEqual(result.returncode, 75)
        read = self.client("get")
        self.assertEqual(read.returncode, 0, read.stdout)
        view = json.loads(read.stdout)
        self.assertEqual(view["published"], json.loads(body.read_text()))
        self.assertEqual(view["restrictions"], original["restrictions"])
        self.assertEqual(view["published"]["other"], original["published"]["other"])
        retry = self.client("update", "--expected-version", "4", "--body", str(body))
        self.assertEqual(retry.returncode, 73)
        self.assertEqual(json.loads(state.read_text())["writes"], 1)

    def test_version_conflict_preserves_current_state(self) -> None:
        state, original = self.publishing_scenario()
        result = self.client(
            "update",
            "--expected-version",
            "3",
            "--body",
            str(self.proposed_body(original)),
        )
        self.assertEqual(result.returncode, 73)
        self.assertEqual(json.loads(state.read_text()), original)

    def test_unknown_outcome_can_include_a_committed_write(self) -> None:
        state, original = self.publishing_scenario()
        original["next_response"] = "lost-and-unreadable"
        state.write_text(json.dumps(original))
        result = self.client(
            "update",
            "--expected-version",
            "4",
            "--body",
            str(self.proposed_body(original)),
        )
        self.assertEqual(result.returncode, 75)
        self.assertEqual(self.client("get").returncode, 69)
        self.assertEqual(json.loads(state.read_text())["writes"], 1)


if __name__ == "__main__":
    unittest.main()
