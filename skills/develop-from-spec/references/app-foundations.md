---
author: Mark A. Lane, Ph.D.
status: Draft development guidance; product evaluations pending
---

# App foundations

Read the sections relevant to the app's data, services, and destination. Resolve business choices with the user; handle routine implementation choices directly. Use synthetic records for development when real data is unnecessary. Follow supplied organizational requirements without inventing Cisco policies or approved services.

## Setup and scope

| Common failure | Agent action and evidence |
| --- | --- |
| A prototype gains unnecessary frameworks and services | Reuse the project stack. Add a dependency only for a current requirement. Keep one coherent implementation and remove abandoned code introduced by this task. |
| It runs only in the agent's session | Document the runtime, package manager, install command, and required configuration. Preserve the lockfile or equivalent dependency pins. Verify startup from those instructions in an isolated environment when practical; disclose any setup step that remains untested. |
| Fixing one issue destroys working features or user edits | Inspect existing changes, keep edits focused, and preserve a recoverable version before broad changes. A checkpoint must not include secrets or unrelated files. Follow the user's commit instructions. |

## Data and storage

| Common failure | Agent action and evidence |
| --- | --- |
| A polished dashboard uses invented figures | Label sample data visibly. Trace displayed measures to the supplied source and independent expected examples. A failed connection must not silently fall back to convincing sample results. |
| Saved work disappears, or colleagues see different records | Decide whether storage is temporary, local to one browser, or shared. Test save, reload, and restart as applicable. For shared records, verify the intended users can see the same saved changes. State storage and backup limitations plainly. |
| A schema change or import overwrites existing work | Test with a disposable copy, preserve existing records, and plan recovery before changing valuable stored data. An empty test database does not demonstrate that an upgrade preserves records. Do not erase records to make startup succeed. |
| Invalid inputs create bad records | Define accepted formats, required fields, ranges, and relevant business rules. Check inputs where the application accepts them; backend apps must also enforce those rules on the server. Test a valid submission and representative rejected inputs. See [OWASP input validation](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html). |

Browser storage can suit a small personal tool, but explain its scope. `localStorage` belongs to a browser origin and persists across sessions; it does not provide shared team storage or a backup. See [MDN localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage).

## Services and access

| Common failure | Agent action and evidence |
| --- | --- |
| A secret leaks through code, logs, or a browser bundle | Use the host's secret mechanism for credentials. Keep secret values out of tracked files, browser code, screenshots, and reports. Provide configuration examples with placeholders. Check the framework's exposure rules: a `.env` file does not itself make a value private. For example, [Vite exposes `VITE_*` values to client code](https://vite.dev/guide/env-and-mode). |
| Hiding a button appears to protect private records | Use the project's supported authentication and enforce permissions at the service or data boundary. Verify unauthenticated access and access by a user who does not own the record, including direct requests. Sign-in alone does not establish permission. See [OWASP authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html). |
| A shared deployment allows usage or costs to grow without limits | For metered APIs, bound request size, concurrency, retries, and consumption where the host supports it. Keep privileged credentials on the server. State any spend control that still needs account configuration; a prompt instruction is not an enforced limit. |

If a credential is actually exposed, report its location without repeating the value and identify revocation or rotation as necessary. Removing the current line does not revoke the credential. Complete the authorized repair and follow existing authority for account changes.

## Hosting

Check the destination against the app's runtime needs before proposing publication. [GitHub Pages serves static HTML, CSS, and JavaScript](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages). Server logic, private secrets, and shared database services need a compatible execution service; do not imply that a Pages upload supplies them.

For a requested deployment, check required configuration, asset paths, direct navigation, and relevant saved-data behavior in the target environment. Use a preview or disposable environment where appropriate. Keep a recovery path for changes to an existing service. Publishing must follow the user's authorization; local validation alone does not establish a successful deployment.
