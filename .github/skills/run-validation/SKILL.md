---
name: run-validation
description: Verify an identified revision with focused checks, reusing applicable evidence and separating code defects from environmental blockers.
---

# Run validation

1. Start with the Task Brief's required checks and acceptance criteria. Reuse sourced commands when relevant configuration is unchanged; inspect manifests, dependencies or docs only for a gap, contradiction or invalidated source. Make required checks explicit before editing.
2. Verify revision/environment identity and that commands use local resources, non-watch mode and no destructive setup, production services, auto-fix or snapshot updates. Respect approvals. Roles without execution tools return the plan to the coordinator.
3. Run the smallest relevant tests first. Demonstrate a bug regression when practical without overwriting user changes to recreate the original state.
4. Run agreed lint/type/integration checks. Expand only when contracts, shared code or failures justify it. Reuse prior passes only for unchanged relevant inputs/environment, recording the reason. Independent review may rerun a check to resolve a specific uncertainty.
5. Classify failures as introduced, pre-existing with evidence, environmental or unknown. Implementer fixes confirmed introduced defects; reviewers report without editing. A required check unavailable or failing without a confirmed patch defect is BLOCKED, not a speculative repair request.
6. Apply the supplied retry budget only after checking partial completion and identifying a transient cause or changed prerequisite. Do not repeatedly execute identical failing commands. Inspect tooling side effects without discarding user work.

Return the validation records in the [workflow contract](../../agents/contracts/workflow.md): check/criterion IDs, revision, command, cwd, exit code, PASS/FAIL/NOT_RUN, classification, summary and evidence reference. Missing required checks block DONE; never silently reduce the agreed validation plan.

In this configuration-only repository, install requirements-dev.txt in an isolated environment, then run from the root:

```text
python scripts/validate_config.py
python -m unittest discover -s tests -v
```

These checks validate static configuration and its validator, not Copilot runtime or an application. In consuming applications use their own commands; these template maintenance scripts are not part of the copied agent configuration.
