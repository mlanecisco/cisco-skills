# Enforcing the check in a repository

A skill reminds the assistant to check. A required check in the repository blocks the merge or the deployment even when nobody remembers. Use both. These steps apply to GitHub repositories with Actions enabled. For another host, adapt the same commands to its pipeline.

## Install

1. Copy [the workflow template](../assets/ci/publish-check.yml) to `.github/workflows/publish-check.yml` in the target repository.
2. Copy [the scanner](../scripts/scan_release.py) to `.github/publish-check/scan_release.py`.
3. Set the variables at the top of the workflow:
   - `SCAN_PATH`: the folder that gets published, or `.` for the whole repository.
   - `FAIL_ON`: `high` to block credentials and personal data, `medium` to also block hidden content and raw data in pages.
   - `EXPECTED_VISIBILITY`: `private`, `internal`, or `public`, as the owner intends.
4. Run the scanner locally on the same path before committing, so the first run doesn't fail on findings already there. Review each finding with the user.
5. Commit the files on a branch and open a pull request if the user asked for that, so the check runs on the host before anything merges.

The workflow uses `actions/checkout` and `actions/setup-python` at the versions shown. If the organization pins actions to commit SHAs or requires approved versions, follow that rule.

## Make it required

The workflow reports a failure; it blocks nothing until it is required. A repository administrator does that in the repository's branch protection rules or rulesets, by requiring the `scan` check to pass before merging into the main branch. Give the user these steps. Don't change repository settings unless the user explicitly asks you to and has the permission.

If the repository deploys a site, have the deployment wait for the check. In a Pages or deploy workflow, add the scan as a job and give the deploy job `needs: scan`, or deploy only from the main branch after the required check passes. A site that deploys straight from a branch can publish before any check runs.

## Accept reviewed findings

Some findings are intended: a published sample value, a public contact address, a test fixture. Record each accepted finding so that the check stays meaningful:

- Add `publish-check: allow` to the end of that line, in a comment, for a single line.
- Add an entry to `.publishcheckignore` in the scanned folder for a whole file or folder. Each line is a path pattern such as `docs/examples/*`, or a rule and a pattern such as `email-address:contacts/*`. Lines starting with `#` are comments; use one to say why.

Changes to the ignore file deserve the same review as code. Where the repository uses code owners, assign the ignore file and the workflow to the owners.

## Limits

The scanner checks the files in the scanned path at the commit being tested. It doesn't check Git history, so a credential committed and later deleted still passes. Where the organization offers GitHub secret scanning and push protection, ask an administrator to turn them on; they check pushes and history for many known credential formats. A history scanner such as gitleaks can run in the same workflow if the team approves it.

A passing check means the patterns weren't found. People still decide whether content is fit for its audience, and the repository's visibility check only compares the setting with the stated intent.

## Updating

The copied scanner doesn't update itself. When the skill's scanner changes, copy the new version, run it locally, and review new findings before merging.
