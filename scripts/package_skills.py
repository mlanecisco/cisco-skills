"""Build and verify complete, versioned skill ZIPs for the local pilot."""

import argparse
import hashlib
import json
import re
import shutil
import stat
import subprocess
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any
from zipfile import ZIP_DEFLATED, BadZipFile, ZipFile, ZipInfo

from scripts.validate_library import Validator, unique_json

AUTHOR = "Mark A. Lane, Ph.D."
RESOURCE_DIRS = {"references", "assets", "scripts", "agents"}
ROOT_FILES = {"SKILL.md", "LICENSE", "LICENSE.txt", "NOTICE", "NOTICE.txt"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_revision(root: Path) -> tuple[str | None, bool | None]:
    commit = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    if commit.returncode:
        return None, None
    status = subprocess.run(
        ["git", "-C", str(root), "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=False,
    )
    return commit.stdout.strip(), bool(status.stdout) if not status.returncode else None


def package_files(skill: Path) -> list[Path]:
    files = []
    for path in sorted(skill.rglob("*")):
        relative = path.relative_to(skill)
        if path.is_symlink():
            raise ValueError(f"{path}: symlinks are not allowed")
        if any(
            part.startswith(".")
            and part not in {".gitignore", ".env.example", ".env.sample"}
            or part in {"__pycache__", "node_modules", "dist", "build"}
            for part in relative.parts
        ) or path.suffix.lower() in {".pyc", ".pem", ".key", ".p12", ".pfx"}:
            raise ValueError(f"{path}: unintended package file or directory")
        if relative.parts[0] not in RESOURCE_DIRS | ROOT_FILES:
            raise ValueError(f"{path}: unsupported top-level skill resource")
        if path.is_file():
            files.append(path)
    return files


def verify_release(directory: Path) -> dict[str, Any]:
    manifest = json.loads(
        (directory / "manifest.json").read_text(encoding="utf-8"),
        object_pairs_hook=unique_json,
    )
    if (
        not isinstance(manifest, dict)
        or manifest.get("format_version") != 1
        or not manifest.get("skills")
    ):
        raise ValueError("invalid release manifest")
    expected_archives = {"manifest.json"}
    skill_names: set[str] = set()
    with tempfile.TemporaryDirectory(prefix="cisco-package-verify-") as temporary:
        stage = Path(temporary)
        (stage / "skills").mkdir()
        for entry in manifest["skills"]:
            name = entry["name"]
            archive_name = entry["archive"]
            if (
                not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)
                or Path(archive_name).name != archive_name
                or "/" in archive_name
                or "\\" in archive_name
                or archive_name in expected_archives
                or name in skill_names
            ):
                raise ValueError("invalid or duplicate archive identity")
            skill_names.add(name)
            expected_archives.add(archive_name)
            archive = directory / archive_name
            if sha256(archive) != entry["sha256"]:
                raise ValueError(f"{archive_name}: archive checksum mismatch")
            expected = {item["path"]: item["sha256"] for item in entry["files"]}
            if len(expected) != len(entry["files"]):
                raise ValueError(f"{archive_name}: duplicate manifest file")
            with ZipFile(archive) as zipped:
                members = zipped.infolist()
                names = [member.filename for member in members]
                if len(names) != len(set(names)) or set(names) != set(expected):
                    raise ValueError(f"{archive_name}: file inventory mismatch")
                for member in members:
                    path = PurePosixPath(member.filename)
                    if (
                        path.is_absolute()
                        or ".." in path.parts
                        or "\\" in member.filename
                        or ":" in member.filename
                        or not path.parts
                        or path.parts[0] != name
                        or member.is_dir()
                        or stat.S_ISLNK(member.external_attr >> 16)
                    ):
                        raise ValueError(f"{archive_name}: unsafe archive member")
                    content = zipped.read(member)
                    if hashlib.sha256(content).hexdigest() != expected[member.filename]:
                        raise ValueError(f"{archive_name}: file checksum mismatch")
                zipped.extractall(stage / "skills")
        if {path.name for path in directory.iterdir()} != expected_archives:
            raise ValueError("release directory contains unexpected files")
        validator = Validator(stage)
        errors = validator.run(evaluations=False)
        if errors:
            raise ValueError("\n".join(errors))
        for entry in manifest["skills"]:
            skill = stage / "skills" / entry["name"]
            package_files(skill)
            parsed = validator.frontmatter(skill / "SKILL.md")
            if parsed is None or any(
                parsed[0].get("metadata", {}).get(key) != entry[key]
                for key in ["version", "status"]
            ):
                raise ValueError(f"{entry['name']}: skill version or status mismatch")
    return manifest


def build_release(
    root: Path, output: Path, version: str, selected: list[str] | None = None
) -> dict[str, Any]:
    root, output = root.resolve(), output.resolve()
    if not re.fullmatch(r"[0-9][a-zA-Z0-9.-]{0,63}", version):
        raise ValueError(
            "release version must start with a digit and use "
            "letters, digits, dots, or hyphens"
        )
    if output.exists():
        raise ValueError(f"{output}: release output already exists; use a new location")
    if output == root or any(
        output.is_relative_to(root / folder)
        for folder in ["skills", "docs", "scripts", "tests", "evals", ".git"]
    ):
        raise ValueError("release output must not replace maintained sources")
    validator = Validator(root)
    errors = validator.run()
    if errors:
        raise ValueError("\n".join(errors))
    names = selected if selected is not None else sorted(validator.skill_names)
    if not names or len(names) != len(set(names)) or set(names) - validator.skill_names:
        raise ValueError("select distinct existing skill names")
    commit, dirty = source_revision(root)
    manifest: dict[str, Any] = {
        "format_version": 1,
        "author": AUTHOR,
        "release_version": version,
        "source_revision": commit,
        "source_dirty": dirty,
        "skills": [],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".skill-package-", dir=output.parent
    ) as temporary:
        stage = Path(temporary) / "release"
        stage.mkdir()
        for name in sorted(names):
            skill = root / "skills" / name
            parsed = validator.frontmatter(skill / "SKILL.md")
            assert parsed is not None
            metadata = parsed[0].get("metadata", {})
            if not metadata.get("version") or not metadata.get("status"):
                raise ValueError(
                    f"{name}: package requires version and status metadata"
                )
            archive_name = f"{name}-{version}.zip"
            inventory = []
            with ZipFile(stage / archive_name, "w", compression=ZIP_DEFLATED) as zipped:
                for path in package_files(skill):
                    member = f"{name}/{path.relative_to(skill).as_posix()}"
                    info = ZipInfo(member, date_time=(1980, 1, 1, 0, 0, 0))
                    info.create_system = 3
                    mode = 0o755 if path.stat().st_mode & stat.S_IXUSR else 0o644
                    info.external_attr = (stat.S_IFREG | mode) << 16
                    info.compress_type = ZIP_DEFLATED
                    zipped.writestr(info, path.read_bytes(), compresslevel=9)
                    inventory.append({"path": member, "sha256": sha256(path)})
            manifest["skills"].append(
                {
                    "name": name,
                    "version": metadata["version"],
                    "status": metadata["status"],
                    "archive": archive_name,
                    "sha256": sha256(stage / archive_name),
                    "files": inventory,
                }
            )
        (stage / "manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
        )
        verify_release(stage)
        shutil.move(str(stage), str(output))
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    parser.add_argument("--version")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--skill", action="append")
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    try:
        if args.verify:
            manifest = verify_release(args.verify)
        else:
            if not args.version:
                parser.error("--version is required when building")
            output = args.output or args.root / "dist" / args.version
            manifest = build_release(args.root, output, args.version, args.skill)
            print(f"Output: {output}")
    except (ValueError, OSError, KeyError, TypeError, BadZipFile) as exc:
        print(f"FAIL: {exc}")
        return 1
    print(
        f"PASS: {len(manifest['skills'])} complete skill packages; "
        "product behavior was not evaluated."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
