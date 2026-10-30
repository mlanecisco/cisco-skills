"""Scan files before they are shared or published.

Looks for credentials, personal data, and content that viewers can recover but
the author may not see: hidden sheets, speaker notes, tracked changes,
comments, document metadata, and data embedded in web pages.

Uses only the Python standard library. Never prints a full secret value.

Usage:
    python scan_release.py PATH [PATH ...] [--json] [--fail-on high|medium|low]

Exit status: 0 when nothing at or above --fail-on was found, 1 when something
was, and 2 when a path cannot be read.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import sys
import zipfile
from collections.abc import Callable, Iterable, Iterator
from dataclasses import asdict, dataclass
from pathlib import Path

SEVERITIES = {"high": 3, "medium": 2, "low": 1}
SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    ".mypy_cache",
    ".ruff_cache",
    ".pytest_cache",
}
IGNORE_FILE = ".publishcheckignore"
ALLOW_MARKER = "publish-check: allow"
MAX_TEXT_BYTES = 5 * 1024 * 1024
MAX_MEMBER_BYTES = 20 * 1024 * 1024
MAX_ARCHIVE_BYTES = 200 * 1024 * 1024
LARGE_INLINE_BYTES = 20 * 1024
MAX_PER_RULE = 20

TEXT_SUFFIXES = {
    ".txt",
    ".md",
    ".csv",
    ".tsv",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".conf",
    ".env",
    ".properties",
    ".xml",
    ".html",
    ".htm",
    ".js",
    ".mjs",
    ".cjs",
    ".ts",
    ".tsx",
    ".jsx",
    ".css",
    ".py",
    ".rb",
    ".go",
    ".java",
    ".cs",
    ".php",
    ".sh",
    ".ps1",
    ".sql",
    ".r",
    ".ipynb",
    ".svg",
    ".map",
    ".log",
}
OOXML_SUFFIXES = {
    ".docx",
    ".docm",
    ".dotx",
    ".xlsx",
    ".xlsm",
    ".xltx",
    ".pptx",
    ".pptm",
    ".potx",
}
SENSITIVE_NAMES = {
    ".env": "Environment file, which usually holds credentials",
    "id_rsa": "SSH private key",
    "id_dsa": "SSH private key",
    "id_ecdsa": "SSH private key",
    "id_ed25519": "SSH private key",
    ".npmrc": "Package registry settings, which can hold access tokens",
    ".pypirc": "Package registry settings, which can hold passwords",
    ".netrc": "Stored login credentials",
    ".htpasswd": "Web server password file",
    "credentials.json": "Credentials file",
    "service-account.json": "Cloud service account key",
}
SENSITIVE_SUFFIXES = {
    ".pem": "Certificate or private key file",
    ".key": "Private key file",
    ".p12": "Certificate bundle that can hold a private key",
    ".pfx": "Certificate bundle that can hold a private key",
    ".jks": "Java keystore",
    ".kdbx": "Password manager database",
    ".sqlite": "Database file; check whether its records are meant for viewers",
    ".sqlite3": "Database file; check whether its records are meant for viewers",
    ".db": "Database file; check whether its records are meant for viewers",
    ".bak": "Backup file, which can hold older or private content",
}
SAFE_ENV_NAMES = {".env.example", ".env.sample", ".env.template"}

SECRET_PATTERNS: list[tuple[str, str, re.Pattern[str]]] = [
    (
        "private-key",
        "Private key block",
        re.compile(r"-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY(?: BLOCK)?-----"),
    ),
    (
        "aws-access-key",
        "AWS access key ID",
        re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    ),
    (
        "github-token",
        "GitHub token",
        re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{50,})\b"),
    ),
    ("slack-token", "Slack token", re.compile(r"\bxox[abposr]-[A-Za-z0-9-]{10,}")),
    (
        "slack-webhook",
        "Slack webhook URL",
        re.compile(r"https://hooks\.slack\.com/services/[A-Za-z0-9/_-]{20,}"),
    ),
    ("google-api-key", "Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    (
        "ai-api-key",
        "AI service API key",
        re.compile(r"\bsk-(?:ant-|proj-)?[A-Za-z0-9_-]{32,}"),
    ),
    (
        "atlassian-token",
        "Atlassian API token",
        re.compile(r"\bATATT[A-Za-z0-9_=-]{40,}"),
    ),
    (
        "jwt",
        "Signed web token (JWT)",
        re.compile(
            r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"
        ),
    ),
    (
        "url-credentials",
        "Password inside a connection URL",
        re.compile(
            r"\b[a-z][a-z0-9+.-]{1,20}://[^\s:/@'\"]{1,64}:[^\s@/'\"]{3,}@[^\s'\"]+"
        ),
    ),
]
ASSIGNMENT = re.compile(
    r"""(?ix)
    (?P<name>[a-z0-9_.-]*(?:password|passwd|pwd|secret|token|api[_-]?key|apikey|
        access[_-]?key|client[_-]?secret|auth[_-]?token|authorization|bearer)[a-z0-9_.-]*)
    ["']?\s*[:=]\s*
    (?P<quote>["'])(?P<value>[^"'\s]{8,})(?P=quote)
    """
)
PLACEHOLDER = re.compile(
    r"(?i)^(?:x+|\*+|\.+|<[^>]*>|\$?\{[^}]*\}|\{\{[^}]*\}\}|%\([^)]*\)s|"
    r"(?:your|my|change|replace|example|sample|dummy|placeholder|redacted|"
    r"insert|enter|todo|none|null|undefined|test)[a-z0-9_-]*)$"
)
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
NATIONAL_ID = re.compile(r"\b(?!000|666|9\d\d)\d{3}-(?!00)\d{2}-(?!0000)\d{4}\b")
CARD = re.compile(r"\b(?:\d[ -]?){13,19}\b")
EXAMPLE_EMAIL_DOMAINS = (
    "example.com",
    "example.org",
    "example.net",
    "test.com",
    "localhost",
)


@dataclass
class Finding:
    severity: str
    rule: str
    path: str
    location: str
    message: str
    excerpt: str = ""


def redact(value: str) -> str:
    """Show enough of a secret to find it again, and no more."""
    value = value.strip()
    if len(value) <= 8:
        return "*" * len(value)
    return f"{value[:4]}...({len(value)} characters)"


def luhn(number: str) -> bool:
    digits = [int(d) for d in number if d.isdigit()]
    if not 13 <= len(digits) <= 19 or len(set(digits)) == 1:
        return False
    total = 0
    for index, digit in enumerate(reversed(digits)):
        if index % 2:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


class Scanner:
    def __init__(self, ignore: list[str]):
        self.ignore = ignore
        self.findings: list[Finding] = []
        self.errors: list[str] = []
        self.skipped: list[str] = []
        self.scanned = 0
        self._counts: dict[tuple[str, str], int] = {}

    # Recording -----------------------------------------------------------

    def ignored(self, rule: str, path: str) -> bool:
        for entry in self.ignore:
            if ":" in entry and not entry.startswith(("*", "/", ".")):
                entry_rule, _, pattern = entry.partition(":")
                if entry_rule == rule and fnmatch.fnmatch(path, pattern):
                    return True
            elif fnmatch.fnmatch(path, entry):
                return True
        return False

    def add(self, finding: Finding) -> None:
        if self.ignored(finding.rule, finding.path):
            return
        key = (finding.path, finding.rule)
        count = self._counts.get(key, 0) + 1
        self._counts[key] = count
        if count <= MAX_PER_RULE:
            self.findings.append(finding)
        elif count == MAX_PER_RULE + 1:
            self.findings.append(
                Finding(
                    finding.severity,
                    finding.rule,
                    finding.path,
                    "",
                    f"More matches for this rule in this file were not listed "
                    f"(limit {MAX_PER_RULE})",
                )
            )

    # Walking -------------------------------------------------------------

    def walk(self, paths: Iterable[Path]) -> Iterator[tuple[Path, str]]:
        for root in paths:
            if root.is_file():
                yield root, root.name
                continue
            for directory, folders, files in os.walk(root):
                folders[:] = sorted(f for f in folders if f not in SKIP_DIRS)
                for name in sorted(files):
                    full = Path(directory) / name
                    yield full, full.relative_to(root).as_posix()

    def scan(self, paths: list[Path]) -> None:
        for path in paths:
            if not path.exists():
                self.errors.append(f"{path}: not found")
        for full, shown in self.walk(p for p in paths if p.exists()):
            if full.is_symlink():
                self.skipped.append(f"{shown}: symbolic link not followed")
                continue
            if self.ignored("", shown):
                continue
            try:
                self.scan_file(full, shown)
            except (OSError, zipfile.BadZipFile, ValueError) as exc:
                self.errors.append(f"{shown}: {exc}")

    def scan_file(self, full: Path, shown: str) -> None:
        self.scanned += 1
        name = full.name.lower()
        suffix = full.suffix.lower()
        self.sensitive_name(name, suffix, shown)
        if suffix in OOXML_SUFFIXES:
            self.office(full, shown)
        elif suffix == ".pdf":
            self.pdf(full, shown)
        elif suffix in {".jpg", ".jpeg", ".tif", ".tiff", ".heic"}:
            self.image(full, shown)
        elif suffix in TEXT_SUFFIXES or name.startswith(".env") or not suffix:
            data = self.read_limited(full, shown)
            if data is None:
                return
            if b"\x00" in data[:4096]:
                self.skipped.append(f"{shown}: binary file not inspected")
                return
            text = data.decode("utf-8", errors="replace")
            self.text(text, shown)
            if suffix in {".html", ".htm"}:
                self.html(text, shown)
            if suffix == ".map" or (
                suffix in {".js", ".mjs", ".cjs", ".css"}
                and re.search(r"[#@] sourceMappingURL=", text)
            ):
                self.source_map(text, shown, suffix)
        else:
            self.skipped.append(f"{shown}: file type not inspected")

    def read_limited(self, full: Path, shown: str) -> bytes | None:
        size = full.stat().st_size
        if size > MAX_TEXT_BYTES:
            self.skipped.append(f"{shown}: larger than {MAX_TEXT_BYTES} bytes")
            return None
        return full.read_bytes()

    # Rules ---------------------------------------------------------------

    def sensitive_name(self, name: str, suffix: str, shown: str) -> None:
        if name in SAFE_ENV_NAMES:
            return
        reason = SENSITIVE_NAMES.get(name)
        if reason is None and name.startswith(".env."):
            reason = SENSITIVE_NAMES[".env"]
        if reason is None:
            reason = SENSITIVE_SUFFIXES.get(suffix)
        if reason:
            severity = (
                "medium" if suffix in {".db", ".sqlite", ".sqlite3", ".bak"} else "high"
            )
            self.add(Finding(severity, "sensitive-file", shown, "", reason))

    def text(self, text: str, shown: str, where: str = "") -> None:
        emails: list[str] = []
        first_email: str | None = None
        for number, line in enumerate(text.splitlines(), 1):
            if ALLOW_MARKER in line:
                continue
            location = f"{where}, line {number}" if where else f"line {number}"
            for rule, label, pattern in SECRET_PATTERNS:
                for match in pattern.finditer(line):
                    self.add(
                        Finding(
                            "high", rule, shown, location, label, redact(match.group(0))
                        )
                    )
            for match in ASSIGNMENT.finditer(line):
                value = match.group("value")
                if PLACEHOLDER.match(value) or any(
                    p.search(value) for _, _, p in SECRET_PATTERNS
                ):
                    continue
                self.add(
                    Finding(
                        "high",
                        "credential-assignment",
                        shown,
                        location,
                        f"Value assigned to {match.group('name')}",
                        redact(value),
                    )
                )
            for match in NATIONAL_ID.finditer(line):
                self.add(
                    Finding(
                        "high",
                        "national-id",
                        shown,
                        location,
                        "Number in US Social Security number format",
                        redact(match.group(0)),
                    )
                )
            for match in CARD.finditer(line):
                if luhn(match.group(0)):
                    self.add(
                        Finding(
                            "high",
                            "card-number",
                            shown,
                            location,
                            "Number that passes the payment card checksum",
                            redact(match.group(0)),
                        )
                    )
            emails += [
                m.group(0)
                for m in EMAIL.finditer(line)
                if not m.group(0).lower().endswith(EXAMPLE_EMAIL_DOMAINS)
            ]
            if emails and first_email is None:
                first_email = location
        if emails:
            local, _, domain = emails[0].partition("@")
            self.add(
                Finding(
                    "low",
                    "email-address",
                    shown,
                    f"first at {first_email}",
                    f"{len(emails)} email address(es), {len(set(emails))} distinct; "
                    "check that viewers may see them",
                    f"{local[:2]}...@{domain}",
                )
            )

    def html(self, text: str, shown: str) -> None:
        for match in re.finditer(
            r"<script\b([^>]*)>(.*?)</script>", text, re.IGNORECASE | re.DOTALL
        ):
            attributes, body = match.group(1), match.group(2)
            size = len(body.encode("utf-8"))
            is_data = re.search(
                r"type\s*=\s*[\"']application/(?:ld\+)?json", attributes
            )
            records = len(re.findall(r"\{[^{}]*:[^{}]*\}", body))
            if (
                size >= LARGE_INLINE_BYTES
                or (is_data and records >= 5)
                or records >= 50
            ):
                line = text.count("\n", 0, match.start()) + 1
                self.add(
                    Finding(
                        "medium",
                        "embedded-data",
                        shown,
                        f"line {line}",
                        f"Inline script with {size} bytes and about {records} records. "
                        "Anyone who opens the page can read all of it, whatever the "
                        "filters show",
                    )
                )
        for match in re.finditer(r"<!--(.*?)-->", text, re.DOTALL):
            body = match.group(1).strip()
            if len(body) >= 40:
                line = text.count("\n", 0, match.start()) + 1
                self.add(
                    Finding(
                        "low",
                        "html-comment",
                        shown,
                        f"line {line}",
                        "HTML comment that viewers can read in the page source",
                        body[:60].replace("\n", " "),
                    )
                )
        for match in re.finditer(
            r"data:[a-z]+/[a-z0-9.+-]+;base64,([A-Za-z0-9+/=]+)", text
        ):
            if len(match.group(1)) > 200_000:
                line = text.count("\n", 0, match.start()) + 1
                self.add(
                    Finding(
                        "low",
                        "embedded-file",
                        shown,
                        f"line {line}",
                        "Large embedded file in the page; check what it contains",
                    )
                )

    def source_map(self, text: str, shown: str, suffix: str) -> None:
        if suffix == ".map" and '"sourcesContent"' in text:
            message = "Source map that includes the original source code"
        elif suffix != ".map":
            message = "Reference to a source map, which can expose the original source"
        else:
            return
        self.add(Finding("medium", "source-map", shown, "", message))

    # Office files --------------------------------------------------------

    def office(self, full: Path, shown: str) -> None:
        with zipfile.ZipFile(full) as archive:
            members = archive.infolist()
            total = sum(m.file_size for m in members)
            if total > MAX_ARCHIVE_BYTES:
                self.skipped.append(f"{shown}: unpacked size too large to inspect")
                return
            names = {m.filename for m in members}

            def read(member: str) -> str:
                info = archive.getinfo(member)
                if info.file_size > MAX_MEMBER_BYTES:
                    self.skipped.append(f"{shown}: {member} too large to inspect")
                    return ""
                return archive.read(member).decode("utf-8", errors="replace")

            self.office_metadata(names, read, shown)
            if any(n.endswith("vbaProject.bin") for n in names):
                self.add(Finding("medium", "macros", shown, "", "File contains macros"))
            embedded = sorted(n for n in names if "/embeddings/" in n)
            if embedded:
                self.add(
                    Finding(
                        "medium",
                        "embedded-object",
                        shown,
                        "",
                        f"{len(embedded)} embedded file(s) or object(s), which can "
                        "carry their own data",
                        embedded[0],
                    )
                )
            kind = full.suffix.lower()[1:3]
            if kind == "do":
                self.word(names, read, shown)
            elif kind == "xl":
                self.excel(names, read, shown)
            elif kind in {"pp", "po"}:
                self.powerpoint(names, read, shown)

    def office_metadata(
        self, names: set[str], read: Callable[[str], str], shown: str
    ) -> None:
        values = []
        if "docProps/core.xml" in names:
            core = read("docProps/core.xml")
            for tag in ["creator", "lastModifiedBy"]:
                found = re.search(rf"<(?:\w+:)?{tag}>([^<]+)<", core)
                if found:
                    values.append(f"{tag}={found.group(1).strip()}")
        if "docProps/app.xml" in names:
            app = read("docProps/app.xml")
            for tag in ["Company", "Manager"]:
                found = re.search(rf"<{tag}>([^<]+)<", app)
                if found:
                    values.append(f"{tag}={found.group(1).strip()}")
        if "docProps/custom.xml" in names:
            values.append("custom properties present")
        if values:
            self.add(
                Finding(
                    "low",
                    "document-metadata",
                    shown,
                    "document properties",
                    "Names or properties stored in the file",
                    "; ".join(values)[:120],
                )
            )

    def xml_text(self, xml: str) -> str:
        # Keep cells, paragraphs, and line breaks apart so values don't run
        # together, without splitting text that Word stores in several runs.
        xml = re.sub(r"</(?:\w+:)?(?:p|si|row|tr)>", "\n", xml)
        xml = re.sub(r"</c>|<(?:\w+:)?(?:br|tab)\b[^>]*/>", "\t", xml)
        return re.sub(r"<[^>]+>", "", xml)

    def word(self, names: set[str], read: Callable[[str], str], shown: str) -> None:
        document = read("word/document.xml") if "word/document.xml" in names else ""
        insertions = len(re.findall(r"<w:ins\b", document))
        deletions = len(re.findall(r"<w:del\b", document))
        if insertions or deletions:
            deleted = " ".join(re.findall(r"<w:delText[^>]*>([^<]*)<", document))
            self.add(
                Finding(
                    "medium",
                    "tracked-changes",
                    shown,
                    "document body",
                    f"{insertions} tracked insertion(s) and {deletions} deletion(s). "
                    "Deleted text stays readable until changes are accepted or "
                    "rejected",
                    deleted[:80],
                )
            )
        if re.search(r"<w:vanish\s*/?>", document):
            self.add(
                Finding(
                    "medium",
                    "hidden-text",
                    shown,
                    "document body",
                    "Text formatted as hidden",
                )
            )
        comments = [n for n in names if re.fullmatch(r"word/comments\w*\.xml", n)]
        count = sum(len(re.findall(r"<w:comment\b", read(n))) for n in comments)
        if count:
            self.add(Finding("medium", "comments", shown, "", f"{count} comment(s)"))
        for member in sorted(names):
            if re.fullmatch(
                r"word/(?:document|comments\w*|footnotes|endnotes|header\d*|footer\d*)\.xml",
                member,
            ):
                self.text(self.xml_text(read(member)), shown, member)

    def excel(self, names: set[str], read: Callable[[str], str], shown: str) -> None:
        workbook = read("xl/workbook.xml") if "xl/workbook.xml" in names else ""
        for match in re.finditer(r"<sheet\b[^>]*>", workbook):
            tag = match.group(0)
            state = re.search(r'state="(hidden|veryHidden)"', tag)
            if state:
                title = re.search(r'name="([^"]*)"', tag)
                self.add(
                    Finding(
                        "medium" if state.group(1) == "hidden" else "high",
                        "hidden-sheet",
                        shown,
                        f"sheet {title.group(1) if title else '?'}",
                        "Hidden sheet"
                        if state.group(1) == "hidden"
                        else "Very hidden sheet, which Excel's Unhide menu does "
                        "not show",
                    )
                )
        if re.search(r"<definedName\b[^>]*hidden=\"(?:1|true)\"", workbook):
            self.add(
                Finding("low", "hidden-name", shown, "workbook", "Hidden defined names")
            )
        for member in sorted(
            n for n in names if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", n)
        ):
            sheet = read(member)
            rows = len(re.findall(r"<row\b[^>]*hidden=\"(?:1|true)\"", sheet))
            columns = len(re.findall(r"<col\b[^>]*hidden=\"(?:1|true)\"", sheet))
            if rows or columns:
                self.add(
                    Finding(
                        "medium",
                        "hidden-cells",
                        shown,
                        member,
                        f"{rows} hidden row(s) and {columns} hidden column group(s)",
                    )
                )
            if "<autoFilter" in sheet:
                self.add(
                    Finding(
                        "low",
                        "filtered-rows",
                        shown,
                        member,
                        "Filter in place; filtered-out rows are still in the file",
                    )
                )
            self.text(self.xml_text(sheet), shown, member)
        comments = [
            n
            for n in names
            if re.fullmatch(r"xl/(?:comments\d*|threadedComments/\w+)\.xml", n)
        ]
        if comments:
            self.add(
                Finding(
                    "medium", "comments", shown, "", f"{len(comments)} comment part(s)"
                )
            )
        if any(n.startswith("xl/externalLinks/") for n in names):
            self.add(
                Finding(
                    "medium",
                    "external-links",
                    shown,
                    "",
                    "Links to other workbooks, which can reveal file paths and "
                    "cached values",
                )
            )
        if any(n.startswith("xl/pivotCache/") for n in names):
            self.add(
                Finding(
                    "medium",
                    "pivot-cache",
                    shown,
                    "",
                    "Pivot table cache, which keeps a copy of the source data",
                )
            )
        for member in ["xl/sharedStrings.xml"] + comments:
            if member in names:
                self.text(self.xml_text(read(member)), shown, member)

    def powerpoint(
        self, names: set[str], read: Callable[[str], str], shown: str
    ) -> None:
        notes = sorted(
            n for n in names if re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml", n)
        )
        with_text = []
        for member in notes:
            body = self.xml_text(read(member))
            words = re.sub(r"\s+", " ", body).strip()
            # Notes pages often hold only a slide number placeholder.
            if len(re.sub(r"[\d\s]", "", words)) >= 3:
                with_text.append(member)
                self.text(body, shown, member)
        if with_text:
            self.add(
                Finding(
                    "medium",
                    "speaker-notes",
                    shown,
                    "",
                    f"{len(with_text)} slide(s) with speaker notes, which travel "
                    "with the file",
                )
            )
        slides = sorted(
            n for n in names if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)
        )
        hidden = []
        for member in slides:
            slide = read(member)
            if re.search(r"<p:sld\b[^>]*\bshow=\"(?:0|false)\"", slide):
                hidden.append(member.rsplit("/", 1)[1])
            self.text(self.xml_text(slide), shown, member)
        if hidden:
            self.add(
                Finding(
                    "medium",
                    "hidden-slides",
                    shown,
                    ", ".join(hidden),
                    f"{len(hidden)} hidden slide(s), which are still in the file",
                )
            )
        comments = [
            n
            for n in names
            if re.fullmatch(r"ppt/(?:comments/\w+|comments\d*)\.xml", n)
        ]
        if comments:
            self.add(
                Finding(
                    "medium", "comments", shown, "", f"{len(comments)} comment part(s)"
                )
            )
            for member in comments:
                self.text(self.xml_text(read(member)), shown, member)

    # Other formats -------------------------------------------------------

    def pdf(self, full: Path, shown: str) -> None:
        data = self.read_limited(full, shown)
        if data is None:
            return
        values = []
        for key in [b"Author", b"Creator", b"Producer"]:
            found = re.search(rb"/" + key + rb"\s*\(([^)]{1,80})\)", data)
            if found:
                values.append(f"{key.decode()}={found.group(1).decode('latin-1')}")
        if values:
            self.add(
                Finding(
                    "low",
                    "document-metadata",
                    shown,
                    "document properties",
                    "Names or tools stored in the PDF",
                    "; ".join(values)[:120],
                )
            )
        if b"/Annot" in data:
            self.add(
                Finding(
                    "low",
                    "annotations",
                    shown,
                    "",
                    "Annotations or comments may be present",
                )
            )
        if b"/EmbeddedFile" in data:
            self.add(
                Finding(
                    "medium",
                    "embedded-object",
                    shown,
                    "",
                    "Attached files inside the PDF",
                )
            )
        if b"/JavaScript" in data or b"/JS" in data:
            self.add(Finding("medium", "macros", shown, "", "PDF contains scripts"))
        self.skipped.append(
            f"{shown}: PDF text was not extracted; compressed text and redaction "
            "under black boxes were not checked"
        )

    def image(self, full: Path, shown: str) -> None:
        with full.open("rb") as handle:
            head = handle.read(256 * 1024)
        if b"Exif" in head:
            gps = b"GPS" in head or b"\x88\x25" in head or b"\x25\x88" in head
            self.add(
                Finding(
                    "medium" if gps else "low",
                    "image-metadata",
                    shown,
                    "",
                    "Photo metadata that may include location"
                    if gps
                    else "Photo metadata such as camera and date",
                )
            )


def load_ignore(paths: list[Path], extra: list[str]) -> list[str]:
    entries = list(extra)
    for path in paths:
        base = path if path.is_dir() else path.parent
        ignore = base / IGNORE_FILE
        if ignore.is_file():
            for line in ignore.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    entries.append(line)
    return entries


def report(scanner: Scanner, fail_on: str) -> str:
    lines = []
    order = sorted(
        scanner.findings,
        key=lambda f: (-SEVERITIES[f.severity], f.path, f.rule, f.location),
    )
    counts = {s: sum(f.severity == s for f in order) for s in SEVERITIES}
    lines.append(
        f"Scanned {scanner.scanned} file(s): {counts['high']} high, "
        f"{counts['medium']} medium, {counts['low']} low."
    )
    for finding in order:
        where = f" ({finding.location})" if finding.location else ""
        excerpt = f" [{finding.excerpt}]" if finding.excerpt else ""
        lines.append(
            f"{finding.severity.upper():6} {finding.rule}: {finding.path}{where}: "
            f"{finding.message}{excerpt}"
        )
    if scanner.skipped:
        lines.append("Not inspected:")
        lines.extend(f"  {item}" for item in scanner.skipped)
    if scanner.errors:
        lines.append("Errors:")
        lines.extend(f"  {item}" for item in scanner.errors)
    lines.append(
        "This scan checks patterns in the files given. It does not check Git "
        "history, hosting or sharing settings, or data the page loads at run time, "
        "and a clean result does not prove the files are safe to publish."
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--json", action="store_true", help="print JSON")
    parser.add_argument(
        "--fail-on",
        choices=list(SEVERITIES),
        default="high",
        help="lowest severity that makes the exit status 1 (default: high)",
    )
    parser.add_argument(
        "--ignore",
        action="append",
        default=[],
        metavar="PATTERN",
        help="path glob, or rule:path-glob, to leave out (repeatable)",
    )
    args = parser.parse_args(argv)
    scanner = Scanner(load_ignore(args.paths, args.ignore))
    scanner.scan(args.paths)
    if args.json:
        print(
            json.dumps(
                {
                    "scanned": scanner.scanned,
                    "findings": [asdict(f) for f in scanner.findings],
                    "skipped": scanner.skipped,
                    "errors": scanner.errors,
                },
                indent=2,
            )
        )
    else:
        print(report(scanner, args.fail_on))
    if scanner.errors:
        return 2
    threshold = SEVERITIES[args.fail_on]
    return (
        1 if any(SEVERITIES[f.severity] >= threshold for f in scanner.findings) else 0
    )


if __name__ == "__main__":
    sys.exit(main())
