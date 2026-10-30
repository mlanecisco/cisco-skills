"""Check the pre-publish scanner against seeded files and the committed fixtures."""

import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from zipfile import ZIP_STORED, ZipFile

REPOSITORY = Path(__file__).resolve().parents[1]
SKILL = REPOSITORY / "skills/check-before-publishing"
SCANNER = SKILL / "scripts/scan_release.py"
FIXTURES = REPOSITORY / "evals/fixtures/publishing"

# Built at run time so no token-shaped literal is stored in the repository.
GITHUB_TOKEN = "gh" + "p_" + "A1b2C3d4E5f6G7h8I9j0" * 2
AWS_KEY = "AK" + "IA" + "Q3EXAMPLEKEY7Z2W"
PRIVATE_KEY = "-----BEGIN " + "RSA PRIVATE KEY-----"
CARD = "4111 1111 " + "1111 1111"
PASSWORD = "review-only-" + "N7k4P9w2"
WORD = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
SHEET = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
SLIDE = (
    'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
    'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
)


def run(*arguments: str | Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", str(SCANNER), *map(str, arguments)],
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )


def scan(*arguments: str | Path) -> tuple[int, dict]:
    result = run("--json", *arguments)
    return result.returncode, json.loads(result.stdout)


def rules(data: dict) -> set[str]:
    return {finding["rule"] for finding in data["findings"]}


class PublishCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)

    def write(self, name: str, content: str | bytes) -> Path:
        path = self.base / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")
        return path

    def archive(self, name: str, parts: dict[str, str], stored: bool = False) -> Path:
        path = self.base / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with ZipFile(path, "w", **({"compression": ZIP_STORED} if stored else {})) as z:
            for member, value in parts.items():
                z.writestr(member, value)
        return path

    def assert_secret_hidden(self, *paths: Path) -> None:
        for arguments in [("--json", *paths), paths]:
            output = run(*arguments).stdout
            for secret in [GITHUB_TOKEN, AWS_KEY, PASSWORD, "hunter22x"]:
                self.assertNotIn(secret, output)

    # Credentials --------------------------------------------------------

    def test_secrets_are_found_and_never_printed_in_full(self) -> None:
        self.write(
            "config.py",
            f'TOKEN = "{GITHUB_TOKEN}"\nkey = "{AWS_KEY}"\n{PRIVATE_KEY}\n'
            'db = "postgres://admin:hunter22x@db.internal/app"\n'
            f'password = "{PASSWORD}"\n',
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
        self.assert_secret_hidden(self.base)

    def test_free_text_findings_carry_no_source_text(self) -> None:
        self.write("page.html", f'<!-- token="{GITHUB_TOKEN}" reviewer note -->\n')
        self.archive(
            "deleted.docx",
            {
                "word/document.xml": f"<w:document {WORD}><w:body><w:p><w:del>"
                f"<w:r><w:delText>{GITHUB_TOKEN}</w:delText></w:r></w:del>"
                "</w:p></w:body></w:document>",
                "docProps/core.xml": '<cp:coreProperties xmlns:cp="urn:cp" '
                f'xmlns:dc="urn:dc"><dc:creator>{PASSWORD}</dc:creator>'
                "</cp:coreProperties>",
            },
        )
        self.write(
            "report.pdf", b"%PDF-1.4\n/Author (" + GITHUB_TOKEN.encode() + b")\n"
        )
        code, data = scan(self.base)
        self.assertEqual(code, 1)
        self.assertTrue(
            {"github-token", "tracked-changes", "document-metadata"} <= rules(data)
        )
        self.assert_secret_hidden(self.base)

    def test_common_assignment_forms(self) -> None:
        self.write("settings.yaml", f"password: {PASSWORD}\n")
        self.write("deploy.sh", f"export DB_PASSWORD={PASSWORD}\n")
        self.write(".env.local", f"API_KEY={PASSWORD}\n")
        self.write("phrase.json", json.dumps({"password": "four plain words here"}))
        self.write("prefix.json", json.dumps({"password": "myQ7v2kd9Lx3"}))
        _, data = scan(self.base)
        flagged = {
            f["path"] for f in data["findings"] if f["rule"] == "credential-assignment"
        }
        self.assertEqual(
            flagged,
            {"settings.yaml", "deploy.sh", ".env.local", "phrase.json", "prefix.json"},
        )

    def test_placeholders_references_and_descriptive_names_pass(self) -> None:
        self.write(
            "settings.py",
            'password = "changeme"\napi_key = "${API_KEY}"\n'
            'token = "<your-token-here>"\nsecret = os.environ["APP_SECRET"]\n'
            'author = "Jordan Sample"\n',
        )
        self.write(
            "oauth.json",
            json.dumps(
                {
                    "token_endpoint": "https://login.example.org/oauth2/token",
                    "password_policy": "At least twelve characters",
                    "secret_name": "production-database",
                    "credentials.json": "Credentials file",
                }
            ),
        )
        self.write("app.js", "const apiKey = process.env.API_KEY_VALUE;\n")
        code, data = scan(self.base)
        self.assertEqual((code, data["findings"]), (0, []))

    def test_allow_marker_only_as_trailing_comment(self) -> None:
        self.write("sample.py", f'TOKEN = "{GITHUB_TOKEN}"  # publish-check: allow\n')
        _, data = scan(self.base / "sample.py")
        self.assertEqual(data["findings"], [])
        for name, text in [
            (
                "data.json",
                json.dumps({"password": PASSWORD, "d": "publish-check: allow"}),
            ),
            ("rows.csv", f"{GITHUB_TOKEN},# publish-check: allow\n"),
            ("inline.py", f'TOKEN = "{GITHUB_TOKEN}"  # publish-check: allow later\n'),
        ]:
            code, _ = scan(self.write(name, text))
            self.assertEqual(code, 1, name)

    def test_long_lines_scan_quickly(self) -> None:
        self.write("bundle.js", "var a='" + "tokenpasswordx" * 20000 + "';\n")
        self.write("names.js", "a" * 300_000 + "=1;\n")
        start = time.monotonic()
        code, _ = scan(self.base)
        self.assertEqual(code, 0)
        self.assertLess(time.monotonic() - start, 10)

    # Personal data and file names --------------------------------------

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

    def test_utf16_text_is_decoded(self) -> None:
        self.write("config.json", json.dumps({"password": PASSWORD}).encode("utf-16"))
        self.write("plain.txt", f"key {AWS_KEY}\n".encode("utf-16-le"))
        _, data = scan(self.base)
        self.assertTrue({"credential-assignment", "aws-access-key"} <= rules(data))

    def test_sensitive_file_names(self) -> None:
        self.write(".env", "DEBUG=1\n")
        self.write(".env.example", "API_KEY=\n")
        self.write("keys/server.pem", "certificate\n")
        _, data = scan(self.base)
        flagged = {f["path"] for f in data["findings"] if f["rule"] == "sensitive-file"}
        self.assertEqual(flagged, {".env", "keys/server.pem"})

    # Ignore files -------------------------------------------------------

    def test_ignore_file_accepts_paths_folders_and_rules(self) -> None:
        self.write("docs/sample.md", f'password = "{PASSWORD}"\n{AWS_KEY}\n')
        self.write("vendor/lib.js", f'token = "{GITHUB_TOKEN}"\n')
        self.write("samples/deep/config.json", json.dumps({"password": PASSWORD}))
        self.write(
            ".publishcheckignore",
            "# reviewed\nvendor/*\nsamples/\ncredential-assignment:docs/*\n",
        )
        _, data = scan(self.base)
        self.assertEqual(rules(data), {"aws-access-key"})

    def test_ignore_files_stay_with_their_folder(self) -> None:
        self.write("one/.publishcheckignore", "*.json\n")
        self.write("one/sample.json", json.dumps({"password": PASSWORD}))
        self.write("two/config.json", json.dumps({"password": PASSWORD}))
        _, data = scan(self.base / "one", self.base / "two")
        self.assertEqual([f["path"] for f in data["findings"]], ["config.json"])

    def test_single_file_uses_nearest_ignore_file(self) -> None:
        self.write(".publishcheckignore", "credential-assignment:sub/config.json\n")
        path = self.write("sub/config.json", json.dumps({"password": PASSWORD}))
        self.assertEqual(scan(path)[0], 0)

    def test_unreadable_ignore_file_is_an_error(self) -> None:
        self.write(".publishcheckignore", b"\xff\xfe\x00bad")
        code, data = scan(self.base)
        self.assertEqual(code, 2)
        self.assertTrue(data["errors"])

    # Completeness and robustness --------------------------------------

    @unittest.skipIf(os.name == "nt" or os.geteuid() == 0, "needs POSIX permissions")
    def test_unreadable_folder_is_an_error(self) -> None:
        locked = self.base / "locked"
        self.write("locked/config.json", json.dumps({"password": PASSWORD}))
        locked.chmod(0)
        self.addCleanup(locked.chmod, 0o755)
        code, data = scan(self.base)
        self.assertEqual(code, 2)
        self.assertTrue(any("locked" in e for e in data["errors"]))

    def test_strict_mode_fails_incomplete_inspection(self) -> None:
        self.archive("bad.docx", {"word/document.xml": "not valid XML"})
        self.archive(
            "dtd.docx", {"word/document.xml": '<!DOCTYPE x [<!ENTITY a "b">]><x/>'}
        )
        self.write("big.txt", "A" * (10 * 1024 * 1024 + 1))
        code, data = scan(self.base)
        self.assertEqual(code, 0)
        self.assertEqual(len(data["incomplete"]), 3)
        self.assertEqual(scan(self.base, "--strict")[0], 2)

    def test_damaged_archives_are_reported_not_crashed(self) -> None:
        encrypted = self.archive("encrypted.docx", {"word/document.xml": "<x/>"}, True)
        data = bytearray(encrypted.read_bytes())
        struct.pack_into("<H", data, 6, 1)
        struct.pack_into("<H", data, data.index(b"PK\x01\x02") + 8, 1)
        encrypted.write_bytes(bytes(data))
        corrupt = self.archive("corrupt.docx", {"word/document.xml": "<x>" * 400})
        data = bytearray(corrupt.read_bytes())
        data[40:60] = b"\xff" * 20
        corrupt.write_bytes(bytes(data))
        self.write("notzip.xlsx", "plain text")
        self.write("after.py", f'TOKEN = "{GITHUB_TOKEN}"\n')
        result = run("--json", self.base)
        report = json.loads(result.stdout)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(len(report["errors"]), 3)
        self.assertIn("github-token", rules(report))
        self.assertNotIn("Traceback", result.stderr)

    def test_display_limit_does_not_hide_a_failing_finding(self) -> None:
        sheets = "".join(
            f'<sheet name="S{i}" sheetId="{i}" state="hidden"/>' for i in range(1, 22)
        )
        sheets += '<sheet name="Last" sheetId="22" state="veryHidden"/>'
        path = self.archive(
            "many.xlsx",
            {
                "xl/workbook.xml": (
                    f"<workbook {SHEET}><sheets>{sheets}</sheets></workbook>"
                )
            },
        )
        code, data = scan(path)
        self.assertEqual(code, 1)
        self.assertEqual(data["counts"]["high"], 1)
        self.assertIn("Last", {f["location"][6:] for f in data["findings"]})

    # Office representations -------------------------------------------

    def test_office_xml_is_read_by_meaning_not_spelling(self) -> None:
        self.archive(
            "hidden.docx",
            {
                "word/document.xml": f"<w:document {WORD}><w:body><w:p><w:r><w:rPr>"
                '<w:vanish w:val="1"/></w:rPr><w:t>Pricing</w:t></w:r></w:p>'
                "</w:body></w:document>"
            },
        )
        self.archive(
            "prefixed.xlsx",
            {
                "xl/workbook.xml": '<x:workbook xmlns:x="http://schemas.openxmlformats'
                '.org/spreadsheetml/2006/main"><x:sheets><x:sheet name="Plan" '
                'sheetId="1" state="veryHidden"/></x:sheets></x:workbook>'
            },
        )
        self.archive(
            "comments.xlsx",
            {
                "xl/workbook.xml": f"<workbook {SHEET}><sheets/></workbook>",
                "xl/comments/comment1.xml": f"<comments {SHEET}><commentList>"
                f'<comment ref="A1"><text><t>{GITHUB_TOKEN}</t></text></comment>'
                "</commentList></comments>",
            },
        )
        _, data = scan(self.base)
        by_file: dict[str, set[str]] = {}
        for finding in data["findings"]:
            by_file.setdefault(finding["path"], set()).add(finding["rule"])
        self.assertIn("hidden-text", by_file["hidden.docx"])
        self.assertIn("hidden-sheet", by_file["prefixed.xlsx"])
        self.assertTrue({"comments", "github-token"} <= by_file["comments.xlsx"])

    def test_cells_are_kept_apart_in_spreadsheets(self) -> None:
        sheet = (
            f"<worksheet {SHEET}><sheetData><row><c><is><t>someone@corp.invalid</t>"
            "</is></c><c><is><t>078-05-1120</t></is></c></row></sheetData></worksheet>"
        )
        path = self.archive(
            "book.xlsx",
            {
                "xl/workbook.xml": f"<workbook {SHEET}><sheets/></workbook>",
                "xl/worksheets/sheet1.xml": sheet,
            },
        )
        _, data = scan(path)
        self.assertTrue({"email-address", "national-id"} <= rules(data))

    def test_speaker_notes_are_scanned_before_counting(self) -> None:
        def notes(body: str, kind: str = "body") -> str:
            return (
                f"<p:notes {SLIDE}><p:cSld><p:spTree><p:sp><p:nvSpPr><p:nvPr>"
                f'<p:ph type="{kind}"/></p:nvPr></p:nvSpPr><p:txBody><a:p><a:r>'
                f"<a:t>{body}</a:t></a:r></a:p></p:txBody></p:sp>{{pic}}</p:spTree>"
                "</p:cSld></p:notes>"
            )

        self.archive(
            "number.pptx",
            {"ppt/notesSlides/notesSlide1.xml": notes("078-05-1120").format(pic="")},
        )
        self.archive(
            "pagenumber.pptx",
            {"ppt/notesSlides/notesSlide1.xml": notes("3", "sldNum").format(pic="")},
        )
        self.archive(
            "picture.pptx",
            {
                "ppt/notesSlides/notesSlide1.xml": notes("3", "sldNum").format(
                    pic="<p:pic/>"
                )
            },
        )
        _, data = scan(self.base)
        by_file: dict[str, set[str]] = {}
        for finding in data["findings"]:
            by_file.setdefault(finding["path"], set()).add(finding["rule"])
        self.assertEqual(by_file["number.pptx"], {"national-id", "speaker-notes"})
        self.assertNotIn("pagenumber.pptx", by_file)
        self.assertEqual(by_file["picture.pptx"], {"notes-pictures"})

    # Fixtures and installation ----------------------------------------

    def test_office_fixtures_show_hidden_content(self) -> None:
        _, data = scan(
            FIXTURES / "enablement-summary.xlsx",
            FIXTURES / "partner-update.pptx",
            FIXTURES / "proposal.docx",
        )
        by_file: dict[str, set[str]] = {}
        for finding in data["findings"]:
            by_file.setdefault(Path(finding["path"]).name, set()).add(finding["rule"])
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
        self.assertEqual(data["incomplete"], [])

    def test_dashboard_fixture_and_clean_summary(self) -> None:
        code, data = scan(FIXTURES / "dashboard")
        self.assertEqual(code, 1)
        self.assertTrue(
            {"credential-assignment", "embedded-data", "email-address"} <= rules(data)
        )
        code, data = scan(FIXTURES / "summary-dashboard")
        self.assertEqual((code, data["findings"]), (0, []))

    def test_installed_workflow_passes_its_own_scan(self) -> None:
        target = self.base / "repo/.github"
        (target / "publish-check").mkdir(parents=True)
        (target / "workflows").mkdir()
        shutil.copy(SCANNER, target / "publish-check/scan_release.py")
        shutil.copy(SKILL / "assets/ci/publish-check.yml", target / "workflows")
        code, data = scan(self.base / "repo", "--strict", "--fail-on", "low")
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
