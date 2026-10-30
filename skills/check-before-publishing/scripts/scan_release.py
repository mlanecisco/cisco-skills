"""Scan files before they are shared or published.

Looks for credentials, personal data, and content that viewers can recover but
the author may not see: hidden sheets, speaker notes, tracked changes,
comments, document metadata, and data embedded in web pages.

Uses only the Python standard library, never writes to the scanned files, and
never prints source text except a masked form of what it matched.

Usage:
    python scan_release.py PATH [PATH ...] [--json] [--fail-on LEVEL] [--strict]

Exit status: 0 when nothing at or above --fail-on was found; 1 when something
was; 2 when a path couldn't be read or, with --strict, when a file of a
supported type couldn't be fully inspected.
"""

from __future__ import annotations

import argparse
import codecs
import fnmatch
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
import xml.parsers.expat
import zipfile
from collections.abc import Callable, Iterator
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

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
MAX_TEXT_BYTES = 10 * 1024 * 1024
MAX_MEMBER_BYTES = 20 * 1024 * 1024
MAX_ARCHIVE_BYTES = 200 * 1024 * 1024
LARGE_INLINE_BYTES = 20 * 1024
MAX_PER_RULE = 20
MAX_MEMBERS = 20_000

CONFIG_SUFFIXES = {
    ".tf",
    ".tfvars",
    ".hcl",
    ".env",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".conf",
    ".properties",
    ".sh",
    ".bash",
    ".zsh",
    "",
}
TEXT_SUFFIXES = CONFIG_SUFFIXES | {
    ".txt",
    ".md",
    ".csv",
    ".tsv",
    ".json",
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
}
REVIEW_SUFFIXES = {
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
        re.compile(r"-----BEGIN (?:[A-Z0-9]+ ){0,4}PRIVATE KEY(?: BLOCK)?-----"),
    ),
    (
        "aws-access-key",
        "AWS access key ID",
        re.compile(r"(?<![A-Za-z0-9])(?:AKIA|ASIA)[0-9A-Z]{16}(?![0-9A-Z])"),
    ),
    (
        "github-token",
        "GitHub token",
        re.compile(
            r"(?<![A-Za-z0-9])(?:gh[pousr]_[A-Za-z0-9]{36,255}|github_pat_\w{50,255})"
        ),
    ),
    (
        "slack-token",
        "Slack token",
        re.compile(r"(?<![A-Za-z0-9])xox[abposr]-[A-Za-z0-9-]{10,255}"),
    ),
    (
        "slack-webhook",
        "Slack webhook URL",
        re.compile(r"https://hooks\.slack\.com/services/[A-Za-z0-9/_-]{20,255}"),
    ),
    (
        "google-api-key",
        "Google API key",
        re.compile(r"(?<![A-Za-z0-9])AIza[0-9A-Za-z_-]{35}(?![0-9A-Za-z-])"),
    ),
    (
        "ai-api-key",
        "AI service API key",
        re.compile(r"(?<![A-Za-z0-9])sk-(?:ant-|proj-)?[A-Za-z0-9_-]{32,255}"),
    ),
    (
        "atlassian-token",
        "Atlassian API token",
        re.compile(r"(?<![A-Za-z0-9])ATATT[A-Za-z0-9_=-]{40,255}"),
    ),
    (
        "jwt",
        "Signed web token (JWT)",
        re.compile(r"\beyJ[\w-]{10,4096}\.eyJ[\w-]{10,8192}\.[\w-]{10,4096}"),
    ),
    (
        "url-credentials",
        "Password inside a connection URL",
        re.compile(
            r"(?<![A-Za-z0-9+.-])[a-z][a-z0-9+.-]{1,20}://"
            r"[^\s:/@'\"]+:[^\s@/'\"]{3,}@[^\s'\"/]+"
        ),
    ),
]
# Matches only a name and its operator, so values aren't consumed and an
# assignment nested inside another value is still found. The lookbehind
# anchors each name at the start of a token, so a bounded name can't be
# retried from every position inside a long identifier.
NAME_OPERATOR = re.compile(
    r"""(?<![A-Za-z0-9_.-])(?P<name>[A-Za-z][A-Za-z0-9_.-]{0,63})["']?[ \t]{0,8}"""
    r"""(?::=|=>|:|=)[ \t]{0,8}"""
)
BARE_VALUE = re.compile(r"[^\s\"'#;,]+")
# In code, an unquoted value counts only if it looks like a literal secret,
# such as one inside a string, rather than a variable or expression: letters,
# digits, and at least one character an identifier can't contain.
BARE_LITERAL = re.compile(
    r"(?=[^\d]*\d)(?=[^A-Za-z]*[A-Za-z])(?=[\w]*[!@%^~+=/-])[\w!@%^~+=/-]{8,}"
)
CREDENTIAL_WORDS = {
    "password",
    "passwd",
    "passphrase",
    "secret",
    "token",
    "apikey",
    "credential",
    "credentials",
    "pwd",
    "authorization",
    "bearer",
}
# Run-together names such as dbpassword or apisecret end with one of these.
CREDENTIAL_SUFFIXES = (
    "password",
    "passwd",
    "pwd",
    "secret",
    "apikey",
    "passphrase",
    "token",
)
CREDENTIAL_PAIRS = {
    ("api", "key"),
    ("access", "key"),
    ("private", "key"),
    ("secret", "key"),
    ("signing", "key"),
    ("client", "secret"),
    ("auth", "token"),
}
# A final word like these describes a setting rather than holding a secret.
DESCRIPTIVE_WORDS = {
    "endpoint",
    "url",
    "uri",
    "policy",
    "name",
    "names",
    "id",
    "type",
    "length",
    "file",
    "path",
    "header",
    "expires",
    "expiry",
    "ttl",
    "regex",
    "pattern",
    "hint",
    "label",
    "field",
    "prompt",
    "min",
    "max",
    "enabled",
    "required",
    "rotation",
    "count",
    "limit",
    "format",
    "version",
    "prefix",
    "description",
    "help",
    "placeholder",
    "title",
    "text",
    "message",
    "error",
    "reset",
    "changed",
    "updated",
    "date",
    "time",
    "age",
    "strength",
    "location",
    "store",
    "manager",
    # File names such as credentials.json name a file, not a value.
    "json",
    "yaml",
    "yml",
    "txt",
    "xml",
    "ini",
    "cfg",
    "toml",
}
PLACEHOLDER = re.compile(
    r"""(?ix)^(?:
        x{3,}|\*{3,}|\.{3,}|<[^>]*>|\$\{\{[^{}]*\}\}|\$\{[^}]*\}|(?-i:\$[A-Z_][A-Z0-9_]*)|
        \{\{[^}]*\}\}|
        \{[^}]*\}|%\([^)]*\)s|%[A-Z_]+%|
        (?:your|my|the)[-_ ]?(?:own[-_ ]?)?
            (?:password|passphrase|secret|token|api[-_ ]?key|key)(?:[-_ ]?here)?|
        (?:enter|insert|add|put)[-_ ]?(?:your[-_ ]?)?
            (?:password|secret|token|api[-_ ]?key|key)[-_ ]?here|
        change[-_ ]?me|replace[-_ ]?me|example|sample|dummy|placeholder|redacted|
        todo|tbd|none|null|nil|undefined|empty|not[-_ ]?set|
        secret|password|token|true|false
    )$"""
)
# Unquoted values in configuration files that refer to a value held elsewhere.
# Values in configuration files that refer to a value held elsewhere. Each
# form must be complete; a leading slash or "env-" alone proves nothing.
REFERENCE = re.compile(
    r"^(?:\$\{\{[^{}]*\}\}|\$\{[A-Za-z_][\w.:-]*\}|\$[A-Za-z_]\w*|\$\([^()]*\)|`[^`]*`|"
    r"%[A-Za-z_]\w*%|[*&][\w-]+|process\.env\.\w+|os\.environ(?:\.get)?[\[(].*|"
    r"(?:os\.)?getenv\(.*\)|env\(.*\)|var\.\w+|local\.\w+|data\.[\w.]+)$"
)
PLAIN_URL = re.compile(r"^https?://[^@\s]+$")
EMAIL = re.compile(
    r"(?<![A-Za-z0-9._%+-])[A-Za-z0-9._%+-]{1,64}@"
    r"[A-Za-z0-9-]{1,63}(?:\.[A-Za-z0-9-]{1,63}){0,8}\.[A-Za-z]{2,24}\b"
)
NATIONAL_ID = re.compile(r"\b(?!000|666|9\d\d)\d{3}-(?!00)\d{2}-(?!0000)\d{4}\b")
CARD = re.compile(r"\b(?:\d[ -]?){13,19}\b")
EXAMPLE_EMAIL_DOMAINS = (
    "example.com",
    "example.org",
    "example.net",
    "test.com",
    "localhost",
)
TEXT_TAGS = {"t", "delText", "instrText", "delInstrText", "text"}
# Formula source and cached values sit in one cell; keep them apart.
SEPARATED_TAGS = {"f", "v"}
LINE_TAGS = {"p", "si", "row", "tr"}
CELL_TAGS = {"c", "tc"}
BREAK_TAGS = {"tab", "br"}
NOTES_PLACEHOLDERS = {"sldNum", "sldImg", "hdr", "ftr", "dt"}
TRUE_VALUES = {"1", "true", "on"}

PartReader = Callable[[str], "ET.Element | None"]
# Part names an Office application writes; anything else could carry copied text.
SAFE_PART = re.compile(
    r"docProps/(?:core|app|custom)\.xml|"
    r"word/(?:document|styles|footnotes|endnotes|header\d+|footer\d+|"
    r"comments(?:Extended|Ids|Extensible)?)\.xml|"
    r"xl/(?:workbook|sharedStrings|comments\d+)\.xml|"
    r"xl/(?:worksheets/sheet|comments/comment|threadedComments/threadedComment)\d+\.xml|"
    r"ppt/(?:slides/slide|notesSlides/notesSlide|comments/comment)\d+\.xml|"
    r"ppt/comments/modernComment_[0-9A-Fa-f_]{1,80}\.xml"
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
    """Show enough of a match to find it again, and no more."""
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


def credential_name(name: str) -> bool:
    words = [w.lower() for w in re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+", name)]
    if not words or words[-1] in DESCRIPTIVE_WORDS:
        return False
    if any(w in CREDENTIAL_WORDS or w.endswith(CREDENTIAL_SUFFIXES) for w in words):
        return True
    return any(pair in CREDENTIAL_PAIRS for pair in zip(words, words[1:]))


def assigned_value(line: str, start: int) -> tuple[str | None, bool]:
    """Read the value after an operator, and say whether it was quoted."""
    if start >= len(line):
        return None, False
    quote = line[start]
    if quote in "\"'":
        end = line.find(quote, start + 1)
        return (line[start + 1 : end] if end != -1 else line[start + 1 :]), True
    match = BARE_VALUE.match(line, start)
    return (match[0] if match else None), False


def part_label(member: str) -> str:
    """Name an archive part only when its name can't carry copied content."""
    return member if SAFE_PART.fullmatch(member) else "a part with an unusual name"


def scrub(text: str, known: list[str]) -> str:
    """Mask detected values, and anything secret-shaped, in text the report
    repeats, such as paths and locations."""
    for value in known:
        if value in text:
            text = text.replace(value, redact(value))
    for _, _, pattern in SECRET_PATTERNS:
        text = pattern.sub(lambda m: redact(m[0]), text)
    return NATIONAL_ID.sub(lambda m: redact(m[0]), text)


class _Declaration(Exception):
    pass


def xml_problem(data: bytes) -> str | None:
    """Ask the XML parser itself, so encoding and comments can't mislead."""
    parser = xml.parsers.expat.ParserCreate()

    def refuse(*_: object) -> None:
        raise _Declaration

    parser.StartDoctypeDeclHandler = refuse
    parser.EntityDeclHandler = refuse
    try:
        parser.Parse(data, True)
    except _Declaration:
        return "declares a DTD"
    except (ValueError, LookupError):
        return "uses an encoding the parser can't read"
    except xml.parsers.expat.ExpatError:
        return "is malformed"
    return None


def decode(data: bytes) -> str | None:
    """Decode text, honoring byte-order marks; return None for binary data."""
    for bom, encoding in (
        (codecs.BOM_UTF32_LE, "utf-32"),
        (codecs.BOM_UTF32_BE, "utf-32"),
        (codecs.BOM_UTF8, "utf-8-sig"),
        (codecs.BOM_UTF16_LE, "utf-16"),
        (codecs.BOM_UTF16_BE, "utf-16"),
    ):
        if data.startswith(bom):
            return data.decode(encoding, errors="replace")
    sample = data[:4096]
    if b"\x00" not in sample:
        return data.decode("utf-8", errors="replace")
    half = max(len(sample) // 2, 1)
    if sample[1::2].count(0) > half * 0.9:
        return data.decode("utf-16-le", errors="replace")
    if sample[0::2].count(0) > half * 0.9:
        return data.decode("utf-16-be", errors="replace")
    return None


def local(tag: object) -> str:
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""


def attribute(element: ET.Element, name: str) -> str | None:
    for key, value in element.attrib.items():
        if local(key) == name:
            return value
    return None


def extract(root: ET.Element) -> str:
    """Join an Office part's text, keeping paragraphs and cells apart."""
    parts: list[str] = []
    stack: list[tuple[ET.Element, bool]] = [(root, False)]
    while stack:
        element, closing = stack.pop()
        name = local(element.tag)
        if closing:
            if name in LINE_TAGS:
                parts.append("\n")
            elif name in CELL_TAGS:
                parts.append("\t")
            continue
        if name in BREAK_TAGS:
            parts.append("\t")
        if name in TEXT_TAGS and element.text:
            parts.append(element.text)
        elif name in SEPARATED_TAGS and element.text:
            parts.append(element.text + "\t")
        stack.append((element, True))
        stack.extend((child, False) for child in reversed(list(element)))
    return "".join(parts)


def parse_ignore(text: str) -> list[tuple[str | None, str]]:
    entries: list[tuple[str | None, str]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        rule, separator, pattern = line.partition(":")
        if separator and re.fullmatch(r"[a-z][a-z-]*", rule) and pattern:
            entries.append((rule, pattern))
        else:
            entries.append((None, line))
    return entries


class Scanner:
    def __init__(self, extra_ignore: list[str]):
        self.global_ignore = parse_ignore("\n".join(extra_ignore))
        self.ignore: list[tuple[str | None, str]] = []
        self.findings: list[Finding] = []
        self.severities: list[str] = []
        self.errors: list[str] = []
        self.incomplete: list[str] = []
        self.skipped: list[str] = []
        self.truncated: dict[tuple[str, str], int] = {}
        self.scanned = 0
        self._counts: dict[tuple[str, str], int] = {}
        self._shown: dict[tuple[str, str], int] = {}
        self.detected: set[str] = set()

    # Recording -----------------------------------------------------------

    def ignored(self, rule: str | None, path: str) -> bool:
        for entry_rule, pattern in self.global_ignore + self.ignore:
            if entry_rule is not None and entry_rule != rule:
                continue
            if fnmatch.fnmatch(path, pattern) or (
                pattern.endswith("/") and path.startswith(pattern)
            ):
                return True
        return False

    def add(self, finding: Finding, value: str = "") -> None:
        if len(value.strip()) >= 6:
            self.detected.add(value.strip())
        if self.ignored(finding.rule, finding.path):
            return
        self.severities.append(finding.severity)
        key = (finding.path, finding.rule)
        count = self._counts.get(key, 0) + 1
        self._counts[key] = count
        level = SEVERITIES[finding.severity]
        if count <= MAX_PER_RULE or level > self._shown.get(key, 0):
            self.findings.append(finding)
            self._shown[key] = max(level, self._shown.get(key, 0))
        else:
            self.truncated[key] = self.truncated.get(key, 0) + 1

    # Walking -------------------------------------------------------------

    def load_ignore(self, base: Path) -> None:
        self.ignore = []
        path = base / IGNORE_FILE
        try:
            if path.is_file():
                self.ignore = parse_ignore(path.read_bytes().decode("utf-8"))
        except (OSError, UnicodeDecodeError) as exc:
            self.errors.append(f"{path}: ignore file unreadable ({type(exc).__name__})")

    def single_file(self, path: Path) -> str:
        """Use the nearest ignore file above a single file, as a folder scan would."""
        full = path.resolve()
        for base in full.parents:
            if (base / IGNORE_FILE).is_file() or (base / ".git").exists():
                break
        else:
            base = full.parent
        self.load_ignore(base)
        return full.relative_to(base).as_posix()

    def files(self, root: Path) -> Iterator[tuple[Path, str]]:
        def failed(exc: OSError) -> None:
            where = exc.filename or root
            self.errors.append(f"{where}: directory unreadable ({type(exc).__name__})")

        for directory, folders, names in os.walk(root, onerror=failed):
            folders[:] = sorted(f for f in folders if f not in SKIP_DIRS)
            for name in sorted(names):
                full = Path(directory) / name
                yield full, full.relative_to(root).as_posix()

    def scan(self, roots: list[Path]) -> None:
        for root in roots:
            try:
                exists = root.exists()
            except OSError:
                exists = False
            if not exists:
                self.errors.append(f"{root}: not found or not accessible")
                continue
            try:
                if root.is_dir():
                    self.load_ignore(root)
                    items: Iterator[tuple[Path, str]] = self.files(root)
                else:
                    items = iter([(root, self.single_file(root))])
            except OSError as exc:
                self.errors.append(f"{root}: not accessible ({type(exc).__name__})")
                continue
            for full, shown in items:
                if full.is_symlink():
                    self.skipped.append(f"{shown}: symbolic link not followed")
                    continue
                if shown == IGNORE_FILE or self.ignored(None, shown):
                    continue
                try:
                    self.scan_file(full, shown)
                except Exception as exc:  # contain any failure to this file
                    self.errors.append(
                        f"{shown}: could not inspect ({type(exc).__name__})"
                    )
            # Ignore entries apply only within the folder they came from.
            self.ignore = []

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
        elif suffix in TEXT_SUFFIXES or name.startswith(".env"):
            if full.stat().st_size > MAX_TEXT_BYTES:
                self.incomplete.append(f"{shown}: larger than {MAX_TEXT_BYTES} bytes")
                return
            text = decode(full.read_bytes())
            if text is None:
                self.incomplete.append(f"{shown}: not readable as text")
                return
            config = suffix in CONFIG_SUFFIXES or name.startswith(".env")
            self.text(text, shown, config=config)
            if suffix in {".html", ".htm"}:
                self.html(text, shown)
            if suffix == ".map" or (
                suffix in {".js", ".mjs", ".cjs", ".css"}
                and re.search(r"[#@] sourceMappingURL=", text)
            ):
                self.source_map(text, shown, suffix)
        else:
            self.skipped.append(f"{shown}: file type not inspected")

    # Rules ---------------------------------------------------------------

    def sensitive_name(self, name: str, suffix: str, shown: str) -> None:
        if name in SAFE_ENV_NAMES:
            return
        reason = SENSITIVE_NAMES.get(name) or SENSITIVE_SUFFIXES.get(suffix)
        if reason is None and name.startswith(".env."):
            reason = SENSITIVE_NAMES[".env"]
        if reason:
            self.add(Finding("high", "sensitive-file", shown, "", reason))
        elif suffix in REVIEW_SUFFIXES:
            self.add(
                Finding("medium", "sensitive-file", shown, "", REVIEW_SUFFIXES[suffix])
            )

    def text(
        self,
        text: str,
        shown: str,
        where: str = "",
        config: bool = False,
    ) -> None:
        emails: list[str] = []
        first_email = ""
        for number, line in enumerate(text.splitlines(), 1):
            location = f"{where}, line {number}" if where else f"line {number}"
            for rule, label, pattern in SECRET_PATTERNS:
                for match in pattern.finditer(line):
                    self.add(
                        Finding("high", rule, shown, location, label, redact(match[0])),
                        match[0],
                    )
            # A name inside a bare value already read is part of that value;
            # skipping it keeps overlapping candidates from rescanning the line.
            read_until = -1
            for match in NAME_OPERATOR.finditer(line):
                if match.start() < read_until or not credential_name(match["name"]):
                    continue
                value, quoted = assigned_value(line, match.end())
                if value is None or not (
                    quoted or config or BARE_LITERAL.fullmatch(value)
                ):
                    continue
                if not quoted:
                    read_until = match.end() + len(value)
                value = value.strip()
                if (
                    len(value) < 8
                    or PLACEHOLDER.match(value)
                    or PLAIN_URL.match(value)
                    or ((config or not quoted) and REFERENCE.match(value))
                    or (match["name"].lower() == "pwd" and value.startswith("/"))
                    or any(p.search(value) for _, _, p in SECRET_PATTERNS)
                ):
                    continue
                self.add(
                    Finding(
                        "high",
                        "credential-assignment",
                        shown,
                        location,
                        "Value assigned to a credential setting",
                        redact(value),
                    ),
                    value,
                )
            for match in NATIONAL_ID.finditer(line):
                self.add(
                    Finding(
                        "high",
                        "national-id",
                        shown,
                        location,
                        "Number in US Social Security number format",
                        redact(match[0]),
                    ),
                    match[0],
                )
            for match in CARD.finditer(line):
                if luhn(match[0]):
                    self.add(
                        Finding(
                            "high",
                            "card-number",
                            shown,
                            location,
                            "Number that passes the payment card checksum",
                            redact(match[0]),
                        ),
                        match[0],
                    )
            found = [
                m[0]
                for m in EMAIL.finditer(line)
                if not m[0].lower().endswith(EXAMPLE_EMAIL_DOMAINS)
            ]
            if found and not emails:
                first_email = location
            emails += found
        if emails:
            user, _, domain = emails[0].partition("@")
            self.add(
                Finding(
                    "low",
                    "email-address",
                    shown,
                    f"first at {first_email}",
                    f"{len(emails)} email address(es), {len(set(emails))} distinct; "
                    "check that viewers may see them",
                    f"{user[:2]}...@{domain}",
                )
            )

    def html(self, text: str, shown: str) -> None:
        for match in re.finditer(
            r"<script\b([^>]*)>(.*?)</script>", text, re.IGNORECASE | re.DOTALL
        ):
            attributes, body = match[1], match[2]
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
            length = len(match[1].strip())
            if length >= 40:
                line = text.count("\n", 0, match.start()) + 1
                self.add(
                    Finding(
                        "low",
                        "html-comment",
                        shown,
                        f"line {line}",
                        f"HTML comment of {length} characters that viewers can read "
                        "in the page source",
                    )
                )
        for match in re.finditer(
            r"data:[a-z]+/[a-z0-9.+-]+;base64,([A-Za-z0-9+/=]+)", text
        ):
            if len(match[1]) > 200_000:
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
            infos = archive.infolist()
            if sum(i.file_size for i in infos) > MAX_ARCHIVE_BYTES:
                self.incomplete.append(f"{shown}: unpacked size too large to inspect")
                return
            if len(infos) > MAX_MEMBERS:
                self.incomplete.append(f"{shown}: more than {MAX_MEMBERS} parts")
                return
            names = sorted(i.filename for i in infos)
            members = set(names)
            cache: dict[str, ET.Element | None] = {}

            def tree(member: str) -> ET.Element | None:
                if member in cache:
                    return cache[member]
                result: ET.Element | None = None
                label = part_label(member)
                if member in members:
                    info = archive.getinfo(member)
                    if info.file_size > MAX_MEMBER_BYTES:
                        self.incomplete.append(f"{shown}: {label} too large to inspect")
                    else:
                        data = archive.read(member)
                        # Office parts never declare a DTD; refusing one
                        # avoids entity-expansion attacks.
                        problem = xml_problem(data)
                        if problem:
                            self.incomplete.append(f"{shown}: {label} {problem}")
                        else:
                            result = ET.fromstring(data)
                cache[member] = result
                return result

            self.office_metadata(tree, shown)
            if any(n.endswith("vbaProject.bin") for n in names):
                self.add(Finding("medium", "macros", shown, "", "File contains macros"))
            embedded = [n for n in names if "/embeddings/" in n]
            if embedded:
                self.add(
                    Finding(
                        "medium",
                        "embedded-object",
                        shown,
                        "",
                        f"{len(embedded)} embedded file(s) or object(s), which can "
                        "carry their own data",
                    )
                )
            self.office_comments(names, tree, shown)
            kind = full.suffix.lower()[1:3]
            if kind == "do":
                self.word(names, tree, shown)
            elif kind == "xl":
                self.excel(names, tree, shown)
            else:
                self.powerpoint(names, tree, shown)

    def scan_part(self, tree: PartReader, member: str, shown: str) -> None:
        root = tree(member)
        if root is not None:
            self.text(extract(root), shown, part_label(member))

    def office_metadata(self, tree: PartReader, shown: str) -> None:
        stored: list[str] = []
        values: list[str] = []
        wanted = {
            "docProps/core.xml": {"creator", "lastModifiedBy"},
            "docProps/app.xml": {"Company", "Manager"},
        }
        for member, fields in wanted.items():
            root = tree(member)
            for element in root.iter() if root is not None else []:
                if local(element.tag) in fields and (element.text or "").strip():
                    stored.append(local(element.tag))
                    values.append(element.text or "")
        custom = tree("docProps/custom.xml")
        if custom is not None:
            stored.append("custom properties")
            values += [e.text for e in custom.iter() if e.text and e.text.strip()]
        if stored:
            self.add(
                Finding(
                    "low",
                    "document-metadata",
                    shown,
                    "document properties",
                    "Stored properties: " + ", ".join(dict.fromkeys(stored)),
                )
            )
            self.text("\n".join(values), shown, "document properties")

    def office_comments(self, names: list[str], tree: PartReader, shown: str) -> None:
        parts = [
            n
            for n in names
            if n.endswith(".xml")
            and "/_rels/" not in n
            and "comment" in n.rsplit("/", 1)[-1].lower()
            and "author" not in n.rsplit("/", 1)[-1].lower()
        ]
        count = 0
        for member in parts:
            root = tree(member)
            if root is None:
                continue
            count += sum(
                local(e.tag) in {"comment", "threadedComment", "cm"}
                for e in root.iter()
            )
            self.text(extract(root), shown, part_label(member))
        if count:
            self.add(Finding("medium", "comments", shown, "", f"{count} comment(s)"))

    def word(self, names: list[str], tree: PartReader, shown: str) -> None:
        document = tree("word/document.xml")
        elements = list(document.iter()) if document is not None else []
        insertions = sum(local(e.tag) == "ins" for e in elements)
        deletions = sum(local(e.tag) == "del" for e in elements)
        if insertions or deletions:
            self.add(
                Finding(
                    "medium",
                    "tracked-changes",
                    shown,
                    "document body",
                    f"{insertions} tracked insertion(s) and {deletions} deletion(s). "
                    "Deleted text stays in the file until changes are accepted or "
                    "rejected",
                )
            )
        for member, where in [
            ("word/document.xml", "document body"),
            ("word/styles.xml", "styles"),
        ]:
            root = tree(member)
            if root is not None and any(
                local(e.tag) == "vanish"
                and (attribute(e, "val") or "true").lower() in TRUE_VALUES
                for e in root.iter()
            ):
                self.add(
                    Finding("medium", "hidden-text", shown, where, "Text set as hidden")
                )
        for member in names:
            if re.fullmatch(
                r"word/(?:document|footnotes|endnotes|header\d*|footer\d*)\.xml", member
            ):
                self.scan_part(tree, member, shown)

    def excel(self, names: list[str], tree: PartReader, shown: str) -> None:
        workbook = tree("xl/workbook.xml")
        position = 0
        for element in workbook.iter() if workbook is not None else []:
            name = local(element.tag)
            if name == "sheet":
                position += 1
                state = attribute(element, "state")
                if state in {"hidden", "veryHidden"}:
                    self.add(
                        Finding(
                            "medium" if state == "hidden" else "high",
                            "hidden-sheet",
                            shown,
                            f"sheet {position} in workbook order",
                            "Hidden sheet"
                            if state == "hidden"
                            else "Very hidden sheet, which Excel's Unhide menu does "
                            "not show",
                        )
                    )
            elif name == "definedName" and (
                (attribute(element, "hidden") or "").lower() in TRUE_VALUES
            ):
                self.add(
                    Finding(
                        "low", "hidden-name", shown, "workbook", "Hidden defined names"
                    )
                )
        for member in names:
            if not re.fullmatch(r"xl/worksheets/[^/]+\.xml", member):
                continue
            sheet = tree(member)
            if sheet is None:
                continue
            rows = columns = 0
            filtered = False
            for element in sheet.iter():
                name = local(element.tag)
                hidden = (attribute(element, "hidden") or "").lower() in TRUE_VALUES
                rows += name == "row" and hidden
                columns += name == "col" and hidden
                filtered = filtered or name == "autoFilter"
            if rows or columns:
                self.add(
                    Finding(
                        "medium",
                        "hidden-cells",
                        shown,
                        part_label(member),
                        f"{rows} hidden row(s) and {columns} hidden column group(s)",
                    )
                )
            if filtered:
                self.add(
                    Finding(
                        "low",
                        "filtered-rows",
                        shown,
                        part_label(member),
                        "Filter in place; filtered-out rows are still in the file",
                    )
                )
            self.text(extract(sheet), shown, part_label(member))
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
        self.scan_part(tree, "xl/sharedStrings.xml", shown)

    def powerpoint(self, names: list[str], tree: PartReader, shown: str) -> None:
        with_text = 0
        with_pictures = 0
        for member in names:
            if not re.fullmatch(r"ppt/notesSlides/[^/]+\.xml", member):
                continue
            root = tree(member)
            if root is None:
                continue
            # Scan everything first, so a note that is only a number is still
            # checked for personal data.
            self.text(extract(root), shown, part_label(member))
            for shape in root.iter():
                if local(shape.tag) != "sp":
                    continue
                kind = next(
                    (
                        attribute(e, "type")
                        for e in shape.iter()
                        if local(e.tag) == "ph"
                    ),
                    None,
                )
                if kind not in NOTES_PLACEHOLDERS and extract(shape).strip():
                    with_text += 1
                    break
            with_pictures += any(local(e.tag) == "pic" for e in root.iter())
        if with_text:
            self.add(
                Finding(
                    "medium",
                    "speaker-notes",
                    shown,
                    "",
                    f"{with_text} slide(s) with speaker notes, which travel "
                    "with the file",
                )
            )
        if with_pictures:
            self.add(
                Finding(
                    "medium",
                    "notes-pictures",
                    shown,
                    "",
                    f"{with_pictures} notes page(s) with pictures, which text "
                    "checks can't read",
                )
            )
        hidden = []
        for member in names:
            if not re.fullmatch(r"ppt/slides/[^/]+\.xml", member):
                continue
            slide = tree(member)
            if slide is None:
                continue
            if (attribute(slide, "show") or "").lower() in {"0", "false", "off"}:
                hidden.append(part_label(member).rsplit("/", 1)[-1])
            self.text(extract(slide), shown, part_label(member))
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

    # Other formats -------------------------------------------------------

    def pdf(self, full: Path, shown: str) -> None:
        if full.stat().st_size > MAX_TEXT_BYTES * 5:
            self.incomplete.append(f"{shown}: too large to inspect")
            return
        data = full.read_bytes()
        stored: list[str] = []
        values: list[str] = []
        for key in ["Author", "Creator", "Producer", "Title", "Subject", "Keywords"]:
            found = re.search(rb"/" + key.encode() + rb"\s*\(([^)]{1,512})\)", data)
            if found:
                stored.append(key)
                values.append(found[1].decode("latin-1"))
        if stored:
            self.add(
                Finding(
                    "low",
                    "document-metadata",
                    shown,
                    "document properties",
                    "Stored properties: " + ", ".join(stored),
                )
            )
            self.text("\n".join(values), shown, "document properties")
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
            f"{shown}: PDF page text not extracted; text in compressed content and "
            "under black boxes was not checked"
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


def counts(scanner: Scanner) -> dict[str, int]:
    return {s: scanner.severities.count(s) for s in SEVERITIES}


def result(scanner: Scanner) -> dict[str, object]:
    """Collect the report, masking detected values and anything secret-shaped
    in every field."""
    known = sorted(scanner.detected, key=len, reverse=True)

    def scrub_all(text: str) -> str:
        return scrub(text, known)

    findings = sorted(
        scanner.findings,
        key=lambda f: (-SEVERITIES[f.severity], f.path, f.rule, f.location),
    )
    return {
        "scanned": scanner.scanned,
        "counts": counts(scanner),
        "findings": [
            {key: scrub_all(value) for key, value in asdict(f).items()}
            for f in findings
        ],
        "not_listed": [
            {"path": scrub_all(path), "rule": rule, "count": extra}
            for (path, rule), extra in sorted(scanner.truncated.items())
        ],
        "incomplete": [scrub_all(item) for item in scanner.incomplete],
        "skipped": [scrub_all(item) for item in scanner.skipped],
        "errors": [scrub_all(item) for item in scanner.errors],
    }


def report(data: dict[str, Any]) -> str:
    total = data["counts"]
    lines = [
        f"Scanned {data['scanned']} file(s): {total['high']} high, "
        f"{total['medium']} medium, {total['low']} low."
    ]
    for finding in data["findings"]:
        where = f" ({finding['location']})" if finding["location"] else ""
        excerpt = f" [{finding['excerpt']}]" if finding["excerpt"] else ""
        lines.append(
            f"{finding['severity'].upper():6} {finding['rule']}: {finding['path']}"
            f"{where}: {finding['message']}{excerpt}"
        )
    for item in data["not_listed"]:
        lines.append(
            f"       {item['rule']}: {item['path']}: {item['count']} more not listed"
        )
    for title, key in [
        ("Not fully inspected:", "incomplete"),
        ("Not inspected:", "skipped"),
        ("Errors:", "errors"),
    ]:
        if data[key]:
            lines.append(title)
            lines.extend(f"  {item}" for item in data[key])
    lines.append(
        "This scan checks patterns in the files given. It does not check Git "
        "history, hosting or sharing settings, or data the page loads at run time, "
        "and a clean result does not prove the files are safe to publish."
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--json", action="store_true", help="print JSON")
    parser.add_argument(
        "--fail-on",
        choices=list(SEVERITIES),
        default="high",
        help="lowest severity that makes the exit status 1 (default: high)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit 2 when a supported file couldn't be fully inspected",
    )
    parser.add_argument(
        "--ignore",
        action="append",
        default=[],
        metavar="PATTERN",
        help="path glob, or rule:path-glob, to leave out of every path (repeatable)",
    )
    args = parser.parse_args(argv)
    scanner = Scanner(args.ignore)
    scanner.scan(args.paths)
    data = result(scanner)
    print(json.dumps(data, indent=2) if args.json else report(data))
    if scanner.errors or (args.strict and scanner.incomplete):
        return 2
    threshold = SEVERITIES[args.fail_on]
    return 1 if any(SEVERITIES[s] >= threshold for s in scanner.severities) else 0


if __name__ == "__main__":
    sys.exit(main())
