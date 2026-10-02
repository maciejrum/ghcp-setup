"""Verify isolation and reproducibility of benchmark preparation."""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.prepare_benchmark import prepare


class BenchmarkPreparationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="benchmark-prepare-test-")
        self.addCleanup(self.tmp.cleanup)
        self.parent = Path(self.tmp.name)
        self.source = self.parent / "source"
        files = {
            "benchmark/fixture/README.md": "Application commands\n",
            "benchmark/fixture/backend/app.py": "fixture = 'original'\n",
            "benchmark/fixture/frontend/package-lock.json": "{}\n",
            "benchmark/fixture/node_modules/ignored.js": "runtime\n",
            "benchmark/assessor/private.py": "external oracle\n",
            "benchmark/task.md": "Frozen task\n",
            "benchmark/quality-rubric.md": "Frozen rubric\n",
            ".github/copilot-instructions.md": (
                "# Project architecture\nOld\n# Development workflow\nCommon\n"
                "Use the relevant skills in `.github/skills/` on demand. Skills describe procedures; "
                "they do not grant tools or change an agent's role.\n"
            ),
            ".github/instructions/backend.instructions.md": "Shared instruction\n",
            ".github/agents/orchestrator.agent.md": "Team only\n",
            ".github/agents/contracts/workflow.md": "Team contract\n",
            ".github/skills/run-validation/SKILL.md": "Team validation\n",
            ".github/prompts/implement-feature.prompt.md": "Team prompt\n",
            ".vscode/settings.json": "{}\n",
        }
        for relative, content in files.items():
            path = self.source / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    def test_common_application_and_instructions_are_identical_and_team_is_separate(self):
        target = self.parent / "pair"
        manifest = prepare(target, self.source, order="BA")
        a, b = target / "A-standard", target / "B-team"
        for relative in ("README.md", "backend/app.py", "frontend/package-lock.json",
                         ".github/copilot-instructions.md", ".github/instructions/backend.instructions.md",
                         ".vscode/settings.json"):
            self.assertEqual((a / relative).read_bytes(), (b / relative).read_bytes())
        self.assertFalse((a / ".github/agents").exists())
        self.assertFalse((a / ".github/skills").exists())
        self.assertTrue((b / ".github/agents/contracts/workflow.md").is_file())
        self.assertTrue((b / ".github/skills/run-validation/SKILL.md").is_file())
        self.assertNotIn(".github/skills/", (a / ".github/copilot-instructions.md").read_text())
        for workspace in (a, b):
            self.assertFalse((workspace / "benchmark/assessor").exists())
            self.assertFalse((workspace / ".github/prompts").exists())
            self.assertFalse((workspace / "node_modules").exists())
        self.assertEqual(manifest["execution_order"], ["B", "A"])
        self.assertEqual(json.loads((target / "manifest.json").read_text()), manifest)

    def test_existing_directory_is_never_overwritten(self):
        existing = self.parent / "existing"
        existing.mkdir()
        sentinel = existing / "sentinel.txt"
        sentinel.write_text("keep me", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            prepare(existing, self.source)
        self.assertEqual(sentinel.read_text(), "keep me")

    def test_symlink_destination_is_never_overwritten(self):
        existing = self.parent / "existing"
        existing.mkdir()
        sentinel = existing / "sentinel.txt"
        sentinel.write_text("keep me", encoding="utf-8")
        link = self.parent / "link"
        try:
            link.symlink_to(existing, target_is_directory=True)
        except OSError as error:
            if getattr(error, "winerror", None) == 1314:
                self.skipTest("Windows does not grant this account symlink creation permission")
            raise
        with self.assertRaises(FileExistsError):
            prepare(link, self.source)
        self.assertEqual(sentinel.read_text(), "keep me")

    def test_editing_one_workspace_does_not_change_other_or_source(self):
        target = self.parent / "pair"
        prepare(target, self.source)
        (target / "A-standard/backend/app.py").write_text("edited\n", encoding="utf-8")
        self.assertEqual((target / "B-team/backend/app.py").read_text(), "fixture = 'original'\n")
        self.assertEqual((self.source / "benchmark/fixture/backend/app.py").read_text(), "fixture = 'original'\n")

    def test_hashes_are_reproducible_and_reflect_baseline_changes(self):
        first = prepare(self.parent / "one", self.source, order="AB")
        second = prepare(self.parent / "two", self.source, order="AB")
        self.assertEqual(first["fixture_sha256"], second["fixture_sha256"])
        self.assertEqual(first["variants"]["B"]["baseline_sha256"], second["variants"]["B"]["baseline_sha256"])
        (self.source / "benchmark/fixture/backend/app.py").write_text("changed\n", encoding="utf-8")
        changed = prepare(self.parent / "three", self.source)
        self.assertNotEqual(first["fixture_sha256"], changed["fixture_sha256"])
        (self.source / "benchmark/task.md").write_text("New task\n", encoding="utf-8")
        changed_protocol = prepare(self.parent / "four", self.source)
        self.assertNotEqual(changed["protocol_sha256"], changed_protocol["protocol_sha256"])

    def test_destination_inside_source_is_rejected_before_copying(self):
        for relative in ("benchmark/fixture/run", ".github/run", ".vscode/run", ".local/run"):
            with self.subTest(relative=relative):
                target = self.source / relative
                with self.assertRaisesRegex(ValueError, "outside the source repository"):
                    prepare(target, self.source)
                self.assertFalse(target.exists())

    def test_missing_source_rolls_back_only_new_target(self):
        (self.source / ".github/copilot-instructions.md").unlink()
        target = self.parent / "incomplete"
        with self.assertRaises(FileNotFoundError):
            prepare(target, self.source)
        self.assertFalse(target.exists())
        self.assertTrue(self.source.exists())

    def test_git_initialization_is_opt_in_and_records_clean_local_baseline(self):
        plain = self.parent / "plain"
        prepare(plain, self.source)
        self.assertFalse((plain / "A-standard/.git").exists())
        target = self.parent / "with-git"
        manifest = prepare(target, self.source, init_git=True)
        for key, name in (("A", "A-standard"), ("B", "B-team")):
            workspace = target / name
            self.assertEqual(len(manifest["variants"][key]["baseline_commit"]), 40)
            self.assertEqual(subprocess.check_output(["git", "-C", str(workspace), "status", "--porcelain"]), b"")


if __name__ == "__main__":
    unittest.main()
