---
author: Mark A. Lane, Ph.D.
reviewed: 2026-10-15
status: Shared prerequisites and verification
---

# Common tools

Install only what the chosen workflow needs. Browser-based ChatGPT and ordinary Claude Desktop document work do not need a local Python or Node.js installation. Local development needs the tools used by the project.

## Open a terminal and identify the folder

On macOS, open Terminal from Applications > Utilities or Spotlight. On Windows, open PowerShell or Windows Terminal with a PowerShell tab. A command prompt is an application where you type commands; do not paste its prompt characters along with the command.

For commands described as running from the library root, open the folder containing `README.md`, `skills`, and `docs`. Use `pwd` on macOS or `Get-Location` in PowerShell to check the current location. Use `cd` followed by the actual folder path in quotes to change it. Paths with spaces need those quotes.

## Git

Git records project history. Follow the [official installation options](https://git-scm.com/install/) for your operating system. On macOS, `git --version` may prompt installation of Apple's developer tools if Git is absent. On Windows, use Git for Windows when appropriate for your environment, then reopen the terminal.

Verify:

```text
git --version
```

Before your first commit, check `git config --get user.name` and `git config --get user.email`. Configure your own human name and work email if missing, using the scope appropriate to your projects. Do not replace an existing identity or add assistant attribution automatically.

## Python for Python projects and library maintenance

Use a supported release from [Python.org](https://www.python.org/downloads/) or your organization's software catalog. The library's maintainer checks require Python 3.11 or later. On macOS, check `python3 --version`; on Windows, check `py --version`. If several versions are installed, select a supported one explicitly.

Create a separate virtual environment per project and install that project's dependencies there. The [maintainer guide](../maintaining.md) provides exact macOS and Windows commands for this repository. You can invoke the environment's Python directly without changing PowerShell execution policy or activating a shell script.

## Node.js for JavaScript and TypeScript projects

Install the LTS release from [Node.js](https://nodejs.org/en/download) or the organization's catalog when the project requires it. Reopen the terminal, then run:

```text
node --version
npm --version
```

Use the project's existing lockfile and package manager. Let the development agent inspect its setup before installing dependencies. Formatters, linters, test runners, and browser tools should be project dependencies where practical; installing every tool globally can create conflicting versions.

If PowerShell blocks an npm script wrapper, `npm.cmd --version` can identify whether npm itself is installed. Use the approved command or installation route for the machine rather than broadly changing execution policy.

## Obtain and package a skill

Ask the maintainer for this library's source folder. Select one folder under `skills/`, such as `cisco-presentation`. Keep `SKILL.md` beside its `references/`, `assets/`, or other bundled resources. Copying only the Markdown entrypoint can break the workflow.

For a product that accepts skill uploads, compress that individual folder using Finder's Compress command on macOS or the ZIP/compressed-folder option in Windows File Explorer. Open the resulting archive and confirm that it contains the named skill folder with `SKILL.md` directly inside it. Do not ZIP the whole library or add another enclosing library folder.

For local products, their guides specify the project destination. Hidden folders beginning with a dot are intentional. In Finder, Command+Shift+period toggles hidden files; in File Explorer, enable hidden items if needed. Preserve an existing installation before replacing it.

## Troubleshooting

If a command is not found, reopen the terminal and verify the selected installation and PATH before installing another copy. If package downloads fail, check the documented network or proxy setup for the environment. If a project check fails, retain the error and ask the agent to diagnose it; do not remove the check just to continue.
