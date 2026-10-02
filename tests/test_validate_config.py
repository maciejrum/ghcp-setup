"""Regression tests exercise invalid configurations in disposable repository copies."""

import csv
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from scripts import validate_config as validator


class ConfigValidationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="copilot-config-test-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for directory in (".github", ".vscode", "docs"):
            shutil.copytree(validator.ROOT / directory, self.root / directory)
        shutil.copy2(validator.ROOT / "README.md", self.root / "README.md")
        # README includes maintenance links outside the copied directories.
        for directory in ("scripts", "tests"):
            shutil.copytree(
                validator.ROOT / directory, self.root / directory,
                ignore=shutil.ignore_patterns("__pycache__"),
            )
        for directory in ("benchmark", "outputs"):
            shutil.copytree(
                validator.ROOT / directory, self.root / directory,
                ignore=shutil.ignore_patterns(
                    "node_modules", ".venv", "__pycache__", ".pytest_cache",
                    "dist", "test-results", "playwright-report", ".DS_Store",
                ),
            )
        shutil.copy2(validator.ROOT / "requirements-dev.txt", self.root / "requirements-dev.txt")

    def change_metadata(self, relative, **updates):
        path = self.root / relative
        original = path.read_text(encoding="utf-8")
        data = validator.frontmatter(path)
        data.update(updates)
        body = original.split("---\n", 2)[2]
        path.write_text("---\n" + yaml.safe_dump(data, sort_keys=False) + "---\n" + body,
                        encoding="utf-8")

    def agent(self, role, **updates):
        self.change_metadata(f".github/agents/{role}.agent.md", **updates)

    def invalid(self, message):
        with self.assertRaisesRegex(ValueError, message):
            validator.validate(self.root)

    def test_current_configuration_passes(self):
        validator.validate(self.root)

    def test_private_jira_skill_is_not_required_for_static_validation(self):
        self.assertFalse((self.root / ".github/skills/jira").exists())
        validator.validate(self.root)

    def test_old_workflow_contract_rejected(self):
        self.change_metadata(".github/agents/contracts/workflow.md", version=2)
        self.invalid("Expected workflow contract version 3")

    def test_ticket_intake_cannot_gain_mutation_permissions(self):
        relative = ".github/agents/contracts/ticket-context.md"
        original = (self.root / relative).read_text(encoding="utf-8")
        for updates, expected in (
            ({"jira_access": "read-write"}, "must be read-only"),
            ({"repository_writes": True}, "must not write repository"),
            ({"repository_writes": "false"}, "must not write repository"),
            ({"mode": "implement"}, "must be context-only"),
            ({"executor": "Explorer"}, "must use Implementer"),
        ):
            with self.subTest(updates=updates):
                (self.root / relative).write_text(original, encoding="utf-8")
                self.change_metadata(relative, **updates)
                self.invalid(expected)

    def test_instance_configuration_cannot_enter_public_contract_metadata(self):
        self.change_metadata(".github/agents/contracts/ticket-context.md",
                             base_url="https://example.invalid")
        self.invalid("Unexpected ticket-context metadata")

    def test_ticket_results_cannot_claim_completion(self):
        self.change_metadata(".github/agents/contracts/ticket-context.md",
                             results=["FETCHED", "PARTIAL", "BLOCKED", "DONE"])
        self.invalid("Invalid ticket-context results")

    def test_unrecognized_external_skill_rejected(self):
        self.change_metadata(".github/agents/contracts/ticket-context.md",
                             external_skill="replacement")
        self.invalid("Expected external skill jira")

    def test_private_skill_directory_cannot_be_bundled(self):
        # Even an empty integration folder would invite accidental vendoring.
        (self.root / ".github/skills/jira").mkdir()
        self.invalid("External Jira skill must remain outside")

    def test_ticket_prompt_cannot_override_model_or_tools(self):
        relative = ".github/prompts/implement-ticket.prompt.md"
        original = (self.root / relative).read_text(encoding="utf-8")
        for key, value in (("tools", ["execute"]), ("model", "GPT-6 Luna")):
            with self.subTest(key=key):
                (self.root / relative).write_text(original, encoding="utf-8")
                self.change_metadata(relative, **{key: value})
                self.invalid("role override")

    def test_ticket_prompt_must_route_to_coordinator(self):
        self.change_metadata(".github/prompts/implement-ticket.prompt.md",
                             agent="Implementer")
        self.invalid("prompt must use Orchestrator")

    def test_ticket_contract_reference_required_on_intake_role(self):
        path = self.root / ".github/agents/implementer.agent.md"
        path.write_text(path.read_text(encoding="utf-8").replace(
            "(contracts/ticket-context.md)", "(contracts/missing-ticket.md)"),
            encoding="utf-8")
        self.invalid("missing ticket-context contract reference")

    def test_orchestrator_cannot_gain_file_or_terminal_tools(self):
        for tool in ("read", "search", "edit", "execute"):
            with self.subTest(tool=tool):
                self.agent("orchestrator", tools=["agent", tool])
                self.invalid("unexpected tool permissions")

    def test_reviewer_cannot_edit(self):
        self.agent("reviewer", tools=["read", "search", "execute", "edit"])
        self.invalid("unexpected tool permissions")

    def test_explorer_cannot_execute(self):
        self.agent("explorer", tools=["read", "search", "execute"])
        self.invalid("unexpected tool permissions")

    def test_duplicate_tools_rejected(self):
        self.agent("explorer", tools=["read", "search", "read"])
        self.invalid("duplicate entries")

    def test_unknown_primary_model_rejected(self):
        self.agent("explorer", model="Unknown Model")
        self.invalid("expected primary model")

    def test_each_role_rejects_previous_model_policy(self):
        previous = {
            "orchestrator": "GPT-5.6 Sol",
            "explorer": "GPT-5.6 Luna",
            "reviewer": "GPT-5.6 Terra",
            "deep-reviewer": "GPT-5.6 Sol",
        }
        for role, old_model in previous.items():
            with self.subTest(role=role):
                self.agent(role, model=old_model)
                self.invalid("expected primary model")
                self.agent(role, model=validator.ROLES[role][2])

    def test_malformed_model_values_rejected(self):
        for value in (None, 5, [], {}, ["GPT-6 Luna", 42]):
            with self.subTest(value=value):
                self.agent("explorer", model=value)
                self.invalid("string list|one primary")

    def test_single_model_list_supported(self):
        self.agent("explorer", model=["GPT-6 Luna"])
        validator.validate(self.root)

    def test_unapproved_fallback_rejected(self):
        self.agent("explorer", model=["GPT-6 Luna", "Claude Sonnet 5"])
        self.invalid("fallback has not been approved")

    def test_duplicate_and_excessive_fallbacks_rejected(self):
        for value in (
            ["GPT-6 Luna", "GPT-6 Luna"],
            ["GPT-6 Luna", "Claude Sonnet 5", "GPT-6 Sol"],
        ):
            with self.subTest(value=value):
                self.agent("explorer", model=value)
                self.invalid("duplicate entries|at most one fallback")

    def test_explicitly_approved_compatible_fallback_supported(self):
        # This test-only policy does not approve a production fallback.
        self.agent("explorer", model=["GPT-6 Luna", "GPT-5.4 mini"])
        with patch.dict(validator.APPROVED_FALLBACKS, {"explorer": ("GPT-5.4 mini",)}):
            with patch.dict(validator.MODEL_TIERS, {"GPT-5.4 mini": 0}):
                validator.validate(self.root)

    def test_fallback_requires_known_tier(self):
        self.agent("explorer", model=["GPT-6 Luna", "Untested Tier"])
        with patch.dict(validator.APPROVED_FALLBACKS, {"explorer": ("Untested Tier",)}):
            self.invalid("unknown model tier")

    def test_parent_fallback_must_support_entire_child_chain(self):
        self.agent("orchestrator", model=["Claude Opus 5.5", "Claude Sonnet 5"])
        with patch.dict(validator.APPROVED_FALLBACKS, {"orchestrator": ("Claude Sonnet 5",)}):
            self.invalid("exceeds a possible parent cost tier")

    def test_powerful_parent_fallback_supports_opus_child(self):
        # Equal categories permit routing even when their token prices differ.
        # This fixture does not approve a production fallback or runtime availability.
        self.agent("orchestrator", model=["Claude Opus 5.5", "GPT-6 Sol"])
        with patch.dict(validator.APPROVED_FALLBACKS, {"orchestrator": ("GPT-6 Sol",)}):
            validator.validate(self.root)

    def test_implementer_fallback_cannot_match_reviewer(self):
        self.agent("implementer", model=["Claude Sonnet 5", "GPT-6 Sol"])
        with patch.dict(validator.APPROVED_FALLBACKS, {"implementer": ("GPT-6 Sol",)}):
            self.invalid("must differ from every possible implementer model")

    def test_implementer_fallback_cannot_match_deep_reviewer(self):
        self.agent("implementer", model=["Claude Sonnet 5", "Claude Opus 5.5"])
        with patch.dict(validator.APPROVED_FALLBACKS,
                        {"implementer": ("Claude Opus 5.5",)}):
            self.invalid("deep-reviewer: model must differ from every possible implementer model")

    def test_nested_delegation_rejected(self):
        self.agent("explorer", agents=["Implementer"])
        self.invalid("nested delegation must be disabled")

    def test_allowlist_cannot_include_generic_agent(self):
        self.agent("orchestrator", agents=["Explorer", "Implementer", "Reviewer", "Agent"])
        self.invalid("invalid delegation allowlist")

    def test_children_hidden_and_delegatable(self):
        for updates, expected in (
            ({"user-invocable": True}, "must be hidden"),
            ({"user-invocable": False, "disable-model-invocation": True}, "must allow delegation"),
        ):
            with self.subTest(updates=updates):
                self.agent("explorer", **updates)
                self.invalid(expected)

    def test_orchestrator_cannot_be_invoked_as_subagent(self):
        self.agent("orchestrator", **{"disable-model-invocation": False})
        self.invalid("must not be a subagent")

    def test_unexpected_nested_agent_rejected(self):
        path = self.root / ".github/agents/contracts/extra.agent.md"
        path.write_text("Unexpected role", encoding="utf-8")
        self.invalid("exactly the five")

    def test_unreviewed_agent_hooks_rejected(self):
        self.agent("reviewer", hooks={"postToolUse": []})
        self.invalid("unexpected agent metadata")

    def test_prompt_cannot_override_tools_or_model(self):
        relative = ".github/prompts/implement-feature.prompt.md"
        original = (self.root / relative).read_text(encoding="utf-8")
        for key, value in (("tools", ["execute"]), ("model", "GPT-6 Luna")):
            with self.subTest(key=key):
                (self.root / relative).write_text(original, encoding="utf-8")
                self.change_metadata(relative, **{key: value})
                self.invalid("role override")

    def test_duplicate_yaml_keys_rejected(self):
        path = self.root / ".github/agents/explorer.agent.md"
        content = path.read_text(encoding="utf-8")
        path.write_text(content.replace("model: GPT-6 Luna",
                                       "model: GPT-6 Luna\nmodel: GPT-6 Sol"),
                        encoding="utf-8")
        self.invalid("Duplicate key: model")

    def test_empty_body_rejected(self):
        path = self.root / ".github/agents/explorer.agent.md"
        path.write_text("---\nname: Explorer\n---\n   \n", encoding="utf-8")
        self.invalid("empty instructions")

    def test_nonmapping_frontmatter_rejected(self):
        path = self.root / ".github/agents/explorer.agent.md"
        path.write_text("---\n- invalid\n---\nBody\n", encoding="utf-8")
        self.invalid("metadata must be a mapping")

    def test_deep_results_cannot_approve_entire_change(self):
        self.change_metadata(
            ".github/agents/contracts/workflow.md",
            deep_results=["CONFIRMED", "REFUTED", "UNRESOLVED", "APPROVED"],
        )
        self.invalid("Invalid contract deep_results")

    def test_contract_reference_required(self):
        path = self.root / ".github/agents/reviewer.agent.md"
        path.write_text(path.read_text(encoding="utf-8").replace(
            "(contracts/workflow.md)", "(contracts/missing.md)"), encoding="utf-8")
        self.invalid("missing shared workflow contract reference")

    def test_broken_documentation_link_rejected(self):
        path = self.root / "docs/demo.md"
        with path.open("a", encoding="utf-8") as stream:
            stream.write("\n[Missing](does-not-exist.md)\n")
        self.invalid("broken link")

    def test_empty_instruction_glob_rejected(self):
        self.change_metadata(".github/instructions/backend.instructions.md", applyTo="**/*.py,")
        self.invalid("empty applyTo glob")

    def test_duplicate_settings_rejected(self):
        path = self.root / ".vscode/settings.json"
        path.write_text('{"chat.tools.terminal.enableAutoApprove": false,'
                        '"chat.tools.terminal.enableAutoApprove": true}', encoding="utf-8")
        self.invalid("Duplicate key")

    def test_permission_settings_cannot_be_enabled(self):
        for key in (
            "chat.tools.terminal.enableAutoApprove",
            "chat.subagents.allowInvocationsFromSubagents",
        ):
            with self.subTest(key=key):
                settings = {
                    "chat.tools.terminal.enableAutoApprove": False,
                    "chat.subagents.allowInvocationsFromSubagents": False,
                    "chat.subagents.showCreditUsage": True,
                }
                settings[key] = True
                (self.root / ".vscode/settings.json").write_text(
                    json.dumps(settings), encoding="utf-8")
                self.invalid("must remain false")

    def test_credit_visibility_requires_boolean_true(self):
        path = self.root / ".vscode/settings.json"
        settings = json.loads(path.read_text(encoding="utf-8"))
        for value in (False, "true", 1, None):
            with self.subTest(value=value):
                settings["chat.subagents.showCreditUsage"] = value
                path.write_text(json.dumps(settings), encoding="utf-8")
                self.invalid("showCreditUsage must be true")

    def test_benchmark_row_width_checked(self):
        path = self.root / "docs/benchmark-results.csv"
        with path.open("a", encoding="utf-8") as stream:
            stream.write("incomplete,row\n")
        self.invalid("wrong column count")

    def test_blocked_review_is_valid_benchmark_result(self):
        path = self.root / "docs/benchmark-results.csv"
        with path.open(encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(stream)
            fields, rows = reader.fieldnames, list(reader)
        rows[0].update(review_verdict="BLOCKED", status="BLOCKED")
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        validator.validate(self.root)


if __name__ == "__main__":
    unittest.main()
