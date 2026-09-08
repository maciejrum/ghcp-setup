---
name: run-validation
description: Select and run focused tests, lint, and type checks for changed code, reporting reproducible commands and distinguishing failures from checks not run.
---

# Run validation

1. Identify the changed behavior, affected applications, and required checks. Read manifests, lockfiles, test configuration, and contributor documentation for the actual package manager and commands.
2. Check that commands target local test resources and do not invoke production services, destructive setup, auto-fix, or snapshot updates. Respect approval prompts. If execution is unavailable in your role, provide a validation plan to the coordinator.
3. Run the smallest relevant tests first in non-watch mode. For a bug fix, demonstrate the regression when practical without overwriting user changes to recreate a baseline.
4. Run configured lint/type checks for affected areas and required integration checks. Expand testing when contracts, shared code, or failures justify it. Avoid repeating passing runs without new evidence.
5. Classify failures as caused by the change, pre-existing (with evidence), or environmental. The implementer fixes introduced failures; reviewers report them without editing.
6. Inspect unexpected tracked changes from tooling; report them and never discard user changes automatically.

Record each command with working directory, exit status, and concise result. Use PASS, FAIL, or NOT RUN; record missing dependencies, services, permissions, or configuration explicitly. Missing required checks block completion.

For this configuration-only repository, use `python scripts/validate_config.py` after installing `requirements-dev.txt`. This validates configuration structure and role constraints; it does not run Copilot or validate a consuming application. In application repositories use their own configured test/lint/typecheck commands.

