---
name: implement-feature
description: Implement a scoped feature with reusable context, validation, and independent review.
agent: Orchestrator
argument-hint: Describe the feature, acceptance criteria, and compatibility constraints.
---

Implement the feature in the user's message and attached context.
If the requested feature is identified by a Jira ticket reference, first use Orchestrator's external ticket intake route; do not invent its requirements or require a second user request through another prompt.
Follow Orchestrator's routing: scoped [feature-analysis](../skills/feature-analysis/SKILL.md) through Explorer unless an eligible complete current brief already exists. Parallelize independent backend/frontend research only when useful.
Version the Task Brief, preserve API compatibility/exclusions, agree required checks, then coordinate one writer, validation, independent review and budgeted escalation/recovery.
If no feature is supplied, ask for the desired behavior before delegating. Finish with criterion evidence, reviewed revision, validation results and the coordinator's final status.
