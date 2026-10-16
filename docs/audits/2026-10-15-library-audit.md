---
author: Mark A. Lane, Ph.D.
date: 2026-10-15
status: Completed repository audit; recommendations not implemented
audited_commit: a25b57a6342debb8d606eadfa233672bd49a03b3
---

# Cisco skills library audit

The library has a sound draft structure and unusually clear distinctions between instructions, automated checks, and behavior that has actually been tested. It is ready for a controlled pilot. It is not yet ready to offer Cisco employees a supported, repeatable installation and delivery experience across the advertised products.

The next investment should be proving a small set of complete workflows. Adding more instructions will have less value until a colleague can install a versioned package, complete a representative task, and obtain an artifact that passes independent checks. The development workflows are closest to that milestone because they already have a runnable calculation fixture. Presentation rendering and Confluence publishing need separate trials in their intended environments.

This audit found two reproducible validator defects, several acknowledged release gaps, and design decisions that become important when a personal pilot becomes a shared library. It did not find a reason to replace the portable skill-folder architecture.

## Scope and evidence

The audit covered all 54 tracked files at commit `a25b57a`, including six skill entrypoints, their references and agent examples, setup and maintenance documentation, four evaluation suites, Python tooling and tests, the GitHub Actions workflow, and both PowerPoint templates. The working tree was clean at the start. The accompanying [evidence record](2026-10-15-audit-evidence.json) contains counts, probe outcomes, and template hashes.

The review included local execution, an independent check against a temporary export of the committed tree, isolated malformed-library probes, and inspection of PowerPoint package XML. Selected current platform and vendor documentation was checked where it affected portability or publishing. The audit did not invoke the six library skills in fresh product sessions, perform Windows installation, render a presentation, authenticate to Cisco services, run hosted CI, or inspect the complete Git history for secrets. No existing implementation or skill was changed.

| Check | Observed result | What it establishes |
| --- | --- | --- |
| `.venv/bin/python scripts/check.py` | Passed on Python 3.12.13 | Current lint, format, type, regression, and structural checks pass |
| Same command against a temporary `git archive HEAD` export | Passed using the existing Python environment | Tracked sources do not need untracked project files to pass these checks |
| Regression tests | 36 passed | Validator regressions and the calculation fixture's acceptance oracle behave as asserted |
| Structural validation | Six skills and 35 evaluation definitions passed | The current files meet the implemented structural rules |
| Installed dependency versions | All matched `requirements-dev.txt` pins | The existing test environment used the declared versions |
| Isolated validator probes | Two substantive bypasses reproduced | Existing passing tests do not cover every packaging or fixture failure |
| PowerPoint ZIP integrity | Both packages passed | No ZIP integrity failure was detected |
| Template XML inspection | Both have 72 slides, 65 layouts, 16:9 dimensions, Inter SemiBold headings, and Inter body fonts | These stored properties agree with the brand reference |
| Git remote inspection | No configured remote | Hosted collaboration and CI are not established in this checkout |
| Limited credential-pattern scan | No matches in tracked text files | No matches to the selected private-key, AWS, GitHub, and OpenAI token patterns; binaries and history were excluded |

The clean-export check reused installed dependencies. It does not establish that dependency installation succeeds on a fresh machine or on every documented Python version. Similarly, package inspection does not establish that a deck renders correctly.

## Findings and priorities

P1 means resolve before a supported team release. P2 means address during the pilot or before the affected capability is promoted. P3 means a useful maintenance improvement. These are delivery priorities, not vulnerability severity ratings. A release gap already disclosed in the README is not treated as a hidden defect.

| ID | Priority | Finding | Evidence category |
| --- | --- | --- | --- |
| F01 | P1 | Runtime quality and added value have not been demonstrated | Acknowledged release gap |
| F02 | P1 | Installation, updates, and rollback lack a tested distribution path | Acknowledged release gap |
| F03 | P1 | Automated Narva publishing has no demonstrated working integration | Acknowledged integration gap |
| F04 | P1 | Distribution scope and asset permissions need an explicit decision | Governance question |
| F05 | P2 | Fixture validation accepts entries that identify no local fixture | Reproduced defect |
| F06 | P2 | Symlinked skill folders bypass Markdown reference checks | Reproduced defect |
| F07 | P2 | Product coverage is broader than the evaluation model supports | Confirmed scope mismatch |
| F08 | P2 | Current evaluations need stronger controls and less revealing inputs | Evaluation design gap |
| F09 | P2 | A team-specific Confluence tenant is embedded in the shared skill | Portability concern |
| F10 | P2 | Presentation dependencies and rendering remain difficult for a new user to resolve | Delivery gap |
| F11 | P2 | Untrusted source instructions have no explicit treatment or evaluation | Coverage gap |
| F12 | P2 | Model policy is duplicated and has no measured advantage yet | Maintenance and evidence gap |
| F13 | P2 | Release ownership and contribution rules are not operational | Maintenance gap |
| F14 | P3 | Structural checks need clearer limits and broader release verification | Hardening opportunity |

## Detailed findings

### F01 Runtime quality and added value have not been demonstrated

The [release criteria](../../README.md#release-criteria) accurately disclose that product evaluations are pending. The 35 cases are specifications, not recorded results. Twenty-four list missing inputs, and only four declare existing fixture paths. One of those four, the presentation case, still needs additional inputs. The only implemented functional fixture is a small Python calculation exercise.

This is the largest limitation on adoption. Well-written instructions can still fail to trigger, load too much context, stop unnecessarily, or produce a convincing but incomplete artifact. The broad development guidance also overlaps with behavior capable agents may already perform, so its incremental benefit needs measurement.

Start with development, review, repair, and check-only tasks in Claude Code and Codex. Record the library revision, client and model versions, selected effort, installed skills, inputs, actual output, independent checks, elapsed time, usage where exposed, and user interventions. Compare representative tasks with the same host and model without the library. Do not remove normal host safeguards for the baseline.

Acceptance: a published result set supports each promoted workflow, includes failures, and explains what the skill improved. Draft status remains on capabilities without that evidence.

### F02 Installation and updates lack a tested distribution path

The [first-session guide](../setup/README.md#first-session) tells employees to obtain a folder from the maintainer. The repository has no configured remote, release archive, package builder, installer, or install manifest. Manual copying is reasonable for development, but there is no reliable answer to which release an employee has, what changed, or how to undo an update.

The documentation already warns about duplicate installations and preserving edits. Those warnings need a practical workflow. This is particularly relevant when the same folder is discoverable by more than one product or account synchronization adds another copy.

Provide versioned ZIPs of individual skills and a small release manifest listing files and checksums. Test those exact archives. Start with explicit manual installation if that keeps maintenance simple; an automatic installer is optional. Document update, disable, remove, and rollback steps, plus how to identify an installed version. A packaging check should reject incomplete folders and unintended files.

Acceptance: a colleague who did not build the library can install, locate, use, update, and roll back one skill on each supported operating system without editing the maintained source.

### F03 Automated Narva publishing lacks a demonstrated integration

The [publishing skill](../../skills/publish-confluence-dashboard/SKILL.md) and [authentication reference](../../skills/publish-confluence-dashboard/references/authentication.md#make-a-bounded-api-update) contain sensible safeguards. They also leave the actual macro representation and API client to the agent. No tested request fixture, publisher, or recorded tenant trial establishes that the workflow works.

Narva documents entering HTML, CSS, JavaScript, and iframe content through its editor. That supports the proposed manual route; it does not establish how a particular installed macro can be created through the page API. [Narva user guide](https://help.narva.net/html-macro-for-confluence).

Draft preservation is an additional integration requirement. Atlassian states that an update to current page content can be reconciled into a draft and can override a substantially divergent draft. A saved published version alone is therefore insufficient evidence that unpublished work is recoverable. [Confluence page update reference](https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-page/#api-pages-id-put).

Keep local preparation and manual insertion as separately testable capabilities. Before promoting API publishing, demonstrate a narrowly scoped update on a disposable page with an existing macro, unrelated content, unpublished work, and a concurrent edit. Capture a sanitized request and response and the observed rendered result. If the integration cannot preserve the intended draft state, finish the local artifact and use the manual route for that case.

Acceptance: the intended macro works after publication, unrelated content and draft work survive, conflicts do not cause blind overwrites, and an intended viewer can use the dashboard. This requirement applies to the API publishing capability, not to release of unrelated skills.

### F04 Distribution scope and asset permissions need a decision

There is no root license or internal-use notice, and the repository does not record permission to redistribute the supplied Cisco templates. The [source review](../source-review.md) is careful about upstream material, but it cannot settle the distribution status of this library's original material or Cisco assets.

The two tracked templates occupy 59,104,691 bytes, about 56.4 MiB and 99.7% of tracked file bytes. Distributing the whole repository transfers those assets even when a user only needs a coding skill. The presentation skill itself correctly explains that its installed folder excludes the templates.

Decide whether the repository is a personal pilot, an internal Cisco service, or intended for public sharing. Record the appropriate owner-approved usage and distribution notice. Identify which assets belong in source control, restricted release storage, or an employee download location. This is an unresolved ownership decision, not a finding that existing possession or use is unauthorized.

Acceptance: the intended audience and distribution conditions are documented; release packaging includes only appropriate assets; template provenance and versions remain traceable. Do not assign a public open-source license to Cisco material by assumption.

### F05 Fixture validation accepts entries that identify no local fixture

In [the validator](../../scripts/validate_library.py), `evaluation()` passes each `fixtures` entry to `local_target()` at lines 236 to 246. That helper, starting at line 147, intentionally skips external URLs and fragment-only Markdown links. Those semantics are appropriate for Markdown references but not for fields documented as existing local fixture paths.

In an otherwise valid temporary library, both `fixtures: ["https://invalid.example/missing.json"]` and `fixtures: ["#missing"]` passed with no errors. Neither identifies an existing local fixture. A directory entry also passed; directories may be legitimate project fixtures, but the schema does not distinguish that intended use from an accidental path.

Give fixtures their own path validation. Require a nonempty relative filesystem path, reject URL schemes and fragments, resolve within the repository, and check existence. Explicitly support file or project-directory fixtures as needed. Keep unresolved or remotely supplied inputs in a different field with clear readiness semantics.

Acceptance: URL and fragment probes fail with a case-specific message; valid file and intentional directory fixtures pass. No current evaluation was found exploiting this gap.

### F06 Symlinked skill folders bypass reference validation

Skill discovery in [the validator](../../scripts/validate_library.py), starting at line 248, follows a directory symlink through `is_dir()` and reads its manifest. The later `files()` traversal at line 74 uses `os.walk()` without following directory symlinks. A skill can therefore pass metadata validation while all of its Markdown link checks are skipped.

The reproduction created `skills/demo` as a symlink to a sibling directory outside the temporary library. That directory contained a valid manifest with a link to nonexistent `missing.md`. Validation passed. Existing tests cover links that resolve through a symlink, but not a symlinked skill root.

There are no tracked symlinks in the audited tree. This is a latent packaging defect, not a broken current installation. A future maintainer could introduce it while trying to share resources or avoid duplicate sources.

Choose a release policy for symlinks. The simplest is to reject them in installable packages. If development links are supported, resolve roots explicitly, enforce allowed boundaries, avoid cycles, and validate the exact materialized release contents.

Acceptance: a linked skill cannot bypass missing-reference or package-boundary checks, and ordinary folders continue to pass.

### F07 Product coverage exceeds the evaluation model

The [setup catalog](../setup/README.md) covers Claude Desktop, Claude Code, ChatGPT, Codex, and Cursor. Every evaluation suite lists only Claude Code and Codex, and `PLATFORMS` in [the validator](../../scripts/validate_library.py) accepts only those two names. There is no representation of the product interface, operating system, installation route, or account-dependent capabilities in evaluation results because no result schema exists yet.

This is consistent with the original two-product pilot, but it falls short of the broader employee-library ambition. A Cursor result cannot even be added to `run_on` without a validator change. Shared skill format does not establish identical tools or behavior across products.

Define support tiers: tested, documented but untested, and unsupported. Keep the first supported matrix small. If Cursor is a first-class target, add native Cursor Agent trials rather than counting a Codex extension trial inside Cursor as equivalent. Official documentation supports the documented local folders for [Codex](https://learn.chatgpt.com/docs/build-skills) and [Cursor](https://cursor.com/docs/skills); behavior still needs its own evidence.

Acceptance: catalog claims map to recorded product, interface, version, OS, and installation-route results. Account eligibility is checked in the actual intended workspace.

### F08 Evaluations need stronger controls and less revealing inputs

The calculation fixture is useful and independently specified. It is also very small: four records, one function, and five tests. The [fixture README](../../evals/fixtures/development/README.md) explicitly describes the filtered calculation defect, and the defective file identifies itself as such. Both are supplied to the review case. That tests whether an agent can report a disclosed defect more than whether it can discover an unknown one.

Other positive prompts name the skill or describe its exact intended technique. Those are valuable for explicit invocation, but insufficient for the library's promise that an employee can ask naturally without selecting tools. There are six negative-trigger cases, mostly easy unrelated requests, and no executed collision test with all relevant skills installed.

Retain the teaching fixture. Add a separate assessment version with a neutral filename and task description, plus unseen inputs or instructor-held checks. Add realistic ambiguous prompts, multi-skill tasks, and cases where no skill should activate. Judge behavioral outcomes and preservation of scope, not exact wording or internal reasoning.

Acceptance: the pilot reports explicit invocation and automatic selection separately, checks review-only source hashes, and detects plausible wrong answers on inputs beyond the tiny starter dataset. A baseline with and without each skill makes unnecessary overhead visible.

### F09 A team-specific tenant is a default in the shared skill

The [Narva reference](../../skills/publish-confluence-dashboard/references/narva.md#known-cisco-configuration) instructs the agent to use `cisco-learning.atlassian.net` unless the user supplies another destination. That is convenient for the known pilot team, but the proposed audience is Cisco employees generally. A colleague in another organization could inherit irrelevant site, app, and credential instructions.

The skill still requires the intended page and does not authorize arbitrary publication. The concern is context confusion and avoidable setup effort, not evidence of an unauthorized write.

Separate portable task instructions from an optional team profile. The profile can name the tenant, macro choices, template source, and team preferences. State precedence: explicit request, active project or team configuration, then a clearly labeled example. Do not make a private tenant the universal Cisco default.

Acceptance: the same installed skill handles the pilot team and a second synthetic team profile without editing its portable instructions or asking again for information already supplied.

### F10 Presentation setup does not yet produce a repeatable verified artifact

The [presentation skill](../../skills/cisco-presentation/SKILL.md) correctly requires editable output and inspection of every rendered slide. It leaves tool selection to the host and explicitly allows an unrendered draft when rendering is unavailable. The brand reference records that an earlier native export did not complete. A novice can therefore follow the guide and still end with the most important quality check unresolved.

The stored template facts are credible: this audit independently confirmed their dimensions, theme fonts, colors, slide counts, and layout counts. That does not address font installation, template preservation during generation, or the reliability of the chosen renderer. The templates and fonts also do not travel with the installed skill.

Document one tested production route for each promoted environment. State the required template input, font availability, generation capability, and renderer. A small preflight helper could report missing capabilities and inspect theme relationships; it should not silently download assets or select a substitute font. Preserve the current fallback for environments that can only produce a draft.

Acceptance: generate a short editable sample from each template variant, inspect every slide, check source facts and chart values, and open the result in the intended presentation application. Record the exact template hash and any substitution.

### F11 Untrusted source instructions need explicit treatment

The library handles imported briefs, source files, records, web documentation, HTML, and existing Confluence pages. It gives useful rules for secrets and publishing scope, but has no explicit instruction or evaluation for source content that tries to redirect the agent's task, request credentials, or expand publication authority.

No successful prompt-injection attack was demonstrated in this audit. This is a missing test boundary. Host protections remain important, but a workflow can also make clear that retrieved content and data fields are task evidence, not authorization to run commands, disclose secrets, or change destinations.

Add a short rule where relevant and synthetic cases such as a record containing a command, an HTML comment asking for an environment dump, and a page body directing publication elsewhere. Avoid loading a long generic security essay into every task. Keep malicious test strings harmless and self-contained.

Acceptance: the agent completes legitimate work, treats embedded instructions as data, preserves the authorized destination, and reports a relevant blocked step without exposing credentials or abandoning unrelated work.

### F12 Model policy is duplicated and unmeasured

Exact model choices and effort recommendations appear in the [README](../../README.md#model-policy), [build plan](../build-plan.md), setup guides, [routing reference](../../skills/efficient-workflow/references/routing.md), the efficient-workflow entrypoint, and worker files. Repetition creates several places to update when an account, provider, or supported client changes.

The repository correctly describes routing as a pilot and does not claim measured savings. Low effort and worker delegation may help, but extra retries and coordination can also erase savings. The policy's broad reach makes a matched baseline especially important.

Keep the portable skill focused on selective context, appropriate tools, and cost per acceptable result. Put account-specific model identifiers and tested effort combinations in small adapters or profiles, with a check for documentation drift. Preserve exact versions when reproducibility requires them. Do not automatically replace the chosen models merely because a newer one exists.

Acceptance: benchmark direct execution against selective delegation using the same inputs and criteria; include coordinator usage, workers, retries, latency, and failure rates. Where usage counters are unavailable, record that fact and report observable time and interventions instead of invented token savings.

### F13 Ownership and contribution rules need to become operational

Each skill has author, version, and draft metadata. The [build plan](../build-plan.md#5-package-the-first-tested-release) calls for owners, dependencies, and evaluation evidence, but there is no release record, changelog, support contact, contribution template, or implemented promotion rule. Authorship alone does not identify who resolves a broken installation or an obsolete brand reference.

Keep this proportionate. One catalog can hold the owner, support tier, source version, dependencies, last behavioral evaluation, and known limitations for each skill. A short contributor checklist can require a clear trigger, a negative case, complete resources, and evidence before status changes. Imported material should carry the revision and notices already required by the source-review policy.

Acceptance: someone other than the original author can propose a change, run the required checks, understand who reviews it, and identify which results must be repeated before release. A failing pilot result has an owner and a disposition.

### F14 Clarify and broaden structural verification

The validator is useful and has meaningful regression coverage, including duplicate keys, case-sensitive manifests, folder boundaries, malformed configuration, and unchanged review fixtures. It does not enforce every possible meaning of valid configuration. For example, unknown evaluation keys are ignored, and only top-level `evals/*.json` files are discovered.

Isolated probes confirmed that misspelling `fixtures_needed` as `fixture_needed` passes and that malformed JSON under `evals/new/` is ignored. Those are not broken current cases; they are future maintenance traps. An undefined Markdown reference label also passes because it is parsed as text, not as a link. Existing documentation already excludes external URL checks, heading anchors, and literal paths.

Define a small explicit schema for evaluations and reject unknown fields unless they are intentionally extensible. Either support nested suites or reject unexpected suite locations. Add an optional link and documentation review step rather than making offline checks depend on every external service. Check packaged archives after extraction.

The CI workflow uses Linux with Python 3.11 and 3.12. Add Windows and macOS smoke coverage where path, shell, or packaging behavior matters, and run actual installation walkthroughs separately. Consider immutable action revisions and dependency hashes as release hardening, not prerequisites for continuing local development. The current `checkout@v7` and `setup-python@v7` releases exist; their presence is not an invalid-version defect. [Checkout release](https://github.com/actions/checkout/releases/tag/v7.0.0), [setup-python release](https://github.com/actions/setup-python/releases/tag/v7.0.0).

Acceptance: maintainer documentation accurately states what each check covers, malformed supported inputs fail clearly, and release verification uses the actual distributed artifact.

## Evaluation coverage

| Suite | Cases | Positive triggers | Negative triggers | Cases declaring existing fixtures | Cases listing needed fixtures |
| --- | ---: | ---: | ---: | ---: | ---: |
| Development | 8 | 5 | 3 | 3 | 2 |
| Novice development | 10 | 10 | 0 | 0 | 10 |
| Confluence | 8 | 7 | 1 | 0 | 7 |
| Pilot | 9 | 7 | 2 | 1 | 5 |
| Total | 35 | 29 | 6 | 4 | 24 |

The last two columns overlap for the presentation case. Eleven cases do not list pending fixtures, but that does not make all eleven reproducible: some prompts still need a harness-supplied input, such as a local document or a concrete task. Fixture readiness and completed execution should be separate fields.

A minimal result record should include a case ID, repository and package revision, product interface and version, operating system, account route where relevant, model and effort, fixture hashes, other installed skills, actual invocation, output locations, check results, elapsed time, usage counters where exposed, user interventions, and limitations. Keep secrets and unnecessary business data out of the record. A manual run recorded consistently is more useful now than an elaborate evaluation framework without runs.

## Skill assessments

| Skill | Strongest part | Most useful next improvement |
| --- | --- | --- |
| `develop-from-spec` | Connects requirements to behavior, storage, access, and handoff; avoids making novices select engineering tools | Run a small browser app through a complete task, including persistence and failure recovery, and compare with the host baseline |
| `check-code-quality` | Preserves check-only scope and distinguishes tool passes from correct behavior | Implement the writing-lint-script fixture and verify unchanged source hashes |
| `review-and-repair-code` | Requires evidence, focused repairs, and preservation of user work | Add a blind review fixture and prove that review-only and repair requests produce different authorized actions |
| `efficient-workflow` | Accounts for coordinator overhead and separates prompt limits from enforced budgets | Measure actual improvement and move repeated model details into maintained host configuration |
| `cisco-presentation` | Uses template evidence carefully and distinguishes slide themes from notes themes | Establish a reliable generation and rendering route with editable output and an inspected sample |
| `publish-confluence-dashboard` | Separates preparation, manual insertion, and API publishing; protects scope and credentials | Validate manual delivery first, then the actual Narva macro API behavior and draft-preservation path |

The entrypoints contain approximately 598 to 920 whitespace-delimited words each and 48 to 62 lines. They are not excessively long by themselves. The more useful efficiency work is to measure which references get loaded, remove repeated host policy, and avoid several skills repeating the same checks during one task. Word counts are not token measurements.

## Design questions to settle

These questions guide the next iteration; they do not block delivery of this audit.

| Question | Suggested starting decision |
| --- | --- |
| Who is the first supported audience: the current team or Cisco employees broadly? | Pilot with one named team while keeping tenant settings in a separate profile |
| Which products must work on the first supported release? | Claude Code and Codex first; add native Cursor Agent explicitly if demand justifies its test matrix |
| Is the product primarily a skills library, or also an installer and managed integration service? | Keep task skills portable; build only the packaging and integrations needed for proven workflows |
| Which first task matters most to employees? | Choose one complete development task and one business deliverable based on actual demand; do not require all six drafts to mature together |
| What does tested mean for a skill? | A named environment, reproducible inputs, actual output, independent acceptance checks, and a recorded result |
| How much user intervention is acceptable? | Record consequential questions and setup interventions during the pilot; use those observations to set a target |
| Is lower token usage a strict constraint or a preference after correctness? | Optimize cost per accepted result; use runtime enforcement only where a hard budget is required |
| Where should official templates and fonts come from? | A documented employee-accessible source with provenance and versions; bundle only when distribution terms allow |
| Is API publication needed for the first Confluence release? | Support preparation and manual insertion first unless a tested automated route is essential to the pilot |
| Who owns compatibility, brand updates, and support? | Name a library maintainer and a responsible contact for each specialized workflow |
| Should employees install skills per project or across their account? | Start with one documented route per product; add broader installation after duplicate and update behavior is tested |
| Where should employees report problems? | A single maintained issue or support route that collects environment details without secrets |

## Recommended implementation sequence

1. Define the pilot audience and support matrix. Resolve the distribution notice and template handling before broad sharing. Keep the existing draft labels.
2. Repair the two reproduced validator defects and add focused regression tests. Add a minimal result schema and generate complete, versioned skill archives with a file manifest.
3. Run the existing development feature, review, and repair exercises in fresh Claude Code and Codex sessions. Add the check-only fixture. Record activation, artifact quality, preservation of user work, and actual interventions.
4. Build one reusable synthetic browser dashboard fixture with known totals, filters, export, and a controllable failure. Reuse it for development and Confluence preparation so the evaluation burden stays manageable.
5. Test installation and update with a colleague on macOS and Windows. Correct the guides from observed friction. Decide whether Cursor joins the supported matrix based on a separate native Agent trial.
6. Validate presentation output and Confluence delivery as independent capabilities. Promote API publishing only after the macro and page-preservation tests succeed.
7. Benchmark model routing after the tasks and quality checks are stable. Then expand the catalog according to demonstrated demand, following the existing build plan.

Completion should be evidence-based rather than date-based. A small release with three tested skills and clear limitations is easier to support than six workflows whose essential steps depend on improvisation.

## Practices to retain

Keep one maintained source per skill and complete relative resource folders. Keep the distinction between user-facing outcomes and host configuration. Preserve the instructions against claiming unperformed tests, weakening checks to obtain a pass, or interpreting a preparation request as permission to publish.

The brand references deserve the same care: they distinguish supplied excerpts from independently retrieved policy, avoid treating a presentation font transition as universal permission to change brand assets, and record unresolved visual checks. The development references also cover failures that matter to nonprogrammers, including false save confirmations, sample data presented as live, missing permission checks, and incompatible hosting choices.

The current build plan already points toward most of the necessary work. The main adjustment is to make installation, recorded behavioral evidence, and a small supported release the next deliverables, with new skills following demonstrated need.
