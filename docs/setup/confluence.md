---
author: Mark A. Lane, Ph.D.
reviewed: 2026-10-15
status: Vendor-documentation-based guide; Cisco user walkthrough pending
---

# Publish a dashboard to Confluence

This guide covers Confluence Cloud at `cisco-learning.atlassian.net`, using Narva Software's HTML Macro for Confluence. The documented pilot configuration lists HTML & Iframe Embed and Advanced HTML & Iframe Embed. Their installed version and exact controls have not yet been checked.

Use this destination when the request or active team configuration selects the Cisco Learning pilot. The skill includes an explicit [pilot profile](../../skills/publish-confluence-dashboard/assets/team-profiles/cisco-learning.json); other teams should supply their own destination. Follow [destination selection](../../skills/publish-confluence-dashboard/references/team-profile.md) and resolve any site/page mismatch before publishing.

You can build and prepare the dashboard in Cursor, Claude Code, or Codex. Confluence is the publishing destination. Install the [publish-confluence-dashboard skill](../../skills/publish-confluence-dashboard/SKILL.md) in your coding product using its [setup guide](README.md).

## Choose how to publish

| Method | What you need |
| --- | --- |
| Insert the dashboard manually | Your usual Confluence sign-in and permission to edit the intended page |
| Have your agent publish through the API | An agent with API access, your Atlassian account email and API token, and permission to edit the intended page |

Atlassian calls the account credential an **API token**. It is needed for the personal REST-client route, but not for manual insertion or local preparation. An existing approved OAuth connection can provide another way for an agent to authenticate. See [Atlassian's authentication documentation](https://developer.atlassian.com/cloud/confluence/basic-auth-for-rest-apis/).

## Ask the assistant to prepare it

For a dashboard already in your project:

> Prepare this dashboard for our Confluence Cloud site using Narva's HTML & Iframe Embed macro. Preserve its design, check the calculations and filters, and provide the final HTML and insertion instructions. Identify any external resources it needs. Do not publish it yet.

Tell the assistant if you use the Advanced macro instead. It should inspect the actual editor when access is available and avoid guessing which settings differ.

Narva's [user guide](https://help.narva.net/html-macro-for-confluence) confirms that the app accepts HTML, CSS, JavaScript, and iframe code. A small dashboard can often use complete HTML directly. An already hosted dashboard can use an iframe. The assistant should choose a suitable route from your project and explain it; GitHub Pages is not required for direct HTML delivery.

## Option 1: insert the dashboard manually

These browser steps apply on macOS and Windows:

1. Open the intended page on your Confluence site and enter edit mode. For a first trial, use a test page with synthetic data.
2. Type `/html` or open the macro browser. Select the Narva macro your team uses. The similarly named native iFrame macro is a different workflow.
3. Open the macro editor and paste the complete prepared HTML or iframe code. Use the assistant's final artifact, which should contain no development-server addresses or unresolved local files.
4. Preview when the editor supports it. Check the visible dashboard and adjust the available height or width controls if needed.
5. Save the macro. When ready to share, publish or update the page with its intended restrictions.
6. Open the published page and try the important task: filter the data, check a known total, follow relevant links, and test export if offered. Confirm an intended colleague can use it when possible.

For large HTML files, Narva documents a separate [HTML from Page Attachment macro](https://help.narva.net/html-macro-for-confluence/embed-html-file-in-confluence). Use that route only when it is available and fits the team's workflow; it is not one of the two macros confirmed for this pilot.

## Option 2: have your agent publish through the API

Create an API token from your [Atlassian account](https://id.atlassian.com/manage-profile/security/api-tokens), selecting Confluence, an expiration date, and the permissions your publishing client needs. Follow the [token setup instructions](../../skills/publish-confluence-dashboard/references/authentication.md) for the current steps and local configuration examples on macOS and Windows.

Store the token locally using the client's credential setup or the documented terminal prompt. Do not paste it into the conversation or dashboard. Give the agent your account email, the target page URL, and the prepared dashboard. For example:

> Publish this prepared dashboard through the Confluence API to [target page URL], using the credentials configured locally. Use our Narva macro, preserve the page's other content and restrictions, and verify the published dashboard's filters and export. Report anything you could not verify.

The agent should handle the client and API endpoint setup; you do not need to write API requests. It should first check access to the page without changing it, preserve the existing page, and use a supported representation of the installed Narva macro. Having a token does not by itself establish that the publishing client can create or update that macro correctly.

If the client or macro integration is unavailable, the agent can still prepare the final HTML and manual instructions. Authenticated API publishing needs a pilot against the actual Cisco site before we describe this route as tested.

## If it works locally but fails in Confluence

Give the assistant the selected macro name, what you tried, what happened, and any visible error without credentials or private records. It should inspect the browser evidence and explain the specific cause. External resources may be blocked by the app's [domain settings](https://help.narva.net/html-macro-for-confluence/html-macro-security), and hosted sites may restrict embedding.

Some issues depend on the installed app version. Narva documents fixes for [iframe links and buttons](https://help.narva.net/html-macro-for-confluence/v3-0-fix-for-links-in-iframe-embed) and [form submissions](https://help.narva.net/html-macro-for-confluence/v3-1-fix-for-html-form-submissions). Checking the version can help diagnose a matching failure. The assistant should preserve your data and access requirements while investigating.

Local checks, an editor preview, and a successful published-page trial establish different things. If the assistant cannot access Confluence, it can still prepare files and instructions; the published-page and viewer-access checks remain for the pilot.
