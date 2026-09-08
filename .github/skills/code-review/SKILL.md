---
name: code-review
description: Review scoped code changes independently against requirements and actual diffs, producing evidence-backed findings, severity, and an actionable verdict.
---

# Code review

1. Establish the original request, acceptance criteria, and review boundary: working tree or explicit base/head. If a base is unknown, state what was inspected and request it when the ambiguity prevents reliable review. Never guess a branch and claim complete coverage.
2. Inspect the actual change and surrounding callers, contracts, and tests. For working-tree reviews include staged, unstaged, and untracked files in scope; distinguish pre-existing user work.
3. Trace changed behavior through relevant success and failure paths. Check compatibility, authorization, validation, errors, state/cache transitions, transactions, types, and regression coverage where applicable.
4. Assess validation evidence. Use focused execution only when needed and available; do not modify code, regenerate snapshots, or run auto-fix. Missing required validation is a blocker, not proof of a code defect.
5. Report only actionable findings backed by code or a reproducible scenario. Include severity, location, trigger, impact, evidence, and a recommended correction. Separate confirmed defects from unresolved concerns.

Severity:

- CRITICAL: exploitable security failure, data loss/corruption, or comparable severe impact.
- MAJOR: incorrect behavior, broken contract, significant regression, or missing coverage that leaves a material correctness risk.
- MINOR: a localized, non-blocking improvement with a concrete benefit.

Verdict:

- APPROVED when there are no blocking findings and required validation passed.
- CHANGES REQUIRED for confirmed blocking findings or missing/failed required checks.
- DEEP REVIEW REQUIRED for a serious unresolved concern needing deeper analysis; provide the precise question. An agent already performing deep review uses CHANGES REQUIRED for unresolved blockers.

Do not manufacture findings, block on stylistic preferences, or treat the implementer's summary as independent evidence. Approval applies only to the reviewed revision.

