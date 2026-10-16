---
author: Mark A. Lane, Ph.D.
date: 2026-10-16
status: Pilot procedure and runnable fixtures; product trials pending
---

# Running the pilot evaluations

An evaluation is a recorded attempt in an identified product, using controlled inputs and independent checks. Passing the maintainer tests establishes that our tools and fixtures behave as asserted. It does not establish that a skill works in Claude Code, Codex, or Cursor.

Start with the four development cases below. Run each in a fresh session in the intended product. Native Cursor Agent and the Codex extension inside Cursor are separate interfaces. The [setup guides](setup/README.md) cover installation; none of the product and operating-system combinations has completed a user walkthrough yet.

| Case | Agent inputs | Evaluator checks |
| --- | --- | --- |
| `development-dashboard-feature` | The existing [teaching fixture](../evals/fixtures/development/README.md), copied as instructed | Five supplied acceptance tests; preserve their expected values |
| `review-dashboard-only` | Only the [assessment project](../evals/fixtures/assessment/project/requirements.md) and its neighboring files | Compare source hashes; assess the findings; use the separate evaluator checks to confirm the behavior |
| `repair-dashboard-filter` | A fresh copy of the same assessment project | Reproduce the symptom and run all seven evaluator checks afterward |
| `quality-check-only` | The [check-only project](../evals/fixtures/check-only/project/README.md) and its neighboring files | Record source hashes before and after; confirm the agent reports lint and format failures without applying fixes |

## Prepare an isolated run

Use a new project directory outside this library for each attempt. Copy only the paths listed in that case's `fixtures` field. For a project-directory fixture, its contents become the test project. `evaluator_fixtures` are for the evaluator; do not copy them into the agent's project or include their contents in its prompt. Keep the source fixtures unchanged.

The original teaching fixture intentionally explains its defect. Use it to check the mechanics of the workflow. The assessment project has neutral filenames and requirements; its evaluator checks include additional inputs. Keep the audit, teaching explanation, proposed fix, and evaluator results out of a blind review's initial context. Repeated runs by an agent that already knows the answer are not independent blind assessments.

Install the selected versioned skills into the test project using the product's guide. Keep the package manifest with the evaluation evidence. Ask the natural-language case prompt first for automatic selection. Test explicit invocation separately, recording the exact prompt. Install the relevant development skills together for a selection trial so we can observe inappropriate or repeated activation.

For the check-only project, use its pinned Ruff dependency and an available Python environment. Inspect the documented commands before running them. The evaluator verifies that the source files remain unchanged, excluding tool caches. Run the writing command only on a separate disposable copy when checking the fixture itself.

## Create a run record

From the library root, with the [maintainer environment](maintaining.md) available:

```bash
.venv/bin/python -m scripts.evaluation_runs init --case review-dashboard-only --product Codex --evaluator "Evaluator Name" --package-manifest dist/0.1.0-pilot.2/manifest.json --output output/evaluations/review-codex.json
```

In Windows PowerShell, replace `.venv/bin/python` with `.\.venv\Scripts\python.exe`. Replace `Evaluator Name` with the person responsible for the evaluation; `--evaluator` is required and sets the record's `author` independently of package authorship. Choose the actual product name: `Claude Code`, `Codex`, or `Cursor` for these development trials. The record command also accepts `Claude Desktop` and `ChatGPT` for applicable future document trials.

This command creates a **planned** record. It captures the current source revision, available package identity, and input hashes. It does not launch an agent, install a skill, measure usage, or record a successful run. Store the record outside the agent's test project because it includes evaluator criteria and input locations.

After the attempt, have the evaluator fill the record from observed evidence:

- Assign a unique `run_id`, set `status` to `completed`, and record the outcome as `pass`, `fail`, or `blocked`.
- Record the actual interface, version, operating system, account route, model, effort, installed library skill versions, and other active skills. Use limitations to identify details that could not be observed.
- Set `started_at` and `finished_at` to ISO timestamps with timezones, and record elapsed seconds and retries.
- Record observed activation and its evidence. Preserve every acceptance criterion, recording `pass`, `fail`, or `not_run` with evidence for performed checks.
- Retain the output or response and relevant check logs. Record each artifact's repository-relative path and SHA-256. Explain failures, unavailable tools, interventions, and unfinished checks.
- Use actual usage counters when available. Leave unavailable values `null` and explain coverage in `usage.note`, including whether workers and retries are included. Reasoning and cached tokens may already be included in provider totals; do not add them twice. Retain per-model details in a sanitized log where available.

An overall pass requires every acceptance check to pass, retained evidence, and the expected activation for a run with skills. A blocked attempt is still useful evidence, with the reason recorded. A structurally valid record does not prove that its statements are true; the evaluator must inspect the evidence.

Validate the record and its retained files:

```bash
.venv/bin/python -m scripts.evaluation_runs validate output/evaluations/review-codex.json --check-files
```

After reviewing and sanitizing a completed record, retain it under `evals/results/`. Keep planned templates under `output/`. The maintainer command validates retained records and rejects planned records presented as results. Validation compares acceptance criteria with the current case definitions. Validate historical results from their recorded library revision when definitions have changed; use `--check-files` against the matching preserved inputs and artifacts to verify hashes.

For the assessment project, the evaluator runs:

```bash
.venv/bin/python evals/fixtures/assessment/checks.py /actual/path/to/test-project
```

The original seed is expected to fail. A repaired project must pass all seven checks, including unseen inputs. The evaluator also reviews scope and the original symptom; passing these calculations does not establish a browser interface, storage, or deployment.

## Compare with a baseline

Use another fresh session and an identical starting project, host, model, effort, permissions, and task. Omit this library's skills while retaining normal host instructions and safeguards. Create the record with `--condition baseline`; record other built-in skills separately. Use the same independent acceptance checks and retain failed attempts.

Compare quality, total available usage, elapsed time, retries, and interventions. Capture these from the first runs, then compare routing strategies after the tasks and checks are stable. A single successful run is a useful smoke check, not evidence of consistent savings. Repeat critical or inconsistent cases before promotion.

Browser-app, presentation, publishing, and installation trials remain separate work. Release a capability only for the environments its recorded evidence supports.
