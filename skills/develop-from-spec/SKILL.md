---
name: develop-from-spec
description: Build or change software from requirements or a specification, using acceptance criteria, small working increments, tests, and review. Use for feature or application development; a simple explanation or a request only to run checks does not need this workflow.
metadata:
  author: Mark A. Lane, Ph.D.
  version: "0.1.0"
  status: draft
---

# Develop from a specification

Turn the requested outcome into working software and evidence that it meets the requirements. Explain choices in language the user understands; the user should not have to select testing tools or design internal interfaces.

## Establish the intended behavior

Use an existing specification when supplied. Otherwise, extract the goal, inputs, outputs, constraints, and acceptance criteria from the conversation. Ask about missing decisions that materially change behavior. Make reversible implementation choices from the existing project and state consequential assumptions.

For a substantial feature, record a short specification in the project's established location. Include concrete examples of expected behavior and what is outside scope. Keep the specification current when requirements change. A small, clear fix can use acceptance criteria in the working plan instead of creating another document.

Inspect the relevant project instructions, code, dependency manifests, and quality commands before planning implementation. Preserve existing user changes and conventions. Identify the smallest increment that produces observable value; avoid designing optional future features.

## Implement and verify

1. Map each acceptance criterion to an observable check. Separate behavior, calculation accuracy, and interface requirements. For a dashboard, check measures, filters, units, empty states, and meaningful user interactions as applicable.
2. Add a failing behavioral test before implementing a nontrivial change when the project supports it. For a defect, reproduce the reported symptom first. Confirm that the failure comes from the intended behavior, rather than broken setup or an unrelated error.
3. Implement one coherent increment. Reuse project patterns and keep changes within scope. Run focused tests while developing; use their results to guide the next change.
4. Run the project's applicable formatting, lint, type, test, and build checks. Use `check-code-quality` if available; otherwise inspect and run the existing commands directly. Do not assume a named script, package, or companion skill is installed.
5. For a web interface, exercise the important user flows in an available real browser. Check responsive layout and visible errors when relevant. If browser verification cannot run, identify the remaining uncertainty.
6. Review the changed behavior against the specification and inspect the diff for defects and unintended changes. Use `review-and-repair-code` if available. Correct material findings and rerun checks affected by the corrections.

Tests should use independent expected results from the requirements or known examples. Exercise public behavior and avoid assertions tied to internal implementation. Keep regression coverage for important defects. Minor prose or cosmetic edits need proportionate verification rather than a new test suite.

## Keep the work economical

Run fast, focused feedback during implementation and the relevant broader checks before delivery. Avoid repeated full-suite runs after unchanged results. Prefer scripts for deterministic transformations. Use low or medium reasoning as appropriate; deeper reasoning and delegated reviews should address a concrete difficulty. Use `efficient-workflow` when available for substantial or repetitive work, without making it a prerequisite for ordinary development.

Do not weaken tests, lint rules, or the specification just to make checks pass. Identify existing failures separately from failures introduced by this change. Continue independent work when a missing tool blocks only one check.

## Deliver

Summarize the resulting behavior, where to try it, and the checks actually performed. State material failures or checks that could not run. Do not claim that structural checks establish user-facing correctness. Commit, publish, or deploy only within the user's instructions and the project's rules.

## Example requests

- "Build a dashboard from these requirements and verify the calculations and filters."
- "Implement this specification using our existing project conventions."
- "Add CSV export, with tests and a review of the changes."
