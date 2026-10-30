# What to check

Each file type below lists what can travel with the file without showing on screen, what the scanner reports, what needs reading, and how to clean it. Clean a copy, never the original, and only after the user agrees.

## Severity

| Severity | Meaning | Examples |
| --- | --- | --- |
| High | Fix before sharing with anyone outside the current audience | Passwords, keys, tokens, card numbers, national ID numbers, private key files, very hidden sheets |
| Medium | Content the author probably can't see; review it for this audience | Hidden sheets, rows, and slides; speaker notes; comments; tracked changes; macros; embedded files; raw data in a web page |
| Low | Usually fine, but worth a look | Author names in document properties, email addresses, HTML comments, photo metadata |

A severity is where review starts. A medium item can be the reason not to share, and a high item can be a published test value that the user confirms is harmless.

## Word documents

Hidden content: tracked changes (deleted text stays in the file until changes are accepted or rejected), comments, text formatted as hidden, headers and footers, document properties, and embedded objects such as a pasted spreadsheet that carries its full workbook.

The scanner reports how many tracked insertions and deletions there are, without quoting them, along with comments, hidden text, properties, macros, and embedded objects. It also checks the text of the body, comments, headers, footers, and notes for secrets and personal data.

Open the document and read the deleted text, the comments, and any embedded object. To clean, accept or reject every change, delete comments, and remove properties with Office's Inspect Document. Save the result as a new file.

## Excel workbooks

Hidden content: hidden and very hidden sheets (very hidden sheets don't appear in the Unhide menu), hidden rows and columns, filtered-out rows, comments and notes, pivot caches that hold a copy of the source data, links to other workbooks with their cached values and file paths, hidden names, and document properties.

The scanner reports each of those it can see in the file structure, including comments in any workbook part whose name contains "comment", the layout Excel and common libraries use, and checks cell text for secrets and personal data. It checks formula text for credentials without running the formulas, and it doesn't read pivot cache records. Hidden sheets are identified by their position in the workbook, not by name, so that a sheet name can't carry a secret into the report.

Open each hidden sheet and look at what the hidden rows hold. To clean, delete the sheets, rows, and columns that shouldn't be shared, rather than hiding them. Refresh or remove pivot tables built on removed data, break external links, and run Inspect Document. If a pivot table must stay, check that its cache no longer holds the removed records.

## PowerPoint presentations

Hidden content: speaker notes, hidden slides, comments, slides kept off screen, document properties, and embedded charts that carry a workbook of their data.

The scanner reports notes, hidden slides, comments, properties, macros, and embedded objects, and checks slide and notes text.

Read every slide's notes and every hidden slide. Notes often say things meant only for the presenter. The scanner also reports notes pages that hold pictures, which its text checks can't read. To clean, delete hidden slides that shouldn't go and remove the notes. Inspect Document removes note text, but not pictures on notes pages, so delete those separately and check the saved copy. Check that each embedded chart's data is fit for the audience. If the user wants to keep their notes, export a copy without them for sharing.

## PDF files

Hidden content: author and tool names in properties, annotations and comments, attached files, scripts, earlier versions kept by incremental saves, and text under black boxes that was covered rather than removed.

The scanner reports properties, annotations, attachments, and scripts. It doesn't extract text, so it can't find secrets inside compressed page content or confirm a redaction.

For a redacted PDF, check that the covered text can't be selected or copied. A redaction tool that removes the text is the only safe method. Otherwise, export a new PDF from the cleaned source document.

## Images

Photos can carry the camera, the date, and the location where they were taken. The scanner reports photo metadata and flags likely location data. Screenshots can show browser tabs, notifications, file paths, and names in the background, so look at each one. To clean, export a copy without metadata and crop or redraw what shouldn't show.

## Web pages, apps, and dashboards

Everything the browser receives is readable: the page source, scripts, stylesheets, data files, source maps, and the responses from any API the page calls. Filtering, hiding a column, or checking a login in browser code changes what is shown, not what is sent.

The scanner reports inline data blocks, HTML comments, source maps, large embedded files, credentials in scripts or configuration, and personal data in any of the text files.

Open the built folder that will be published, not only the source. If you can run the page, watch its network requests and read the responses. To clean, embed summarized data at the level viewers need, move credentials and raw data behind a server that checks who is asking, remove source maps from public builds, and remove comments meant for developers.

## Code repositories

Hidden content: files the author forgot were there, such as `.env` files, keys, database files, backups, logs, and exported data. Git history keeps everything that was ever committed, including files deleted later.

The scanner checks the files currently in the folder. It doesn't read Git history. Where a history scanner the project already uses is available, such as gitleaks or trufflehog, run it in read-only mode. Otherwise, report that history wasn't checked. Treat any credential found in history as exposed, and have its owner revoke it.

## Data files

CSV, JSON, and database files often hold more columns or rows than the deliverable needs. The scanner flags database and backup files and checks text data for personal data. Compare the columns with what the audience needs, and share an extract rather than the full export.

## Files the scanner couldn't read

The scanner lists files it couldn't fully inspect, such as very large files, malformed Office parts, and text it couldn't decode. Review those by hand or report them as unchecked. Don't count them as clean.

## Other scanners

The bundled scanner is a small, dependency-free first pass. Where the project or the organization provides a dedicated tool, such as a secret scanner, a data loss prevention service, or GitHub secret scanning, use it as well and report both results. Don't install a new tool, or send files to an external service, without the user's agreement.

## Sources

Checked 2026-10-30:

- Microsoft, [Remove hidden data and personal information by inspecting documents, presentations, or workbooks](https://support.microsoft.com/en-us/office/collab-files/remove-hidden-data-and-personal-information-by-inspecting-documents-presentations-or-workbooks)
- Microsoft, [Vanish class (Open XML SDK)](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.wordprocessing.vanish?view=openxml-3.0.1)
