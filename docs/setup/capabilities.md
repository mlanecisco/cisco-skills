---
author: Mark A. Lane, Ph.D.
reviewed: 2026-10-21
status: Partly verified against official pages; no observed tests recorded
---

# Capability matrix

This matrix records what each product and mode can do, so the other guides can link here instead of repeating platform claims. Choose a route by the capabilities your task needs, not by product name.

Every cell carries a status. `V` means the claim was read on an official page on the review date (2026-10-21), and the source key follows. `U` means unverified: the claim comes from an earlier guide, the product's general behavior, or an official page that could not be read. No cell is backed by an observed test with a record, so treat `V` as "documented", not "works here". Treat a `U` cell as an open question and check it before relying on it. Documentation can lag the product, and account or administrator settings can change what a given person sees.

## Matrix

| Product and mode | Supplied files | Local filesystem | Code execution | Document editing | Rendering | Browser interaction | Authenticated publishing |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Claude Desktop chat | U | U | V: required for skills (S1) | U | U | U | U |
| Claude Cowork | U | U | U | U | U | U | U |
| Claude Code | U | U: skills load from local folders (S2), but file access is not documented there | U | U | U | U | U |
| ChatGPT chat | U | U | U | U | U | U | U |
| Codex in ChatGPT Desktop or CLI | U | U: skills load from local folders, but file access is not documented there | U | U | U | U | U |
| Cursor Agent | U | U: skills load from local folders, but file access is not documented there | U | U | U | U | U |

| Product and mode | Permissions, account, or admin settings | Skill install routes | Team distribution route |
| --- | --- | --- | --- |
| Claude Desktop chat | V: code execution and file creation must be on. Team and Enterprise owners enable code execution and Skills under Organization settings, Plugins & skills. Owners can turn off user-created skills (S1) | V: Customize > Skills, upload a ZIP of one skill folder (S1) | V: owners can provision skills for everyone, or share with the organization or groups (groups on Enterprise only). Publishing is on Team and Enterprise, and owners can require review (S1) |
| Claude Cowork | V: skill sharing works in Cowork, which has a directory for organization skills (S1). Other settings U | V: enable the skill on the claude.ai account to sync it. Personal `~/.claude/skills/` skills do not load in Cowork (S2) | V: organization skills directory (S1) |
| Claude Code | V: terminal sync needs v2.1.273 or later and a claude.ai sign-in, and does not run with API-key or cloud-provider sign-in (S1, S2) | V: project `.claude/skills/`, personal `~/.claude/skills/`, plugin, enterprise managed location, or account sync (S2) | V: commit `.claude/skills/` to the repository, ship a plugin through a marketplace, or deploy through managed settings (S2) |
| ChatGPT chat | U: an earlier guide cites eligible Business, Enterprise, Healthcare, and Edu workspaces and administrator settings. The cited help page (S5) returned an access error and was not read | U: Plugins > Skills > Create > Upload, per earlier guide (S5). Plugin-bundled skills are also documented for Chat and Work (S4) | U: workspace sharing per earlier guide (S5). Plugin directory shared by ChatGPT and Codex (S4) |
| Codex in ChatGPT Desktop or CLI | V: standalone skills run in the ChatGPT desktop app, CLI, and IDE extension. Skill support in Codex Cloud is not addressed (S4). Other permissions U | V: project `.agents/skills` (each folder up to the repository root), user `$HOME/.agents/skills`, admin `/etc/codex/skills`, `$skill-installer` (S4) | V: package skills as a plugin shared through the directory used by ChatGPT and Codex (S4) |
| Cursor Agent | V: Cloud Agents see only `~/.cursor/skills/`, and only with Sync Skills for Cloud Agents turned on. Admins can turn that sync off for a team (S3) | V: project `.agents/skills/` or `.cursor/skills/`, user `~/.agents/skills/` or `~/.cursor/skills/`. Cursor also reads `.claude/skills/` and `.codex/skills/` (S3) | V: package as a plugin and publish to a team marketplace. A GitHub import needs `.cursor-plugin/marketplace.json`. Sync is private (S3) |

## Sources

| Key | Source | Read on |
| --- | --- | --- |
| S1 | [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude) | 2026-10-21 |
| S2 | [Claude Code skills](https://code.claude.com/docs/en/skills). The first 100,000 of about 110,500 characters were read | 2026-10-21 |
| S3 | [Cursor skills](https://cursor.com/docs/skills) | 2026-10-21 |
| S4 | [Build skills for ChatGPT and Codex](https://learn.chatgpt.com/docs/build-skills), reached by redirect from the Codex skills page | 2026-10-21 |
| S5 | [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt). Fetch returned HTTP 403, so nothing here is confirmed | not read |

## Reading the gaps

The file, execution, editing, rendering, browser, and publishing columns are mostly `U` because the pages read so far describe where skills load from, not what each session can do with files or tools. Close these gaps with a short observed test per product and a retained record, not with more documentation reading. Until then, a skill that needs rendering or publishing should say so up front and report what the session actually did.

Local Cursor and Codex project folders are separate from Cloud Agent or cloud task environments. A skill that works in a local folder is not thereby available in a cloud environment.

## Where each guide fits

- [Claude Desktop](claude-desktop.md) covers Desktop chat and points to Cowork and Code.
- [Claude Code CLI](claude-code.md)
- [ChatGPT](chatgpt.md)
- [Codex](codex.md)
- [Cursor](cursor.md)

For model and reasoning settings, see the [routing reference](../../skills/efficient-workflow/references/routing.md).
