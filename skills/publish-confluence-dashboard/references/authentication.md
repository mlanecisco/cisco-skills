---
author: Mark A. Lane, Ph.D.
reviewed: 2026-10-15
status: Official-documentation-based guidance; authenticated Narva API workflow pending
---

# Authentication and API publishing

## Choose the publishing method

| Method | Authentication |
| --- | --- |
| Prepare files locally | No Confluence credential required |
| Insert manually in Confluence | Normal account sign-in and permission to edit the page |
| Publish with a personal local REST client | Atlassian account email and API token |
| Publish through a configured OAuth connection | The connection's account authorization; a separate personal token may be unnecessary |

Atlassian documents email-and-token authentication for personal scripts in its [REST authentication guide](https://developer.atlassian.com/cloud/confluence/basic-auth-for-rest-apis/). Account permissions still govern API access. Reuse an approved existing integration where available. A shared hosted publishing service should use an appropriate OAuth integration rather than collecting colleagues' personal tokens.

## Create and store an API token

For the personal REST-client route:

1. Sign in to [Atlassian account API tokens](https://id.atlassian.com/manage-profile/security/api-tokens) with the account that can edit the target page.
2. Choose **Create API token with scopes**, give it a purpose such as `Confluence dashboard publishing`, and choose an expiration date.
3. Select Confluence and only the scopes needed by the chosen client. The agent should explain these before creation. The v2 page-read and page-update operations document `read:page:confluence` and `write:page:confluence`; attachment or other operations may need additional scopes. See the [page API reference](https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-page/).
4. Create the token and save it in the user's password manager or approved secret store. It cannot be retrieved again from the creation screen.
5. Configure the local client to read it through a secret provider or process environment. Share the account email, site, and target page with the agent as needed; keep the token out of chat, source files, dashboards, shell history, and logs.

The current creation steps and expiry behavior are documented in [Atlassian's token guide](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/). If the organization's account settings prevent creation, use its existing access process or the manual publishing route. Do not request an account password as a substitute.

## Temporary terminal configuration

These examples enter the token at a hidden prompt. Replace the email and placeholder site with the account and [selected destination](team-profile.md). The variable names are this library's convention; the chosen client must be configured to read them.

macOS, using zsh:

```zsh
export ATLASSIAN_EMAIL="your.name@cisco.com"
export CONFLUENCE_SITE_URL="https://your-team.atlassian.net"
read -r -s 'ATLASSIAN_API_TOKEN?Atlassian API token: '
export ATLASSIAN_API_TOKEN
printf '\n'
```

Windows PowerShell:

```powershell
$env:ATLASSIAN_EMAIL = "your.name@cisco.com"
$env:CONFLUENCE_SITE_URL = "https://your-team.atlassian.net"
$confluenceTokenInput = Read-Host "Atlassian API token" -AsSecureString
$env:ATLASSIAN_API_TOKEN = [System.Net.NetworkCredential]::new("", $confluenceTokenInput).Password
Remove-Variable confluenceTokenInput
```

The PowerShell prompt uses [Read-Host with AsSecureString](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/read-host?view=powershell-7.5). The client ultimately receives a plain token through its environment; the masked prompt prevents visible entry and a literal token in command history. Close the publishing session when finished, or remove the token with `unset ATLASSIAN_API_TOKEN` in zsh or `Remove-Item Env:ATLASSIAN_API_TOKEN` in PowerShell.

Run the configured REST client or CLI agent from the same terminal session so it inherits these values. Setting them in an integrated terminal does not configure an already running editor or its agent processes. For that case, use the product's supported credential setup. The agent should check whether credentials are available without printing them. These examples are not a bundled publisher or proof of a successful API connection; the zsh input syntax was checked with a synthetic value, while a Windows walkthrough remains pending.

## Match authentication to the endpoint

Scoped account tokens use the Atlassian API gateway, with the Confluence base `https://api.atlassian.com/ex/confluence/{cloudId}`. The agent must resolve and verify the site's actual cloud ID and the selected operation's API path. A cloud ID identifies the site; it is not a replacement for the token.

A compatible unscoped-token client may instead use the site's API base. Do not silently create a broader token because a client has the wrong endpoint. Confirm the client's token support and follow the [scoped-token instructions](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/).

## Make a bounded API update

Match the selected site, page URL or identifier, and authenticated client's site identity before a write. Read the page and establish recoverable published and relevant draft state, including title, body, version, restrictions, and unrelated content. A published-body backup alone does not establish draft recovery. If the client cannot inspect or preserve relevant unpublished work, complete the artifact and provide the manual route. Read access is not proof of write permission; do not create a page merely to test credentials unless authorized.

Confirm a vendor-supported or successfully tested representation of the installed Narva macro. Its visible name is not an API identifier, and arbitrary dashboard HTML is not automatically a valid Confluence page body. Test the macro representation on an authorized disposable page before relying on an unverified integration.

Use the page API's current body format and version requirements. On a version conflict, reread and reconcile the actual changes rather than retrying the old body with a higher version number. Preserve unpublished work as well as published content; Atlassian notes that updating the current body can affect existing drafts. See [update-page behavior](https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-page/#api-pages-id-put).

After an authorized write, read back the result and verify the rendered macro and key interactions when tools allow. An HTTP success response does not establish correct dashboard behavior. Report account or scope failures without exposing credentials. API authentication and macro-update behavior at the pilot site remain untested.

## Reconcile an uncertain write

A timeout or lost response does not establish whether the update applied. Before another write, read the intended page again and compare its current content and version with the proposed bounded change and preserved state. Inspect the intended macro in place; do not append a replacement merely because the response was lost.

- If the intended change applied, avoid repeating it. Continue published-view and viewer-access checks, reporting any remaining uncertainty.
- If it did not apply, reconcile intervening edits and draft state before a new attempt. Retain the original authorization and preservation requirements.
- If the result cannot be determined, report publication status as unknown. Preserve the artifact and recovery evidence for manual reconciliation, without a blind retry or a claim that the page is unchanged.
