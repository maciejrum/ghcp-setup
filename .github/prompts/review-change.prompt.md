---
name: review-change
description: Independently review a working-tree change or explicit diff without applying fixes.
agent: Orchestrator
argument-hint: Specify the change purpose and review scope, such as working tree or base/head.
---

Coordinate an independent review of the requested change using [code-review](../skills/code-review/SKILL.md) through Reviewer.
Use the user's explicit diff range when supplied; otherwise inspect current working-tree changes and state that scope. Preserve pre-existing changes and include untracked files within scope.
Escalate only evidence-backed serious concerns to Deep Reviewer. Report findings, validation evidence, unresolved risks, and the final verdict. Do not delegate fixes unless the user asks for them. If there are no changes to inspect, report that fact rather than approving an empty review.

