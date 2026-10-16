---
author: Mark A. Lane, Ph.D.
---

# Repository instructions

## Commits

Use the configured human Git identity. Do not credit an assistant, model, or tool as an author, committer, or co-author, or add assistant attribution to commit messages. Preserve attribution and license notices required for any imported upstream material.

## Library work

Maintain shared skill sources under `skills/`. Keep platform configuration separate from portable task instructions. Follow the priorities in [the build plan](docs/build-plan.md) when expanding the library.

Keep workflows usable by nonprogrammers and proportionate to the task. Favor economical reasoning settings, selective context, and deterministic tools where they help. Record actual checks and measurements; distinguish draft examples from behavior verified in Claude Code or Codex.

Write shared guidance for its intended users, using roles and project or team configuration. Identify evidence by its source, version, date, and verification status. Keep conversational attribution and personal names out of operating instructions unless they are needed for the task or a source credit. Preserve author metadata and required attribution. Shared tools must accept run-specific identities separately from the library's authorship.

For original reader-facing prose written into files, use the humanizer skill in embedded mode when available, keeping the drafting and audit internal. Preserve technical literals, quotations, and citations. Set the author of generated repository documents to `Mark A. Lane, Ph.D.`.
