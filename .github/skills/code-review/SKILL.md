---
name: code-review
description: Independently inspect scoped changes and reproducible evidence, returning actionable findings for the identified revision.
---

# Code review

1. Establish requirements, criteria and review boundary: working tree or explicit base/head. Never guess a branch and claim full coverage. Verify revision evidence; if ambiguity prevents reliable review, identify missing input.
2. Inspect actual changes and surrounding callers/contracts/tests before evaluating the implementer's narrative. Include staged, unstaged and relevant untracked/new/deleted files; distinguish pre-existing work.
3. Trace meaningful success/failure paths: compatibility, authorization, validation, errors, state/cache transitions, transactions, types and regression coverage. Review tests' assertions and coverage, not only their reported result.
4. Assess command evidence against current code/configuration/environment. Use focused execution only when it resolves uncertainty and your tools allow it. Missing required evidence is a blocker, not proof of a code defect.
5. Report only actionable code-backed or reproducible findings with stable IDs, severity, location, trigger, impact, evidence and correction. Separate confirmed defects from unresolved concerns.
6. Use the [workflow contract](../../agents/contracts/workflow.md) as the source for severity, decision precedence, verdicts and completion rules. Reviewer returns a full review verdict; Deep Reviewer returns only CONFIRMED/REFUTED/UNRESOLVED for its assigned question.

Never edit, auto-fix, regenerate snapshots or modify dependencies during review. Do not manufacture issues, block on stylistic preferences or treat an implementer's summary as independent evidence. Approval applies to the reviewed state; after changes, assess the full current task scope while reusing still-valid evidence.
