"""Create planned evaluation records and validate recorded pilot evidence."""

import argparse
import json
import math
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from scripts.package_skills import AUTHOR, sha256, source_revision
from scripts.validate_library import PLATFORMS, unique_json


def find_case(root: Path, case_id: str) -> dict[str, Any]:
    matches = [
        case
        for path in (root / "evals").glob("*.json")
        for case in json.loads(path.read_text(encoding="utf-8"))["cases"]
        if case["id"] == case_id
    ]
    if len(matches) != 1:
        raise ValueError(f"expected one evaluation case named {case_id}")
    return matches[0]


def new_record(
    root: Path,
    case_id: str,
    product: str,
    condition: str = "with-skills",
    invocation: str = "automatic",
    package_manifest: Path | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    case = find_case(root, case_id)
    revision, dirty = source_revision(root)
    inputs = []
    for key, visibility in [("fixtures", "agent"), ("evaluator_fixtures", "evaluator")]:
        for value in case.get(key, []):
            path = (root / "evals" / value).resolve()
            files = sorted(path.rglob("*")) if path.is_dir() else [path]
            for item in files:
                if item.is_symlink() or not item.resolve().is_relative_to(
                    root.resolve()
                ):
                    raise ValueError(f"{item}: input must remain in the repository")
                if item.is_file():
                    inputs.append(
                        {
                            "path": item.relative_to(root).as_posix(),
                            "sha256": sha256(item),
                            "visibility": visibility,
                        }
                    )
    package_version = None
    package_hash = None
    if package_manifest is not None:
        package = json.loads(package_manifest.read_text(encoding="utf-8"))
        package_version = package["release_version"]
        package_hash = sha256(package_manifest)
    return {
        "schema_version": 1,
        "author": AUTHOR,
        "run_id": "",
        "case_id": case_id,
        "status": "planned",
        "condition": condition,
        "invocation": invocation,
        "prompt": case["prompt"],
        "environment": {
            "product": product,
            "interface": None,
            "version": None,
            "os": None,
            "account_route": None,
            "model": None,
            "reasoning_effort": None,
            "other_skills": [],
        },
        "source": {
            "revision": revision,
            "dirty": dirty,
            "package_version": package_version,
            "package_manifest_sha256": package_hash,
        },
        "inputs": inputs,
        "installed_skills": [],
        "activation": {"observed": None, "evidence": ""},
        "checks": [
            {"check": check, "outcome": "not_run", "evidence": ""}
            for check in case["checks"]
        ],
        "artifacts": [],
        "elapsed_seconds": None,
        "started_at": None,
        "finished_at": None,
        "retries": None,
        "usage": {
            "input_tokens": None,
            "output_tokens": None,
            "reasoning_tokens": None,
            "cached_input_tokens": None,
            "includes_workers": None,
            "note": "Not measured.",
        },
        "interventions": [],
        "limitations": [],
        "outcome": None,
    }


def validate_record(
    data: Any, case: dict[str, Any], root: Path | None = None
) -> list[str]:
    errors: list[str] = []

    def text(value: Any) -> bool:
        return isinstance(value, str) and bool(value.strip())

    def shape(value: Any, fields: set[str], label: str) -> bool:
        if not isinstance(value, dict) or set(value) != fields:
            errors.append(f"{label}: expected exactly {', '.join(sorted(fields))}")
            return False
        return True

    fields = {
        "schema_version",
        "author",
        "run_id",
        "case_id",
        "status",
        "condition",
        "invocation",
        "prompt",
        "environment",
        "source",
        "inputs",
        "installed_skills",
        "activation",
        "checks",
        "artifacts",
        "elapsed_seconds",
        "retries",
        "usage",
        "interventions",
        "limitations",
        "outcome",
        "started_at",
        "finished_at",
    }
    if not shape(data, fields, "record"):
        return errors
    completed = data["status"] == "completed"
    passed = completed and data["outcome"] == "pass"
    if (
        type(data["schema_version"]) is not int
        or data["schema_version"] != 1
        or data["case_id"] != case["id"]
        or not text(data["author"])
        or data["status"] not in {"planned", "completed"}
        or data["condition"] not in {"with-skills", "baseline"}
        or data["invocation"] not in {"automatic", "explicit"}
        or not text(data["prompt"])
    ):
        errors.append("invalid record identity, condition, invocation, or status")
    if completed and (
        not text(data["run_id"]) or data["outcome"] not in {"pass", "fail", "blocked"}
    ):
        errors.append("completed runs require a run_id and outcome")
    if not completed and data["outcome"] is not None:
        errors.append("planned records cannot claim an outcome")
    env = data["environment"]
    if shape(
        env,
        {
            "product",
            "interface",
            "version",
            "os",
            "account_route",
            "model",
            "reasoning_effort",
            "other_skills",
        },
        "environment",
    ):
        if env["product"] not in PLATFORMS:
            errors.append("unsupported product")
        for key in set(env) - {"product", "other_skills"}:
            if env[key] is not None and not text(env[key]):
                errors.append(f"environment.{key}: expected text or null")
        if not isinstance(env["other_skills"], list) or any(
            not text(value) for value in env["other_skills"]
        ):
            errors.append("environment.other_skills: expected skill names or versions")
        if completed and data["outcome"] != "blocked":
            if any(
                not text(env[key])
                for key in ["interface", "version", "os", "model", "reasoning_effort"]
            ):
                errors.append(
                    "completed attempts require environment and model details"
                )
    source = data["source"]
    if shape(
        source,
        {"revision", "dirty", "package_version", "package_manifest_sha256"},
        "source",
    ):
        if source["revision"] is not None and not re.fullmatch(
            r"[0-9a-f]{40,64}", str(source["revision"])
        ):
            errors.append("source.revision: expected a Git revision or null")
        if source["dirty"] is not None and type(source["dirty"]) is not bool:
            errors.append("source.dirty: expected a boolean or null")
        if completed and not source["revision"]:
            errors.append("completed runs require a source revision")
        if source["package_version"] is not None and not text(
            source["package_version"]
        ):
            errors.append("source.package_version: expected text or null")
        if source["package_manifest_sha256"] is not None and not re.fullmatch(
            r"[0-9a-f]{64}", str(source["package_manifest_sha256"])
        ):
            errors.append("source.package_manifest_sha256: invalid checksum")
        if bool(source["package_version"]) != bool(source["package_manifest_sha256"]):
            errors.append(
                "package version and manifest checksum must be recorded together"
            )
    for field in ["inputs", "artifacts"]:
        values = data[field]
        if not isinstance(values, list):
            errors.append(f"{field}: expected a list")
            continue
        for item in values:
            item_fields = {"path", "sha256"} | (
                {"visibility"} if field == "inputs" else set()
            )
            if not shape(item, item_fields, field):
                continue
            if not text(item["path"]) or not re.fullmatch(
                r"[0-9a-f]{64}", str(item["sha256"])
            ):
                errors.append(f"{field}: require a path and SHA-256")
            if field == "inputs" and item["visibility"] not in {"agent", "evaluator"}:
                errors.append("inputs.visibility: expected agent or evaluator")
            if root is not None and text(item["path"]):
                path = (root / item["path"]).resolve()
                if not path.is_relative_to(root.resolve()) or not path.is_file():
                    errors.append(
                        f"{field}: missing or out-of-repository file: {item['path']}"
                    )
                elif sha256(path) != item["sha256"]:
                    errors.append(f"{field}: checksum mismatch: {item['path']}")
    skills = data["installed_skills"]
    if not isinstance(skills, list) or any(
        not isinstance(skill, dict)
        or set(skill) != {"name", "version"}
        or not text(skill["name"])
        or not text(skill["version"])
        for skill in skills
    ):
        errors.append("installed_skills: require name/version entries")
    elif data["condition"] == "baseline" and skills:
        errors.append("baseline must not install library skills")
    elif (
        passed
        and data["condition"] == "with-skills"
        and case["skill"] not in {skill["name"] for skill in skills}
    ):
        errors.append("passing skill runs must record the target skill version")
    checks = data["checks"]
    if not isinstance(checks, list) or any(
        not isinstance(check, dict)
        or set(check) != {"check", "outcome", "evidence"}
        or check["outcome"] not in {"pass", "fail", "not_run"}
        or not isinstance(check["evidence"], str)
        for check in checks
    ):
        errors.append("checks: invalid check record")
    else:
        if [check["check"] for check in checks] != case["checks"]:
            errors.append("checks must preserve every case acceptance criterion")
        if completed and any(
            check["outcome"] != "not_run" and not text(check["evidence"])
            for check in checks
        ):
            errors.append("performed checks require evidence")
        if passed and any(check["outcome"] != "pass" for check in checks):
            errors.append("passing runs require every acceptance check to pass")
    activation = data["activation"]
    if shape(activation, {"observed", "evidence"}, "activation"):
        if (
            activation["observed"] is not None
            and type(activation["observed"]) is not bool
        ):
            errors.append("activation.observed: expected a boolean or null")
        if not isinstance(activation["evidence"], str):
            errors.append("activation.evidence: expected text")
        if data["condition"] == "baseline" and activation["observed"] is True:
            errors.append("baseline cannot claim library skill activation")
        if (
            passed
            and data["condition"] == "with-skills"
            and (
                activation["observed"] != case["should_trigger"]
                or not text(activation["evidence"])
            )
        ):
            errors.append("passing skill runs require evidence of expected activation")
    for key in ["elapsed_seconds", "retries"]:
        value = data[key]
        if value is not None and (
            type(value) not in {int, float}
            or not math.isfinite(value)
            or value < 0
            or key == "retries"
            and type(value) is not int
        ):
            errors.append(f"{key}: expected a nonnegative number or null")
        if completed and value is None:
            errors.append(f"completed runs require {key}")
    timestamps = []
    for key in ["started_at", "finished_at"]:
        value = data[key]
        if value is None and not completed:
            continue
        try:
            timestamp = datetime.fromisoformat(value)
            if timestamp.utcoffset() is None:
                raise ValueError("timezone required")
            timestamps.append(timestamp)
        except (ValueError, TypeError):
            errors.append(f"{key}: expected an ISO timestamp with timezone")
    if len(timestamps) == 2 and timestamps[1] < timestamps[0]:
        errors.append("finished_at must not precede started_at")
    usage = data["usage"]
    if shape(
        usage,
        {
            "input_tokens",
            "output_tokens",
            "reasoning_tokens",
            "cached_input_tokens",
            "includes_workers",
            "note",
        },
        "usage",
    ):
        for key in [
            "input_tokens",
            "output_tokens",
            "reasoning_tokens",
            "cached_input_tokens",
        ]:
            if usage[key] is not None and (
                type(usage[key]) is not int or usage[key] < 0
            ):
                errors.append(f"usage.{key}: expected a nonnegative integer or null")
        if (
            usage["includes_workers"] is not None
            and type(usage["includes_workers"]) is not bool
        ):
            errors.append("usage.includes_workers: expected a boolean or null")
        if not text(usage["note"]):
            errors.append(
                "usage.note: explain counter coverage or missing measurements"
            )
    for key in ["interventions", "limitations"]:
        if not isinstance(data[key], list) or any(
            not text(value) for value in data[key]
        ):
            errors.append(f"{key}: expected a list of nonempty strings")
    if passed and not data["artifacts"]:
        errors.append("passing runs require a retained artifact or response record")
    if completed and data["outcome"] == "blocked" and not data["limitations"]:
        errors.append("blocked runs require an explanation in limitations")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init")
    init.add_argument("--case", required=True)
    init.add_argument("--product", choices=sorted(PLATFORMS), required=True)
    init.add_argument(
        "--condition", choices=["with-skills", "baseline"], default="with-skills"
    )
    init.add_argument(
        "--invocation", choices=["automatic", "explicit"], default="automatic"
    )
    init.add_argument("--package-manifest", type=Path)
    init.add_argument("--output", type=Path, required=True)
    validate = commands.add_parser("validate")
    validate.add_argument("file", type=Path)
    validate.add_argument("--check-files", action="store_true")
    commands.add_parser("validate-all")
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if args.command == "init":
            data = new_record(
                root,
                args.case,
                args.product,
                args.condition,
                args.invocation,
                args.package_manifest,
            )
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open("x", encoding="utf-8") as target:
                target.write(json.dumps(data, indent=2) + "\n")
            print(
                f"Created planned record: {args.output}; no product run has occurred."
            )
            return 0
        paths = (
            [args.file]
            if args.command == "validate"
            else sorted((root / "evals/results").rglob("*.json"))
        )
        errors: list[str] = []
        for path in paths:
            data = json.loads(
                path.read_text(encoding="utf-8"), object_pairs_hook=unique_json
            )
            case = find_case(root, data["case_id"])
            problems = validate_record(
                data, case, root if getattr(args, "check_files", False) else None
            )
            if args.command == "validate-all" and data.get("status") != "completed":
                problems.append(
                    "retained results must be completed attempts, not planned templates"
                )
            errors.extend(f"{path}: {problem}" for problem in problems)
        if errors:
            raise ValueError("\n".join(errors))
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f"FAIL: {exc}")
        return 1
    print(
        f"PASS: {len(paths)} run records validated; "
        "validation does not establish their truth."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
