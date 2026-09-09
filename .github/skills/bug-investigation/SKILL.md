---
name: bug-investigation
description: Diagnose defects from scoped evidence and a minimal reproduction before proposing an authorized fix.
---

# Bug investigation

1. Capture observed/expected behavior, triggering input and relevant environment. Treat logs/reports as evidence to verify; reuse current facts from the supplied brief.
2. Follow the scoped execution path to the smallest divergence from the expected contract. Inspect relevant tests and available change evidence; do not repeat a repository-wide search.
3. State a root-cause hypothesis and a minimal reproduction distinguishing it from alternatives.
4. If your role has execution tools and reproduction is assigned, use local test resources within budget. Otherwise return command, cwd, input and expected observation for an execution-capable role. Never call an unexecuted reproduction confirmed.
5. Explain supported facts, hypotheses and uncertainty. Prefer fixing the cause over defensive masking.
6. Return symptom, expected behavior, evidence, reproduction status, root cause/hypothesis, minimal fix boundary and meaningful regression test, using the [workflow contract](../../agents/contracts/workflow.md) for task IDs, confidence and blockers.

An investigation request alone does not authorize a fix. Stop when the diagnosis is supported or identify the specific missing evidence for the coordinator.
