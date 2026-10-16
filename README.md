---
author: Mark A. Lane, Ph.D.
status: Draft library; pilot validation pending
date: 2026-10-16
---

# Cisco skills library

This library is for Cisco colleagues building apps and business deliverables with Claude Code or Codex, including people without a software background. Setup guidance also covers Claude Desktop, ChatGPT, and Cursor. The current drafts support development, Cisco presentations, token efficiency, and Confluence dashboard publishing. Dedicated dashboard design, GitHub Pages, rubric evaluation, and document and workbook skills are planned.

The goal is reliable results with less prompting and a measured use of tokens. Users should be able to say "build a dashboard from this data" or "evaluate this presentation against this rubric" without knowing which programming tools to select.

For people building apps without a software background, the development workflows handle routine engineering choices and common failure checks. The [app-building guide](docs/building-apps.md) explains what to tell the assistant, what it should verify, and what a useful handoff looks like.

## Start here

Six draft skills capture the current priorities:

| Skill | Purpose | Status |
| --- | --- | --- |
| [cisco-presentation](skills/cisco-presentation/SKILL.md) | Create and edit presentations using a supplied Cisco template and its font variant | Draft; 2026 Inter templates inspected; rendered sample pending |
| [efficient-workflow](skills/efficient-workflow/SKILL.md) | Control context, model routing, reasoning effort, and repeated work | Draft; needs runtime benchmarks |
| [develop-from-spec](skills/develop-from-spec/SKILL.md) | Build apps from requirements with sensible defaults, common failure checks, tests, and review | Draft; product evaluations pending |
| [check-code-quality](skills/check-code-quality/SKILL.md) | Discover and run formatting, lint, type, test, and build checks | Draft; product evaluations pending |
| [review-and-repair-code](skills/review-and-repair-code/SKILL.md) | Review changes or reproduce and repair defects while preserving request scope | Draft; product evaluations pending |
| [publish-confluence-dashboard](skills/publish-confluence-dashboard/SKILL.md) | Prepare and publish HTML or iframe dashboards using Narva's Confluence Cloud app | Draft; Cisco site walkthrough and product evaluations pending |

For Cisco brand guidance and approved assets, visit the [Cisco Brand Exchange employee collection](https://bx.cisco.com/cisco-brand-exchange/employee). Sign in with Cisco SSO to find current resources for your deliverable.

The [source review](docs/source-review.md) records the materials reviewed and the proposed reuse decisions. [Pilot cases](evals/pilot-cases.json) define observable checks; they are test specifications, not completed evaluations.

The [build plan](docs/build-plan.md) sets the implementation order and acceptance criteria, including development workflows, automated quality checks, and efficiency benchmarks.

For installation on macOS and Windows, start with the [setup guides](docs/setup/README.md). Maintainers can use the [repeatable check command](docs/maintaining.md). The [development evaluations](evals/development-cases.json) include a synthetic dashboard calculation fixture with known expected results.

The [evaluation guide](docs/evaluations.md) explains the pilot procedure, blind review and check-only fixtures, and run records with explicit evaluator attribution. The [packaging guide](docs/packaging.md) covers versioned skill ZIPs, manifests, verification, updates, and rollback. The current local draft candidate is `0.1.0-pilot.2`. All product routes remain documented but untested in colleague walkthroughs. Native Cursor Agent is included in the development pilot alongside Claude Code and Codex.

[Novice development cases](evals/novice-development-cases.json) specify checks for lost records, exposed credentials, incomplete access controls, failed saves, hosting mismatches, and excessive repair attempts. Their listed fixtures and product runs remain pending.

For Confluence delivery, use the [Narva publishing guide](docs/setup/confluence.md), which covers manual insertion and agent publishing through the API. The known Cisco destination is Confluence Cloud at `cisco-learning.atlassian.net`, using HTML & Iframe Embed and Advanced HTML & Iframe Embed. [Confluence evaluations](evals/confluence-cases.json) specify packaging, authentication, blocked-resource, version, and published-view checks; their fixtures and runs remain pending.

## Library design

Maintain one source folder per skill under `skills/`, using the open Agent Skills format. Keep descriptions precise and entrypoints short. Load detailed references only when needed. Include scripts when they replace repeated model work or provide a reliable check.

Keep platform configuration separate from task instructions. A skill can describe routing, but the host must supply model access, delegation tools, and enforcement of spending limits. Platform examples belong beside the relevant skill. Avoid maintaining separate copies of its core instructions for each product.

Keep Cisco templates and team knowledge distinct from personal preferences. Document authors, destinations, and presentation audiences come from the user or team configuration. Shared guidance identifies evidence by its source, version, date, and verification status.

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
| Create a dashboard | Check the data, define meaningful measures, build an attractive Cisco interface from representative examples, and verify calculations and interaction |
| Publish with GitHub Pages | Prepare a compatible static site, preview it, and publish when authorized |
| Evaluate a document or presentation | Apply a supplied rubric, cite evidence by page or slide, and explain scores and uncertainty |
| Create Cisco documents and workbooks | Produce editable deliverables from team templates and validate their contents and presentation |

GitHub Pages hosting and applications that need a backend require different deployment choices. Evaluation should distinguish content, visual design, and spoken delivery; slides alone do not establish delivery quality.

## Next steps

1. Run the development pilot in Claude Code, Codex, and native Cursor Agent using the evaluation guide. Use the feature, blind review, repair, and check-only fixtures, then add a browser app covering saved records, filters, exports, and failed requests. Record actual results and user interventions.
2. Benchmark token efficiency alongside those tasks. Compare direct execution with selective delegation using the same inputs and acceptance criteria. Include coordinator usage, retries, latency, and result quality; cumulative budget enforcement still needs runtime implementation.
3. Validate the Cisco business workflows. Generate an editable presentation and inspect every rendered slide. Test Confluence manual insertion and API publishing on a designated test page, including the actual Narva macro representation, interactions, and viewer access.
4. Build dashboard design and GitHub Pages publishing skills. Use representative dashboard examples to establish visual conventions and reuse a synthetic dashboard across development and delivery evaluations.
5. Validate a pilot release with colleagues on both operating systems using the generated ZIPs and manifests. Test installation, updates, and rollback, and correct the first-task walkthrough from observed friction. Configure the team repository and run hosted CI.
6. Add rubric evaluation, followed by Cisco documents and workbooks. Reuse suitable upstream skills selectively, recording source revisions, licenses, dependencies, and required notices before bundling material.

## Trying a draft

For a project, place the selected skill folder in `.claude/skills/` for Claude Code or `.agents/skills/` for Codex. Copy the whole folder so relative references remain available. Keep `skills/` as the maintained source and avoid loading duplicate installations in one host.

Ask the assistant to install a selected draft into a test project, then try a representative request. Merely storing it under this repository's `skills/` directory does not make it discoverable by both products. Model routing also requires the host setup described in [routing](skills/efficient-workflow/references/routing.md).

For broader team distribution, use verified packages and an installation guide. Add product-specific plugin metadata when using a plugin distribution route. ChatGPT workspace installation is a separate route and can depend on account eligibility and administrator settings. No team-wide installation or publishing is part of this pilot.

## Release criteria

A release needs correct triggering, valid artifacts, appropriate handling of missing inputs, and successful use in both target products. Check cases that should not activate the skill, as well as ordinary and difficult requests. For efficiency, compare total usage and quality against the same baseline task. A valid `SKILL.md` alone does not establish those results.

The latest local maintainer run passed linting, formatting, type checking, 61 regression tests, and structural validation of six skills and 35 evaluation definitions. The tests cover package integrity, independent evaluator attribution, run-record consistency, and the teaching and assessment fixtures. Those checks do not execute the skills in the target products. Completed product evaluations are not recorded, and 23 cases still list inputs that must be created or supplied. No measured token savings, completed platform installation walkthroughs, or validated presentation sample is claimed.

The [validator](scripts/validate_library.py) checks local Markdown links throughout each skill, rejects symlinked skill resources, requires existing relative local fixture paths, and rejects unknown evaluation fields and unsupported suite locations. The maintainer command also validates retained run records. The [audit follow-up](docs/audits/2026-10-16-follow-up.md) records addressed findings and remaining work.

The repository has a local package builder and verifier, with no configured remote, published release, or bundled installer. Hosted CI has not run. The immediate milestone is a tested pilot release with recorded artifacts, quality checks, installation results, and usage measurements.
