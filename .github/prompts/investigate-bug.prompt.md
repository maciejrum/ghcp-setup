---
name: investigate-bug
description: Diagnose a bug and propose a minimal fix without implementing it unless requested.
agent: Orchestrator
argument-hint: Describe observed and expected behavior, reproduction steps, and whether to apply a fix.
---

Investigate the bug described in the user's message and attached context.
Delegate [bug-investigation](../skills/bug-investigation/SKILL.md) to Explorer. If execution is needed, delegate a bounded reproduction to Implementer.
Return evidence, reproduction status, root cause or hypothesis, and proposed fix/test scope. Do not modify application code unless the user requested a fix. When a fix is requested, complete implementation, validation, and independent review.
If no symptom or failing behavior is supplied, ask for it before proceeding.

