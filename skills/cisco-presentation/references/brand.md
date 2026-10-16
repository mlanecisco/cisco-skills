---
author: Mark A. Lane, Ph.D.
reviewed: 2026-10-15
status: Template-derived values; supplied policy excerpts; visual validation pending
---

# Cisco presentation brand reference

## Source priority

Use the current official template and applicable guidance supplied for the team, event, and audience. Record the template version and font variant. Its masters, layout geometry, theme fonts, logo placement, and footer treatments govern the presentation's design. Resolve a material conflict between applicable guidance and the template explicitly rather than guessing which rule has been superseded.

Find brand guidance and approved assets in the [Cisco Brand Exchange employee collection](https://bx.cisco.com/cisco-brand-exchange/employee). The collection requires employee sign-in through Cisco SSO. If the agent cannot access it, have the user download the template or asset files needed for the task.

The repository contains the following Cisco PowerPoint reference templates, identified as September 17, 2026 Inter variants, in `docs/reference/`:

- `Cisco_PowerPoint_Template_Light_09-17-2026_Inter.potx`
- `Cisco_PowerPoint_Template_DARK_09-17-2026_Inter.potx`

These source files are separate from the installed skill folder. Locate the actual template in the user's project or supplied files; do not assume that installing this skill installs the templates or fonts. If a template is unavailable, produce a clearly identified draft and disclose the missing template validation.

## Verified theme colors

The values below were read directly from the slide-master theme in both supplied templates. Follow theme references when generating content so light and dark variants retain their intended color behavior.

| Color | Hex | Template use |
| --- | --- | --- |
| Midnight Blue | `#07182D` | Dark base background; light base text |
| White | `#FFFFFF` | Light base background; dark base text |
| Cisco Blue | `#02C8FF` | Theme accent 1 |
| Medium Blue | `#0A60FF` | Theme accent 2 |
| Magenta | `#FF007F` | Theme accent 3; usage restrictions apply |
| Orange | `#FF9000` | Theme accent 4; usage restrictions apply |
| Light gray | `#D6D6D6` | Theme accent 5 |
| Medium gray | `#6B6B6B` | Theme accent 6 |
| Light supporting shade | `#B4B9C0` | Supporting theme color; slot differs by variant |
| Dark supporting shade | `#525E6C` | Supporting theme color; slot differs by variant |
| Visited hyperlink gray | `#C0C0C0` | Followed hyperlink color |

The templates resolve the earlier public-source discrepancy: stored Cisco Blue is `#02C8FF`, equivalent to RGB `(2, 200, 255)`. Use the actual theme value when another supplied version differs.

## Typography and layouts

The supplied templates use Inter SemiBold for the Latin heading theme and Inter for the Latin body theme. A Cisco Brand AI summary captured on October 15, 2026 reports a documented transition from CiscoSansTT to Inter. Use the selected template's theme for new presentation text; the transition does not establish that every asset-specific CiscoSansTT rule has been withdrawn. Read [typography policy and evidence](typography-policy.md) when guidance conflicts, a font variant is unclear, or an asset such as a program ID lockup has its own rules.

Resolve the theme through the slide master's relationships. Both packages also contain an older CiscoSansTT theme for notes; it is not the active slide theme. Some sample slide text has explicit overrides: CiscoSansTT on slides 32, 47, 48, and 49, and Aptos on classification labels on slides 20, 21, 24, 25, and 26. Check reused content for intended formatting instead of assuming that a theme change updates every run. Preserve approved lockups and other supplied brand assets.

Each template contains 72 sample slides and 65 layouts at 16:9, measuring 13 1/3 by 7.5 inches. Use the relevant layout's sizes and spacing rather than imposing one universal title or body size. Review speaker, date, session, and other sample placeholders. Set classification for the intended use; a sample `Cisco Confidential` label or `BRKSEC-XXXX` session ID is not a business decision.

If the required font is unavailable, report the substitution and verify its effect on wrapping and layout. For a draft without a template, use an available readable sans-serif font and identify the fallback. Preserve supplied logo proportions and placement; omit an unavailable logo rather than drawing an approximation.

## Color usage and readability

Theme membership does not authorize every use of a color. The [Cisco-hosted 2025 guidance](https://community.cisco.com/kxiwq67737/attachments/kxiwq67737/4031-docs-wireless-mobility/157/1/Webcast_WI-ISSU-oct09-2025.pdf?inline=true) restricts solid Magenta and Orange to small accents, with a 5% maximum of the visual. It prohibits their use as text or call-to-action buttons, as certain two-color gradients, and as logo components, backdrops, or nearby elements. It also prohibits pairing them solely with White or Midnight Blue. These rules come from the older public source; preserve supplied approved compositions and consult current usage guidance before inventing additional treatments.

Check contrast for each actual foreground/background pair. As a working accessibility check, target 4.5:1 for ordinary text and 3:1 for large text and meaningful non-text graphics. See [W3C text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) and [non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html).

## Validation limits

The template review inspected package XML, slide-master relationships, themes, layouts, text overrides, and embedded previews. Native PowerPoint opened both templates, but PDF export did not complete. Full visual validation of rendered slides and a generated sample remains outstanding. The private policy pages were not independently retrieved; their supplied excerpts are attributed in the typography reference.
