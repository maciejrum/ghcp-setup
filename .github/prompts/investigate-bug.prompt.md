---
name: investigate-bug
description: Diagnose a bug and propose a minimal fix without implementing it unless requested.
agent: Orchestrator
argument-hint: Describe observed and expected behavior, reproduction steps, and whether to apply a fix.
---

Investigate the bug in the user's message and attached context.
Delegate scoped [bug-investigation](../skills/bug-investigation/SKILL.md) to Explorer, reusing current evidence. If execution is needed, assign bounded reproduction to Implementer with remaining budgets.
Return evidence, reproduction status, root cause or hypothesis, confidence with reason, proposed fix/test boundary and blockers. Do not modify application code unless a fix was requested.
If a fix is requested, complete implementation, validation and independent review under the workflow contract. Missing environment or evidence does not authorize speculative fixes. If no symptom is supplied, ask for it before proceeding.
