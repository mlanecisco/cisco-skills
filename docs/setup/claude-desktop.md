---
author: Mark A. Lane, Ph.D.
reviewed: 2026-10-15
status: Guide prepared; hands-on walkthrough pending
---

# Claude Desktop

Use this route for presentations and other document work. For a local code project, Claude Code's terminal route is described in the [CLI guide](claude-code.md).

## Install and sign in

1. Open the [official Desktop installation instructions](https://support.claude.com/en/articles/10065433-install-claude-desktop) and follow their download link. Check the current operating-system requirements.
2. Download the macOS or Windows installer for the machine. Open it and complete installation.
3. Launch Claude from Applications on macOS or the Start menu on Windows.
4. Sign in with the account and organization intended for the work. Complete corporate sign-in if prompted.

## Add a library skill

The [capability matrix](capabilities.md) covers chat, Cowork, and Code. Follow [Claude's skill guide](https://support.claude.com/en/articles/12512180-use-skills-in-claude). Enable code execution and file creation where required. Team settings may govern access.

Open Customize > Skills. If the team already provides the selected skill, enable that copy. Otherwise use the create/upload option and upload a ZIP containing one complete skill folder, prepared as described in [common tools](common-tools.md). Enable the uploaded skill.

Use `cisco-presentation` for the first document exercise. Its brand reference is derived from the 2026 Inter templates and has not been checked against a rendered presentation, so a generated deck still needs visual validation. A local folder elsewhere on the machine does not by itself install a skill into account-based chat.

## Verify first use

Start a new conversation, attach a short project brief and a current Cisco template if available, and ask:

> Use cisco-presentation to prepare a three-slide project update. Preserve the supplied facts, identify the template or draft styling used, and tell me which output checks you could perform.

Confirm that the skill is enabled and the result addresses the brief. Download and open the generated file. Check that any claim of rendering or visual inspection matches what the session actually did. If only a draft or outline is produced, retain the stated limitation instead of treating it as a validated deck.

## Local Code and account sync

Desktop includes additional work modes depending on access. Local coding sessions need a selected project and its toolchain. Account skills can also sync to supported Claude Code terminal sessions using the same account; consult the [CLI guide](claude-code.md) before installing duplicate local copies.

## Troubleshooting and updates

If skill creation or code execution is missing, check the correct account, workspace, and available organization settings. If upload fails, inspect the ZIP structure, exact `SKILL.md` name, and matching folder name. If output references missing resources, confirm the whole folder was packaged.

Update Desktop through its supported update route. Replace a personal uploaded skill through its skill-management interface after preserving local changes. Disabling the skill removes its availability without deleting documents already created.
