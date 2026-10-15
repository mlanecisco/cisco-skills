---
author: Mark A. Lane, Ph.D.
status: Tool selection guidance
---

# Tooling by project

Use the commands already defined by the project. These examples apply when the named tool is installed and the referenced scripts or targets exist. Inspect configuration before executing commands that may write files or access external systems.

## JavaScript and TypeScript

Inspect `package.json`, the lockfile, formatter and linter configuration, and `tsconfig.json` where present. Use the existing package manager; avoid creating a second lockfile.

Common checks are an [ESLint](https://eslint.org/docs/latest/use/getting-started) command, a [Prettier check](https://prettier.io/docs/cli#--check), TypeScript checking without emitted output where appropriate, the project's test runner, and the production build. Existing scripts may expose these as `lint`, `format:check`, `typecheck`, `test`, and `build`; those names are not guaranteed.

Use non-watch test runs for unattended checks. Exercise important browser interactions with the project's browser tooling when available. Passing a build does not establish that filters, forms, or calculations work.

## Python

Inspect `pyproject.toml`, dependency files, and the project's virtual environment and test configuration. A small project can use [Ruff](https://docs.astral.sh/ruff/) for linting and formatting, plus its existing tests. Add [mypy](https://mypy.readthedocs.io/en/stable/running_mypy.html) or another established type checker when useful and compatible with the code.

Examples for configured tools:

```bash
python -m ruff check .
python -m ruff format --check .
python -m mypy
python -m unittest discover -s tests
```

The bare mypy command needs configured targets. Use the existing pytest command instead of unittest when the project uses pytest. Do not introduce a second test framework just for a small change.

## Other stacks and mixed projects

Use the language's established tools and the repository's scripts. Identify which subprojects a change affects and run their relevant checks. A documentation-only project does not need an application build, and untyped code does not automatically need a new typing system.

## Check versus fix

Check modes should leave source files unchanged. Formatter write modes and automatic lint fixes need an editing request or existing authorization. Some formatters and linters overlap; choose a compatible combination and avoid conflicting style rules.
