# Enforcing the check in a repository

A skill reminds the assistant to check. A required check in the repository blocks the merge or the deployment even when nobody remembers. Use both. These steps apply to GitHub repositories with Actions enabled. For another host, adapt the same commands to its pipeline.

## Install

1. Copy [the workflow template](../assets/ci/publish-check.yml) to `.github/workflows/publish-check.yml` in the target repository.
2. Copy [the scanner](../scripts/scan_release.py) to `.github/publish-check/scan_release.py`.
3. Set the variables at the top of the workflow:
   - `SCAN_PATH`: the folder that gets published, or `.` for the whole repository.
   - `FAIL_ON`: `high` blocks tokens and keys in known formats, private keys, passwords in connection URLs, sensitive files such as key stores, card numbers, national ID numbers, and very hidden sheets. `medium` also blocks other values assigned to settings named like passwords or secrets, hidden sheets, rows, and slides, speaker notes, comments, tracked changes, macros, and raw data in pages. Email addresses and document properties are `low`, so blocking them needs `low`, with reviewed exceptions for public contact addresses.
   - `EXPECTED_VISIBILITY`: `private`, `internal`, or `public`, as the owner intends.
4. Run the scanner locally on the same path before committing, so the first run doesn't fail on findings already there. Review each finding with the user.
5. Commit the files on a branch and open a pull request if the user asked for that, so the check runs on the host before anything merges.

The workflow runs the scanner with `--strict`, so a supported file it can't fully inspect, such as one that is too large or malformed, fails the check instead of passing unexamined. It also fails if GitHub doesn't report the repository's visibility. The workflow uses `actions/checkout` and `actions/setup-python` at the versions shown. If the organization pins actions to commit SHAs or requires approved versions, follow that rule.

## Make it required

The workflow reports a failure; it blocks nothing until it is required. A repository administrator does that in the repository's branch protection rules or rulesets, by requiring the `scan` check to pass before merging into the main branch. Give the user these steps. Don't change repository settings unless the user explicitly asks you to and has the permission.

If the repository deploys a site, have the deployment wait for the check. In a Pages or deploy workflow, add the scan as a job and give the deploy job `needs: scan`, or deploy only from the main branch after the required check passes. A site that deploys straight from a branch can publish before any check runs.

## Accept reviewed findings

Some findings are intended: a published sample value, a public contact address, a test fixture. Record each accepted finding so that the check stays meaningful.

Accepted findings go in `.publishcheckignore` in the scanned folder, so each exception sits in one reviewed file. The scanner has no inline marker, because text inside a file can't reliably be told apart from a real comment. Add an entry for a whole file or folder, or for one rule in it. Each line is a path pattern such as `docs/examples/*`, a folder ending in `/` such as `samples/`, or a rule and a pattern such as `email-address:contacts/*`. Paths are relative to the folder that holds the ignore file. When a single file is scanned, the nearest ignore file above it applies, searching no further than the top of its Git repository. Lines starting with `#` are comments; use one to say why.

Changes to the ignore file deserve the same review as code. Where the repository uses code owners, assign the ignore file, the workflow, and the copied scanner to them. A required check runs whatever version of these files the pull request contains, so it can't protect itself from an unreviewed change to them.

## Limits

The scanner checks the files in the scanned path at the commit being tested. It doesn't check Git history, so a credential committed and later deleted still passes. Where the organization offers GitHub secret scanning and push protection, ask an administrator to turn them on; they check pushes and history for many known credential formats. A history scanner such as gitleaks can run in the same workflow if the team approves it.

The report repeats file paths as they appear in the repository. It masks values it detected wherever they recur, and anything shaped like a known token, but it can't recognize a password that appears only in a file name. File names are already visible to anyone who can read the repository.

Credential detection uses patterns, not a parser for each language. Values that match a known token format are found wherever they appear, and they block at `high`. A value assigned to a setting named like a password, such as `password: ...`, is reported at `medium` instead, because a pattern can't reliably tell a literal from a reference to a value stored elsewhere in every format. At the default `high`, these findings appear in the report without failing the check. Some still pass unreported: a password made only of letters and digits inside a string in source code, such as `"password=Q7v2kd9Lx3"`, looks the same as a variable name, and a value written as `${...}` or `$NAME` is treated as a placeholder in every format. For broader blocking, set `FAIL_ON` to `medium`, or turn on GitHub secret scanning or an approved scanner such as gitleaks.

A passing check means the patterns weren't found. People still decide whether content is fit for its audience, and the repository's visibility check only compares the setting with the stated intent.

## Updating

The copied scanner doesn't update itself. When the skill's scanner changes, copy the new version, run it locally, and review new findings before merging.
