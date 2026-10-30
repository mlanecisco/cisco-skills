---
author: Mark A. Lane, Ph.D.
date: 2026-10-30
status: Roadmap; phases are gated by recorded results, not dates
---

# Roadmap

This page sets the order of work and what has to be true before each phase is done. The [build plan](build-plan.md) holds the acceptance criteria for each piece. The [evaluation guide](evaluations.md) and the [presentation pilot](presentation-pilot.md) describe how results are recorded.

Phases move on evidence, not on a calendar. Work from a later phase can start early when it doesn't depend on an earlier result, but nothing is called tested or released before its gate is met.

## Where things stand

As of 2026-10-30:

- Seven skills are drafts. None has been through a user walkthrough, and no cell in the [capability matrix](setup/capabilities.md) is marked Observed yet.
- The presentation pilot is ready to run with package `0.1.0-pilot.5`. No attempt is recorded.
- `check-before-publishing` `0.1.0` has a scanner with regression tests, a CI workflow template, and six evaluation cases. It isn't in a pilot package yet and has no product runs.
- Two historical Codex batch attempts are the only retained run records.

## Phase 1: one skill, end to end, on the desktop

Show that someone without a development background can install a skill in Claude Desktop and ChatGPT and get a usable result.

- Run the technical pass of the presentation pilot in both products.
- Run one user walkthrough with a participant who didn't help build the library.
- Record every attempt, including blocked ones, and update the capability matrix only where a record supports it.
- Correct the skill and the setup guides from what the pilot shows.

Gate: reviewed run records for both products, a walkthrough record, and matrix cells updated from those records.

## Phase 2: safe sharing

Give builders a check before anything is shared, and give teams a way to enforce it. This phase started alongside Phase 1 because it doesn't depend on the pilot's results.

- Run the [publishing cases](../evals/publishing-cases.json) in at least one desktop product and one coding product.
- Install the CI workflow in a test repository, watch it fail a pull request that adds a credential, and confirm it blocks the merge once it is a required check.
- Add `check-before-publishing` to the next pilot package.
- Point the Confluence publishing skill at the check, so it runs before a dashboard goes live. The app-building guide already does.

Gate: the publishing cases pass in a desktop and a coding product, and the workflow has been seen blocking a merge on the host.

## Phase 3: evidence tooling, distribution, and coding products

Make results cheap to record, and make installation work beyond a hand-uploaded ZIP.

- Add installation and walkthrough fields to run records, and generate the status counts from the records instead of editing them by hand.
- Choose an organization distribution route with an administrator, then test installation, updates, and rollback on macOS and Windows.
- Run the development pilot in Claude Code, Codex, and Cursor (build plan stage 2), with the efficiency benchmarks beside it (stage 3).

Gate: release `0.1.0` once the [release criteria](maintaining.md#release-criteria-and-current-status) are met for the skills it includes. Skills that haven't met them stay out of that release or remain marked draft.

## Phase 4: more deliverables

Build new skills in the order that use supports. Each one needs representative inputs, an expected output, evaluation cases, and an owner before it is built (build plan stage 6).

1. Rubric evaluation of documents and presentations.
2. Dashboard design.
3. Cisco documents and workbooks.
4. Publishing with GitHub Pages, private by default where the plan allows, with the publish check as a required step.

Candidates under consideration: risk triage with a handoff to a named reviewer, and a shared sign-off summary that each deliverable skill ends with.

## Ongoing

- Recheck product documentation for the capability matrix and setup guides, starting with the ChatGPT cells.
- Keep wording consistent across the guides as they are revised.
- Update this page when a gate is met or the order changes, and change its date.
