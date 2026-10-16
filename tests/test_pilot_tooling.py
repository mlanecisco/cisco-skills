"""Check package integrity and evidence-record invariants independently."""

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from scripts.evaluation_runs import new_record, validate_record
from scripts.package_skills import build_release, sha256, verify_release

REPOSITORY = Path(__file__).resolve().parents[1]


class PilotToolingTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.root = self.base / "library"
        skill = self.root / "skills/demo"
        (skill / "references").mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            "---\nname: demo\ndescription: Demonstration.\nmetadata:\n"
            '  version: "0.1.0"\n  status: draft\n---\n'
            "Read [guide](references/guide.md).\n"
        )
        (skill / "references/guide.md").write_text("A complete reference.\n")
        (self.root / "evals/fixtures").mkdir(parents=True)
        (self.root / "evals/fixtures/input.json").write_text("{}\n")
        self.case = {
            "id": "demo",
            "skill": "demo",
            "prompt": "Do the task.",
            "should_trigger": True,
            "checks": ["Result matches supplied inputs"],
            "fixtures": ["fixtures/input.json"],
        }
        (self.root / "evals/demo.json").write_text(
            json.dumps(
                {
                    "author": "Mark A. Lane, Ph.D.",
                    "status": "Draft",
                    "run_on": ["Codex"],
                    "cases": [self.case],
                }
            )
        )

    def record(self) -> dict:
        return new_record(self.root, "demo", "Codex", evaluator="Pilot Evaluator")

    def test_evaluator_identity_is_independent_of_package_authorship(self) -> None:
        release = self.base / "release"
        package = build_release(self.root, release, "0.1.0")
        data = new_record(
            self.root,
            "demo",
            "Codex",
            package_manifest=release / "manifest.json",
            evaluator="  Independent Evaluator  ",
        )
        self.assertEqual(data["author"], "Independent Evaluator")
        self.assertNotEqual(data["author"], package["author"])
        self.assertEqual(
            data["source"]["package_manifest_sha256"], sha256(release / "manifest.json")
        )
        self.assertEqual(validate_record(data, self.case, self.root), [])

    def test_empty_evaluator_identity_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "evaluator must be a nonempty name"):
            new_record(self.root, "demo", "Codex", evaluator=" \t ")

    def test_evaluation_cli_requires_and_uses_explicit_evaluator_identity(self) -> None:
        output = self.base / "planned.json"
        command = [
            sys.executable,
            "-m",
            "scripts.evaluation_runs",
            "--root",
            str(self.root),
            "init",
            "--case",
            "demo",
            "--product",
            "Codex",
            "--output",
            str(output),
        ]
        missing = subprocess.run(
            command,
            cwd=REPOSITORY,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(missing.returncode, 2)
        self.assertIn("--evaluator", missing.stderr)
        self.assertFalse(output.exists())
        supplied = subprocess.run(
            [*command, "--evaluator", "Pilot Reviewer"],
            cwd=REPOSITORY,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(supplied.returncode, 0, supplied.stdout)
        data = json.loads(output.read_text())
        self.assertEqual(data["author"], "Pilot Reviewer")
        self.assertEqual(data["status"], "planned")
        self.assertIsNone(data["outcome"])

    def completed(self) -> dict:
        data = self.record()
        data.update(
            status="completed",
            run_id="synthetic-test-run",
            outcome="pass",
            elapsed_seconds=1.0,
            retries=0,
            started_at="2026-01-01T00:00:00+00:00",
            finished_at="2026-01-01T00:00:01+00:00",
        )
        data["environment"].update(
            interface="CLI",
            version="synthetic",
            os="test",
            model="test-model",
            reasoning_effort="low",
        )
        data["source"]["revision"] = "0" * 40
        data["installed_skills"] = [{"name": "demo", "version": "0.1.0"}]
        data["activation"] = {"observed": True, "evidence": "Synthetic trace fixture"}
        data["checks"][0].update(outcome="pass", evidence="Synthetic check fixture")
        artifact = self.root / "output/response.txt"
        artifact.parent.mkdir()
        artifact.write_text("Synthetic response fixture.\n")
        data["artifacts"] = [
            {"path": "output/response.txt", "sha256": sha256(artifact)}
        ]
        return data

    def test_archives_include_complete_skills_and_exclude_repository_assets(
        self,
    ) -> None:
        (self.root / "docs").mkdir()
        (self.root / "docs/template.potx").write_text("Repository-only asset")
        manifest = build_release(self.root, self.base / "release", "0.1.0-pilot.1")
        self.assertEqual(manifest["skills"][0]["status"], "draft")
        archive = self.base / "release" / manifest["skills"][0]["archive"]
        with ZipFile(archive) as zipped:
            self.assertEqual(
                set(zipped.namelist()),
                {
                    "demo/SKILL.md",
                    "demo/references/guide.md",
                },
            )
        self.assertEqual(verify_release(self.base / "release"), manifest)

    def test_archive_bytes_are_reproducible_for_unchanged_sources(self) -> None:
        first = build_release(self.root, self.base / "first", "0.1.0")
        second = build_release(self.root, self.base / "second", "0.1.0")
        self.assertEqual(first["skills"], second["skills"])

    def test_package_verification_detects_archive_tampering(self) -> None:
        manifest = build_release(self.root, self.base / "release", "0.1.0")
        archive = self.base / "release" / manifest["skills"][0]["archive"]
        with archive.open("ab") as target:
            target.write(b"changed")
        with self.assertRaisesRegex(ValueError, "checksum mismatch"):
            verify_release(self.base / "release")

    def test_extracted_archive_receives_reference_validation(self) -> None:
        release = self.base / "release"
        manifest = build_release(self.root, release, "0.1.0")
        entry = manifest["skills"][0]
        archive = release / entry["archive"]
        with ZipFile(archive) as zipped:
            manifest_content = zipped.read("demo/SKILL.md")
        with ZipFile(archive, "w") as zipped:
            zipped.writestr("demo/SKILL.md", manifest_content)
        entry["files"] = [
            item for item in entry["files"] if item["path"] == "demo/SKILL.md"
        ]
        entry["sha256"] = sha256(archive)
        (release / "manifest.json").write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, "missing local reference"):
            verify_release(release)

    def test_packaging_rejects_unintended_files_and_overwrites(self) -> None:
        release = self.base / "release"
        build_release(self.root, release, "0.1.0")
        with self.assertRaisesRegex(ValueError, "already exists"):
            build_release(self.root, release, "0.1.0")
        (self.root / "skills/demo/.env").write_text("SYNTHETIC=placeholder")
        with self.assertRaisesRegex(ValueError, "unintended"):
            build_release(self.root, self.base / "other", "0.1.1")
        self.assertFalse((self.base / "other").exists())

    def test_planned_records_do_not_claim_product_execution(self) -> None:
        data = self.record()
        self.assertEqual(validate_record(data, self.case, self.root), [])
        self.assertEqual(data["status"], "planned")
        self.assertIsNone(data["outcome"])
        data["outcome"] = "pass"
        self.assertIn(
            "planned records cannot claim an outcome", validate_record(data, self.case)
        )

    def test_complete_record_requires_all_checks_and_activation_evidence(self) -> None:
        data = self.completed()
        self.assertEqual(validate_record(data, self.case, self.root), [])
        data["checks"][0]["outcome"] = "not_run"
        data["activation"]["observed"] = None
        errors = " ".join(validate_record(data, self.case))
        self.assertIn("every acceptance check", errors)
        self.assertIn("expected activation", errors)

    def test_baselines_cannot_claim_installed_library_skills(self) -> None:
        data = self.completed()
        data["condition"] = "baseline"
        self.assertIn(
            "baseline must not install library skills", validate_record(data, self.case)
        )
        data["installed_skills"] = []
        self.assertIn(
            "baseline cannot claim library skill activation",
            validate_record(data, self.case),
        )
        data["activation"] = {"observed": False, "evidence": "Library not installed"}
        self.assertEqual(validate_record(data, self.case), [])

    def test_record_file_checks_detect_changed_inputs_and_artifacts(self) -> None:
        data = self.completed()
        (self.root / "output/response.txt").write_text("Changed response")
        (self.root / "evals/fixtures/input.json").write_text("Changed input")
        errors = " ".join(validate_record(data, self.case, self.root))
        self.assertIn("inputs: checksum mismatch", errors)
        self.assertIn("artifacts: checksum mismatch", errors)

    def test_record_rejects_unknown_fields_and_invalid_counters(self) -> None:
        data = self.record()
        for field, value in [("elapsed_seconds", float("nan")), ("retries", True)]:
            changed = copy.deepcopy(data)
            changed[field] = value
            self.assertTrue(validate_record(changed, self.case))
        data["usage"]["input_tokens"] = True
        self.assertTrue(validate_record(data, self.case))
        data["unexpected"] = "ignored?"
        self.assertTrue(validate_record(data, self.case))

    def test_planned_templates_cannot_be_retained_as_completed_results(self) -> None:
        results = self.root / "evals/results"
        results.mkdir()
        (results / "planned.json").write_text(json.dumps(self.record()))
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "scripts.evaluation_runs",
                "--root",
                str(self.root),
                "validate-all",
            ],
            cwd=REPOSITORY,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("retained results must be completed attempts", result.stdout)

    def test_record_rejects_reversed_timestamps(self) -> None:
        data = self.completed()
        data["finished_at"] = "2025-12-31T23:59:00+00:00"
        self.assertIn(
            "finished_at must not precede started_at", validate_record(data, self.case)
        )

    def test_package_verification_rejects_promoted_status(self) -> None:
        release = self.base / "release"
        manifest = build_release(self.root, release, "0.1.0")
        manifest["skills"][0]["status"] = "tested"
        (release / "manifest.json").write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, "status mismatch"):
            verify_release(release)


if __name__ == "__main__":
    unittest.main()
