---
author: Mark A. Lane, Ph.D.
status: Destination selection guidance; tenant trials pending
---

# Select a publishing destination

Use a site or page URL already established in the request. Otherwise use an explicitly selected project or team profile. A profile records configuration; it does not supply credentials or authorize publication. This library defines no automatic profile discovery or activation mechanism.

For the Cisco Learning pilot, select the bundled [cisco-learning profile](../assets/team-profiles/cisco-learning.json). For another team, use its supplied site and installed macro information or a separate profile outside the installed skill. Do not copy the pilot site into unrelated projects.

Before a write, match the page URL's site with the selected site and the authenticated client's resolved site identity. Stop destination-dependent work if those inputs conflict; resolve the mismatch without silently choosing one. Reuse a destination already unambiguously supplied rather than asking again. With only a page ID, establish its site before writing.

Local preparation can proceed without a destination. Return the artifact, dependencies, macro requirements, and verification limits. Identify any destination-specific steps still needed. Terminal credential examples use a placeholder site that must be replaced with the selected destination.
