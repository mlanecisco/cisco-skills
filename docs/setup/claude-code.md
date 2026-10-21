---
author: Mark A. Lane, Ph.D.
reviewed: 2026-10-15
status: Commands checked against official documentation; user walkthrough pending
---

# Claude Code CLI

Use this route to work with files and tools in a local project. Start with [common tools](common-tools.md), then install the CLI independently of the Claude Desktop application.

## Install

The [official quickstart](https://code.claude.com/docs/en/quickstart) provides native installation commands.

macOS Terminal:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Windows PowerShell:

```powershell
irm https://claude.ai/install.ps1 | iex
```

Reopen the terminal and run `claude --version`. A version number confirms the command is available. Follow the organization's distribution route if it supplies the application. Git for Windows is recommended for Git and Bash-based project work; current native Windows Claude Code can also use PowerShell. See [advanced setup](https://code.claude.com/docs/en/setup).

## Sign in and select the project

Change to the actual project folder with `cd`, then run `claude`. Follow the browser sign-in for the intended Claude account or the organization's configured provider. The [quickstart's account guidance](https://code.claude.com/docs/en/quickstart) distinguishes subscription, Console, and enterprise-provider routes. Do not add an API key merely because a different sign-in route is unavailable.

Choose the model and effort from the [routing reference](../../skills/efficient-workflow/references/routing.md). The [CLI reference](https://code.claude.com/docs/en/cli-reference) documents the `--model` and `--effort` flags. Check the installed version's `claude --help` if an option is unavailable.

## Add the library

Capabilities and distribution routes are summarized in the [capability matrix](capabilities.md). Choose one route, following [Claude Code's skill documentation](https://code.claude.com/docs/en/skills):

- Account route: enable the skill in the same Claude account used for terminal sign-in. Sync requires a supported CLI version; the reviewed documentation specifies v2.1.273 or later. API-key and cloud-provider sessions do not use that account-sync route.
- Project route: create `.claude/skills/` inside the project and copy a complete selected skill folder there. The result should include `.claude/skills/check-code-quality/SKILL.md` and its `references/` folder.

Use the account's skill interface to update a synced skill; do not edit the managed synced cache. Keep maintained sources in this library. Inspect `/skills` for installed skills and their origins, then restart the session if a new local installation is not visible.

## Verify first use

Run `/skills`, confirm the selected skill, and ask:

> Use check-code-quality to identify the checks configured in this project. Do not edit files or install tools. Explain which checks apply and which tools are missing.

Confirm the answer refers to the actual project and does not claim missing checks passed. For a functional development exercise, use an isolated copy of the [dashboard fixture](../../evals/fixtures/development/README.md).

## Workers, updates, and troubleshooting

The [efficient-workflow routing reference](../../skills/efficient-workflow/references/routing.md) explains the optional Haiku worker for easy or repetitive work and the Opus worker for difficult questions or consultation. Prefer Opus at High or Extra when justified before considering Fable, which is reserved for extreme situations. All workers and consultants use standard speed and never select Max. Copying a task skill does not install or activate those agents.

Native installations update automatically; package-manager installations use their own update commands. Recheck `claude --version` after updating. For command-not-found errors, check PATH and reopen the terminal. For sign-in problems, verify the intended account and provider. For missing skills, check the project root, folder layout, exact filename, and duplicate account/project installations.
