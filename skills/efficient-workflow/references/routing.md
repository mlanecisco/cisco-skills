---
author: Mark A. Lane, Ph.D.
reviewed: 2026-10-15
status: Configuration guidance; runtime behavior not yet benchmarked
---

# Model routing

## Claude Code

Use `claude-sonnet-5-5` for the main session. Route simple extraction, classification, and repetitive subtasks to `claude-haiku-5-5`. Reserve `claude-opus-5-5` for exceptionally difficult work that needs a focused expert pass.

These model IDs appear in Anthropic's official [Sonnet](https://platform.claude.com/docs/en/models/sonnet-5-5/overview), [Haiku](https://platform.claude.com/docs/en/models/haiku-5-5/overview), and [Opus](https://platform.claude.com/docs/en/models/opus-5-5/overview) documentation. Account and provider availability still need checking.

[Claude Code custom subagents](https://code.claude.com/docs/en/sub-agents) can select a model and bound turns. A model configured for the main session does not by itself establish the intended worker routing. Explicit model IDs keep these versions stable; aliases may resolve differently over time.

The example worker definitions are [bulk-worker](../assets/claude-code/agents/cisco-bulk-worker.md) and [hard-problem](../assets/claude-code/agents/cisco-hard-problem.md). Copy selected files into a test project's `.claude/agents/` directory when setting up this workflow. They are configuration examples, not installed agents. Their turn limits are pilot defaults, not total spending caps. Do not repeatedly resume a limited worker without accounting for the cumulative work.

Start the main session with Sonnet 5.5 and a supported low effort setting for routine work. Use medium when needed. Check the installed client's effort controls; reasoning names and availability need not match Codex exactly.

## Codex

Use `gpt-6.1-sol` for the main session, with low effort for routine work and medium when needed. Route repetitive work to `gpt-6-luna` with a supported economical effort setting. Treat the low-effort Luna example as a pilot configuration to evaluate, not an established optimum.

The [Codex subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents) describes custom agent files, model settings, and inheritance. Configure model and reasoning together so a worker does not inherit an unnecessarily expensive setting. Verify that the account and client support the requested combination.

The [Luna worker example](../assets/codex/agents/cisco-bulk-worker.toml) can be copied into a test project's `.codex/agents/` directory. It leaves the coordinator's model unchanged. Custom agent instructions do not establish a separate security sandbox; workers inherit the host's permissions.

For difficult decisions, keep GPT-6.1 Sol and increase effort only as the evidence warrants. The highest available levels remain exceptional. This configuration does not call Anthropic models from Codex.

## Enforcement and measurement

Use host controls for concurrency and turn limits where available. For API workflows, enforce a cumulative allowance in the orchestration layer across coordinator and workers. A per-response output limit does not cap total input, reasoning, retries, or worker usage.

Compare the same representative tasks under a single-model baseline and the proposed routing. Record completion quality, total usage, latency, and failures. API costs require current account/provider rates; subscription workflows should report usage and limits without implying that a fixed subscription charge falls with each cheaper model call.
