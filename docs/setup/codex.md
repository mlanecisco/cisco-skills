---
author: Mark A. Lane, Ph.D.
reviewed: 2026-10-15
status: Commands checked against official documentation; user walkthrough pending
---

# Codex

Codex offers terminal, editor, desktop, and web interfaces. This guide starts with local CLI setup, which gives the development skills access to the selected project and its installed tools. See the [official CLI guide](https://developers.openai.com/codex/cli).

## Install the CLI

The current [OpenAI Codex repository](https://github.com/openai/codex) documents standalone installers.

macOS Terminal:

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
```

Use the organization's supplied installation route where applicable. Reopen the terminal and run `codex --version`. Node.js is not a prerequisite for these standalone routes. The repository also documents npm and Homebrew alternatives; use one route consistently for updates.

## Sign in and open a project

Change to the actual project folder and run `codex`. Choose Sign in with ChatGPT when that is the account route provided to you, and complete browser authentication. Organization or API-provider setups can differ. Follow the account's [current access instructions](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan) rather than assuming an app installation establishes access.

Keep the selected permissions appropriate to the task. The [Windows sandbox guide](https://developers.openai.com/codex/windows) covers Windows-specific execution setup. Native Windows and WSL are different environments with separate paths and tools.

## Install a selected skill

See the [capability matrix](capabilities.md) for routes by product. Follow [Codex's skill documentation](https://developers.openai.com/codex/skills). Create `.agents/skills/` at the project root and copy the whole selected skill folder into it. For example:

```text
your-project/
  .agents/
    skills/
      check-code-quality/
        SKILL.md
        references/
          tooling.md
```

The maintained source folder is `skills/check-code-quality` in this library. Preserve any existing installed copy before replacing it. In the CLI, use `/skills` or type `$` to locate the installed skill. Restart the session if a new installation is not visible.

## Select model settings

Choose the model and reasoning effort from the [routing reference](../../skills/efficient-workflow/references/routing.md), which also links the official configuration guidance and the optional worker setup. Installing a task skill does not configure workers. Where the active configuration uses TOML, merge the model settings into the active configuration or profile rather than replacing the file or creating duplicate keys. The usual personal file is `~/.codex/config.toml`, or `.codex\config.toml` in the Windows user profile. Verify account support for the selected model and settings.

## Verify and use other interfaces

Ask:

> Use $check-code-quality to identify the checks configured in this project. Do not edit files or install tools. Report which checks apply and which tools are missing.

Confirm the skill and project are correct before a larger task. Use the isolated [dashboard fixture](../../evals/fixtures/development/README.md) for a development exercise.

For Cursor or another supported editor, install the OpenAI-published extension by following the [official IDE guide](https://developers.openai.com/codex/ide), open the project, and sign in. An editor extension and the terminal CLI are separate interfaces; check the active model and project in each.

## Desktop and web

The current [quickstart](https://developers.openai.com/codex/quickstart) describes Codex through the ChatGPT desktop interface:

1. Install the current ChatGPT desktop app for the operating system and sign in, following the [ChatGPT guide](chatgpt.md).
2. Open the local project folder in the app.
3. Select Codex from the ChatGPT product dropdown to use the software-development interface.
4. Confirm the selected folder, model, effort, and available skills before starting a task.
5. Run the first-use check above and verify its result in that interface.

Cloud tasks use an environment with its own files and setup. A local installed tool or user skill does not prove it is available remotely. Use the product's environment setup when the task needs cloud execution; the initial local library installation does not configure it.

## Updates and troubleshooting

Use the update route corresponding to the installer, then check the version again. For missing skills, verify the project root, full folder copy, and exact manifest name. For unavailable models or failed sign-in, check account and provider access. For failed commands, check that the required project tool is installed in the same environment where Codex runs.
