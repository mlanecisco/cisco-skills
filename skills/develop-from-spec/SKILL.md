---
name: develop-from-spec
description: Build or change software from requirements or a specification, using acceptance criteria, small working increments, tests, and review. Use for feature or application development; a simple explanation or a request only to run checks does not need this workflow.
metadata:
  author: Mark A. Lane, Ph.D.
  version: "0.2.0"
  status: draft
---

# Develop from a specification

Turn the requested outcome into working software and evidence that it meets the requirements. Own routine engineering choices and checks even when the user does not name them. Explain consequential choices in plain language; the user should not have to select testing tools or design internal interfaces.

## Establish the intended behavior

Use an existing specification when supplied. Otherwise, extract the goal, inputs, outputs, constraints, and acceptance criteria from the conversation. Ask about missing decisions that materially change behavior. Make reversible implementation choices from the existing project and state consequential assumptions.

For a substantial feature, record a short specification in the project's established location. Include concrete examples of expected behavior and what is outside scope. Keep the specification current when requirements change. A small, clear fix can use acceptance criteria in the working plan instead of creating another document.

Inspect the relevant project instructions, code, dependency manifests, and quality commands before planning implementation. Preserve existing user changes and conventions. Identify the smallest increment that produces observable value; avoid designing optional future features.

## Choose defaults that fit the app

For a new app or a change to how it handles data, establish who will use it, whether its data is sample or real, what must survive closing it, and whether people must share records. Use answers already in the project or conversation. Ask only about unresolved decisions that affect the intended result, access, or data handling. Do not silently turn an internal tool into a public site or substitute sample data for a requested integration.

Choose the smallest implementation that meets those needs. Preserve working tooling, keep dependencies necessary and reproducible, and avoid introducing accounts or paid services without a need. Inspect the working tree before edits and preserve recoverable increments using the project's version-control practices. Never discard user work or reset stored data to bypass a defect.

For new apps, persistence, external services, or hosting decisions, read the relevant sections of [app foundations](references/app-foundations.md). For web interfaces, use the relevant checks in [user flows and handoff](references/user-flows.md). Apply checks to features the app actually has; a static information page does not need a database or sign-in system.

## Implement and verify

1. Map each acceptance criterion to an observable check. Separate behavior, calculation accuracy, and interface requirements. For a dashboard, check measures, filters, units, empty states, and meaningful user interactions as applicable.
2. Add a failing behavioral test before implementing a nontrivial change when the project supports it. For a defect, reproduce the reported symptom first. Confirm that the failure comes from the intended behavior, rather than broken setup or an unrelated error.
3. Implement one coherent increment. Reuse project patterns and keep changes within scope. Run focused tests while developing; use their results to guide the next change.
4. Run the project's applicable formatting, lint, type, test, and build checks. Use `check-code-quality` if available; otherwise inspect and run the existing commands directly. Do not assume a named script, package, or companion skill is installed.
5. For a web interface, start the app and exercise important user flows in an available real browser, including relevant failure paths. Verify controls reach their intended result, not just that the page renders. If browser verification cannot run, complete available checks and identify the remaining uncertainty.
6. Review the changed behavior against the specification and inspect the diff for defects and unintended changes. Use `review-and-repair-code` if available. Correct material findings and rerun checks affected by the corrections.

Tests should use independent expected results from the requirements or known examples. Exercise public behavior and avoid assertions tied to internal implementation. Keep regression coverage for important defects. Minor prose or cosmetic edits need proportionate verification rather than a new test suite.

## Keep the work economical

Run fast, focused feedback during implementation and the relevant broader checks before delivery. Avoid repeated full-suite runs after unchanged results. Prefer scripts for deterministic transformations. Use low or medium reasoning as appropriate; deeper reasoning and delegated reviews should address a concrete difficulty. Use `efficient-workflow` when available for substantial or repetitive work, without making it a prerequisite for ordinary development.

Do not weaken tests, lint rules, or the specification just to make checks pass. Identify existing failures separately from failures introduced by this change. Continue independent work when a missing tool blocks only one check.

## Deliver

Summarize the resulting behavior, where to try it, and the checks actually performed. For a new app or changed setup, maintain brief instructions for starting, stopping, and checking it, required configuration, and where its data lives. Label sample data and unfinished integrations.

Distinguish implementation, local verification, and deployment. State material failures or checks that could not run, including anything that prevents the intended use. Do not claim that structural checks establish user-facing correctness or that a local demo is ready for production. Commit, publish, or deploy only within the user's instructions and the project's rules.

## Example requests

- "Build a dashboard from these requirements and verify the calculations and filters."
- "Implement this specification using our existing project conventions."
- "Add CSV export, with tests and a review of the changes."
- "I'm not a developer. Build a small team tracker and choose sensible defaults."
