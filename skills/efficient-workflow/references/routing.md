---
author: Mark A. Lane, Ph.D.
reviewed: 2026-10-16
status: Configuration guidance; runtime behavior not yet benchmarked
---

# Model routing

Apply a product section only when that host and its configured capabilities match the session. Preserve active user and project selections. Native Cursor Agent and unfamiliar hosts have no routing profile here: use the current suitable model directly, without inventing switching or installing adapters. Codex inside an editor uses the Codex route only when its actual controls are available. Do not substitute another vendor's models without an authorized configured integration.

## Task categories

These examples support the entrypoint's selection rubric; they are not automatic tier assignments. Use relevant completed tasks or benchmarks when available. Without comparable evidence, retain the configured pilot choices and acknowledge uncertainty. Consider coordinator context, retries, and verification as part of total cost.

| Category | Typical evidence and work | Use of existing options |
| --- | --- | --- |
| Routine processing | Clear extraction or classification criteria; identifiers, counts, and required fields can be checked independently | Haiku or Luna may fit an authorized batch; a script or direct coordinator action may be cheaper |
| Bounded implementation | A stated contract or reproduction, with meaningful interpretation and checks for important behavior | Small work can stay with Sonnet or Sol in the coordinator; no additional worker role is required |
| Complex judgment | Unresolved ambiguity, interacting constraints, conflicting evidence, or consequential decisions that are difficult to validate | Improve evidence or decompose first; retain capable coordinator judgment and use the existing exceptional escalation path only when justified |

A configuration rename can be mechanical yet break existing consumers. Verify old and new interfaces, precedence, and relevant callers rather than assuming inexpensive repetition means low consequence. Conversely, many independently checkable records do not become difficult judgment merely because there are many of them.

Treat tests as evidence for the behavior they cover. If the contract requires compatibility but current tests cover only the new key, add or run an independent compatibility check before judging success. An economical model can perform narrow objective checks of another model's output. Consequential judgment needs a suitably capable reviewer and adequate evidence; it does not require a universal ban on cheaper reviewers.

Diagnose a failed check before changing models. Missing inputs call for better inputs; ambiguous requirements call for clarification or decomposition; a missing tool or denied operation calls for an authorized environment route or an honest limit. Escalate capability when the unresolved reasoning problem supports it, rather than after every failure. A repeated failure does not by itself identify its cause.

## Claude Code

Use `claude-sonnet-5-5` for the main session. Route simple extraction, classification, and repetitive subtasks to `claude-haiku-5-5`. Reserve `claude-opus-5-5` for exceptionally difficult work that needs a focused expert pass.

These model IDs appear in Anthropic's official [Sonnet](https://platform.claude.com/docs/en/models/sonnet-5-5/overview), [Haiku](https://platform.claude.com/docs/en/models/haiku-5-5/overview), and [Opus](https://platform.claude.com/docs/en/models/opus-5-5/overview) documentation. Account and provider availability still need checking.

[Claude Code custom subagents](https://code.claude.com/docs/en/sub-agents) can select a model and bound turns. A model configured for the main session does not by itself establish the intended worker routing. Explicit model IDs keep these versions stable; aliases may resolve differently over time.

The example worker definitions are [bulk-worker](../assets/claude-code/agents/cisco-bulk-worker.md) and [hard-problem](../assets/claude-code/agents/cisco-hard-problem.md). Copy selected files into a test project's `.claude/agents/` directory when setting up this workflow. They are configuration examples, not installed agents. Their turn limits are pilot defaults, not total spending caps. Do not repeatedly resume a limited worker without accounting for the cumulative work.

Start the main session with Sonnet 5.5 and a supported low effort setting for routine work. Use medium when needed. Check the installed client's effort controls; reasoning names and availability need not match Codex exactly.

Current [model-selection documentation](https://code.claude.com/docs/en/sub-agents#choose-a-model) describes invocation overrides, inherited settings, and substitutions under organization controls. A definition's model is a request, not proof of execution. Where the installed client provides it, retain the running task's `/tasks` model/effort display and any substitution warning as evidence. Check the installed version's behavior; do not change environment or account settings to force an unavailable selection.

## Codex

Use `gpt-6.1-sol` for the main session, with low effort for routine work and medium when needed. Route repetitive work to `gpt-6-luna` with a supported economical effort setting. Treat the low-effort Luna example as a pilot configuration to evaluate, not an established optimum.

The [Codex subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents) describes custom agent files, model settings, and inheritance. Configure model and reasoning together so a worker does not inherit an unnecessarily expensive setting. Verify that the account and client support the requested combination.

The [Luna worker example](../assets/codex/agents/cisco-bulk-worker.toml) can be copied into a test project's `.codex/agents/` directory. It leaves the coordinator's model unchanged. Custom agent instructions do not establish a separate security sandbox; workers inherit the host's permissions.

For difficult decisions, keep GPT-6.1 Sol and increase effort only as the evidence warrants. The highest available levels remain exceptional. This configuration does not call Anthropic models from Codex.

The current [custom-agent rules](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents) give model and effort values in an agent file precedence over previously resolved spawn, default, or inherited settings. Inspect relevant configuration before interpreting a requested selection. A configured value or spawn argument still does not prove the executing model. Use reliable per-worker execution metadata when exposed; otherwise record the effective model or effort as unknown. Aggregate turn usage and the coordinator's model do not identify each worker's execution.

## Selection and execution evidence

For substantial delegated work or benchmarks, a short handoff or evaluation entry should identify the task, selection rationale, requested model and effort, observed effective model and effort, and known changes. Cite the task-specific receipt or trace that establishes observed fields. Keep requested and observed values separate even when they match; do not fill unknown execution fields from configuration or a worker's unsupported self-report.

If a selection is unavailable or overridden, preserve user choices and report the actual limitation or observed change. Continue independent work with a suitable available approach within existing authority. Missing metadata is not a reason to add adapters, expand permissions, or modify user configuration. Ordinary direct tasks need no printed selection table.

The [upstream review and notices](upstream.md) record the pinned source that informed this rubric and the local departures from it.

## Enforcement and measurement

Use host controls for concurrency and turn limits where available. For API workflows, enforce a cumulative allowance in the orchestration layer across coordinator and workers. A per-response output limit does not cap total input, reasoning, retries, or worker usage.

Compare the same representative tasks under a single-model baseline and the proposed routing. Record completion quality, total usage, latency, and failures. API costs require current account/provider rates; subscription workflows should report usage and limits without implying that a fixed subscription charge falls with each cheaper model call.
