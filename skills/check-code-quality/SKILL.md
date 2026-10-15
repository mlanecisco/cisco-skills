---
name: check-code-quality
description: Configure or run appropriate code-quality checks, including formatters, linters, type checking, tests, and builds. Use when the user requests these checks or a development workflow needs verification; preserve a check-only request without editing files.
metadata:
  author: Mark A. Lane, Ph.D.
  version: "0.1.0"
  status: draft
---

# Check code quality

Use deterministic tools to check the code and report what the results establish. Keep the user's existing tooling and avoid introducing overlapping tools without a reason.

## Discover the checks

Read the project instructions, relevant dependency manifests, tool configuration, package scripts, and CI workflow. Identify the commands for formatting, linting, type checking, tests, and building. Inspect what scripts actually do before running them; a script named `lint` may also modify files.

Read [tooling guidance](references/tooling.md) only for the relevant language or stack. The examples are candidates, not required installations. For an existing project, prefer its documented commands, package manager, lockfile, and local environment.

For a new project or a request to set up checks, choose a small compatible set and expose clear project commands. Include only checks meaningful for that project. Explain necessary tool choices briefly and install dependencies within the authorized project environment.

## Run the checks

For a check-only request, use non-writing modes and report findings. Do not reformat code or apply fixes. If only a writing command is available, identify that limitation and use a supported non-writing alternative when possible.

During development, start with relevant files and focused tests. Before calling the change ready, run the applicable broader checks, including a production build where one is configured. Avoid rerunning unchanged successful checks unless an edit or unresolved concern justifies it.

Keep tool output concise: report the command, result, and actionable failure details. Preserve enough evidence to reproduce a problem. Distinguish pre-existing failures, new failures, missing dependencies, and checks that do not apply. An unavailable tool is not a passing check.

If fixes are requested or already authorized, correct the underlying problem while preserving behavior and unrelated user changes. Apply formatter fixes only to the relevant scope. Rerun the affected checks after corrections. Do not remove tests, relax type checks, add broad ignores, or disable lint rules solely to obtain a pass.

## Interpret the results

Formatting checks consistency; linting identifies configured code problems; type checking tests the configured type assumptions. None of those alone establishes that the requested behavior works. Retain meaningful behavioral tests and browser checks for relevant user flows.

For CI setup, run the same project commands used locally. Keep the workflow within the requested scope. Report configuration validation separately from an actual hosted CI run.

## Deliver

Provide a compact record of the applicable checks and their results, with unresolved failures and skipped checks explained. If setup changed, identify the configuration and commands the user or their agent can use next. Prefer a single documented check command when the project benefits from one.

## Example requests

- "Run the linters, tests, and build before we use this dashboard."
- "Set up sensible code-quality checks for this new Python project."
- "Check formatting and types, but don't change any files."
