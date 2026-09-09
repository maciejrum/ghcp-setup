---
name: review-change
description: Independently review a working-tree change or explicit diff without applying fixes.
agent: Orchestrator
argument-hint: Specify the change purpose and review scope, such as working tree or base/head.
---

Delegate independent [code-review](../skills/code-review/SKILL.md) directly to Reviewer.
Pass original requirements and explicit diff range when supplied; otherwise Reviewer inspects current working-tree changes, including relevant untracked files, and records the reviewed state. Do not guess a baseline or claim authorship of existing edits.
Escalate only a precise evidence-backed serious question within budget. A REFUTED deep concern returns to Reviewer for the full verdict; CONFIRMED findings are reported without fixes. Missing required evidence is BLOCKED.
Report inspected scope/revision, findings, validation and final verdict. With no changes, report REVIEWED with review_verdict NOT_RUN, not APPROVED. Do not delegate fixes without a user request.
