"""Acceptance checks using independently specified dashboard totals."""

import json
import unittest
from pathlib import Path

from summary import summarize

ROOT = Path(__file__).resolve().parent
RECORDS = json.loads((ROOT / "records.json").read_text())
EXPECTED = json.loads((ROOT / "expected.json").read_text())


class DashboardSummaryTests(unittest.TestCase):
    def test_unfiltered_summary(self):
        self.assertEqual(summarize(RECORDS), EXPECTED["all"])

    def test_east_filter_changes_completion_rate(self):
        self.assertEqual(summarize(RECORDS, "East"), EXPECTED["East"])

    def test_west_filter_changes_completion_rate(self):
        self.assertEqual(summarize(RECORDS, "West"), EXPECTED["West"])

    def test_unknown_region_has_empty_summary(self):
        self.assertEqual(summarize(RECORDS, "North"), EXPECTED["empty"])

    def test_empty_records_have_empty_summary(self):
        self.assertEqual(summarize([]), EXPECTED["empty"])


if __name__ == "__main__":
    unittest.main()
