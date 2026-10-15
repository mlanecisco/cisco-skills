---
author: Mark A. Lane, Ph.D.
status: Maintainer guide
---

# Maintaining the library

Use Python 3.11 or later. Create an isolated environment and install the pinned maintainer tools once from the repository root. The commands below use Python 3.12 as an example.

macOS:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/check.py
```

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe scripts/check.py
```

If the installed supported Python has a different command or version, use that command for the first line. Environment activation is optional because the remaining commands address its interpreter directly. With uv already installed, `uv venv --python 3.12 .venv` and `uv pip install --python .venv -r requirements-dev.txt` are alternatives.

After setup, run the last command whenever the library changes. CI uses `python scripts/check.py` in its configured Python environment. The workflow is prepared for GitHub; it has not run there while this repository has no remote.

## What the command checks

| Check | Coverage |
| --- | --- |
| Ruff lint and formatting | Maintainer Python code and configuration |
| mypy | Types in the maintainer scripts |
| unittest | Validator regressions and the development fixture's acceptance oracle |
| Library validator | Skill metadata, exact manifest names, local Markdown links, configuration syntax, and evaluation definitions |

The validator follows the [Agent Skills specification](https://agentskills.io/specification). It rejects duplicate YAML and JSON keys, malformed files, unresolved local links, cross-folder skill dependencies, and evaluation cases that refer to unknown skills or missing fixtures. Agent examples receive syntax and required-field checks; their model availability and runtime behavior are not established by parsing.

Markdown links, images, and reference-style links are checked with a Markdown parser. Local links in every Markdown file within a skill, including supporting references and nested resources, must resolve inside that skill's folder. The check resolves symbolic links before testing the boundary. Repository documentation can link across folders within the repository.

External URLs and heading anchors are not fetched or verified. Literal paths in prose and code blocks are not checked as links. Tool caches and generated outputs are excluded from discovery. Evaluation input code under `evals/fixtures/` is deliberately unfinished or defective and is excluded from maintainer linting and typing; separate tests verify its acceptance oracle.

To run only structural checks, including against an isolated fixture:

```bash
python scripts/validate_library.py --root /path/to/library
```

Use the environment's Python interpreter when the shell's default is different. Failed checks return a nonzero status with the file and problem. The validator does not execute bundled scripts, invoke agents, or establish the quality of an artifact.

## Adding a skill

Create a folder under `skills/` with a matching name and `SKILL.md`. Use standard frontmatter, keep instructions focused, and bundle any resources the skill actually needs. Keep local references within the skill folder so copying the folder preserves its instructions.

Add evaluation cases under `evals/` with a unique ID, target skill, realistic prompt, trigger expectation, and observable acceptance checks. Use `fixtures` for existing paths relative to the evaluation file and `fixtures_needed` for descriptive inputs still to be supplied. The latter does not prove that an evaluation is ready to run.

Run the maintainer command, then test behavior in the intended products. Record actual outputs and usage separately from evaluation specifications. Keep a draft label until those results justify a stronger claim. Preserve upstream licenses and notices whenever material is incorporated.

## Updating tools

The supported ranges are in `requirements-dev.in`; exact resolved versions are in `requirements-dev.txt`. With uv, regenerate the pinned file using its recorded compile command, then reinstall and run the checks on supported Python versions. Review dependency changes before committing them. Do not edit tool rules or acceptance criteria merely to conceal a failure.
