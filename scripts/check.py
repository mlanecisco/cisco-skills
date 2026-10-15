"""Run the library's maintainer checks with the active Python environment."""

import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    checks = [
        ("Lint", ["-m", "ruff", "check", "."]),
        ("Format", ["-m", "ruff", "format", "--check", "."]),
        ("Types", ["-m", "mypy"]),
        ("Regression tests", ["-m", "unittest", "discover", "-s", "tests", "-v"]),
        ("Library structure", ["scripts/validate_library.py"]),
    ]
    failed = []
    for label, arguments in checks:
        print(f"\n{label}", flush=True)
        if subprocess.run(
            [sys.executable, *arguments], cwd=root, check=False
        ).returncode:
            failed.append(label)
    if failed:
        print(f"\nFailed: {', '.join(failed)}", file=sys.stderr)
        return 1
    print("\nAll maintainer checks passed. Product behavior was not evaluated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
