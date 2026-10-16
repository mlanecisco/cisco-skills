"""Run the project's lint command."""

import subprocess
import sys
from pathlib import Path

raise SystemExit(
    subprocess.run(
        [sys.executable, "-m", "ruff", "check", ".", "--fix"],
        cwd=Path(__file__).resolve().parents[1],
        check=False,
    ).returncode
)
