---
author: Mark A. Lane, Ph.D.
reviewed: 2026-10-21
status: Partly documented from official pages; no observed tests recorded
---

# Capability matrix

This matrix records what each product and mode can do, so the other guides can link here instead of repeating platform claims. Choose a route by the capabilities your task needs, not by product name. Rows are split by execution environment where file access or tools differ.

Each cell has one of three statuses:

- **Documented**: an official page read on the review date (2026-10-21) states it. The source key follows, and any prerequisites are listed. A tenant or account test is still pending.
- **Observed**: an actual test in this environment, with a retained record. No cell has this status yet.
- **Unknown**: no official page read so far states it, or the page could not be read. Check it before relying on it.

Documentation can lag the product, and account or administrator settings can change what a given person sees.

## Matrix

| Product and mode | Supplied files | Local filesystem | Code execution | Document editing | Rendering | Browser interaction | Authenticated publishing |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Claude Desktop chat | Unknown | Unknown | Documented: required for skills (S1) | Unknown | Unknown | Unknown | Unknown |
| Claude Cowork | Unknown | Documented: reads and writes files in folders you connect, using the Desktop app (S6) | Documented: code and shell commands run in an isolated environment on Anthropic's servers, and need an internet connection (S6) | Documented: creates Excel workbooks with formulas, PowerPoint presentations, and formatted documents (S6) | Unknown | Documented: built-in browser can open pages, click, type, and fill forms, and is rolling out gradually (S6) | Unknown |
| Claude Code | Unknown | Unknown: skills load from local folders (S2), but file access is not documented there | Unknown | Unknown | Unknown | Unknown | Unknown |
| ChatGPT chat | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown |
| ChatGPT Work | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown |
| Codex Local (CLI, IDE, ChatGPT Desktop) | Unknown | Documented: runs in your current project directory on your computer (S7) | Unknown | Unknown | Unknown | Unknown | Unknown |
| Codex Worktree | Unknown | Documented: runs on your computer in a Git worktree separate from your checkout, for local Git projects (S7) | Unknown | Unknown | Unknown | Unknown | Unknown |
| Codex Cloud tasks | Unknown | Documented: your computer's local files, processes, browser sign-ins, and VPN access aren't automatically transferred (S7) | Unknown | Unknown | Unknown | Unknown | Unknown |
| Cursor Agent, local | Unknown | Unknown: skills load from local folders (S3), but file access is not documented there | Unknown | Unknown | Unknown | Unknown | Unknown |
| Cursor Cloud Agents | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown |

| Product and mode | Permissions, account, or admin settings | Skill install routes | Team distribution route |
| --- | --- | --- | --- |
| Claude Desktop chat | Documented: code execution and file creation must be on. Team and Enterprise owners enable code execution and Skills under Organization settings, Plugins & skills. Owners can turn off user-created skills (S1) | Documented: Customize > Skills, upload a ZIP of one skill folder (S1) | Documented: owners can provision skills for everyone or share with the organization or groups (groups on Enterprise only). Publishing is on Team and Enterprise, and owners can require review (S1) |
| Claude Cowork | Documented: paid plans only (Pro, Max, Team, Enterprise). Desktop is the most complete surface, and Enterprise web access depends on an admin. Owners can turn off web search, and permission modes are Manual, Auto, and Skip (S6) | Documented: enable the skill on the claude.ai account to sync it, and personal `~/.claude/skills/` skills do not load in Cowork (S2). Plugins bundle skills and work in chat, Code, and Cowork (S6) | Documented: Cowork has a directory for organization skills (S1) |
| Claude Code | Documented: terminal sync needs v2.1.273 or later and a claude.ai sign-in, and does not run with API-key or cloud-provider sign-in (S1, S2) | Documented: project `.claude/skills/`, personal `~/.claude/skills/`, plugin, enterprise managed location, or account sync (S2) | Documented: commit `.claude/skills/` to the repository, ship a plugin through a marketplace, or deploy through managed settings (S2) |
| ChatGPT chat | Unknown: an earlier guide cites eligible Business, Enterprise, Healthcare, and Edu workspaces and administrator settings, but the cited help page (S5) could not be read | Unknown: earlier guide describes Plugins > Skills > Create > Upload (S5, not read). Plugin-bundled skills are documented for Chat and Work (S4) | Unknown: workspace sharing per earlier guide (S5, not read). Documented: plugin directory shared by ChatGPT and Codex (S4) |
| ChatGPT Work | Unknown | Documented: plugin-bundled skills are available in Work (S4). Standalone-skill support in Work is not stated | Documented: plugin directory shared by ChatGPT and Codex (S4) |
| Codex Local (CLI, IDE, ChatGPT Desktop) | Unknown | Documented: project `.agents/skills` (each folder up to the repository root), user `$HOME/.agents/skills`, admin `/etc/codex/skills`, and `$skill-installer`. Standalone skills run in the ChatGPT desktop app, CLI, and IDE extension (S4) | Documented: package skills as a plugin shared through the directory used by ChatGPT and Codex (S4) |
| Codex Worktree | Unknown | Unknown: the modes page (S7) does not address skills | Unknown |
| Codex Cloud tasks | Documented: requires an accessible published environment, which you create or get from a workspace admin (S7) | Unknown: skill support in Codex Cloud is not addressed (S4, S7) | Unknown |
| Cursor Agent, local | Unknown | Documented: project `.agents/skills/` or `.cursor/skills/`, user `~/.agents/skills/` or `~/.cursor/skills/`. Cursor also reads `.claude/skills/` and `.codex/skills/` (S3) | Documented: package as a plugin and publish to a team marketplace. A GitHub import needs `.cursor-plugin/marketplace.json`. Personal sync is private and does not share with teammates (S3) |
| Cursor Cloud Agents | Documented for personal skills: only `~/.cursor/skills/` syncs to Cloud Agents, and only with Sync Skills for Cloud Agents turned on. Admins can turn that sync off for a team (S3) | Documented: personal sync copies only `~/.cursor/skills/`, and does not copy project skills or other local skill directories (S3). Unknown: availability through repository and plugin distribution, which needs separate verification | Documented: for self-hosted workers, the documentation describes using project skills from the repository or skills included in the worker image (S3). Unknown for other distribution routes |

## Sources

| Key | Source | Read on |
| --- | --- | --- |
| S1 | [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude) | 2026-10-21 |
| S2 | [Claude Code skills](https://code.claude.com/docs/en/skills). The first 100,000 of about 110,500 characters were read | 2026-10-21 |
| S3 | [Cursor skills](https://cursor.com/docs/skills) | 2026-10-21 |
| S4 | [Build skills for ChatGPT and Codex](https://learn.chatgpt.com/docs/build-skills), reached by redirect from the Codex skills page | 2026-10-21 |
| S5 | [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt). Fetch returned HTTP 403, so nothing here is confirmed | not read |
| S6 | [Get started with Claude Cowork](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork) | 2026-10-21 |
| S7 | [Codex modes](https://learn.chatgpt.com/docs/environments/modes). The page does not address internet access or skill availability per mode | 2026-10-21 |

## Reading the gaps

Where an official page documents a capability, the cell says Documented with its prerequisites. Further official documentation can move a cell from Unknown to Documented. Tenant or account tests establish account-specific availability and are the only route to Observed, which no cell has yet. A skill that needs rendering or publishing should say so up front and report what the session actually did.

Local Cursor and Codex project folders are separate from Cloud Agent or cloud task environments. A skill that works in a local folder is not thereby available in a cloud environment.

## Where each guide fits

- [Claude Desktop](claude-desktop.md) covers Desktop chat and points to Cowork and Code.
- [Claude Code CLI](claude-code.md)
- [ChatGPT](chatgpt.md)
- [Codex](codex.md)
- [Cursor](cursor.md)

For model and reasoning settings, see the [routing reference](../../skills/efficient-workflow/references/routing.md).
