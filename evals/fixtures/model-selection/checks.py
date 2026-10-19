"""Held-out checks for the fixture's old and new configuration contract."""

import importlib.util
from pathlib import Path
import sys

project = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("assessed_configuration", project / "configuration.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
cases = [
    ("new client", {"service_url": "https://new.invalid"}, "https://new.invalid"),
    ("legacy client", {"endpoint": "https://legacy.invalid"}, "https://legacy.invalid"),
    ("precedence", {"service_url": "https://new.invalid", "endpoint": "https://legacy.invalid"}, "https://new.invalid"),
    ("default", {}, "https://default.invalid"),
]
errors = []
for name, config, expected in cases:
    actual = module.resolve_url(config)
    if actual != expected:
        errors.append(f"{name}: expected {expected!r}, got {actual!r}")
print("\n".join(errors) if errors else "PASS: all four independent compatibility checks")
raise SystemExit(bool(errors))
