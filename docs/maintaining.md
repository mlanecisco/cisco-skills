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

After setup, run the last command whenever the library changes. CI uses `python scripts/check.py` in its configured Python environment. The repository has a public GitHub remote, `mlanecisco/cisco-skills` (visibility checked 2026-10-22), and the hosted "Library checks" workflow passed on commit `10a87bb` (run 39261842430, 2026-10-19). That run does not cover later commits.

## What the command checks

| Check | Coverage |
| --- | --- |
| Ruff lint and formatting | Maintainer Python code and configuration |
| mypy | Types in the maintainer scripts and the bundled publish scanner |
| unittest | Validator regressions and the development fixture's acceptance oracle |
| Library validator | Skill metadata, exact manifest names, local Markdown links, configuration syntax, and evaluation definitions |
| Evaluation records | Retained run identities, environment details, acceptance checks, outcomes, and evidence fields |

The validator follows the [Agent Skills specification](https://agentskills.io/specification). It rejects duplicate YAML and JSON keys, malformed files, unresolved local links, cross-folder skill dependencies, and symlinks anywhere in installable skills. Agent examples receive syntax and required-field checks; their model availability and runtime behavior are not established by parsing.

Markdown links, images, and reference-style links are checked with a Markdown parser. Local links in every Markdown file within a skill, including supporting references and nested resources, must resolve inside that skill's folder. The check resolves symbolic links before testing the boundary. Repository documentation can link across folders within the repository.

External URLs and heading anchors are not fetched or verified. Literal paths in prose and code blocks are not checked as links. Tool caches and generated outputs are excluded from discovery. Evaluation input code under `evals/fixtures/` is deliberately unfinished or defective and is excluded from maintainer linting and typing; separate tests verify its acceptance oracle.

To run only structural checks, including against an isolated fixture:

```bash
python scripts/validate_library.py --root /path/to/library
```

Use the environment's Python interpreter when the shell's default is different. Failed checks return a nonzero status with the file and problem. The validator does not execute bundled scripts, invoke agents, or establish the quality of an artifact.

## Adding a skill

Create a folder under `skills/` with a matching name and `SKILL.md`. Use standard frontmatter, keep instructions focused, and bundle any resources the skill actually needs. Keep local references within the skill folder so copying the folder preserves its instructions.

Place evaluation suites directly under `evals/`. Suite fields are `author`, `status`, `run_on`, and `cases`. Case fields are `id`, `skill`, `prompt`, `should_trigger`, `checks`, `fixtures`, `evaluator_fixtures`, and `fixtures_needed`; unknown fields fail validation. `run_on` accepts Claude Code, Codex, Cursor, Claude Desktop, and ChatGPT. Listing a product identifies an intended trial, not completed support.

Use `fixtures` for existing files or project directories, with plain relative paths from the suite file and forward slashes. URL schemes, queries, fragments, absolute paths, and paths outside the repository are rejected. `evaluator_fixtures` follows the same path rules and identifies inputs withheld from the agent. `fixtures_needed` describes unresolved prerequisites and does not establish readiness. JSON under `evals/fixtures/` is input data; retained evidence under `evals/results/` receives separate run-record validation through the maintainer command. Other nested suite locations fail.

Run the maintainer command, then test behavior in the intended products. Record actual outputs and usage separately from evaluation specifications. Keep a draft label until those results justify a stronger claim. Preserve upstream licenses and notices whenever material is incorporated.

Use the [evaluation guide](evaluations.md) to prepare independent runs and records. Use the [packaging guide](packaging.md) to build, verify, and pilot the exact skill archives. Planned record templates stay under `output/`; only reviewed completed attempts belong under `evals/results/`.

## Updating tools

The supported ranges are in `requirements-dev.in`; exact resolved versions are in `requirements-dev.txt`. With uv, regenerate the pinned file using its recorded compile command, then reinstall and run the checks on supported Python versions. Review dependency changes before committing them. Do not edit tool rules or acceptance criteria merely to conceal a failure.

## Release criteria and current status

A release needs correct triggering, valid artifacts, appropriate handling of missing inputs, and successful use in both target products. Check cases that should not activate the skill, as well as ordinary and difficult requests. For efficiency, compare total usage and quality against the same baseline task. A valid `SKILL.md` alone does not establish those results.

The latest local maintainer run passed linting, formatting, type checking, 129 regression tests, structural validation of seven skills and 59 evaluation definitions, and validation of two historical run records. Tests cover packaging, execution-record consistency, calculation and compatibility fixtures, non-fixing checks, isolated data targets, batch integrity, and controlled clients. Separate historical Codex batch attempts produced correct outputs: explicit invocation of efficiency `0.1.1` passed, while automatic activation remained unconfirmed. Current efficiency `0.3.0` and its new selection cases have no fresh product runs. Twenty-three cases still list needed inputs. The `check-before-publishing` scanner has regression tests; the skill has no product runs. No token savings, completed installation walkthroughs, or validated presentation sample is claimed.

The [validator](../scripts/validate_library.py) checks local Markdown links throughout each skill, rejects symlinked skill resources, requires existing relative local fixture paths, and rejects unknown evaluation fields and unsupported suite locations. The maintainer command also validates retained run records. The [audit follow-up](audits/2026-10-16-follow-up.md) and [skill revision record](audits/2026-10-16-skill-revision.md) distinguish implemented changes from pending product evidence.

The repository has a local package builder and verifier and a public GitHub remote, `mlanecisco/cisco-skills` (visibility checked 2026-10-22). The hosted "Library checks" workflow passed on commit `10a87bb` (run 39261842430, 2026-10-19). No release package is published, no installer is bundled, and no user installation trial has run. The immediate milestone is a tested pilot release with recorded artifacts, quality checks, installation results, and usage measurements.
