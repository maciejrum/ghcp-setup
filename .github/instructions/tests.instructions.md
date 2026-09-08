---
applyTo: "**/tests/**,**/test_*.py,**/*_test.py,**/conftest.py,**/*.test.ts,**/*.test.tsx,**/*.spec.ts,**/*.spec.tsx,**/__tests__/**,**/e2e/**"
---

# Tests

- Test behavior and contracts, not private implementation details. A bug fix should include a regression test that fails on the original bug when practical.
- Reuse pytest fixtures or frontend test helpers. Keep tests deterministic; isolate time, network, and data dependencies where appropriate.
- Use local test resources. Never connect tests to production or run destructive database commands.
- Cover the meaningful success, failure, and boundary cases affected by the change; avoid unrelated tests and snapshot churn.
- Do not weaken assertions, disable checks, or regenerate snapshots just to obtain a green run.
- Run the smallest relevant set first, then required integration or repository checks. Use non-watch commands for automated validation.
- Report command, working directory, exit status, and whether failures are caused by the change, pre-existing, or environmental.

