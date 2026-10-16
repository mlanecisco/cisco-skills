"""Regression checks for malformed libraries and portable valid examples."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.validate_library import Validator

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_library.py"


class LibraryValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "library"
        self.manifest = """---
name: demo
description: Create a demonstration artifact when requested.
metadata:
  author: Mark A. Lane, Ph.D.
  version: "0.1.0"
---

# Demonstration

Create the requested artifact.
"""
        self.write("skills/demo/SKILL.md", self.manifest)
        self.evaluation = {
            "author": "Mark A. Lane, Ph.D.",
            "status": "Specifications only",
            "run_on": ["Claude Code", "Codex"],
            "cases": [
                {
                    "id": "demo-request",
                    "skill": "demo",
                    "prompt": "Create a demonstration artifact.",
                    "should_trigger": True,
                    "checks": ["The artifact meets the request"],
                }
            ],
        }
        self.save_evaluation()

    def write(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def save_evaluation(self) -> None:
        self.write("evals/demo.json", json.dumps(self.evaluation))

    def errors(self) -> str:
        return "\n".join(Validator(self.root).run())

    def test_valid_library(self) -> None:
        self.assertEqual(self.errors(), "")

    def test_optional_standard_fields_are_accepted(self) -> None:
        self.write(
            "skills/demo/SKILL.md",
            self.manifest.replace(
                "metadata:",
                "compatibility: Requires Python 3.11\nlicense: MIT\n"
                "allowed-tools: Read\nmetadata:",
            ),
        )
        self.assertEqual(self.errors(), "")

    def test_wrong_manifest_case_is_rejected(self) -> None:
        path = self.root / "skills/demo/SKILL.md"
        text = path.read_text()
        path.unlink()
        self.write("skills/demo/skill.md", text)
        self.assertIn("missing SKILL.md", self.errors())

    def test_folder_and_name_must_match(self) -> None:
        self.write(
            "skills/demo/SKILL.md", self.manifest.replace("name: demo", "name: other")
        )
        self.assertIn("name must match", self.errors())

    def test_invalid_names_are_rejected(self) -> None:
        for name in ["Demo", "demo--task", "-demo", "demo_thing", "x" * 65]:
            with self.subTest(name=name):
                self.write(
                    "skills/demo/SKILL.md",
                    self.manifest.replace("name: demo", f"name: {name}"),
                )
                self.assertIn("name", self.errors())

    def test_missing_or_non_string_description_is_rejected(self) -> None:
        for value in ["", "true", "42", "[]", "x" * 1025]:
            with self.subTest(value=value[:20]):
                self.write(
                    "skills/demo/SKILL.md",
                    self.manifest.replace(
                        "Create a demonstration artifact when requested.", value
                    ),
                )
                self.assertIn("description", self.errors())

    def test_duplicate_frontmatter_keys_are_rejected(self) -> None:
        self.write(
            "skills/demo/SKILL.md",
            self.manifest.replace("name: demo", "name: overwritten\nname: demo"),
        )
        self.assertIn("duplicate YAML key", self.errors())

    def test_host_specific_skill_field_is_rejected(self) -> None:
        self.write(
            "skills/demo/SKILL.md",
            self.manifest.replace(
                "metadata:", "disable-model-invocation: true\nmetadata:"
            ),
        )
        self.assertIn("unsupported portable skill field", self.errors())

    def test_metadata_values_must_be_strings(self) -> None:
        self.write(
            "skills/demo/SKILL.md",
            self.manifest.replace('version: "0.1.0"', "version: 1"),
        )
        self.assertIn("metadata", self.errors())

    def test_empty_body_is_rejected(self) -> None:
        self.write("skills/demo/SKILL.md", self.manifest.split("# Demonstration")[0])
        self.assertIn("instructions are empty", self.errors())

    def test_links_images_titles_and_reference_links_are_checked(self) -> None:
        for link in [
            "[Guide](references/missing.md)",
            '![Example](assets/missing.png "Preview")',
            "[Guide][guide]\n\n[guide]: references/missing.md",
        ]:
            with self.subTest(link=link):
                self.write("skills/demo/SKILL.md", self.manifest + link)
                self.assertIn("missing local reference", self.errors())

    def test_encoded_spaces_and_parentheses_in_links_are_valid(self) -> None:
        self.write("skills/demo/references/My guide (v1).md", "A reference.")
        self.write(
            "skills/demo/SKILL.md",
            self.manifest + "[Guide](<references/My%20guide%20(v1).md>)",
        )
        self.assertEqual(self.errors(), "")

    def test_code_examples_external_links_and_fragments_are_not_fetched(self) -> None:
        self.write(
            "skills/demo/SKILL.md",
            self.manifest
            + """
[External](https://invalid.example/anything)
[Section](#section)
`[Literal](missing.md)`
```markdown
[Literal](also-missing.md)
```
""",
        )
        self.assertEqual(self.errors(), "")

    def test_skill_links_must_stay_in_installable_folder(self) -> None:
        self.write("README.md", "Library instructions.")
        self.write("skills/demo/SKILL.md", self.manifest + "[Guide](../../README.md)")
        self.assertIn("leaves its installable folder", self.errors())

    def test_supporting_resource_links_cannot_leave_skill_folder(self) -> None:
        self.write("README.md", "Library instructions.")
        for relative, target in [
            ("skills/demo/references/guide.md", "../../../README.md"),
            ("skills/demo/assets/examples/guide.md", "../../../../README.md"),
        ]:
            for link in [
                f"[Guide]({target})",
                f'![Example]({target} "Preview")',
                f"[Guide][guide]\n\n[guide]: {target}",
            ]:
                with self.subTest(relative=relative, link=link):
                    path = self.write(relative, link)
                    self.assertIn(
                        f"{path.relative_to(self.root)}: "
                        "skill reference leaves its installable folder: "
                        f"{target}",
                        self.errors(),
                    )

    def test_supporting_reference_cannot_link_to_another_skill(self) -> None:
        self.write(
            "skills/demo-other/SKILL.md",
            self.manifest.replace("name: demo", "name: demo-other"),
        )
        self.write("skills/demo-other/references/guide.md", "Other skill instructions.")
        self.write(
            "skills/demo/references/guide.md",
            "[Other guide](../../demo-other/references/guide.md)",
        )
        self.assertIn("leaves its installable folder", self.errors())

    def test_supporting_resources_allow_links_within_skill_folder(self) -> None:
        self.write("skills/demo/assets/preview.png", "Synthetic image fixture.")
        self.write("skills/demo/references/My guide (v1).md", "A reference.")
        self.write(
            "skills/demo/references/guide.md",
            """[Instructions](../SKILL.md)
[Related guide](<My%20guide%20(v1).md#section>)
![Preview](../assets/preview.png)
[External](https://invalid.example/anything)
[Section](#section)
""",
        )
        self.write(
            "skills/demo/assets/examples/guide.md",
            "[Guide](../../references/guide.md)",
        )
        self.assertEqual(self.errors(), "")

    def test_supporting_reference_cannot_escape_through_symlink(self) -> None:
        outside = self.write("README.md", "Library instructions.")
        shortcut = self.root / "skills/demo/assets/shared.md"
        shortcut.parent.mkdir(parents=True)
        try:
            shortcut.symlink_to(outside)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"Symlinks unavailable: {exc}")
        self.write("skills/demo/references/guide.md", "[Shared](../assets/shared.md)")
        self.assertIn("leaves its installable folder", self.errors())

    def test_repository_documentation_can_link_across_folders(self) -> None:
        self.write("skills/demo/references/guide.md", "Skill instructions.")
        self.write("docs/guide.md", "[Skill guide](../skills/demo/references/guide.md)")
        self.write("README.md", "[Setup](docs/guide.md)")
        self.assertEqual(self.errors(), "")

    def test_local_links_cannot_leave_repository(self) -> None:
        self.write("README.md", "[Outside](../outside.md)")
        self.assertIn("leaves the repository", self.errors())

    def test_malformed_configuration_is_rejected(self) -> None:
        self.write(".github/workflows/check.yml", "jobs: [unterminated")
        self.write("pyproject.toml", "[unterminated")
        errors = self.errors()
        self.assertIn("invalid YAML", errors)
        self.assertIn("pyproject.toml", errors)

    def test_yaml_merge_overrides_are_valid(self) -> None:
        self.write(
            "example.yml",
            """defaults: &defaults
  retries: 2
worker:
  <<: *defaults
  retries: 1
""",
        )
        self.assertEqual(self.errors(), "")

    def test_manifest_directory_is_reported_as_missing(self) -> None:
        path = self.root / "skills/demo/SKILL.md"
        path.unlink()
        path.mkdir()
        self.assertIn("missing SKILL.md", self.errors())

    def test_invalid_text_encoding_reports_file(self) -> None:
        (self.root / "skills/demo/SKILL.md").write_bytes(b"\xff\xfe")
        self.assertIn("skills/demo/SKILL.md", self.errors())

    def test_agent_required_fields_and_turn_limit_are_checked(self) -> None:
        self.write(
            "skills/demo/assets/claude-code/agents/worker.md",
            """---
name: worker
description: A worker.
model: selected-model
maxTurns: true
---
Do the assigned task.
""",
        )
        self.write("skills/demo/assets/codex/agents/worker.toml", 'name = "worker"')
        errors = self.errors()
        self.assertIn("maxTurns must be a positive integer", errors)
        self.assertIn("developer_instructions", errors)

    def test_unknown_skill_and_boolean_string_are_rejected(self) -> None:
        self.evaluation["cases"][0]["skill"] = "missing"
        self.evaluation["cases"][0]["should_trigger"] = "false"
        self.save_evaluation()
        self.assertIn("unknown skill", self.errors())
        self.assertIn("should_trigger must be a boolean", self.errors())

    def test_empty_acceptance_checks_are_rejected(self) -> None:
        self.evaluation["cases"][0]["checks"] = []
        self.save_evaluation()
        self.assertIn("checks must be non-empty strings", self.errors())

    def test_duplicate_case_ids_across_suites_are_rejected(self) -> None:
        self.write("evals/second.json", json.dumps(self.evaluation))
        self.assertIn("duplicate evaluation id", self.errors())

    def test_duplicate_json_keys_are_rejected(self) -> None:
        self.write("evals/demo.json", '{"cases": [], "cases": []}')
        self.assertIn("duplicate JSON key", self.errors())

    def test_declared_fixture_paths_must_exist(self) -> None:
        self.evaluation["cases"][0]["fixtures"] = ["fixtures/missing.json"]
        self.save_evaluation()
        self.assertIn("missing local reference", self.errors())

    def test_fixture_paths_reject_urls_fragments_and_absolute_paths(self) -> None:
        existing = self.write("evals/fixtures/input.json", "{}")
        for value in [
            "https://invalid.example/input.json",
            "http://[",
            "#missing",
            "?input=missing",
            str(existing),
            "C:/fixtures/input.json",
            "C:input.json",
            "//server/input",
            "fixtures/input.json#section",
            "fixtures\\input.json",
        ]:
            with self.subTest(value=value):
                self.evaluation["cases"][0]["fixtures"] = [value]
                self.save_evaluation()
                self.assertIn("case demo-request: fixture must be", self.errors())

    def test_fixtures_accept_local_files_and_project_directories(self) -> None:
        self.write("evals/fixtures/project/input.json", "{}")
        self.evaluation["cases"][0]["fixtures"] = ["fixtures/project"]
        self.evaluation["cases"][0]["evaluator_fixtures"] = [
            "fixtures/project/input.json"
        ]
        self.save_evaluation()
        self.assertEqual(self.errors(), "")

    def test_fixture_cannot_leave_repository(self) -> None:
        self.evaluation["cases"][0]["fixtures"] = ["../../outside.json"]
        self.save_evaluation()
        self.assertIn("fixture leaves the repository", self.errors())

    def test_unknown_evaluation_fields_are_rejected(self) -> None:
        self.evaluation["unexpected"] = True
        self.evaluation["cases"][0]["fixture_needed"] = ["Missing input"]
        self.save_evaluation()
        self.assertIn("unknown evaluation suite field", self.errors())
        self.assertIn("unknown evaluation field: fixture_needed", self.errors())

    def test_nested_suites_are_rejected_but_fixture_json_is_not_a_suite(self) -> None:
        self.write("evals/fixtures/input.json", "not an evaluation suite")
        self.assertEqual(self.errors(), "")
        self.write("evals/nested/invalid.json", "not JSON")
        self.assertIn("evaluation suites must be directly under evals/", self.errors())

    def test_product_names_include_native_cursor_and_document_interfaces(self) -> None:
        self.evaluation["run_on"] = ["Cursor", "Claude Desktop", "ChatGPT"]
        self.save_evaluation()
        self.assertEqual(self.errors(), "")

    def test_symlinked_skill_directories_and_resources_are_rejected(self) -> None:
        for relative in [
            "skills/demo",
            "skills/demo/references",
            "skills/demo/asset.md",
        ]:
            with (
                self.subTest(relative=relative),
                tempfile.TemporaryDirectory() as other,
            ):
                external = Path(other) / "external"
                external.mkdir()
                (external / "SKILL.md").write_text(
                    self.manifest + "[Missing](missing.md)"
                )
                link = self.root / relative
                if link.is_dir():
                    (link / "SKILL.md").unlink()
                    link.rmdir()
                link.parent.mkdir(parents=True, exist_ok=True)
                try:
                    link.symlink_to(external, target_is_directory=True)
                except (OSError, NotImplementedError) as exc:
                    self.skipTest(f"Symlinks unavailable: {exc}")
                self.assertIn("symlinks are not allowed", self.errors())
                link.unlink()
                self.write("skills/demo/SKILL.md", self.manifest)

    def test_empty_library_fails(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.assertTrue(Validator(Path(temporary.name)).run())

    def test_cli_is_independent_of_working_directory(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root)],
            cwd=self.root.parent,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Product behavior was not evaluated", result.stdout)

    def test_cli_failure_identifies_the_file(self) -> None:
        self.write("skills/demo/SKILL.md", "No frontmatter.")
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("skills/demo/SKILL.md", result.stderr)


if __name__ == "__main__":
    unittest.main()
