---
name: efficient-workflow
description: Reduce token use in substantial or repetitive work through selective context, scripts, bounded delegation, and task-appropriate models and reasoning. Use when the user requests efficiency, model routing, cost control, or high-volume processing.
metadata:
  author: Mark A. Lane, Ph.D.
  version: "0.1.0"
  status: draft
---

# Efficient workflows

Complete the requested outcome with the least unnecessary model work. Preserve correctness and required verification. Judge efficiency by the cost of an acceptable result, including retries and coordination.

## Choose the execution path

For a small task, work directly. Use scripts for deterministic operations such as counting, sorting, format conversion, and repeated calculations. Delegate when a bounded worker can perform a substantial portion of the work more economically or keep large temporary material out of the main conversation.

Use the model policy in [routing](references/routing.md) for the active product. Read only the relevant product section. A skill supplies guidance; the host supplies actual model selection, delegation, and usage controls. If a requested model or capability is unavailable, say so and continue with an available suitable approach without claiming that routing occurred.

Keep any explicit user budget and authorized scope. Do not change global model settings, installation, or account configuration merely to complete an ordinary task.

## Control context and reasoning

- Load the relevant skill and references when needed. Avoid reading the entire library, repository, document collection, or conversation into every worker.
- Search for relevant files and sections before opening full files. Inspect bounded excerpts and extend them when the evidence requires it. Ensure required inputs are covered; a partial excerpt must not become an unsupported claim about the whole file.
- Favor low reasoning effort for routine work. Use medium for work that needs more analysis. Use high only for a demonstrated unresolved difficulty or an established task benchmark.
- Strongly discourage the highest thinking levels as routine defaults. Use them only for an explicit user choice or a relevant benchmark that supports their cost, within the available budget and host capabilities.
- Make proportionate changes. Avoid speculative features, unrelated refactoring, exhaustive planning for small tasks, and repeated rewrites after the result meets its criteria.
- Run the checks that establish correctness. Repeat or broaden them when a change, failure, or remaining uncertainty justifies it.

## Delegate bounded work

When delegation is authorized and supported, give each worker a clear output and acceptance check. Include only the needed inputs, paths, constraints, and relevant decisions. Use independent chunks and avoid assigning the same task to multiple workers unless comparison is the actual purpose.

Start with at most two workers concurrently and no nested delegation. These are pilot defaults that can be adjusted for a measured workload or explicit user request. A short task often needs no worker.

Specify the worker's task limit and expected response size. Return large results as files when permitted, with a concise summary and location. Keep full logs and repeated source text out of handoffs unless needed to diagnose a failure.

A useful handoff contains:

```text
Outcome:
Relevant inputs and permitted output paths:
Constraints and decisions already made:
Acceptance check:
Time, turn, or token allowance supported by the host:
Return format, evidence, and unresolved questions:
```

The coordinator checks the result before using it. Validate deterministic outputs with code where possible; examine a representative sample of routine bulk work and all flagged or ambiguous cases. If consequences require checking every item, retain that coverage.

After a failed attempt, use the failure evidence to choose a narrower retry, better inputs, or a more capable model. Do not repeat an unchanged attempt. After two unsuccessful attempts on a subtask, reassess before spending more; this is a checkpoint, not permission to silently abandon required work.

Use Opus 5.5 for exceptionally difficult Claude subtasks. Keep routine Claude work on Haiku 5.5 and coordination on Sonnet 5.5. In Codex, use GPT-6 Luna for repetitive work and GPT-6.1 Sol for coordination and harder decisions. Do not substitute a different vendor's models without a configured integration and authorization.

## Measure and stop

When usage data is available, capture model, reasoning setting, input/output tokens, cached or reasoning tokens where exposed, worker calls, retries, elapsed time, and whether the result passed its checks. Report actual values, not estimates presented as measurements. Avoid double-counting token categories that the provider already includes in totals.

A prompt instruction is a best-effort limit. Hard limits require host or API enforcement that accounts for all workers and prevents further calls when the allowance is exhausted. Preserve completed work and report what remains when an enforced limit stops execution.

Finish when the requested deliverable passes the relevant checks. Give a concise result and any material limitation. Do not continue optimizing, reviewing, or spawning workers without a concrete reason.
