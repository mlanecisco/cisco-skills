"""Check this assessment's batch coverage and independently specified categories."""

import json
import sys
from collections import Counter
from pathlib import Path


def check(records, output, expected):
    errors = []
    if not isinstance(output, list):
        return ["output must be a JSON array"]
    expected_ids = Counter(row["source_id"] for row in records)
    actual_ids = Counter()
    categories = {row["source_id"]: row["category"] for row in expected}
    for index, row in enumerate(output):
        if not isinstance(row, dict) or not isinstance(row.get("source_id"), str):
            errors.append(f"row {index}: missing string source_id")
            continue
        key = row["source_id"]
        actual_ids[key] += 1
        if row.get("category") != categories.get(key) or key not in categories:
            errors.append(f"{key}: incorrect or missing category")
    missing = expected_ids - actual_ids
    extra = actual_ids - expected_ids
    if missing:
        errors.append(f"missing source rows: {dict(missing)}")
    if extra:
        errors.append(f"unexpected or duplicated source rows: {dict(extra)}")
    return errors


if __name__ == "__main__":
    records, output, expected = [json.loads(Path(p).read_text()) for p in sys.argv[1:]]
    errors = check(records, output, expected)
    print("\n".join(errors) if errors else "PASS: coverage and categories match this fixture")
    raise SystemExit(bool(errors))
