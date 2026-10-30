# Checking exposure

Who can reach the destination matters as much as what the files contain. Check access without changing it. A request to check doesn't authorize changing visibility, sharing links, page restrictions, or hosting settings. If a setting looks wrong, report it with the steps to change it, and leave the change to the user or the administrator.

## How to check

Use the most direct evidence available, in this order:

1. The destination's own record of access, such as a repository's visibility, a page's restrictions, or a link's sharing setting, read through an approved tool or shown by the user.
2. A test as the intended viewer, and a test while signed out, such as opening the link in a private browser window. A page that loads while signed out is public.
3. The user's description, recorded as unverified.

Say which kind of evidence you have. If you can't check access at all, report that, and don't call the destination private.

## GitHub repositories and Pages sites

With the GitHub command line installed and signed in, `gh repo view OWNER/REPO --json visibility` reports `PUBLIC`, `PRIVATE`, or `INTERNAL`. Forks and mirrors can have different visibility from the original.

A GitHub Pages site is public on the internet, even when the repository is private, unless the organization uses GitHub Enterprise Cloud with private Pages turned on for that site. Check the site's access in the repository's Pages settings, or by opening it while signed out. Treat everything published to a public site as readable by anyone, including search engines and archive services.

## Confluence pages

A page inherits its space's permissions and can add its own restrictions. Check who can view the space, whether the page has view restrictions, and whether anonymous or public access is turned on for the site or space. Child pages and attachments follow the parent's restrictions unless set otherwise. An HTML macro embedding a hosted dashboard shows that dashboard to page viewers, but the dashboard's own hosting decides who else can reach it.

## Shared files and links

For OneDrive, SharePoint, Box, Webex, and similar services, check each link's setting. "Anyone with the link" can usually be opened by people outside Cisco and forwarded further. "People in the organization" and "specific people" are narrower. Check whether the link allows download or editing, and whether it expires. Files attached to email or chat can't be recalled once delivered.

## Hosted apps and dashboards

For an app on another host, find out who can open it. Check whether the host requires sign-in before serving any page, whether data endpoints check the viewer as well as the page, and whether preview or staging addresses are public too. A login screen drawn by browser code doesn't protect data that the server sends without checking.

## Reporting

Report the destination, the access you found and how you found it, whether that access matches the intended audience, and what you couldn't confirm.
