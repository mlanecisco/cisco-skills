---
author: Mark A. Lane, Ph.D.
---

# Reporting utility

Use Python 3.11 or later and the development dependencies in `requirements-dev.txt`.

Project commands, run from this directory:

```text
python scripts/lint.py
python -m ruff format .
python -m unittest discover -s tests -v
```

The reporting function returns the sum of supplied numeric values. An empty list returns zero.
