---
name: review-and-repair-code
description: Review code changes against requirements and project standards, or diagnose and repair a reported defect with reproducible evidence and regression checks. Use for code reviews, debugging, and repair; review-only requests must not modify files.
metadata:
  author: Mark A. Lane, Ph.D.
  version: "0.2.0"
  status: draft
---

# Review and repair code

Find defects that matter to the requested behavior and explain them with evidence. Distinguish reviewing changes from permission to modify them.

## Establish scope

Determine whether the user wants a review, diagnosis, or repair. For review-only work, inspect and report without editing. For authorized repairs, preserve unrelated changes and existing conventions.

Identify the relevant specification, acceptance criteria, project standards, and diff. Use the supplied base when one is given. Otherwise inspect current changes and choose an appropriate comparison from the repository's state, stating the choice. Ask if the intended scope remains materially ambiguous.

## Review changes

Check both whether the implementation meets the requirements and whether it introduces defects or violates applicable project standards. Trace affected paths, callers, and tests far enough to substantiate findings. Consider boundary conditions, invalid inputs, calculations, state changes, and error handling relevant to the change.

For app changes, look for plausible but incomplete behavior: a save that does not persist, sample data presented as live, controls with no working action, and failures reported as success. When the change touches private data or services, check the relevant permission enforcement and secret exposure. Keep these checks within the affected paths and support findings with evidence.

Let configured tools handle formatting and routine lint rules. Use `check-code-quality` when available or inspect the project's existing checks directly. Focus model review on behavior, requirements, and maintainability concerns that tools do not establish.

Report actionable findings with a file and location, the triggering condition, the consequence, and supporting evidence. Separate confirmed defects from uncertain concerns. Avoid presenting a stylistic preference as a defect or claiming complete coverage from a limited diff.

A small change can use a direct review. An independent reviewer can help with a substantial or difficult change when delegation is available and authorized. Give that reviewer the specification, relevant diff, and needed evidence rather than the entire conversation. Keep review scope and output bounded; do not spawn reviewers automatically for every edit.

## Diagnose and repair

For a reported defect, reproduce the user's symptom through a focused test, command, or browser interaction where possible. Confirm that the reproduction exercises the actual failing path. If it cannot run, distinguish observed evidence from hypotheses and identify the missing input or environment.

Test a focused explanation of the failure rather than making speculative changes. Use targeted instrumentation or a minimal example when helpful. For performance problems, measure the relevant operation before and after the change.

For an important reproducible defect, add a regression check that fails for the original behavior, then make the smallest sound correction. Use independently derived expected values. Rerun the original reproduction and relevant project checks. Preserve the requirements rather than weakening tests or suppressing errors.

Remove temporary instrumentation created for the investigation and inspect the final diff. After two unsuccessful attempts at the same symptom, reassess the evidence and approach instead of repeating the same change. Do not reset user data or rewrite working parts of the app to bypass the failure. Use a more capable model or higher reasoning effort only for a specific unresolved difficulty and within the applicable budget.

## Deliver

For a review, lead with material findings and identify coverage limits. If none are found, say so without implying a guarantee. For a repair, summarize the resulting behavior, the cause supported by evidence, and the checks actually run. State remaining failures or unverified behavior. Follow the user's instructions for commits and external actions.

## Example requests

- "Review these changes against the specification without editing files."
- "This dashboard shows the wrong total after filtering. Reproduce and fix it."
- "Find the cause of this failing test and add a regression check."
