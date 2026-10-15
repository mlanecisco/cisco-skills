---
author: Mark A. Lane, Ph.D.
status: Working proposal and pilot skills
date: 2026-10-15
---

# Cisco skills library

This library helps Cisco colleagues describe an outcome and complete the work with Claude Code or Codex, with setup guidance for Claude Desktop, ChatGPT, and Cursor as well. It covers software projects and business deliverables, including dashboards, presentations, documents, and evaluations.

The goal is reliable results with less prompting and a measured use of tokens. Users should be able to say "build a dashboard from this data" or "evaluate this presentation against this rubric" without knowing which programming tools to select.

For people building apps without a software background, the development workflows handle routine engineering choices and common failure checks. The [app-building guide](docs/building-apps.md) explains what to tell the assistant, what it should verify, and what a useful handoff looks like.

## Start here

Five draft skills capture the first agreed priorities:

| Skill | Purpose | Status |
| --- | --- | --- |
| [cisco-presentation](skills/cisco-presentation/SKILL.md) | Create and edit presentations using a supplied Cisco template and its font variant | Draft; 2026 Inter templates inspected; rendered sample pending |
| [efficient-workflow](skills/efficient-workflow/SKILL.md) | Control context, model routing, reasoning effort, and repeated work | Draft; needs runtime benchmarks |
| [develop-from-spec](skills/develop-from-spec/SKILL.md) | Build apps from requirements with sensible defaults, common failure checks, tests, and review | Draft; product evaluations pending |
| [check-code-quality](skills/check-code-quality/SKILL.md) | Discover and run formatting, lint, type, test, and build checks | Draft; product evaluations pending |
| [review-and-repair-code](skills/review-and-repair-code/SKILL.md) | Review changes or reproduce and repair defects while preserving request scope | Draft; product evaluations pending |

The [source review](docs/source-review.md) records the materials reviewed and the proposed reuse decisions. [Pilot cases](evals/pilot-cases.json) define observable checks; they are test specifications, not completed evaluations.

The [build plan](docs/build-plan.md) sets the implementation order and acceptance criteria, including development workflows, automated quality checks, and efficiency benchmarks.

For installation, start with the [setup guides](docs/setup/README.md). Maintainers can use the [repeatable check command](docs/maintaining.md). The [development evaluations](evals/development-cases.json) include a synthetic dashboard calculation fixture with known expected results.

[Novice development cases](evals/novice-development-cases.json) specify checks for lost records, exposed credentials, incomplete access controls, failed saves, hosting mismatches, and excessive repair attempts. Their listed fixtures and product runs remain pending.

## Library design

Maintain one source folder per skill under `skills/`, using the open Agent Skills format. Keep descriptions precise and entrypoints short. Load detailed references only when needed. Include scripts when they replace repeated model work or provide a reliable check.

Keep platform configuration separate from task instructions. A skill can describe routing, but the host must supply model access, delegation tools, and enforcement of spending limits. Platform examples belong beside the relevant skill. Avoid maintaining separate copies of its core instructions for each product.

Keep Cisco templates and team knowledge distinct from personal preferences. Document authors, destinations, and presentation audiences come from the user or team configuration. This repository's documents are authored by Mark A. Lane, Ph.D.

## Model policy

| Product | Primary model | Routine or repetitive work | Difficult work |
| --- | --- | --- | --- |
| Claude Code | Sonnet 5.5 | Haiku 5.5 | Sonnet first; Opus 5.5 for exceptionally difficult subtasks |
| Codex | GPT-6.1 Sol | GPT-6 Luna | GPT-6.1 Sol with a justified increase in reasoning effort |

Favor low reasoning effort and use medium when task complexity calls for it. Reserve high for demonstrated need. Strongly discourage the highest thinking levels as routine settings; use them only when the user explicitly chooses them or a relevant benchmark supports their cost. Model names and available effort settings must be checked in the target account.

These are library defaults, not claims that one effort level always gives the best result. Measure cost per acceptable result, including failed attempts, coordinator overhead, and verification. Subscription usage and API charges require different reporting.

## Proposed next skills

| User outcome | Scope |
| --- | --- |
| Create a dashboard | Check the data, define meaningful measures, build the interface, and verify calculations and interaction |
| Publish with GitHub Pages | Prepare a compatible static site, preview it, and publish when authorized |
| Evaluate a document or presentation | Apply a supplied rubric, cite evidence by page or slide, and explain scores and uncertainty |
| Create Cisco documents and workbooks | Produce editable deliverables from team templates and validate their contents and presentation |

GitHub Pages hosting and applications that need a backend require different deployment choices. Evaluation should distinguish content, visual design, and spoken delivery; slides alone do not establish delivery quality.

## Development sequence

1. Establish repeatable library validation and continuous integration. Collect representative requests and define the expected deliverables and success criteria.
2. Build the development workflows for specifications, implementation, automated quality checks, code review, and defect repair.
3. Pilot efficient execution and Cisco presentations. Compare realistic tasks with and without the skills, and validate presentation fidelity against the current official template.
4. Reuse suitable upstream skills selectively. Record their source revision, license, dependencies, local changes, and evaluation results before including them in a release.
5. Package a small tested release with a plain-language catalog, example prompts, and a simple installation path. Assign maintainers and expand from demonstrated demand.

## Trying a draft

For a project, place the selected skill folder in `.claude/skills/` for Claude Code or `.agents/skills/` for Codex. Copy the whole folder so relative references remain available. Keep `skills/` as the maintained source and avoid loading duplicate installations in one host.

Ask the assistant to install a selected draft into a test project, then try a representative request. Merely storing it under this repository's `skills/` directory does not make it discoverable by both products. Model routing also requires the host setup described in [routing](skills/efficient-workflow/references/routing.md).

For broader team distribution, package tested releases with product-specific plugin metadata and an installation guide. ChatGPT workspace installation is a separate route and can depend on account eligibility and administrator settings. No team-wide installation or publishing is part of this pilot.

## Release criteria

A release needs correct triggering, valid artifacts, appropriate handling of missing inputs, and successful use in both target products. Check cases that should not activate the skill, as well as ordinary and difficult requests. For efficiency, compare total usage and quality against the same baseline task. A valid `SKILL.md` alone does not establish those results.

The maintainer command runs linting, formatting, type checking, regression tests, and structural validation for five skills and twenty-seven evaluation definitions. The evaluation specifications have not yet been run as product workflows. No measured token savings, completed platform installation walkthroughs, or official template fidelity is claimed. Hosted CI will run after the repository is published to a configured GitHub remote.
