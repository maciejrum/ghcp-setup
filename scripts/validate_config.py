"""Validate the v2 static contract; runtime behavior needs the VS Code scenarios."""

import csv
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    raise SystemExit("Install dependencies: python -m pip install -r requirements-dev.txt")


ROOT = Path(__file__).resolve().parents[1]
ROLES = {
    "orchestrator": ("Orchestrator", {"agent"}, "GPT-5.6 Sol"),
    "explorer": ("Explorer", {"read", "search"}, "GPT-5.6 Luna"),
    "implementer": ("Implementer", {"read", "search", "edit", "execute"}, "Claude Sonnet 5"),
    "reviewer": ("Reviewer", {"read", "search", "execute"}, "GPT-5.6 Terra"),
    "deep-reviewer": ("Deep Reviewer", {"read", "search", "execute"}, "GPT-5.6 Sol"),
}
# No fallback has been smoke-tested for this template. Add at most one per role
# after the runtime checks, with its verified tier. Do not infer tiers from prices.
APPROVED_FALLBACKS = {slug: () for slug in ROLES}
MODEL_TIERS = {
    "GPT-5.6 Luna": 0,  # Lightweight
    "Claude Sonnet 5": 1,  # Versatile
    "GPT-5.6 Terra": 1,
    "GPT-5.6 Sol": 2,  # Powerful
}
SKILLS = {"feature-analysis", "bug-investigation", "run-validation", "code-review"}
PROMPTS = {"implement-feature", "investigate-bug", "review-change"}
CONTRACT_ENUMS = {
    "review_verdicts": {"APPROVED", "CHANGES REQUIRED", "DEEP REVIEW REQUIRED", "BLOCKED"},
    "deep_results": {"CONFIRMED", "REFUTED", "UNRESOLVED"},
    "final_statuses": {"DONE", "INVESTIGATED", "REVIEWED", "BLOCKED"},
    "check_results": {"PASS", "FAIL", "NOT_RUN"},
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate key: {key}")
        result[key] = value
    return result


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate YAML keys instead of silently keeping the last value."""


def unique_mapping(loader, node):
    return unique_pairs(
        (loader.construct_object(key), loader.construct_object(value))
        for key, value in node.value
    )


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
)


def frontmatter(path):
    content = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n(.+)\Z", content, re.DOTALL)
    require(match is not None, f"{path.name}: missing frontmatter or body")
    metadata = yaml.load(match.group(1), Loader=UniqueKeyLoader)
    require(isinstance(metadata, dict), f"{path.name}: metadata must be a mapping")
    require(bool(match.group(2).strip()), f"{path.name}: empty instructions")
    return metadata


def nonempty_string(value):
    return isinstance(value, str) and bool(value.strip())


def string_list(value, label):
    require(
        isinstance(value, list) and all(nonempty_string(item) for item in value),
        f"{label}: expected a string list",
    )
    require(len(value) == len(set(value)), f"{label}: duplicate entries")
    return value


def validate_models(slug, value):
    models = [value] if isinstance(value, str) else value
    models = string_list(models, f"{slug}: model")
    require(1 <= len(models) <= 2, f"{slug}: one primary and at most one fallback")
    primary = ROLES[slug][2]
    require(models[0] == primary, f"{slug}: expected primary model {primary}")
    require(
        all(model in APPROVED_FALLBACKS[slug] for model in models[1:]),
        f"{slug}: fallback has not been approved",
    )
    require(all(model in MODEL_TIERS for model in models), f"{slug}: unknown model tier")
    return models


def validate_links(root):
    paths = [root / "README.md", *sorted((root / ".github").rglob("*.md")),
             *sorted((root / "docs").rglob("*.md"))]
    for path in paths:
        content = path.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]+\]\(([^\s)]+)\)", content):
            if "://" in target or target.startswith("#"):
                continue
            destination = (path.parent / target.split("#", 1)[0]).resolve()
            require(destination.is_relative_to(root.resolve()), f"{path}: link outside repository")
            require(destination.exists(), f"{path}: broken link to {target}")


def validate_benchmark(root, contract):
    path = root / "docs/benchmark-results.csv"
    with path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.reader(stream))
    require(bool(rows), "Empty benchmark CSV")
    header = rows[0]
    require(len(header) == len(set(header)), "Duplicate benchmark columns")
    required = {
        "task_id", "variant", "run", "experiment", "models", "requested_models",
        "resolved_models", "routing_violations", "tool_calls", "redundant_reads",
        "delegations", "input_tokens", "output_tokens", "recovery_attempts",
        "deep_reviews", "remaining_defects", "accepted", "trace_ref",
        "tests", "review_verdict", "status",
    }
    require(required <= set(header), "Missing v2 benchmark columns")
    for number, values in enumerate(rows[1:], 2):
        require(len(values) == len(header), f"Benchmark row {number}: wrong column count")
        row = dict(zip(header, values))
        require(
            row["review_verdict"] in set(contract["review_verdicts"]) | {"NOT_RUN"},
            f"Benchmark row {number}: invalid review verdict",
        )
        require(row["status"] in {"NOT_RUN", "DONE", "FAILED", "BLOCKED"},
                f"Benchmark row {number}: invalid status")
        require(row["tests"] in {"PASS", "FAIL", "NOT_RUN", "PARTIAL"},
                f"Benchmark row {number}: invalid tests result")
        require(row["accepted"] in {"", "YES", "NO"},
                f"Benchmark row {number}: invalid acceptance result")


def validate(root):
    root = Path(root)
    github = root / ".github"
    agent_dir = github / "agents"
    require(
        {p.relative_to(agent_dir).as_posix() for p in agent_dir.rglob("*.agent.md")}
        == {f"{slug}.agent.md" for slug in ROLES},
        "Expected exactly the five v2 agent files",
    )
    require(
        {p.name for p in agent_dir.glob("*.md")} == {f"{slug}.agent.md" for slug in ROLES},
        "Unexpected top-level agent document",
    )
    contract_path = agent_dir / "contracts/workflow.md"
    contract = frontmatter(contract_path)
    require(set(contract) == {"version", *CONTRACT_ENUMS}, "Unexpected contract metadata")
    require(type(contract["version"]) is int and contract["version"] == 2,
            "Expected workflow contract version 2")
    for key, expected in CONTRACT_ENUMS.items():
        require(set(string_list(contract[key], key)) == expected, f"Invalid contract {key}")

    names = {name for name, _, _ in ROLES.values()}
    selected_models = {}
    for slug, (name, tools, _) in ROLES.items():
        path = agent_dir / f"{slug}.agent.md"
        data = frontmatter(path)
        allowed = {
            "name", "description", "model", "tools", "agents",
            "user-invocable", "disable-model-invocation",
        }
        require(set(data) <= allowed, f"{slug}: unexpected agent metadata")
        require(data.get("name") == name, f"{slug}: wrong agent name")
        require(nonempty_string(data.get("description")), f"{slug}: missing description")
        selected_models[slug] = validate_models(slug, data.get("model"))
        declared = string_list(data.get("tools"), f"{slug}: tools")
        require(set(declared) == tools, f"{slug}: unexpected tool permissions")
        # Check the structural reference, not whether prose will be obeyed.
        require(
            "(contracts/workflow.md)" in path.read_text(encoding="utf-8"),
            f"{slug}: missing shared workflow contract reference",
        )
        if slug == "orchestrator":
            children = string_list(data.get("agents"), "Orchestrator: agents")
            require(set(children) == names - {name}, "Orchestrator: invalid delegation allowlist")
            require(data.get("user-invocable") is True, "Orchestrator must be user-invocable")
            require(data.get("disable-model-invocation") is True,
                    "Orchestrator must not be a subagent")
        else:
            require(data.get("agents") == [], f"{slug}: nested delegation must be disabled")
            require(data.get("user-invocable") is False, f"{slug}: must be hidden from picker")
            require(data.get("disable-model-invocation", False) is False,
                    f"{slug}: must allow delegation")

    parent_floor = min(MODEL_TIERS[model] for model in selected_models["orchestrator"])
    for slug, models in selected_models.items():
        require(all(MODEL_TIERS[model] <= parent_floor for model in models),
                f"{slug}: model exceeds a possible parent cost tier")
    for role in ("reviewer", "deep-reviewer"):
        require(
            set(selected_models["implementer"]).isdisjoint(selected_models[role]),
            f"{role}: model must differ from every possible implementer model",
        )

    skill_paths = list((github / "skills").glob("*/SKILL.md"))
    require({p.parent.name for p in skill_paths} == SKILLS, "Expected four v2 skills")
    for path in skill_paths:
        data = frontmatter(path)
        require(data.get("name") == path.parent.name, f"{path}: skill name must match directory")
        require(set(data) == {"name", "description"}, f"{path}: unexpected skill metadata")
        require(nonempty_string(data.get("description")) and len(data["description"]) <= 1024,
                f"{path}: invalid description")

    prompt_paths = list((github / "prompts").glob("*.prompt.md"))
    require({p.name.removesuffix(".prompt.md") for p in prompt_paths} == PROMPTS,
            "Expected three v2 prompts")
    for path in prompt_paths:
        data = frontmatter(path)
        require(set(data) <= {"name", "description", "agent", "argument-hint"},
                f"{path}: unexpected prompt metadata or role override")
        require(data.get("agent") == "Orchestrator", f"{path}: prompt must use Orchestrator")
        require(data.get("name") == path.name.removesuffix(".prompt.md"),
                f"{path}: prompt name mismatch")
        require(nonempty_string(data.get("description")), f"{path}: missing description")
        require(nonempty_string(data.get("argument-hint")), f"{path}: missing argument hint")

    instruction_dir = github / "instructions"
    require(
        {p.name for p in instruction_dir.glob("*.instructions.md")}
        == {f"{name}.instructions.md" for name in ("backend", "frontend", "tests")},
        "Expected backend, frontend, and tests instructions",
    )
    for path in instruction_dir.glob("*.instructions.md"):
        data = frontmatter(path)
        require(set(data) == {"applyTo"}, f"{path}: unexpected instruction metadata")
        require(nonempty_string(data.get("applyTo")), f"{path}: missing applyTo glob")
        parts = data["applyTo"].split(",")
        require(all(part.strip() for part in parts), f"{path}: empty applyTo glob")
    require(bool((github / "copilot-instructions.md").read_text(encoding="utf-8").strip()),
            "Missing repository instructions")

    settings = json.loads(
        (root / ".vscode/settings.json").read_text(encoding="utf-8"),
        object_pairs_hook=unique_pairs,
    )
    require(isinstance(settings, dict), "Settings must be a JSON object")
    for key in ("chat.tools.terminal.enableAutoApprove", "chat.subagents.allowInvocationsFromSubagents"):
        require(settings.get(key) is False, f"{key} must remain false for v2")

    validate_links(root)
    validate_benchmark(root, contract)


if __name__ == "__main__":
    try:
        validate(ROOT)
    except (OSError, ValueError, TypeError, yaml.YAMLError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
    print("PASS: v2 roles, model policy, protocol enums, skills, prompts, links, settings, benchmark")
    print("Prose effectiveness, model availability and Copilot behavior require VS Code scenarios.")
