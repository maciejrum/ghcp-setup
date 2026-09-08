---
name: implement-feature
description: Implement a scoped feature with analysis, validation, and independent review.
agent: Orchestrator
argument-hint: Describe the feature, acceptance criteria, and compatibility constraints.
---

Implement the feature described in the user's message and attached context.
Use [feature-analysis](../skills/feature-analysis/SKILL.md) through Explorer, then coordinate implementation, validation, independent review, and justified escalation.
Preserve explicit API compatibility and scope constraints. If no feature is supplied, ask for the desired behavior before delegating.
Finish with the coordinator's final report, including validation evidence and review verdict.

