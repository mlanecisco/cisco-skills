---
author: Mark A. Lane, Ph.D.
date: 2026-10-16
status: Local draft packaging implemented; employee installation trials pending
---

# Packaging and updating pilot skills

Build individual ZIPs from complete skill folders. The output includes a release manifest with the source revision, working-tree state, each skill's version and status, archive checksums, and file checksums. Draft status travels with each package. Packaging verification does not promote a skill to tested status.

From the library root, using the [maintainer environment](maintaining.md):

```bash
.venv/bin/python -m scripts.package_skills --version 0.1.0-pilot.3
.venv/bin/python -m scripts.package_skills --verify dist/0.1.0-pilot.3
```

In Windows PowerShell, replace `.venv/bin/python` with `.\.venv\Scripts\python.exe`. To package selected skills, repeat `--skill`, for example `--skill develop-from-spec --skill check-code-quality`. `--output` selects another destination. The builder refuses to overwrite an existing output directory; use a new version or location for a revised candidate.

The builder validates the source, writes sorted archive members with fixed timestamps, extracts the actual archives into a temporary location, and validates those extracted skills. Verification checks archive and file hashes, complete inventories, manifest versions and statuses, configuration syntax, and local references. Symlinks and unintended package files fail validation. Checksums establish consistency with the manifest, not the identity of the person supplying it; obtain packages from the maintainer's designated location.

Each archive contains one named skill folder with `SKILL.md` directly inside it and all supporting resources. Repository PowerPoint templates, fonts, audits, evaluation inputs, and credentials are not bundled. Users obtain presentation assets through [Cisco Brand Exchange](https://bx.cisco.com/cisco-brand-exchange/employee) or supplied project files. The broader distribution location, ownership notice, and template distribution conditions remain decisions for the pilot owner before broad sharing.

## Install and identify a version

Obtain the selected ZIP and its release manifest from the maintainer. Keep the manifest with the archive. Follow the [product guide](setup/README.md): account-based products use their upload route; local products use the extracted skill folder in the documented project location.

The release version identifies the archive set. The skill's `metadata.version` in `SKILL.md` identifies its instruction version; different releases may contain the same unchanged skill version. Preserve both identities when reporting a problem. A newly copied folder is not proof that the product discovered or used it; run the guide's first-use check.

## Update, disable, remove, or roll back

For a local installation, identify its actual path and origin first. Save the existing folder and manifest outside every skill-discovery directory. Preserve local edits for review. Replace the installed folder with the complete new folder, then verify discovery and first use. Avoid keeping backup copies under another discoverable skill name.

To roll back, restore the saved complete folder to that same installation path and repeat the first-use check. To remove a local skill, remove only its installed folder. Keep the source library and project files.

For an uploaded or managed account skill, use that product's supported update, disable, or removal controls. Keep the previous ZIP so it is available for a supported rollback or re-upload. Account synchronization and plugin-managed installations need their own product route; do not edit a managed cache or install another copy to bypass an update problem.

These are pilot instructions. Colleague installation, update, and rollback walkthroughs on macOS and Windows remain pending. No public release or team-wide installation is performed by the packaging command.
