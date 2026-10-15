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

These examples enter the token at a hidden prompt. Replace the email with the Atlassian account email. The variable names are this library's convention; the chosen client must be configured to read them.

macOS, using zsh:

```zsh
export ATLASSIAN_EMAIL="your.name@cisco.com"
export CONFLUENCE_SITE_URL="https://cisco-learning.atlassian.net"
read -r -s 'ATLASSIAN_API_TOKEN?Atlassian API token: '
export ATLASSIAN_API_TOKEN
printf '\n'
```

Windows PowerShell:

```powershell
$env:ATLASSIAN_EMAIL = "your.name@cisco.com"
$env:CONFLUENCE_SITE_URL = "https://cisco-learning.atlassian.net"
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

Read the intended page first and preserve its body, title, version, and unrelated content. A read-only access check establishes readability, not write permission. Do not create a page merely to test credentials unless that test is authorized.

Confirm a vendor-supported or successfully tested representation of the installed Narva macro. Its visible name is not an API identifier, and arbitrary dashboard HTML is not automatically a valid Confluence page body. Test the macro representation on an authorized disposable page before relying on an unverified integration.

Use the page API's current body format and version requirements. On a version conflict, reread and reconcile the actual changes rather than retrying the old body with a higher version number. Preserve unpublished work as well as published content; Atlassian notes that updating the current body can affect existing drafts. See [update-page behavior](https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-page/#api-pages-id-put).

After an authorized write, read back the result and verify the rendered macro and key interactions in the published page when tools allow. Report account or scope failures without exposing credentials. An HTTP success response does not establish that Narva rendered the dashboard correctly. API authentication and macro-update behavior at the Cisco site remain untested.
