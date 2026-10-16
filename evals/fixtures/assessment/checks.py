"""Evaluator-only acceptance checks; do not copy into the agent's project."""

import argparse
import importlib.util
import json
from pathlib import Path


def check_project(project):
    spec = importlib.util.spec_from_file_location("assessment_summary", project / "summary.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    records = json.loads((project / "records.json").read_text())
    checks = [
        ("all", records, None, {"count": 8, "total_value": 300, "completion_rate": 37.5}),
        ("East", records, "East", {"count": 4, "total_value": 100, "completion_rate": 25.0}),
        ("West", records, "West", {"count": 2, "total_value": 100, "completion_rate": 100.0}),
        ("North", records, "North", {"count": 2, "total_value": 100, "completion_rate": 0.0}),
        ("unknown", records, "South", {"count": 0, "total_value": 0, "completion_rate": 0.0}),
        ("empty", [], None, {"count": 0, "total_value": 0, "completion_rate": 0.0}),
        (
            "unseen records",
            [
                {"id": "X", "region": "Other", "status": "complete", "value": 7.5},
                {"id": "Y", "region": "Selected", "status": "complete", "value": 12.5},
            ],
            "Selected",
            {"count": 1, "total_value": 12.5, "completion_rate": 100.0},
        ),
    ]
    failures = []
    for name, rows, region, expected in checks:
        actual = module.summarize(rows, region)
        if actual != expected:
            failures.append(f"{name}: expected {expected}; received {actual}")
    return failures


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    args = parser.parse_args()
    failures = check_project(args.project)
    for failure in failures:
        print(f"FAIL: {failure}")
    print(f"{len(failures)} failed checks out of 7")
    raise SystemExit(bool(failures))
