---
author: Mark A. Lane, Ph.D.
reviewed: 2026-10-19
status: Configuration guidance; runtime behavior not yet benchmarked
---

# Model routing

Apply a product section only when that host and its configured capabilities match the session. Preserve active user and project selections. Native Cursor Agent and unfamiliar hosts have no routing profile here: use the current suitable model directly, without inventing switching or installing adapters. Codex inside an editor uses the Codex route only when its actual controls are available. Do not substitute another vendor's models without an authorized configured integration.

## Reasoning and speed limits

Use Medium or High across providers. Start Sonnet, Opus, Fable, GPT-6.1 Sol, and GPT-6 Astra at Medium, increasing to High when warranted. Start Haiku and Luna at High; use Extra on Haiku or Extra High on Luna when harder work or recurring reasoning problems justify it. Reserve Extra/Extra High on the more powerful models for very difficult tasks or repeated issues that warrant deeper reasoning. Choose effort at the agent's discretion within the task budget. Low/Light is available for deliberately simple work.

OpenAI permits Light, Medium, High, and Extra High; Ultra is prohibited. Anthropic permits Low, Medium, High, and Extra; Max is prohibited. Extra/Extra High remains allowed when it is the highest setting exposed by the client. Diagnose repeated failures before raising effort; unavailable inputs, permissions, or tools do not establish a reasoning shortfall. Use standard speed only; never enable Fast, Ultrafast, or other premium speed modes. Apply the same limits to workers and check inherited settings when the host exposes them. If a conflicting runtime setting cannot be changed through authorized controls, disclose it without claiming compliance or changing account configuration.

These are library operating choices as of October 19, 2026. The OpenAI ceiling excludes Ultra because its additional token use is not justified for this library's work; this is an operating policy, not a claim of measured gains across every task. Provider documentation establishes available controls, not the optimal route for this library. The [Claude Code fast-mode guide](https://code.claude.com/docs/en/fast-mode) describes higher per-token pricing; the [OpenAI speed guide](https://learn.chatgpt.com/docs/agent-configuration/speed) distinguishes subscription-usage and credit multipliers. Keep those charges separate from measured input and output token counts. No universal doubling of generated tokens is assumed.

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

Use `claude-sonnet-5-5` for most work. Delegate easy or repetitive subtasks to `claude-haiku-5-5` when delegation earns its overhead. Use `claude-opus-5-5` for difficult work or a bounded consultant pass on a specific question. Sonnet can retain responsibility for implementation and verification after the consultation.

Prefer Opus 5.5 with a justified increase to High or Extra before considering Fable. Reserve Fable for extreme situations where evidence identifies a capability gap that Opus cannot adequately address within those limits. Record that gap and the expected benefit; a failed tool call or missing input is not sufficient justification. Use the account's supported Fable version and record its exact requested and observed model IDs. Return routine work to Sonnet after the exceptional question is resolved.

Anthropic's [Opus 5.5 announcement](https://www.anthropic.com/claude-opus-5-5), reviewed October 19, 2026, reports competitive or better results than Fable 5.1 on several tasks at lower cost. This supports trying Opus first. It does not establish equal effectiveness or fewer tokens on every workload or effort setting; matched library benchmarks remain pending.

These model IDs appear in Anthropic's official [Sonnet](https://platform.claude.com/docs/en/models/sonnet-5-5/overview), [Haiku](https://platform.claude.com/docs/en/models/haiku-5-5/overview), and [Opus](https://platform.claude.com/docs/en/models/opus-5-5/overview) documentation. Account and provider availability still need checking.

[Claude Code custom subagents](https://code.claude.com/docs/en/sub-agents) can select a model and bound turns. A model configured for the main session does not by itself establish the intended worker routing. Explicit model IDs keep these versions stable; aliases may resolve differently over time.

The example worker definitions are [bulk-worker](../assets/claude-code/agents/cisco-bulk-worker.md) and [hard-problem](../assets/claude-code/agents/cisco-hard-problem.md). Copy selected files into a test project's `.claude/agents/` directory when setting up this workflow. They are configuration examples, not installed agents. Their turn limits are pilot defaults, not total spending caps. Do not repeatedly resume a limited worker without accounting for the cumulative work.

Start Sonnet 5.5 at Medium and Haiku workers at High. Opus and Fable consultations start at Medium; increase effort when the task warrants it under the limits above. Check the installed client's effort controls; reasoning names and availability need not match Codex exactly.

Current [model-selection documentation](https://code.claude.com/docs/en/sub-agents#choose-a-model) describes invocation overrides, inherited settings, and substitutions under organization controls. A definition's model is a request, not proof of execution. Where the installed client provides it, retain the running task's `/tasks` model/effort display and any substitution warning as evidence. Check the installed version's behavior; do not change environment or account settings to force an unavailable selection.

## Codex

Use `gpt-6.1-sol` for the main session, starting at Medium and using High when warranted. Route repetitive work to `gpt-6-luna`; the worker example starts at High, with Extra High available for harder work or recurring reasoning problems. Start rare Astra consultations at Medium and increase effort as needed within the limits above. Light can be selected for deliberately simple work. Treat these settings as library defaults to evaluate, not established optima.

The [Codex subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents) describes custom agent files, model settings, and inheritance. Configure model and reasoning together so a worker does not inherit an unnecessarily expensive setting. Verify that the account and client support the requested combination.

The [Luna worker example](../assets/codex/agents/cisco-bulk-worker.toml) can be copied into a test project's `.codex/agents/` directory. It leaves the coordinator's model unchanged. Custom agent instructions do not establish a separate security sandbox; workers inherit the host's permissions.

Reserve Extra High on GPT-6.1 Sol for very difficult decisions or repeated issues that warrant deeper reasoning. Use `gpt-6-astra` only in rare cases where a specific unresolved problem needs greater capability than Sol can provide within those limits. Keep the assignment bounded, record the reason, and return routine work to Sol afterward. Astra also uses standard speed and permits Light through Extra High, never Ultra. The [OpenAI model guide](https://learn.chatgpt.com/docs/models), reviewed October 19, 2026, documents Sol, Luna, and Astra; verify account access before selecting them. This configuration does not call Anthropic models from Codex.

The current [custom-agent rules](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents) give model and effort values in an agent file precedence over previously resolved spawn, default, or inherited settings. Inspect relevant configuration before interpreting a requested selection. A configured value or spawn argument still does not prove the executing model. Use reliable per-worker execution metadata when exposed; otherwise record the effective model or effort as unknown. Aggregate turn usage and the coordinator's model do not identify each worker's execution.

## Selection and execution evidence

For substantial delegated work or benchmarks, a short handoff or evaluation entry should identify the task, selection rationale, requested model and effort, observed effective model and effort, and known changes. Cite the task-specific receipt or trace that establishes observed fields. Keep requested and observed values separate even when they match; do not fill unknown execution fields from configuration or a worker's unsupported self-report.

If a selection is unavailable or overridden, preserve user choices and report the actual limitation or observed change. Continue independent work with a suitable available approach within existing authority. Missing metadata is not a reason to add adapters, expand permissions, or modify user configuration. Ordinary direct tasks need no printed selection table.

The [upstream review and notices](upstream.md) record the pinned source that informed this rubric and the local departures from it.

## Enforcement and measurement

Use host controls for concurrency and turn limits where available. For API workflows, enforce a cumulative allowance in the orchestration layer across coordinator and workers. A per-response output limit does not cap total input, reasoning, retries, or worker usage.

Compare the same representative tasks under a single-model baseline and the proposed routing. Record completion quality, total usage, latency, and failures. API costs require current account/provider rates; subscription workflows should report usage and limits without implying that a fixed subscription charge falls with each cheaper model call.
