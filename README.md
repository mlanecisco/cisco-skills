---
author: Mark A. Lane, Ph.D.
status: Draft library; initial Codex batch evidence recorded; broader validation pending
date: 2026-10-22
---

# Cisco skills library

Running out of tokens or hitting usage limits too soon? Not sure where to start, or what to ask for? Getting results that look finished until you check the numbers? Explaining the Cisco template to your assistant every time? Built an app that worked in the demo, then lost your data?

These skills are written for those moments. A skill is a short set of instructions your assistant picks up when your request needs it. You ask in plain words, and the skill brings the steps an expert would follow. It loads only what the task needs and uses scripts for counting and sorting instead of spending tokens on them. It works from the real Cisco template and checks its own results. Then it tells you what it checked and what it couldn't.

They're written for the assistants Cisco colleagues already use: Claude Desktop, ChatGPT, Codex, Cursor, and Claude Code. The [capability matrix](docs/setup/capabilities.md) shows what each product and mode offers, with its source and verification status.

## Why I built it

I'm a seasoned developer, and I've built a lot of apps with AI tools. I think the next wave belongs to people without that background, who know their work and want to use these tools to create amazing things. I built this library to help them build things properly and use their AI tools effectively and efficiently. The skills below are the first set, and several more are planned.

It's early. Every skill here is a draft, and none has been through a colleague trial yet. If you'd like to try one on real work and tell me where it falls short, reach me on Webex or by email at malane2@cisco.com.

For people building apps without a software background, the [app-building guide](docs/building-apps.md) explains what to tell the assistant, what it should verify, and what a useful handoff looks like.

## Start here

All skills are drafts. Pick the track that matches what you want to produce, then try the example request after installing the skill with the [setup guides](docs/setup/README.md).

### Create and evaluate business deliverables

| Skill | Example request | Status |
| --- | --- | --- |
| [Create a Cisco presentation](skills/cisco-presentation/SKILL.md) | "Using this template and my project notes, make a three-slide update for my director." | Draft; 2026 Inter templates inspected; rendered sample pending |
| [Publish a Confluence dashboard](skills/publish-confluence-dashboard/SKILL.md) | "Put this finished HTML dashboard on our team's Confluence page." | Draft; tenant walkthrough and product evaluations pending |
| [Work efficiently on large or repetitive tasks](skills/efficient-workflow/SKILL.md) | "Sort these 400 survey comments into themes, and keep the token use low." | Draft; needs runtime benchmarks |

Planned in this track: dashboard design, rubric evaluation of documents and presentations, and Cisco documents and workbooks.

### Build and improve applications

| Skill | Example request | Status |
| --- | --- | --- |
| [Build or improve an app](skills/develop-from-spec/SKILL.md) | "Build a small tracker where my team can add, filter, and export requests." | Draft; product evaluations pending |
| [Check code quality](skills/check-code-quality/SKILL.md) | "Run whatever checks this project has and tell me what fails." | Draft; product evaluations pending |
| [Review, diagnose, or repair code](skills/review-and-repair-code/SKILL.md) | "Saving a record sometimes loses data. Find out why before changing anything." | Draft; product evaluations pending |

Planned in this track: publishing with GitHub Pages.

For Cisco brand guidance and approved assets, visit the [Cisco Brand Exchange employee collection](https://bx.cisco.com/cisco-brand-exchange/employee). Sign in with Cisco SSO to find current resources for your deliverable.

The [source review](docs/source-review.md) records the materials reviewed and the proposed reuse decisions. [Pilot cases](evals/pilot-cases.json) define observable checks; they are test specifications, not completed evaluations.

The [build plan](docs/build-plan.md) sets the implementation order and acceptance criteria, including development workflows, automated quality checks, and efficiency benchmarks.

For installation on macOS and Windows, start with the [setup guides](docs/setup/README.md). Maintainers can use the [repeatable check command](docs/maintaining.md). The [development evaluations](evals/development-cases.json) include a synthetic dashboard calculation fixture with known expected results.

The [evaluation guide](docs/evaluations.md) explains the pilot procedure, runnable fixtures, initial Codex batch results, and requested-versus-observed execution records. Working sources contain efficiency `0.3.0`, with a model-selection rubric, exceptional Fable/Astra escalation, and firm limits on reasoning and speed modes. The current packaged draft remains `0.1.0-pilot.4`, which predates those changes. All product routes remain untested in colleague walkthroughs. Native Cursor Agent is included in the development pilot alongside Claude Code and Codex.

[Novice development cases](evals/novice-development-cases.json) specify checks for lost records, exposed credentials, incomplete access controls, failed saves, hosting mismatches, and excessive repair attempts. Their listed fixtures and product runs remain pending.

For Confluence delivery, use the [Narva publishing guide](docs/setup/confluence.md), which covers manual insertion and agent publishing through the API. Select the destination from the request or an active team profile. The bundled [Cisco Learning pilot profile](skills/publish-confluence-dashboard/assets/team-profiles/cisco-learning.json) records `cisco-learning.atlassian.net` and its supplied macro names; it is not a default for other teams. [Confluence evaluations](evals/confluence-cases.json) include local draft-preservation and lost-response scenarios. Live authentication, macro, and published-view trials remain pending.

## Library design

Maintain one source folder per skill under `skills/`, using the open Agent Skills format. Keep descriptions precise and entrypoints short. Load detailed references only when needed. Include scripts when they replace repeated model work or provide a reliable check.

Keep platform configuration separate from task instructions. A skill can describe routing, but the host must supply model access, delegation tools, and enforcement of spending limits. Platform examples belong beside the relevant skill. Avoid maintaining separate copies of its core instructions for each product.

Keep Cisco templates and team knowledge distinct from personal preferences. Document authors, destinations, and presentation audiences come from the user or team configuration. Shared guidance identifies evidence by its source, version, date, and verification status.

## Model policy

Model choices, reasoning settings, and escalation rules live in the [routing reference](skills/efficient-workflow/references/routing.md). Setup guides and the build plan link to it instead of repeating the rules.

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
5. Validate a pilot release with colleagues on both operating systems using the generated ZIPs and manifests. Test installation, updates, and rollback, and correct the first-task walkthrough from observed friction. Run the hosted checks on each change to the team repository.
6. Add rubric evaluation, followed by Cisco documents and workbooks. Reuse suitable upstream skills selectively, recording source revisions, licenses, dependencies, and required notices before bundling material.

## Trying a draft

For a project, place the selected skill folder in `.claude/skills/` for Claude Code or `.agents/skills/` for Codex. Copy the whole folder so relative references remain available. Keep `skills/` as the maintained source and avoid loading duplicate installations in one host.

Ask the assistant to install a selected draft into a test project, then try a representative request. Merely storing it under this repository's `skills/` directory does not make it discoverable by both products. Model routing also requires the host setup described in [routing](skills/efficient-workflow/references/routing.md).

For broader team distribution, use verified packages and an installation guide. Add product-specific plugin metadata when using a plugin distribution route. ChatGPT workspace installation is a separate route and can depend on account eligibility and administrator settings. No team-wide installation or publishing is part of this pilot.

## Release status

Nothing here is a validated release. The GitHub repository `mlanecisco/cisco-skills` is public (visibility checked 2026-10-22), and its hosted "Library checks" workflow passed on commit `10a87bb` (run 39261842430, 2026-10-19). Published release packages and colleague installation trials remain pending. Release criteria, validator behavior, and the current evaluation counts are in the [maintainer guide](docs/maintaining.md).
