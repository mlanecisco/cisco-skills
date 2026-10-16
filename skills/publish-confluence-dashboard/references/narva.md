---
author: Mark A. Lane, Ph.D.
reviewed: 2026-10-15
status: Vendor-documentation-based draft; Cisco site walkthrough pending
---

# Narva delivery guidance

## Select the team configuration

Resolve the destination using [team-profile guidance](team-profile.md). The [Cisco Learning pilot profile](../assets/team-profiles/cisco-learning.json) records the supplied October 15, 2026 configuration; select it explicitly for that pilot. It is not a default destination for Cisco employees.

The pilot tenant has not been inspected. Installed version, exact editor controls, allowed domains, and page permissions remain unverified. Narva's overview documents HTML & Iframe Embed; the Advanced macro name is recorded in the pilot profile and has not been independently verified in the installed app. Confirm the editor rather than inventing differences between the macros.

## Delivery routes

Narva documents support for complete HTML, CSS, JavaScript, and iframe code in its [user guide](https://help.narva.net/html-macro-for-confluence). This supports a direct HTML route without separately hosting every dashboard. Inline HTML is browser code; it does not supply a backend or shared database.

For direct HTML, resolve required assets and scripts into the artifact where practical, and identify any external dependencies. Test the built output rather than assuming a source project can be pasted into a macro. For a hosted dashboard, use Narva's [iframe workflow](https://help.narva.net/html-macro-for-confluence/embed-iframe-in-confluence) and verify the hosted URL independently.

Narva also provides [HTML from Page Attachment](https://help.narva.net/html-macro-for-confluence/embed-html-file-in-confluence), which it recommends for large or complex HTML. This is a separate macro, not a confirmed feature of the two macros used in the Cisco pilot. Attachment delivery also needs app access to the source page; see [common issues](https://help.narva.net/html-macro-for-confluence/common-issues-and-limitations).

## Checks for common failures

| Symptom | Evidence to inspect |
| --- | --- |
| Styling, fonts, or charts disappear | Missing local assets, blocked external resources, unresolved imports, and browser console errors. Verify actual rendering inside the macro. |
| Blank embed or blocked API request | Narva's configured domain allowlist. Its [security documentation](https://help.narva.net/html-macro-for-confluence/html-macro-security) describes CSP restrictions on frames, connections, and scripts. Identify the needed domain and setting without disabling the controls. |
| Hosted dashboard refuses to embed | The host's response headers and actual frame ancestry. A host's `frame-ancestors` policy checks all ancestors, which may include app frames as well as Confluence. See [MDN frame-ancestors](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors). |
| It works for the author but not colleagues | Published-page permissions, external-site permissions, and authentication in the embedded context. Page access does not grant access to an external service. |
| Buttons, links, or forms fail only in Confluence | Installed app version, browser errors, and the failing interaction. Compare with the vendor's version-specific fixes below. |
| Content is cut off or exports fail | Actual frame dimensions, scrolling, and browser download behavior. Test the relevant control in the published page; a local screenshot is insufficient. |

Treat the embed as a separate browser document. Avoid code that depends on Confluence's page DOM, CSS, globals, or login context. Keep useful error states when an external dependency cannot load.

## Version-specific diagnosis

Narva documents a [Forge migration in v2.0](https://help.narva.net/html-macro-for-confluence/v2-0-migration-to-atlassian-forge) on March 25, 2026. Hosting origins changed; iframe troubleshooting should inspect the actual deployed origins rather than relying on older Heroku examples.

The [v3.0 notes](https://help.narva.net/html-macro-for-confluence/v3-0-fix-for-links-in-iframe-embed) describe a fix for unresponsive links and buttons in external iframe embeds. The [v3.1 notes](https://help.narva.net/html-macro-for-confluence/v3-1-fix-for-html-form-submissions) describe form submissions being resent through `fetch()`, with CORS requirements. Check these against the installed version and observed symptom. An update is an administrator action, not an automatic repair step.

For authenticated requests, use an access design appropriate to the actual origin and credentials. Do not treat wildcard CORS as a universal fix: [credentialed CORS requests cannot use `Access-Control-Allow-Origin: *`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS/Errors/CORSNotSupportingCredentials). Do not remove authentication or put a privileged token in the dashboard to make a request succeed.

The [changelog](https://help.narva.net/html-macro-for-confluence/changelog) is the source for version details. These vendor findings do not establish the version installed at the Cisco site or prove a dashboard works there.
