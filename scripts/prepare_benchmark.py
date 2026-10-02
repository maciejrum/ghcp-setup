"""Create fresh A/B incident benchmark applications without touching existing runs."""

import argparse
import hashlib
import json
import random
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IGNORED = {".git", "node_modules", ".venv", "__pycache__", ".pytest_cache", "dist", ".DS_Store",
           "test-results", "playwright-report"}
VARIANTS = {"A": "A-standard", "B": "B-team"}


def copy_tree(source, destination):
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns(*IGNORED))


def inventory(directory):
    return {
        path.relative_to(directory).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(directory.rglob("*"))
        if path.is_file() and not any(part in IGNORED for part in path.relative_to(directory).parts)
    }


def digest(files):
    return hashlib.sha256(json.dumps(files, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def common_instructions(source):
    text = (source / ".github/copilot-instructions.md").read_text(encoding="utf-8")
    marker = "# Development workflow"
    if marker not in text:
        raise ValueError("The common instruction file has no development-workflow section")
    body = text[text.index(marker):].replace(
        "Use the relevant skills in `.github/skills/` on demand. Skills describe procedures; "
        "they do not grant tools or change an agent's role.\n", "",
    )
    if ".github/skills" in body:
        raise ValueError("Common instructions cannot advertise team skills unavailable in A")
    return (
        "# Project architecture\n\n"
        "- This workspace contains the incident-dashboard application: `backend/` is FastAPI and "
        "`frontend/` is React/Vite/TypeScript. Use their existing architecture and manifests.\n"
        "- The root `README.md` documents local setup and required validation commands. "
        "Application dependencies and seeded tenant data are fixed for this task.\n"
        "- Prefer minimal changes; never modify unrelated code or overwrite pre-existing user changes.\n\n"
        + body
    )


def initialize_git(workspace):
    subprocess.run(["git", "init", "--quiet", str(workspace)], check=True)
    disabled_hooks = workspace / ".git/benchmark-disabled-hooks"
    disabled_hooks.mkdir()
    subprocess.run(["git", "-C", str(workspace), "add", "."], check=True)
    subprocess.run([
        "git", "-C", str(workspace), "-c", "user.name=Benchmark baseline",
        "-c", "user.email=benchmark@local.invalid", "-c", "commit.gpgsign=false",
        "-c", f"core.hooksPath={disabled_hooks}", "commit", "--quiet", "-m", "Benchmark baseline",
    ], check=True)
    return subprocess.check_output(["git", "-C", str(workspace), "rev-parse", "HEAD"], text=True).strip()


def prepare(destination, source=ROOT, init_git=False, order=None):
    destination = Path(destination).expanduser().absolute()
    source = Path(source).resolve()
    fixture = source / "benchmark/fixture"
    if not fixture.is_dir():
        raise ValueError(f"Fixture is missing: {fixture}")
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"Destination already exists: {destination}")
    if destination.resolve().is_relative_to(source):
        raise ValueError("Destination must be outside the source repository to preserve isolation")
    # Exclusive creation also rejects a symlink or an existing empty directory.
    destination.mkdir(parents=True, exist_ok=False)
    try:
        shared_text = common_instructions(source)
        workspaces = {}
        for key, name in VARIANTS.items():
            workspace = destination / name
            copy_tree(fixture, workspace)
            github = workspace / ".github"
            github.mkdir(exist_ok=True)
            (github / "copilot-instructions.md").write_text(shared_text, encoding="utf-8")
            copy_tree(source / ".github/instructions", github / "instructions")
            if (source / ".vscode").is_dir():
                copy_tree(source / ".vscode", workspace / ".vscode")
            if key == "B":
                copy_tree(source / ".github/agents", github / "agents")
                copy_tree(source / ".github/skills", github / "skills")
            files = inventory(workspace)
            commit = initialize_git(workspace) if init_git else None
            workspaces[key] = {
                "directory": name, "inventory": files, "baseline_sha256": digest(files),
                "baseline_commit": commit,
                "mode": "standard Agent" if key == "A" else "Orchestrator",
                "requested_parent_model": "Claude Opus 5.5",
            }
        fixture_files = inventory(fixture)
        config_files = inventory(source / ".github")
        assessor_files = inventory(source / "benchmark/assessor")
        protocol_files = {
            f"benchmark/{name}": hashlib.sha256((source / "benchmark" / name).read_bytes()).hexdigest()
            for name in ("task.md", "quality-rubric.md")
        }
        common_files = {
            name: checksum for name, checksum in workspaces["A"]["inventory"].items()
            if name.startswith((".github/", ".vscode/"))
        }
        execution_order = order or random.SystemRandom().choice(("AB", "BA"))
        if execution_order not in ("AB", "BA"):
            raise ValueError("Order must be AB or BA")
        manifest = {
            "protocol_version": 1, "task_id": "incident-status", "experiment": "package-v4",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "execution_order": list(execution_order),
            "fixture_inventory": fixture_files, "fixture_sha256": digest(fixture_files),
            "source_configuration_sha256": digest(config_files),
            "common_configuration_sha256": digest(common_files),
            "assessor_inventory": assessor_files, "assessor_sha256": digest(assessor_files),
            "protocol_inventory": protocol_files, "protocol_sha256": digest(protocol_files),
            "variants": workspaces,
            "comparison": "Common parent model; B additionally has custom role/model routing and team skills. "
                          "This measures the workflow/model-policy package, not orchestration alone.",
            "measurement": "No runs, time, credit consumption, or quality outcomes have been measured by preparation.",
        }
        (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        return manifest
    except BaseException:
        # Only remove the directory that this invocation created exclusively.
        shutil.rmtree(destination)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, required=True,
                        help="A new directory, normally /private/tmp/ghcp-benchmark-r1")
    parser.add_argument("--init-git", action="store_true",
                        help="Explicitly create local baseline commits in the two new fixture repositories")
    parser.add_argument("--order", choices=("AB", "BA"),
                        help="Record a preselected order; otherwise randomize the pair")
    args = parser.parse_args()
    try:
        manifest = prepare(args.destination, init_git=args.init_git, order=args.order)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Preparation failed: {error}\n")
    print(f"Prepared {args.destination.absolute()}")
    print(f"Execution order: {' then '.join(manifest['execution_order'])}")
    print("See manifest.json for frozen baseline hashes. No measurements have been generated.")


if __name__ == "__main__":
    main()
