---
author: Mark A. Lane, Ph.D.
status: User guide for draft development skills
date: 2026-10-15
---

# Building apps without a software background

Describe what you want people to accomplish. The development skills should choose suitable tools, build in manageable steps, and check the result without requiring you to know programming terminology. You should not need to remember to ask for tests, linters, or a code review.

Start with the [setup guide for your product](setup/README.md). For app work, install `develop-from-spec`; `check-code-quality` and `review-and-repair-code` provide companion workflows. Each skill also works on its own. These are drafts, and evaluations in Claude Code and Codex are still pending.

## What to tell the assistant

Explain who will use the app, the task they need to complete, and what a successful result looks like. Include a small example or existing file when available. Say whether records are private, whether colleagues need to share them, and whether work should still be there after closing the app. If you do not know an answer, describe the situation and let the assistant explain the practical choices.

For example:

> Build a tracker for our team's project milestones. Colleagues need to see the same records, and changes must still be there tomorrow. We need to filter by owner and export the current selection. Start with synthetic records. Choose sensible tools and verify the main tasks before handing it over. Ask about business decisions you cannot infer from this description.

You can start smaller:

> Create a single page explaining this workshop, using the supplied content. It has no sign-in, saved records, or external services. Check the links and how it works on a narrow screen.

The assistant should handle routine technical decisions. It should explain a choice when it changes what people can do, where their data goes, or what the project costs.

## What the development skills should handle

| Common problem | Expected agent behavior |
| --- | --- |
| The result looks right but does the wrong thing | Write concrete acceptance criteria, check calculations against known examples, and exercise the main task through the app. |
| Saved work disappears | Choose storage that fits the intended use and check that records survive the relevant reload or restart. Explain whether colleagues share those records. |
| A demo looks like a connected business tool | Label sample data and unfinished integrations. Show a useful error when a real connection fails. |
| Bad input or a failed connection breaks the app | Check relevant invalid inputs, empty results, request failures, and recovery. A failed save must not look successful. |
| Private records or credentials become exposed | Keep secret values out of browser code and tracked files. For private shared apps, verify who can read and change records at the service boundary. |
| Each fix creates another problem | Make focused changes, retain useful regression checks, preserve your existing work, and diagnose repeated failures before trying again. |
| Nobody knows how to run it later | Maintain clear setup, start, stop, and check instructions, with configuration placeholders and an explanation of where data lives. |

These checks should fit the app. A small public information page needs fewer checks than a shared tool with private records and paid integrations. The assistant should load detailed guidance as needed and use ordinary reasoning settings for routine work.

## What a useful handoff looks like

Expect a short explanation of what works and where to try it, with the checks the assistant actually performed. It should identify anything that prevents your intended use. "Implemented," "verified locally," and "deployed" describe different evidence. If the assistant could not test a browser flow or connect a service, it should say which part remains unverified.

Try your most important task with a small example you understand. For a tracker, create a record, change it, filter it, and reload. For a dashboard, compare a total or percentage with a known example. Your trial adds useful feedback; the assistant still owns its engineering checks.

Before sharing an app, the intended audience, data access, and hosting must match its purpose. An attractive local preview does not establish that a shared deployment works. The agent should prepare and verify what it can within your instructions and identify any remaining decision or account setup. Before you share it, ask for a [check before publishing](../skills/check-before-publishing/SKILL.md): "Check this app before I share it with my team."

## When something goes wrong

Describe what you tried, what you expected, and what happened instead. Include the exact error when available, with credentials and private records removed. You can say:

> Saving a new milestone shows "Saved," but the record disappears when I reload. Reproduce that behavior, preserve the existing records, and fix it with a regression check. Keep changes focused and report what you verified.

If repeated attempts fail, ask the assistant to explain the evidence for its diagnosis before making further changes. A fresh session can use the project's specification, setup instructions, and current changes as context instead of repeating a long conversation.
