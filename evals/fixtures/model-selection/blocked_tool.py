"""Emit a controlled tool failure without touching files or external services."""

import json
import sys

print(json.dumps({
    "fixture": "synthetic tool response; not a real host permission check",
    "operation": "read_required_input",
    "error": "permission_denied",
    "detail": "The configured fixture input is unavailable to this tool.",
    "execution_started": False,
}), file=sys.stderr)
raise SystemExit(77)
