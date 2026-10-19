---
author: Mark A. Lane, Ph.D.
reviewed: 2026-10-15
status: Guide prepared; user walkthrough pending
---

# Cursor

Cursor is an editor with its own Agent interface. You can also use supported extensions inside it, including Codex. Choose which agent you are using before installing skills or configuring models.

## Install and sign in

Follow the [official Cursor quickstart](https://cursor.com/docs/get-started/quickstart) and its download link. Select the macOS or Windows installer matching the machine and complete installation. Open Cursor and sign in with the intended account or team. Check the current operating-system requirements on the download page.

Open a selected project folder in Cursor. Use an existing project or a separate sandbox for the first exercise. The integrated terminal runs local commands, so install the project's prerequisites from [common tools](common-tools.md) as needed. An editor installation does not install Python, Node.js, or every test runner.

## Add skills for Cursor Agent

The reviewed [Cursor skill documentation](https://cursor.com/docs/skills) supports local project folders `.agents/skills/` and `.cursor/skills/`. Use `.agents/skills/` when sharing the same installed copy with local Codex.

Create the chosen directory under the project and copy one complete skill folder from this library. For `check-code-quality`, confirm that the destination contains `check-code-quality/SKILL.md` and its `references/tooling.md` resource.

Open Cursor's Customize interface to inspect skills and their origins, or start a fresh Agent session if the newly added skill is not visible. Cursor also reads compatible Claude and Codex locations, so check for duplicate copies before installing another one.

GitHub repository imports use the product's plugin/marketplace route. This pilot has no published Cursor plugin or marketplace manifest; use the local folder method rather than claiming a repository URL alone installs the library. Local project installation and Cloud Agent skill availability are separate concerns.

## Verify first use

In Cursor Agent, ask:

> Use check-code-quality to identify the checks configured in this project. Do not edit files or install tools. Report which checks apply and which tools are missing.

Confirm that it uses the expected skill, cites the actual project configuration, and preserves the files. Then try the [dashboard calculation fixture](../../evals/fixtures/development/README.md) in an isolated project for a development task.

Choose a model and reasoning setting available in the current Cursor interface. Use Medium or High across providers: start main and more powerful models at Medium, and smaller models at High. Use Extra/Extra High for harder work on smaller models, or very difficult tasks or recurring reasoning problems on more powerful models. Never use Anthropic Max or OpenAI Ultra. Use standard speed and never enable premium speed modes. The Claude Code and Codex worker examples in this library do not automatically configure Cursor's native Agent routing. Report unavailable controls without claiming the policy has been enforced.

## Using Codex inside Cursor

Follow the [Codex guide](codex.md) for the OpenAI extension and its sign-in. Start the task in the Codex extension when you want its model and routing configuration; starting it in Cursor Agent uses Cursor's own configuration. Keep the project skill folder shared where supported, while verifying discovery in each interface.

## Updates and troubleshooting

Use Cursor's supported application update route and update extensions through their own controls. After changing installed skills, verify their origin and first-use behavior again.

If a skill is missing, check the open project, folder name, exact `SKILL.md` filename, and full resource copy. If terminal commands fail, verify the local toolchain and selected environment. If a cloud or remote agent cannot see a local user skill, follow Cursor's documented sync or project distribution route instead of assuming local files transfer automatically.
