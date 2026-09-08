"""Validate the v1 Copilot configuration contract; does not invoke Copilot."""

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    raise SystemExit("Install validation dependencies: python -m pip install -r requirements-dev.txt")


ROOT = Path(__file__).resolve().parents[1]
ROLES = {
    "orchestrator": ("Orchestrator", {"agent", "read", "search"}),
    "explorer": ("Explorer", {"read", "search"}),
    "implementer": ("Implementer", {"read", "search", "edit", "execute"}),
    "reviewer": ("Reviewer", {"read", "search", "execute"}),
    "deep-reviewer": ("Deep Reviewer", {"read", "search", "execute"}),
}
SKILLS = {"feature-analysis", "bug-investigation", "run-validation", "code-review"}
PROMPTS = {"implement-feature", "investigate-bug", "review-change"}


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate keys rather than silently accepting the final value."""


def unique_mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if key in result:
            raise ValueError(f"Duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node)
    return result


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


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


def validate(root):
    github = root / ".github"
    agent_dir = github / "agents"
    require(
        {p.name for p in agent_dir.glob("*.md")}
        == {f"{slug}.agent.md" for slug in ROLES},
        "Expected exactly the five v1 agent files",
    )
    names = {name for name, _ in ROLES.values()}
    for slug, (name, tools) in ROLES.items():
        data = frontmatter(agent_dir / f"{slug}.agent.md")
        require(data.get("name") == name, f"{slug}: wrong agent name")
        require(nonempty_string(data.get("description")), f"{slug}: missing description")
        require(nonempty_string(data.get("model")), f"{slug}: explicit model required")
        declared = data.get("tools")
        require(isinstance(declared, list) and all(isinstance(t, str) for t in declared), f"{slug}: tools must be a string list")
        require(set(declared) == tools and len(declared) == len(tools), f"{slug}: unexpected tool permissions")
        if slug == "orchestrator":
            children = data.get("agents")
            require(isinstance(children, list) and all(isinstance(a, str) for a in children), "Orchestrator: agents must be a string list")
            require(set(children) == names - {name} and len(children) == 4, "Orchestrator: invalid delegation allowlist")
            require(data.get("user-invocable") is True, "Orchestrator must be user-invocable")
            require(data.get("disable-model-invocation") is True, "Orchestrator must not be a subagent")
        else:
            require(data.get("agents") == [], f"{slug}: nested delegation must be disabled")
            require(data.get("user-invocable") is False, f"{slug}: must be hidden from picker")
            require(data.get("disable-model-invocation", False) is False, f"{slug}: must allow delegation")

    skill_paths = list((github / "skills").glob("*/SKILL.md"))
    require({p.parent.name for p in skill_paths} == SKILLS, "Expected four v1 skills")
    for path in skill_paths:
        data = frontmatter(path)
        require(data.get("name") == path.parent.name, f"{path}: skill name must match directory")
        require(set(data) == {"name", "description"}, f"{path}: unexpected skill metadata")
        require(nonempty_string(data.get("description")) and len(data["description"]) <= 1024, f"{path}: invalid description")

    prompt_paths = list((github / "prompts").glob("*.prompt.md"))
    require({p.name.removesuffix(".prompt.md") for p in prompt_paths} == PROMPTS, "Expected three v1 prompts")
    for path in prompt_paths:
        data = frontmatter(path)
        require(data.get("agent") == "Orchestrator", f"{path}: prompt must use Orchestrator")
        require(data.get("name") == path.name.removesuffix(".prompt.md"), f"{path}: prompt name mismatch")
        require(nonempty_string(data.get("description")), f"{path}: missing description")
        require("tools" not in data and "model" not in data, f"{path}: prompt must not override role tools/model")

    instruction_dir = github / "instructions"
    require(
        {p.name for p in instruction_dir.glob("*.instructions.md")}
        == {f"{name}.instructions.md" for name in ("backend", "frontend", "tests")},
        "Expected backend, frontend, and tests instructions",
    )
    for path in instruction_dir.glob("*.instructions.md"):
        data = frontmatter(path)
        require(nonempty_string(data.get("applyTo")), f"{path}: missing applyTo glob")
        require(all(part.strip() for part in data["applyTo"].split(",")), f"{path}: empty applyTo glob")
    require(bool((github / "copilot-instructions.md").read_text(encoding="utf-8").strip()), "Missing repository instructions")

    for path in github.rglob("*.md"):
        for target in re.findall(r"\[[^\]]+\]\(([^\s)]+)\)", path.read_text(encoding="utf-8")):
            if "://" not in target and not target.startswith("#"):
                require((path.parent / target.split("#", 1)[0]).exists(), f"{path}: broken link to {target}")

    settings = json.loads((root / ".vscode/settings.json").read_text(encoding="utf-8"))
    for key in ("chat.tools.terminal.enableAutoApprove", "chat.subagents.allowInvocationsFromSubagents"):
        require(settings.get(key) is False, f"{key} must remain false for v1")


if __name__ == "__main__":
    try:
        validate(ROOT)
    except (OSError, ValueError, TypeError, yaml.YAMLError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
    print("PASS: 5 agents, 4 skills, 3 prompts, 3 path instructions, role boundaries, links, and settings")
    print("Model availability and Copilot runtime behavior require a VS Code smoke test.")
