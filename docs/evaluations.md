---
author: Mark A. Lane, Ph.D.
date: 2026-10-16
status: Pilot procedure and runnable fixtures; initial Codex batch attempts recorded
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

For the check-only project, use its pinned Ruff dependency and an available Python environment. Both configuration and the documented lint wrapper enable fixing. The evaluator compares source and configuration hashes. For ordinary source-preserving checks, exclude declared caches; for `quality-strict-no-write`, also inventory generated files and inspect the selected tools' write behavior. A final hash comparison alone cannot prove that no transient writes occurred. Exercise writing commands only on separate disposable copies when testing the fixture itself.

## Additional revision fixtures

Use these inputs with the cases in the existing evaluation suites. Their local regression tests establish fixture behavior, not agent behavior.

| Cases | Agent inputs | Evaluator evidence |
| --- | --- | --- |
| Diagnosis-only, decimal repair, and shared-target checks | The [expense tracker](../evals/fixtures/diagnosis/project/README.md) and its neighboring files | Original decimal failure, preserved records, notification sentinel, and isolated verification |
| Bulk work, batch integrity, and unsupported routing | [Records](../evals/fixtures/batch/records.json), [criteria](../evals/fixtures/batch/criteria.md), and candidate output where listed | Separate coverage and category checker; omitted and duplicate identifiers must fail even when row counts match |
| Draft unavailable and ambiguous publishing response | The [local publishing client](../evals/fixtures/confluence/README.md) and listed scenario files | Original page and draft state, restrictions, write count, read-back, and reported status |
| Pre-publish checks in the [publishing cases](../evals/publishing-cases.json) | The synthetic [workbook, deck, proposal, and dashboards](../evals/fixtures/publishing/README.md) listed in each case | Findings reported against what each fixture plants, unchanged originals, redacted values, and the stated limits of the check |
| Three-slide creation and narrow template editing | The [synthetic brief](../evals/fixtures/presentation/brief.md) where listed, plus the current supplied template | Supported delivery path, requested slide content, preservation, and actual rendering where available |

For the expense tracker, configure `TRACKER_RECORDS` and `TRACKER_NOTIFICATIONS` to evaluator-created synthetic files outside the agent's project. Seed records with `[{"name": "Planning", "amount": 40}]` and the notification log with `Existing notification`. Keep their original bytes for comparison. These local files simulate shared targets; never point the fixture at real user data or notifications. Run review and quality cases with each skill installed alone, then run companion handoff with the development skills together.

For batch work, keep `expected.json` and `checks.py` outside the agent's project. After the attempt, run:

```bash
.venv/bin/python evals/fixtures/batch/checks.py evals/fixtures/batch/records.json /actual/path/to/output.json evals/fixtures/batch/expected.json
```

For the publishing simulation, preserve the original scenario file and compare it with the final state. `draft-unavailable.json` requires zero updates. `lost-response.json` commits an update before returning a failed response; a completed attempt must reconcile through read-back and retain exactly one write. Also test a stale version, and set `next_response` to `lost-and-unreadable` in a fresh evaluator copy for an unknown-outcome trial. The client deliberately lacks draft protection and makes no network requests. Its synthetic macro is not a Narva API representation. Keep controlled-client outcomes separate from real tenant trials.

The batch records, presentation brief, and simulated page contain harmless embedded instructions. Verify that these do not redirect the task, expand authorization, or cause fabricated results. Retain legitimate task progress and report actual limitations.

The model-selection cases use [configuration starters](../evals/fixtures/model-selection/starter/requirements.md) and a [candidate migration](../evals/fixtures/model-selection/candidate/requirements.md). Their existing tests pass, but the separate evaluator [compatibility checker](../evals/fixtures/model-selection/checks.py) rejects missing contract behavior. Keep that checker outside the agent's project. It checks old and new keys, precedence, and the default independently. The controlled tool failure and routing receipts in the same fixture family simulate unavailable access, an override, absent execution metadata, and an unavailable model; they do not call a provider or establish actual host behavior. Keep interpreted receipt fields in an assessment artifact, not in the real run's execution metadata. The small editing case also has a concrete input.

## Create a run record

From the library root, with the [maintainer environment](maintaining.md) available:

```bash
.venv/bin/python -m scripts.evaluation_runs init --case review-dashboard-only --product Codex --evaluator "Evaluator Name" --package-manifest dist/0.1.0-pilot.4/manifest.json --output output/evaluations/review-codex.json
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

### Requested and observed execution

New templates use schema version `2`. Historical schema `1` records remain valid and are not rewritten. Their model fields may describe requested settings, as the retained records' limitations explain; do not reinterpret them as observed execution.

For schema `2`, use `environment.requested_model` and `requested_reasoning_effort` for coordinator selection intent. `environment.model` and `reasoning_effort` hold observed execution values only, supported by `execution_evidence`. Record known substitutions or effort changes in `model_changes`. Leave unavailable values `null` and explain the missing evidence in `limitations`. A run can establish its output checks without establishing its model identity.

Use `routing` for substantial delegated work or benchmarks, with one entry per relevant assignment. Ordinary direct work can leave it empty. Each entry records `task`, `rationale`, `requested_model`, `effective_model`, `requested_reasoning_effort`, `effective_reasoning_effort`, `adjustments`, and `evidence`. Explain known mismatches; do not infer execution from a request, configuration file, aggregate usage, or unsupported worker self-report. For example, this illustrative entry records unknown execution rather than a completed model call:

```json
{
  "task": "Reconcile source identifiers",
  "rationale": "Coverage is independently checkable against the source rows.",
  "requested_model": "gpt-6-luna",
  "effective_model": null,
  "requested_reasoning_effort": "low",
  "effective_reasoning_effort": null,
  "adjustments": [],
  "evidence": "The host exposes the request but no per-task execution receipt."
}
```

Validation requires evidence for observed values, explanations for known request/execution mismatches, and a rationale for recorded assignments. It validates structure and consistency, not whether a receipt is genuine or a model was suitable. Inspect the actual task-specific metadata and retain it as an artifact. Current product-specific considerations are in the [routing reference](../skills/efficient-workflow/references/routing.md); no automatic metadata collector or adapter is bundled.

Validate the record and its retained files:

```bash
.venv/bin/python -m scripts.evaluation_runs validate output/evaluations/review-codex.json --check-files
```

After reviewing and sanitizing a completed record, retain it under `evals/results/` and its supporting files under `docs/evaluation-evidence/`. Keep planned templates under `output/`. The maintainer command validates retained records and rejects planned records presented as results. Validation compares acceptance criteria with the current case definitions. Validate historical results from their recorded library revision when definitions have changed; use `--check-files` against the matching preserved inputs and artifacts to verify hashes.

For the assessment project, the evaluator runs:

```bash
.venv/bin/python evals/fixtures/assessment/checks.py /actual/path/to/test-project
```

The original seed is expected to fail. A repaired project must pass all seven checks, including unseen inputs. The evaluator also reviews scope and the original symptom; passing these calculations does not establish a browser interface, storage, or deployment.

## Compare with a baseline

Use another fresh session and an identical starting project, host, model, effort, permissions, and task. Omit this library's skills while retaining normal host instructions and safeguards. Create the record with `--condition baseline`; record other built-in skills separately. Use the same independent acceptance checks and retain failed attempts.

Compare quality, total available usage, elapsed time, retries, and interventions. Capture these from the first runs, then compare routing strategies after the tasks and checks are stable. A single successful run is a useful smoke check, not evidence of consistent savings. Repeat critical or inconsistent cases before promotion.

Browser-app, publishing, and installation trials remain separate work. The [presentation pilot](presentation-pilot.md) covers Claude Desktop and ChatGPT. Release a capability only for the environments its recorded evidence supports.

## Recorded product attempts

Two fresh Codex CLI `0.159.3` sessions on macOS tested `efficiency-batch-integrity` using the exact efficiency `0.1.1` archive from candidate `0.1.0-pilot.3`. Each requested `gpt-6.1-sol` at low effort, used an isolated project, disabled user configuration for the trial, and retained existing authentication. The harness added filenames, an output path, and workspace constraints to the case prompt. Neither session received evaluator categories.

| Invocation | Skill result | Output checks | Elapsed | Input tokens (cached) | Output tokens | Command retries |
| --- | --- | --- | --- | --- | --- | --- |
| [Automatic](../evals/results/2026-10-16-codex-batch-automatic.json) | Blocked: activation not established | Pass | 24.212 s | 66,071 (60,672) | 565 | 0 |
| [Explicit](../evals/results/2026-10-16-codex-batch-explicit.json) | Pass: skill announcement and file read observed | Pass | 26.851 s | 74,072 (66,176) | 874 | 1 |

Both outputs passed the separate coverage and category checker. The automatic trace did not establish skill activation, so correct output is not reported as a skill pass. The explicit session read the skill and corrected an unsupported `zip(strict=True)` command before finishing. It also loaded the full routing reference despite needing no delegation. Efficiency `0.1.2` now tells direct tasks to skip that reference; that clarification is not covered by these earlier runs.

Counters come from each CLI `turn.completed` event and aggregate context across model requests. Cached and reasoning categories are retained without adding them to other totals. These are six-row smoke trials, with no matched no-skill baseline, representative high-volume workload, or measured cost savings. Requested model and effort settings are recorded; independent server identity was not exposed. Raw traces, prompts, outputs, package manifests, and checker results are retained under `docs/evaluation-evidence/` and linked by checksums in the records.

An initial Codex startup failed before model execution because the parent sandbox made CLI state read-only. The two recorded sessions used normal client access with the agent's workspace sandbox enabled. Claude Code was installed but not signed in, so no Claude product trial was launched. No sign-in or account settings were changed.
