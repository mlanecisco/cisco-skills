---
author: Mark A. Lane, Ph.D.
date: 2026-10-16
status: Implementation plan
---

# Build plan

Build a small library that Cisco colleagues can use with Claude Code and Codex. Each release should help users complete real work, demonstrate the checks performed, and avoid unnecessary model usage.

## 1. Establish the repository and maintainer checks

Track the maintained sources, examples, and evaluation specifications in Git. Keep generated outputs, local environments, and credentials out of version control. Use human commit attribution without assistant credits.

Add one repeatable validation command for skill frontmatter, names, local references, example configuration syntax, and evaluation definitions. Run the same checks in continuous integration. Keep dependencies small and document how a maintainer runs the checks locally.

Acceptance: a clean checkout can run the checks; a malformed skill or broken reference produces an actionable failure. Structural checks must not claim to establish runtime quality.

## 2. Build the development workflows

Create a development category with three accessible entrypoints:

| Entrypoint | Required behavior |
| --- | --- |
| Build or improve an app | Capture the intended outcome and acceptance criteria, plan proportionate increments, complete the authorized requirements, and verify behavior |
| Check code quality | Detect the project's tooling; configure suitable defaults for a new project; run formatting, linting, type checks, tests, and build checks where applicable |
| Review and repair code | Compare changes with the requirements and project standards, diagnose defects with evidence, fix them, and verify the result |

Preserve existing conventions and working tooling. Use test-first development when it helps establish important behavior or reproduce a defect. Avoid tests that only restate the implementation. For web applications, verify the important user interactions in a real browser when supported.

Connect requirements to observable checks so a passing linter cannot stand in for correct behavior. Do not disable rules, remove tests, or weaken acceptance criteria simply to obtain a passing result. Report checks that could not run.

For users without a software background, handle routine engineering decisions and common failure checks as part of development. Use the intended audience and data needs to choose proportionate storage, access, and hosting. Verify relevant persistence, failed requests, input handling, and complete user flows. Preserve user work during repairs and provide operating instructions with an honest account of what remains unverified. Keep conditional detail in references so simple tasks stay economical.

Use the reviewed upstream skills as candidates and references, with license and dependency checks before incorporating material. Adapt extensive interviews, specifications, and mandatory multi-agent reviews to the team's task sizes and token constraints. Keep publishing and deployment within the user's authorization.

Acceptance: pilot a small dashboard feature and a reproducible defect. Demonstrate the requested behavior, meaningful checks, and a review of the resulting changes. A nonprogrammer should be able to request the complete workflow without selecting tools or remembering commands. Include [novice development cases](../evals/novice-development-cases.json) that expose convincing but incomplete apps, and a simple-page case that checks whether the workflow avoids unnecessary tools and services.

## 3. Evaluate efficient execution

Create representative fixtures for repetitive classification, a small coding task, and a difficult defect. Compare a direct baseline with the agreed routing: Sonnet 5.5 coordinating Haiku 5.5, Opus 5.5 for exceptional difficulty, and GPT-6.1 Sol coordinating Luna in Codex.

Favor low reasoning effort and use medium when needed. Reserve high for demonstrated difficulty. Keep the highest levels exceptional. Measure coordinator and worker usage, retries, latency, and whether the result meets the same acceptance criteria.

Add runtime enforcement if a hard cumulative budget is required. Prompt instructions alone do not provide that enforcement. Check unsupported-model and no-delegation fallbacks as well.

Working efficiency `0.2.0` adds a compact selection rubric informed by a pinned upstream review, with the existing models and workers retained. New compatibility, incomplete-test-coverage, controlled tool-failure, and execution-metadata cases have inputs; agent trials remain pending. New run templates distinguish selection intent from observed coordinator and worker execution, preserving historical records. Use those fields to establish actual routing before drawing conclusions about savings.

Acceptance: publish measured results for the pilot tasks, including cases where delegation does not help. Choose defaults from the evidence rather than assuming that more agents or less expensive models always reduce total cost.

## 4. Validate Cisco presentations

Use a current official Cisco PowerPoint template and a representative business brief. Replace provisional brand assumptions with the template's actual theme, typography, layouts, and footer treatment. Keep assets in a distribution location appropriate to their access and licensing requirements.

Create an editable sample, render every slide, and inspect readability, layout, source fidelity, and charts. Verify the no-template fallback separately.

Acceptance: the sample opens correctly, preserves the intended template, and passes both content and visual checks. Record the template version and any remaining tooling limitation.

## 5. Package the first tested release

Provide a catalog organized by user outcomes, a short installation guide for each target product, and example requests with expected deliverables. Package portable skill sources with the required product metadata. Avoid duplicate installations of the same skill in one host.

Record each skill's owner, version, dependencies, evaluation results, and upstream revision and notices where applicable. Pilot installation with a colleague who did not help build the library.

Acceptance: that colleague can install the selected skills and complete the sample tasks in both target products with minimal guidance. Runtime claims match the recorded results.

## 6. Expand from demonstrated demand

Add dashboards, GitHub Pages publishing, rubric evaluation, and Cisco documents and workbooks in the order supported by actual use. Each addition needs representative inputs, an expected output, meaningful checks, and a clear maintenance owner.

The Confluence pilot targets Confluence Cloud at `cisco-learning.atlassian.net`, with Narva Software's HTML Macro for Confluence and the HTML & Iframe Embed and Advanced HTML & Iframe Embed macros listed in the pilot configuration. The draft publishing skill and user guide cover direct HTML and hosted iframe delivery, with both manual insertion and agent publishing through the API. Document account-email and API-token setup for personal REST clients, and retain existing approved OAuth connections where available. Pilot both routes against the actual installed app, including the macro's API representation, viewer access, and published-page behavior. Collect representative dashboard examples to define reusable visual conventions; dashboard design and GitHub Pages publishing remain separate skills to build.

Keep rubric evaluation separate from presentation creation. Require evidence for scores and distinguish slide content from spoken delivery. For dashboards, verify calculations as well as the interface. For GitHub Pages, choose a deployment approach compatible with the site's runtime needs.

## Next implementation increment

The repeatable maintainer command, CI workflow, and three development entrypoints are implemented. The [audit follow-up](audits/2026-10-16-follow-up.md) records fixture-path and symlink repairs, strict evaluation fields, versioned packaging, and run-record validation. The [skill revision record](audits/2026-10-16-skill-revision.md) covers operating modes, handoffs, host-policy placement, destination selection, and source-content boundaries. Inputs now include configuration-enabled lint fixes, diagnosis and shared-target sentinels, batch reconciliation, controlled publishing responses, and a three-slide presentation brief.

Two initial Codex batch attempts are recorded: explicit efficiency invocation passed, while automatic activation remained unconfirmed. Use the [evaluation procedure](evaluations.md) for feature, review, repair, and check-only cases in fresh Claude Code, Codex, and native Cursor Agent sessions. Record matched baselines and retest the subsequent reference-loading clarification. The [package builder](packaging.md) creates complete individual ZIPs and a manifest; colleague installation, update, and rollback trials on macOS and Windows remain pending.

Next, run the revision cases in fresh product sessions, build the reusable browser fixture, validate a rendered presentation sample, and test Confluence manual and API delivery separately. Keep untested capabilities in draft status. Distribution ownership, actual host routing, team-profile selection across products, presentation tooling, and untrusted-input behavior still need runtime evidence. Controlled publishing fixtures do not establish real API or Narva behavior. Hosted CI still requires a configured remote.
