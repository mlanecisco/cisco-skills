# Publishing fixtures

Synthetic inputs for the [publishing cases](../../publishing-cases.json). Every person, address, number, and token here is invented. The Social Security number format value is a long-retired sample number, and the email domain uses the reserved `.invalid` top-level domain.

| Fixture | Purpose |
| --- | --- |
| `enablement-summary.xlsx` | Workbook with a visible summary and hidden content |
| `partner-update.pptx` | Three-slide deck with notes and hidden content |
| `proposal.docx` | Short proposal with review history |
| `dashboard/` | Browser-only dashboard with embedded records and a script |
| `summary-dashboard/` | Summary page that should produce no findings |

`make_fixtures.py` regenerates all of them reproducibly. Its docstring lists the libraries it needs, which are not maintainer dependencies. Run the scanner tests after regenerating.
