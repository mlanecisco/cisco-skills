"""Check the pre-publish scanner against seeded files and the committed fixtures."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

REPOSITORY = Path(__file__).resolve().parents[1]
SCANNER = REPOSITORY / "skills/check-before-publishing/scripts/scan_release.py"
FIXTURES = REPOSITORY / "evals/fixtures/publishing"

# Built at run time so no token-shaped literal is stored in the repository.
GITHUB_TOKEN = "gh" + "p_" + "A1b2C3d4E5f6G7h8I9j0" * 2
AWS_KEY = "AK" + "IA" + "Q3EXAMPLEKEY7Z2W"
PRIVATE_KEY = "-----BEGIN " + "RSA PRIVATE KEY-----"
CARD = "4111 1111 " + "1111 1111"


def scan(*arguments: str | Path) -> tuple[int, dict]:
    result = subprocess.run(
        [sys.executable, "-B", str(SCANNER), "--json", *map(str, arguments)],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode, json.loads(result.stdout)


def rules(data: dict) -> set[str]:
    return {finding["rule"] for finding in data["findings"]}


class PublishCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)

    def write(self, name: str, text: str) -> Path:
        path = self.base / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_secrets_are_found_and_never_printed_in_full(self) -> None:
        self.write(
            "config.py",
            f'TOKEN = "{GITHUB_TOKEN}"\nkey = "{AWS_KEY}"\n{PRIVATE_KEY}\n'
            'db = "postgres://admin:hunter22x@db.internal/app"\n'
            'password = "correct-horse-battery"\n',
        )
        code, data = scan(self.base)
        self.assertEqual(code, 1)
        self.assertTrue(
            {
                "github-token",
                "aws-access-key",
                "private-key",
                "url-credentials",
                "credential-assignment",
            }
            <= rules(data)
        )
        output = json.dumps(data)
        for secret in [GITHUB_TOKEN, AWS_KEY, "hunter22x", "correct-horse-battery"]:
            self.assertNotIn(secret, output)

    def test_placeholders_and_allowed_lines_are_not_reported(self) -> None:
        self.write(
            "settings.py",
            'password = "changeme123"\napi_key = "${API_KEY}"\n'
            'token = "<your-token-here>"\n'
            f'sample = "{GITHUB_TOKEN}"  # publish-check: allow\n',
        )
        code, data = scan(self.base)
        self.assertEqual(code, 0)
        self.assertEqual(data["findings"], [])

    def test_personal_data_needs_valid_formats(self) -> None:
        self.write(
            "people.csv",
            f"name,card,id\nA,{CARD},123-45-6789\nB,4111 1111 1111 1112,000-12-3456\n",
        )
        _, data = scan(self.base)
        found = [(f["rule"], f["location"]) for f in data["findings"]]
        self.assertIn(("card-number", "line 2"), found)
        self.assertIn(("national-id", "line 2"), found)
        self.assertNotIn(("card-number", "line 3"), found)
        self.assertNotIn(("national-id", "line 3"), found)

    def test_sensitive_file_names(self) -> None:
        self.write(".env", "DEBUG=1\n")
        self.write(".env.example", "API_KEY=\n")
        self.write("keys/server.pem", "certificate\n")
        _, data = scan(self.base)
        flagged = {f["path"] for f in data["findings"] if f["rule"] == "sensitive-file"}
        self.assertEqual(flagged, {".env", "keys/server.pem"})

    def test_ignore_file_accepts_paths_and_rule_scoped_paths(self) -> None:
        self.write("docs/sample.md", f'password = "real-looking-value"\n{AWS_KEY}\n')
        self.write("vendor/lib.js", f'token = "{GITHUB_TOKEN}"\n')
        self.write(".publishcheckignore", "vendor/*\ncredential-assignment:docs/*\n")
        _, data = scan(self.base)
        self.assertEqual(rules(data), {"aws-access-key"})

    def test_cells_are_kept_apart_in_spreadsheets(self) -> None:
        path = self.base / "book.xlsx"
        sheet = (
            "<worksheet><sheetData><row><c><is><t>someone@corp.invalid</t></is></c>"
            "<c><is><t>078-05-1120</t></is></c></row></sheetData></worksheet>"
        )
        with ZipFile(path, "w") as archive:
            archive.writestr("xl/workbook.xml", "<workbook><sheets/></workbook>")
            archive.writestr("xl/worksheets/sheet1.xml", sheet)
        _, data = scan(path)
        self.assertTrue({"email-address", "national-id"} <= rules(data))

    def test_office_fixtures_show_hidden_content(self) -> None:
        _, data = scan(
            FIXTURES / "enablement-summary.xlsx",
            FIXTURES / "partner-update.pptx",
            FIXTURES / "proposal.docx",
        )
        by_file: dict[str, set[str]] = {}
        for finding in data["findings"]:
            by_file.setdefault(finding["path"], set()).add(finding["rule"])
        self.assertTrue(
            {"hidden-sheet", "national-id", "email-address", "document-metadata"}
            <= by_file["enablement-summary.xlsx"]
        )
        self.assertTrue(
            {"speaker-notes", "hidden-slides"} <= by_file["partner-update.pptx"]
        )
        self.assertTrue({"tracked-changes", "comments"} <= by_file["proposal.docx"])
        hidden = [f for f in data["findings"] if f["rule"] == "hidden-sheet"]
        self.assertEqual(
            {(f["location"], f["severity"]) for f in hidden},
            {("sheet Roster", "medium"), ("sheet Planning", "high")},
        )

    def test_dashboard_fixture_and_clean_summary(self) -> None:
        code, data = scan(FIXTURES / "dashboard")
        self.assertEqual(code, 1)
        self.assertTrue(
            {"credential-assignment", "embedded-data", "email-address"} <= rules(data)
        )
        code, data = scan(FIXTURES / "summary-dashboard")
        self.assertEqual((code, data["findings"]), (0, []))

    def test_fail_threshold_and_missing_path(self) -> None:
        self.write(
            "page.html", "<!-- " + "a reviewer note that is long enough " * 2 + "-->"
        )
        self.assertEqual(scan(self.base)[0], 0)
        self.assertEqual(scan(self.base, "--fail-on", "low")[0], 1)
        self.assertEqual(scan(self.base / "missing")[0], 2)

    def test_scanner_writes_nothing(self) -> None:
        target = self.base / "copy"
        target.mkdir()
        for path in FIXTURES.glob("*.xlsx"):
            (target / path.name).write_bytes(path.read_bytes())
        before = {p: p.read_bytes() for p in target.rglob("*")}
        scan(target)
        self.assertEqual({p: p.read_bytes() for p in target.rglob("*")}, before)


if __name__ == "__main__":
    unittest.main()
