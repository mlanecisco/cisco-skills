"""Validate maintained skills, references, configurations, and eval definitions."""

import argparse
import json
import os
import re
import sys
import tomllib
from collections.abc import Iterable
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

import yaml
from markdown_it import MarkdownIt

SKILL_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
IGNORED = {
    ".git",
    ".venv",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    "__pycache__",
    "output",
    "tmp",
}
PLATFORMS = {"Claude Code", "Codex"}


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate mapping keys rather than silently replacing values."""

    def construct_mapping(
        self, node: yaml.MappingNode, deep: bool = False
    ) -> dict[Any, Any]:
        seen = set()
        for key_node, _ in node.value:
            if key_node.tag == "tag:yaml.org,2002:merge":
                continue
            key = self.construct_object(key_node, deep=deep)
            if key in seen:
                raise ValueError(f"duplicate YAML key: {key!r}")
            seen.add(key)
        return super().construct_mapping(node, deep=deep)


def unique_json(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


class Validator:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.errors: list[str] = []
        self.skill_names: set[str] = set()
        self.case_ids: set[str] = set()

    def error(self, path: Path, message: str) -> None:
        self.errors.append(f"{path.relative_to(self.root)}: {message}")

    def files(self, suffixes: set[str]) -> Iterable[Path]:
        for directory, folders, filenames in os.walk(self.root):
            folders[:] = sorted(name for name in folders if name not in IGNORED)
            for name in sorted(filenames):
                path = Path(directory) / name
                if path.is_file() and path.suffix.lower() in suffixes:
                    yield path

    def yaml(self, path: Path, text: str) -> Any:
        try:
            return yaml.load(text, Loader=UniqueLoader)
        except (yaml.YAMLError, ValueError, TypeError) as exc:
            self.error(path, f"invalid YAML: {exc}")
            return None

    def frontmatter(self, path: Path) -> tuple[dict[str, Any], str] | None:
        lines = path.read_text(encoding="utf-8").splitlines()
        if not lines or lines[0] != "---" or "---" not in lines[1:]:
            self.error(path, "expected YAML frontmatter enclosed by --- lines")
            return None
        end = lines.index("---", 1)
        data = self.yaml(path, "\n".join(lines[1:end]))
        if not isinstance(data, dict):
            self.error(path, "frontmatter must be a mapping")
            return None
        return data, "\n".join(lines[end + 1 :])

    def string(
        self, path: Path, data: dict[str, Any], key: str, limit: int = 0
    ) -> bool:
        value = data.get(key)
        if not isinstance(value, str) or not value.strip():
            self.error(path, f"{key} must be a non-empty string")
            return False
        if limit and len(value) > limit:
            self.error(path, f"{key} exceeds {limit} characters")
            return False
        return True

    def skill(self, path: Path) -> None:
        parsed = self.frontmatter(path)
        if parsed is None:
            return
        data, body = parsed
        for key in data.keys() - SKILL_FIELDS:
            self.error(path, f"unsupported portable skill field: {key!r}")
        if self.string(path, data, "name", 64):
            name = data["name"]
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
                self.error(path, "name must use lowercase letters, digits, and hyphens")
            if name != path.parent.name:
                self.error(path, "name must match the skill folder")
            if name in self.skill_names:
                self.error(path, f"duplicate skill name: {name}")
            self.skill_names.add(name)
        self.string(path, data, "description", 1024)
        for key, limit in [
            ("license", 0),
            ("compatibility", 500),
            ("allowed-tools", 0),
        ]:
            if key in data:
                self.string(path, data, key, limit)
        if "metadata" in data:
            metadata = data["metadata"]
            if not isinstance(metadata, dict) or any(
                not isinstance(k, str) or not isinstance(v, str)
                for k, v in metadata.items()
            ):
                self.error(path, "metadata must map strings to strings")
        if not body.strip():
            self.error(path, "skill instructions are empty")

    def local_target(self, path: Path, target: str) -> None:
        link = urlsplit(target)
        if link.scheme or link.netloc or not link.path:
            return
        destination = (path.parent / unquote(link.path)).resolve()
        if not destination.is_relative_to(self.root):
            self.error(path, f"local reference leaves the repository: {target}")
        elif not destination.exists():
            self.error(path, f"missing local reference: {target}")
        elif path.name == "SKILL.md" and not destination.is_relative_to(path.parent):
            self.error(path, f"skill reference leaves its installable folder: {target}")

    def markdown(self, path: Path) -> None:
        text = path.read_text(encoding="utf-8")
        parsed = self.frontmatter(path) if text.startswith("---\n") else None
        body = parsed[1] if parsed is not None else text
        for token in MarkdownIt().parse(body):
            for child in token.children or []:
                attribute = {"link_open": "href", "image": "src"}.get(child.type)
                if attribute:
                    target = child.attrGet(attribute)
                    if isinstance(target, str):
                        self.local_target(path, target)

    def agent(self, path: Path, data: dict[str, Any], codex: bool = False) -> None:
        fields = ["name", "description", "developer_instructions" if codex else "model"]
        for key in fields:
            self.string(path, data, key)
        for key in ["model", "effort", "model_reasoning_effort"]:
            if key in data and key not in fields:
                self.string(path, data, key)
        if "maxTurns" in data and (
            type(data["maxTurns"]) is not int or data["maxTurns"] < 1
        ):
            self.error(path, "maxTurns must be a positive integer")

    def evaluation(self, path: Path) -> None:
        try:
            data = json.loads(
                path.read_text(encoding="utf-8"), object_pairs_hook=unique_json
            )
        except (ValueError, OSError) as exc:
            self.error(path, f"invalid evaluation JSON: {exc}")
            return
        if not isinstance(data, dict):
            self.error(path, "evaluation must be an object")
            return
        for key in ["author", "status"]:
            self.string(path, data, key)
        platforms = data.get("run_on")
        if (
            not isinstance(platforms, list)
            or not platforms
            or any(not isinstance(p, str) or p not in PLATFORMS for p in platforms)
        ):
            self.error(path, "run_on must list Claude Code and/or Codex")
        cases = data.get("cases")
        if not isinstance(cases, list) or not cases:
            self.error(path, "cases must be a non-empty list")
            return
        for index, case in enumerate(cases):
            if not isinstance(case, dict):
                self.error(path, f"case {index + 1} must be an object")
                continue
            if self.string(path, case, "id"):
                if case["id"] in self.case_ids:
                    self.error(path, f"duplicate evaluation id: {case['id']}")
                self.case_ids.add(case["id"])
            self.string(path, case, "prompt")
            if (
                not isinstance(case.get("skill"), str)
                or case["skill"] not in self.skill_names
            ):
                self.error(path, f"case {index + 1} references an unknown skill")
            if type(case.get("should_trigger")) is not bool:
                self.error(path, f"case {index + 1}: should_trigger must be a boolean")
            checks = case.get("checks")
            if (
                not isinstance(checks, list)
                or not checks
                or any(not isinstance(c, str) or not c.strip() for c in checks)
            ):
                self.error(path, f"case {index + 1}: checks must be non-empty strings")
            for key in ["fixtures", "fixtures_needed"]:
                if key not in case:
                    continue
                values = case[key]
                if not isinstance(values, list) or any(
                    not isinstance(v, str) or not v.strip() for v in values
                ):
                    self.error(path, f"case {index + 1}: {key} must list strings")
                elif key == "fixtures":
                    for value in values:
                        self.local_target(path, value)

    def run(self) -> list[str]:
        skills = self.root / "skills"
        if not skills.is_dir() or not any(skills.iterdir()):
            self.error(skills, "expected at least one skill folder")
        elif skills.is_dir():
            for folder in sorted(skills.iterdir()):
                if folder.is_dir():
                    manifest = folder / "SKILL.md"
                    if (
                        "SKILL.md" in {entry.name for entry in folder.iterdir()}
                        and manifest.is_file()
                    ):
                        try:
                            self.skill(manifest)
                        except (OSError, ValueError) as exc:
                            self.error(manifest, f"cannot read skill: {exc}")
                    else:
                        self.error(manifest, "missing SKILL.md (case-sensitive)")
        for path in self.files({".md", ".yaml", ".yml", ".toml"}):
            try:
                if path.suffix.lower() == ".md":
                    self.markdown(path)
                    if "claude-code" in path.parts and path.parent.name == "agents":
                        parsed = self.frontmatter(path)
                        if parsed is not None:
                            self.agent(path, parsed[0])
                elif path.suffix.lower() == ".toml":
                    data = tomllib.loads(path.read_text(encoding="utf-8"))
                    if "codex" in path.parts and path.parent.name == "agents":
                        self.agent(path, data, codex=True)
                else:
                    self.yaml(path, path.read_text(encoding="utf-8"))
            except (ValueError, OSError) as exc:
                self.error(path, f"cannot validate file: {exc}")
        for path in sorted((self.root / "evals").glob("*.json")):
            self.evaluation(path)
        if not self.case_ids:
            self.error(self.root / "evals", "expected at least one evaluation case")
        return list(dict.fromkeys(self.errors))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    args = parser.parse_args()
    validator = Validator(args.root)
    errors = validator.run()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"FAIL: {len(errors)} structural problem(s)", file=sys.stderr)
        return 1
    print(
        f"PASS: {len(validator.skill_names)} skills, references, configuration syntax, "
        f"and {len(validator.case_ids)} evaluation definitions. "
        "Product behavior was not evaluated."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
