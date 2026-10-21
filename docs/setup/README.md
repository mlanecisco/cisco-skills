---
author: Mark A. Lane, Ph.D.
reviewed: 2026-10-21
status: Official-documentation-based guides; user walkthroughs pending
---

# Setup and installation

Start with the product you already have access to, and check the [capability matrix](capabilities.md) for what each product and mode can do. You do not need all five products or every development tool. These guides cover macOS and Windows, with shared prerequisites in [common tools](common-tools.md).

| Product | Start here | Library installation |
| --- | --- | --- |
| Claude Desktop | [Desktop guide](claude-desktop.md) | Upload an individual skill or use a team-provisioned skill; local Code work has an additional project route |
| Claude Code CLI | [CLI guide](claude-code.md) | Account-synced skills where supported, or a project `.claude/skills/` folder |
| ChatGPT | [ChatGPT guide](chatgpt.md) | Eligible workspace skill installation or upload |
| Codex | [Codex guide](codex.md) | Project `.agents/skills/` for local CLI and editor use |
| Cursor | [Cursor guide](cursor.md) | Project `.agents/skills/` or `.cursor/skills/` for local Agent use |

The product installation, account sign-in, library installation, and verification are separate steps. A subscription or app installation alone does not install this library. A shared `SKILL.md` format also does not make local command-line tools available inside a hosted chat session.

## First session

1. Install and sign in to one product using its guide.
2. Obtain a selected skill ZIP and its version manifest from the maintainer, or the source folder for local development. The [packaging guide](../packaging.md) explains package identity, verification, updates, and rollback. The private repository `mlanecisco/cisco-skills` exists on GitHub, but no release package is published yet, so obtain packages from the maintainer.
3. Add one relevant draft skill, preserving its full folder and references.
4. Run that guide's first-use check before asking for a larger project.
5. Choose model and reasoning settings from the [routing reference](../../skills/efficient-workflow/references/routing.md). Installing a skill does not configure workers or enforce those limits.

For local coding products, work in a selected project folder so the agent has a clear scope. For document work, attach the actual input and template. A skill cannot replace missing files, accounts, or tool permissions.

For app development, continue with [building apps without a software background](../building-apps.md). It provides example requests and explains the checks the development skills should handle without a separate reminder.

For dashboard delivery to Cisco's Confluence Cloud site, use the [Narva publishing guide](confluence.md). Confluence is a destination for the completed dashboard; the coding product still builds and prepares its files.

## Updates and support

Keep the library source separate from installed copies. Before replacing an installed skill, preserve local edits and use the same distribution route. Avoid installing the same skill through several routes in one product. To remove it, disable it in the product or remove only its installed folder; retain the project and maintained sources.

For troubleshooting, record the product and version, operating system, installation route, exact error, and whether the first-use check succeeded. Do not include passwords, API keys, or login tokens. Use the organization's existing software-distribution and account instructions where they apply.

The guides were checked against official documentation on the review date. Full macOS and Windows user walkthroughs remain to be completed. Product menus, account eligibility, and synchronization behavior may change; each guide links its source documentation.
