---
author: Mark A. Lane, Ph.D.
date: 2026-10-22
status: Pilot plan; no product run recorded
---

# Presentation pilot

This pilot tests `cisco-presentation` in Claude Desktop and ChatGPT before any wider release. It has two parts. In the technical pass, the maintainer checks installation, activation, and the output against fixed criteria. In the user walkthrough, someone who did not help build the library tries a real task with as little help as possible. One part does not stand in for the other.

The pilot does not test organization-wide distribution. Installing a ZIP by hand answers whether a person can use the skill, not whether a rollout through an organization or workspace works. Test that route separately once an administrator has chosen it.

## Package

Use release `0.1.0-pilot.5`, built from `main` at `02b58a2` with a clean working tree. Build and verify it as described in the [packaging guide](packaging.md):

```bash
.venv/bin/python -m scripts.package_skills --version 0.1.0-pilot.5
.venv/bin/python -m scripts.package_skills --verify dist/0.1.0-pilot.5
```

| Item | Value |
| --- | --- |
| Skill | `cisco-presentation` `0.2.2`, status draft |
| Archive | `cisco-presentation-0.1.0-pilot.5.zip` |
| Archive SHA-256 | `f99ae6752d2797c49b6ba9ceaa5b04719460a3828d559e366fef2310cfe9fc6d` |
| Manifest SHA-256 | `ead82a179f246c2e4447f2475df0661e7fb8aad85cd57181f60d12e38c98c317` |

A rebuild from the same revision should reproduce the archive checksum, because the builder writes sorted members with fixed timestamps. If the checksum differs, stop and find out why before running the pilot. Give participants the archive and its manifest together.

## Before you start

Check the prerequisites for each product in the [capability matrix](setup/capabilities.md). In Claude Desktop, code execution and file creation must be on, and Team and Enterprise owners control whether members can add skills. In ChatGPT, skills may depend on the workspace plan and administrator settings; the matrix marks those details Unknown. If a route is blocked, record it as blocked. Do not change account or workspace settings for the pilot.

Use only the synthetic [project brief](../evals/fixtures/presentation/brief.md) and the current template in [docs/reference](reference/). The brief includes a quoted test note that tries to get the assistant to claim visual checks it did not do. The note is deliberate. Do not remove it or warn the participant about it.

Make sure no other copy of `cisco-presentation` is installed on the account, because duplicate copies make activation results unreliable.

## Technical pass

Run the cases in [presentation pilot cases](../evals/presentation-pilot-cases.json) in each product, starting a new chat for each case:

1. `presentation-pilot-template`, with the brief and the light template attached.
2. `presentation-pilot-no-template`, with only the brief attached.
3. `presentation-pilot-rubric-only`, with a deck from case 1 and a short rubric. This case should not trigger the presentation skill.

Use each case's prompt exactly as written. The prompts do not name the skill, so they test whether the skill activates on ordinary wording. If it does not activate, record that result first. Then, in another new chat, you may add "Use cisco-presentation." to the start of the prompt and record that attempt separately as an explicit invocation.

Create a planned record before each attempt and fill it in from what you observed:

```bash
.venv/bin/python -m scripts.evaluation_runs init --case presentation-pilot-template --product "Claude Desktop" --invocation automatic --evaluator "Evaluator Name" --package-manifest dist/0.1.0-pilot.5/manifest.json --output output/evaluations/pilot5-template-claude-desktop.json
```

The [evaluation guide](evaluations.md) explains each field. The current record format has no separate fields for installation or for a user walkthrough. Until it does, record those results in `interventions` and `limitations`, and say there which part of the pilot the record covers.

For each attempt, keep:

- whether the upload succeeded and any error message;
- what showed that the skill was active, such as a visible skill indicator or the assistant naming it;
- the generated deck, opened in PowerPoint, with every slide inspected by eye;
- the assistant's own report of what it checked, compared with what it actually did.

An attempt passes only if every check passes, the evidence is kept, and activation matches the case. A blocked attempt is still worth recording, with the reason.

## User walkthrough

Choose a participant who did not help build the library and who would plausibly make Cisco presentations. Give them the archive, the [setup guide](setup/README.md) for their product, the brief, and the template. Ask them to install the skill and make a short leadership update from the brief, in their own words.

The observer stays quiet unless the participant is stuck. Every hint counts as an intervention. Note:

- each place the participant hesitated, and what they did next;
- the words they used to ask for the deck, since those become trigger test cases;
- how long installation and the task took;
- whether they understood the assistant's statement of what it checked and what it couldn't;
- their own judgement of the deck, and whether they would use it.

Afterwards, have the participant remove the hand-installed skill, so that it does not duplicate a later copy installed by the organization.

## Afterwards

Review each record against its evidence before keeping it. Sanitize completed records and store them under `evals/results/`, with supporting files under `docs/evaluation-evidence/`. Update the [capability matrix](setup/capabilities.md) only where a record supports it, and only for the product, mode, and date tested.

Use what the pilot shows to decide on the next changes to the skill, the setup guides, and the rubric-evaluation skill planned after it.
