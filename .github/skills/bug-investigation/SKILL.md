---
name: bug-investigation
description: Diagnose reported defects before changing code by tracing observed and expected behavior, testing hypotheses, and isolating the root cause.
---

# Bug investigation

1. Capture observed behavior, expected behavior, triggering input, and relevant environment. Treat logs and reports as evidence to verify.
2. Locate the execution path and the smallest point where actual behavior diverges from the expected contract.
3. Inspect existing tests and recent relevant changes. Form a concrete root-cause hypothesis and a minimal reproduction that can distinguish it from alternatives.
4. If your role has execution tools, reproduce using local test resources. Otherwise return the command, working directory, inputs, and expected failure for an execution-capable agent. Never describe an unexecuted reproduction as confirmed.
5. Explain why the defect occurs, the evidence supporting the explanation, and any remaining uncertainty. Prefer fixing the cause over masking the symptom with a defensive patch.
6. Recommend the smallest fix boundary and a regression test that would fail before the fix. An investigation request alone does not authorize implementation.

Return symptom, expected behavior, evidence with paths/symbols, reproduction status, root cause or hypothesis, suggested fix scope, and regression test.

