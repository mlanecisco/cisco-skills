---
author: Mark A. Lane, Ph.D.
reviewed: 2026-10-15
status: Guide prepared; workspace walkthrough pending
---

# ChatGPT

Use ChatGPT for business deliverables and supported connected workflows. Use the [Codex guide](codex.md) when the task needs an agent working in a local software project.

## Open ChatGPT and sign in

Open [ChatGPT](https://chatgpt.com/) in a browser and sign in with the account intended for the work. Select the correct company workspace when more than one is available.

Desktop is optional. On macOS, follow [OpenAI's macOS installation guide](https://help.openai.com/en/articles/9275200-downloading-the-chatgpt-macos-app). On Windows, use the [Windows app guide](https://help.openai.com/en/articles/9982051-using-the-chatgpt-windows-app). Check current hardware and operating-system requirements before downloading. Complete the app or store installation and sign in to the same intended workspace.

The current [quickstart](https://developers.openai.com/codex/quickstart) distinguishes Chat for conversation, Work for finished deliverables, and Codex for software development. Choose the interface that matches the task. In the desktop app, local file work also needs the intended folder selected.

## Add a library skill

The [capability matrix](capabilities.md) records which parts of this are verified. The reviewed [Skills in ChatGPT guidance](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) describes eligible Business, Enterprise, Healthcare, and Edu accounts, subject to workspace settings and availability.

1. Open Plugins in the sidebar, then the Skills tab.
2. If the team has shared the desired skill, locate it under Shared with me or the workspace list and install it.
3. For a personal upload, choose Create > Upload from your computer and provide the individual skill package prepared in [common tools](common-tools.md).
4. Complete any displayed review and installation steps. Confirm the skill appears among installed skills.

If Skills or Upload is absent, check account eligibility, the selected workspace, and administrator settings. Pasting a `SKILL.md` into a conversation is not the same as installing a reusable skill. Local Codex folders are a separate installation route.

## Verify first use

For a first exercise, install `cisco-presentation`, attach a short brief and the current Cisco template if available, and ask:

> Use cisco-presentation to create a short update from these files. Identify the template or draft styling, preserve the source facts, and report the output checks you actually completed.

Open the output and confirm the result against the supplied material. Treat an outline or an unrendered draft according to its stated limits. The skill's brand reference is derived from the 2026 Inter templates, and a generated presentation still needs rendered visual validation before you treat it as faithful.

An uploaded development skill can only run checks if the session has the necessary files, execution tools, and environment. It does not automatically gain access to the laptop's project folder. Configure a supported connected workflow or use Codex for that local task.

## Updates and troubleshooting

Use the product's skill-management interface to replace or disable an installed copy. Team sharing and workspace publishing depend on access settings; uploading a personal copy does not publish it to everyone.

If upload fails, check that the package contains the complete selected skill and its references. If a tool is unavailable, identify the missing capability instead of repeatedly asking the model to execute the same step. Record whether a claim concerns successful installation, an actual generated artifact, or a completed verification; those are different results.
