"""Check that the evaluation oracle rejects the seeds and accepts correct behavior."""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

FIXTURE = Path(__file__).resolve().parents[1] / "evals" / "fixtures" / "development"
CORRECT = """
def summarize(records, region=None):
    selected = [r for r in records if region is None or r["region"] == region]
    count = len(selected)
    completed = sum(r["status"] == "complete" for r in selected)
    return {
        "count": count,
        "total_value": sum(r["value"] for r in selected),
        "completion_rate": completed / count * 100 if count else 0.0,
    }
"""


class DevelopmentFixtureTests(unittest.TestCase):
    def run_acceptance(self, source: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ["records.json", "expected.json", "test_summary.py"]:
                shutil.copyfile(FIXTURE / name, root / name)
            (root / "summary.py").write_text(source, encoding="utf-8")
            return subprocess.run(
                [sys.executable, "-m", "unittest", "discover", "-s", ".", "-v"],
                cwd=root,
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )

    def test_feature_seed_does_not_meet_acceptance_criteria(self) -> None:
        result = self.run_acceptance((FIXTURE / "summary.py").read_text())
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("completion_rate", result.stderr)

    def test_defect_seed_fails_for_region_filters(self) -> None:
        result = self.run_acceptance((FIXTURE / "buggy_summary.py").read_text())
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("FAIL: test_east_filter_changes_completion_rate", result.stderr)
        self.assertIn("FAIL: test_west_filter_changes_completion_rate", result.stderr)

    def test_correct_calculation_meets_all_acceptance_criteria(self) -> None:
        result = self.run_acceptance(CORRECT)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Ran 5 tests", result.stderr)


if __name__ == "__main__":
    unittest.main()
