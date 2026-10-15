---
author: Mark A. Lane, Ph.D.
status: Draft development guidance; product evaluations pending
---

# User flows and handoff

Select checks from the changed behavior and its likely failure paths. Use a disposable environment for actions that write records. Avoid triggering live emails, payments, or other external effects merely to test a button. Do not require the user to know which checks to request.

## Exercise the actual app

Start the app using its documented command and exercise a representative task through the interface when browser tools are available. Inspect relevant browser console and network failures. A screenshot, running process, or successful build alone does not establish that the task works.

| Feature or condition | Useful verification |
| --- | --- |
| Forms and actions | Follow the main task through its visible result and saved state. Check required fields, invalid values, repeated clicks, and feedback. A failed save must not appear successful. Prevent duplicate records where repeat submission would matter. |
| Loading and external requests | Exercise loading, empty results, request failure, and recovery. Preserve useful input after a failure. Show a useful error and retry route instead of an endless spinner, blank screen, or fabricated result. |
| Dashboards and exports | Compare totals, percentages, units, and filters against small independent examples. Include empty or missing values and date boundaries where relevant. Confirm that exported rows and measures match the intended selection. |
| Stored work | Create or edit a record, reload, and verify its expected persistence. Test restart and access from another user or browser only when those are requirements. Check representative existing data after a storage change. |
| Routes and links | Follow navigation and open a nested URL directly. Check refresh behavior and asset paths in the intended hosting configuration. |
| Interface use | Exercise important controls by keyboard, confirm visible focus and useful labels, and check readable contrast and a narrow screen. Ensure status is understandable without relying only on color. Report limits of this check; it is not a complete accessibility audit. |

Keep meaningful regression checks for important behavior. Derive expected values from requirements or known examples rather than the implementation under test. Do not replace assertions with weaker ones, mock away the failing integration, or suppress errors to claim success.

## When verification fails

Use the smallest reproduction and inspect the relevant evidence before changing code. After two unsuccessful attempts at the same symptom, reassess the cause and missing evidence. Preserve working changes; a framework rewrite or repeated dependency upgrade is not a substitute for diagnosis. Escalate reasoning effort only for a specific unresolved problem.

If a browser, account, or service is unavailable, run the checks that remain possible. Identify exactly which flow remains unverified and give a short manual check when useful. Do not describe those instructions as a completed test.

## Hand off an app the user can operate

Keep the handoff brief and concrete. Include what works, where to try it, the actual checks and their outcomes, and any issue that prevents the intended use. For new apps or changed setup, maintain instructions for installation, starting, stopping, checking, and required configuration without secret values. Explain where records are stored and whether users share them.

Label sample data, placeholder controls, and unfinished integrations. Separate "implemented" from "verified locally" and "deployed" using the evidence available. A limited trial can still have documented limitations; do not call the app production ready while its essential user flows, access controls, or deployment remain unverified.
