---
author: Mark A. Lane, Ph.D.
reviewed: 2026-10-15
scope: Source review and reuse recommendations
---

# Source review

The library should use the open Agent Skills format, add Cisco-specific knowledge, and reuse suitable tools selectively. A shared format does not guarantee that a skill's dependencies, model controls, or installation method work in every product.

This review covers the requested guidance, repository documentation, and selected relevant skills. It is not an audit of every file in the linked repositories. Most workflows are original; the efficiency selection rubric now adapts the pinned getedgehq material described below, with its source and license notices preserved.

## Foundational guidance

| Source | Finding | Decision for this library |
| --- | --- | --- |
| [Anthropic's complete guide](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) | Covers use cases, skill structure, triggering, functional checks, iteration, and distribution | Begin with concrete requests and acceptance criteria; test whether the skill activates appropriately and completes the work |
| [Equipping agents for the real world](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) | Explains selective loading and using executable helpers for operations that do not need model reasoning | Keep entrypoints lean and move repeated deterministic work into scripts when useful |
| [Agent Skills overview](https://agentskills.io/home) and [specification](https://agentskills.io/specification) | Establish the portable folder structure and metadata | Use standard frontmatter; keep host-specific controls outside the shared entrypoint |
| [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) | Describes installation, sharing, and workspace controls, with differences across products | Treat ChatGPT workspace distribution as an additional route; do not assume a local Codex installation automatically installs a workspace skill |

The Anthropic PDF is useful for design principles. Its distribution section describes January 2026 behavior, so implementation details should be checked against current product documentation.

## Official skills libraries

### Anthropic

Reviewed the [repository overview](https://github.com/anthropics/skills) and the [PowerPoint](https://github.com/anthropics/skills/tree/main/skills/pptx), [frontend design](https://github.com/anthropics/skills/tree/main/skills/frontend-design), and [web application testing](https://github.com/anthropics/skills/tree/main/skills/webapp-testing) entrypoints.

Frontend design and browser testing are candidates for supporting dashboard and application work. Cisco templates and project requirements should govern their use. A distinctive design preference should not override an established business interface or brand template.

The repository distinguishes many Apache-licensed examples from its source-available document skills. The [PowerPoint license](https://github.com/anthropics/skills/blob/main/skills/pptx/LICENSE.txt) restricts copying, derivatives, and distribution. Keep our Cisco presentation workflow original; use authorized document tooling in its intended environment. The [frontend design license](https://github.com/anthropics/skills/blob/main/skills/frontend-design/LICENSE.txt) is Apache 2.0. Review each selected skill's actual license and dependencies before bundling it.

### OpenAI

Reviewed the [catalog](https://github.com/openai/skills), its curated listing, and the [PDF](https://github.com/openai/skills/tree/main/skills/.curated/pdf), [Playwright](https://github.com/openai/skills/tree/main/skills/.curated/playwright), and [GitHub CI repair](https://github.com/openai/skills/tree/main/skills/.curated/gh-fix-ci) entrypoints.

PDF handling and real-browser verification are useful candidates for document and dashboard workflows. CI repair can help maintain projects after the first prototype. Evaluate them in the target environments, since paths, tools, and prerequisites can be specific to their original hosts.

The catalog places licenses in individual skill directories. The reviewed CI repair skill also includes an explicit approval step; that behavior needs consideration against the team's intended workflow. It should not silently become a requirement for unrelated local fixes. No upstream skill has been installed or bundled in this pilot.

## Community libraries requested for review

### Karpathy-inspired guidelines

The [multica-ai repository](https://github.com/multica-ai/andrej-karpathy-skills) describes guidelines inspired by Andrej Karpathy's observations. It is a third-party project, not a skills library authored by Karpathy. Reviewed its README and `CLAUDE.md`.

The useful ideas are modest implementations, focused changes, visible assumptions, and verifiable outcomes. These fit a short project policy and a project-building skill. Apply judgment to ambiguity: ask when an answer changes the result, and make reversible routine choices without repeatedly stopping the user.

Its README states MIT licensing, but the attempted root `LICENSE` URL returned 404. Confirm the actual license file and notices before copying material. Also inspect installation instructions before using them: the reviewed README points some commands to a different repository owner. This pilot uses none of those commands.

### Matt Pocock

Reviewed the [repository README](https://github.com/mattpocock/skills), [grill-me](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md), [tdd](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md), [to-spec](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-spec/SKILL.md), and the [MIT license](https://github.com/mattpocock/skills/blob/main/LICENSE).

Useful ideas include a shared project vocabulary, turning an existing conversation into a specification, and checking observable behavior as development proceeds. Adapt these to business language and proportionate task sizes.

Some reviewed workflows are deliberately demanding: `tdd` requires agreement on test boundaries, while `to-spec` requests extensive user stories and publishes to a configured issue tracker. Keep that depth optional. Our defaults should use a brief intake, small working increments, and appropriate verification. Publishing needs authorization in the actual task.

`grill-me` is a small wrapper that invokes another skill, `grilling`. Installing only that wrapper would leave a dependency unresolved. Trace linked skills and scripts before selecting reusable units. The MIT license permits reuse with its required notices; no material has been copied here.

### getedgehq model picker

Reviewed [subagent-model-picker](https://github.com/getedgehq/skills/blob/20a91ea359e6d09c2cca50879f0e6a2c19e7e44c/subagent-model-picker/SKILL.md) and the repository license at revision `20a91ea359e6d09c2cca50879f0e6a2c19e7e44c`. The Apache 2.0 license includes `Copyright 2026 Floom`; its complete text is retained within the efficiency skill. Standard root and skill-directory NOTICE paths returned 404. The [adaptation record](../skills/efficient-workflow/references/upstream.md) identifies the source, review scope, preserved license, and local changes.

The useful ideas are selecting delegated models from the task's ambiguity, independent checks, and consequences, and considering total completion cost. The local rubric also requires relevant evidence, preserves explicit settings, and diagnoses input or environment failures before changing capability. It adds task-specific requested/observed execution records. Upstream pricing tables, extra model tiers, fixed one-tier escalation, and the blanket restriction on cheaper reviewers are not adopted. Existing model defaults and worker definitions are unchanged.

## Recommended implementation decisions

1. Share portable task instructions and keep product adapters small. Resolve optional dependencies when the workflow needs them.
2. Provide a human catalog organized by outcomes. Give each skill example requests, inputs, outputs, and a clear statement of what has been tested.
3. Keep team policy concise. Do not install every upstream library or load every guide into each session.
4. Use the agreed Sonnet/Haiku/Opus and Sol/Luna routing, with economical reasoning defaults. Delegation and higher effort need to earn their overhead in benchmarks.
5. Separate presentation creation from rubric evaluation. An evaluation skill needs score definitions, evidence locations, and treatment of missing or ambiguous evidence.
6. Release a small tested set first. Record an upstream revision and notices for any included dependency; update through review rather than silently tracking a moving branch.

For runtime details, consult [Claude Code subagents](https://code.claude.com/docs/en/sub-agents) and [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents). The pilot provides example worker definitions. Hard spending caps and measurements still require runtime implementation and evaluation.
