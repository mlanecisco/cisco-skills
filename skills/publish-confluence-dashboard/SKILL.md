---
name: publish-confluence-dashboard
description: Prepare, publish, or troubleshoot HTML dashboards in Confluence Cloud using Narva Software's HTML Macro for Confluence, including HTML & Iframe Embed and Advanced HTML & Iframe Embed. Use for dashboard embedding and delivery; dashboard creation and ordinary Confluence page writing are separate tasks.
metadata:
  author: Mark A. Lane, Ph.D.
  version: "0.2.0"
  status: draft
---

# Publish a Confluence dashboard

Make an existing dashboard usable in the intended Confluence page while preserving its design and behavior. Handle routine packaging choices directly and explain consequential choices in plain language.

## Establish the destination

Use the supplied site, page, audience, dashboard files, and requested action. Read [Narva delivery guidance](references/narva.md) for the known Cisco configuration, supported delivery routes, and relevant failure checks. Do not ask again for site or app information already supplied.

Distinguish preparing files, diagnosing an embed, and updating a page. A preparation or review request does not authorize a live page update. When publication is requested, use the intended page and preserve unrelated content, existing restrictions, and a recoverable version. Do not infer permission to create public hosting, change site-wide settings, or upgrade an app.

## Choose manual or API publishing

Respect the user's preferred method. For manual insertion, provide the final artifact and editor steps; normal Confluence sign-in and page-edit permission suffice. Do not require an API token to prepare files or insert them manually.

For agent publishing through a personal REST client, explain that Atlassian calls the credential an API token. Read [authentication and API publishing](references/authentication.md) for account-email pairing, token setup, scoped endpoints, and update checks. Handle client and endpoint setup using available API tooling or a small local script; the user should not need to write requests or select an HTTP library. Reuse a configured approved OAuth connection when applicable instead of requiring another personal token. Have the user enter secrets through local credential setup, never through chat, generated HTML, or tracked configuration.

Before API changes, verify target-page access and the supported Narva macro representation. An API token authenticates a Confluence request; it does not establish that arbitrary HTML can be written as a working macro. Preserve the current page body and version, make the bounded change, and handle concurrent edits without overwriting them. If authentication or macro support is unavailable, finish preparation and provide the manual route with the remaining API validation identified.

## Prepare the artifact

Inspect the project's actual build and dependencies. Choose a route that fits the dashboard and the installed macro:

- For a small browser-only dashboard, prepare complete HTML with its required CSS, JavaScript, and data where practical. Preserve supplied Cisco styling; do not redesign the dashboard merely to package it.
- For an already hosted dashboard, prepare iframe code using its actual HTTPS URL and meaningful title. Keep the hosted site's access controls consistent with the intended audience.
- For large HTML, consider Narva's separate attachment macro only if it is available and suitable. Do not silently substitute another macro for the user's selected one.

A development server URL, unresolved source imports, or relative references to local project files are not a published artifact. Reuse the project's build tools to resolve dependencies. Inventory any remaining external fonts, scripts, images, and API domains. Prefer an existing valid build or a small deterministic packaging step over rewriting working code.

Keep secrets out of HTML and browser assets. Check that the exported data is intended for the viewers; hiding rows with a filter does not enforce data access. Do not replace real data with unlabeled sample values to conceal a failed integration. Set author metadata for generated standalone HTML according to the user's or team's instructions.

## Verify the delivery

Run available project checks and exercise the resulting artifact in a real browser when supported. Check the dashboard's key calculations, filters, links, exports, and relevant error states. Inspect narrow layouts, labels, contrast, and clipping at the intended macro size. Local browser success establishes only local behavior.

For an authorized Confluence update, verify the installed macro and its actual controls or API representation, perform the requested update, and check the published page. Exercise important interactions there and verify access as an intended viewer when possible. The editor preview or a successful API response does not establish published-page behavior or audience access. Keep page restrictions and app settings within the user's authorization.

Diagnose blank frames, blocked requests, or unresponsive controls using console and network evidence. Check the relevant domain allowlist, hosting headers, authentication, and installed app version before changing code. Do not bypass controls or repeatedly upgrade dependencies to obtain a pass.

## Deliver

Return the final HTML or iframe snippet, the chosen macro and settings, required external domains, and concise insertion or update instructions. State which checks actually ran and whether the page was published. If account access or tools are unavailable, complete local preparation and identify the Confluence checks still outstanding. Do not claim that a live page was verified from a local test.

## Example requests

- "Prepare this dashboard for our Narva HTML macro in Confluence; do not publish yet."
- "Publish this dashboard to the specified page through the API using credentials configured locally."
- "Embed this hosted dashboard in the specified Confluence page and verify its filters."
- "This dashboard works locally but is blank in Confluence. Find the cause."
