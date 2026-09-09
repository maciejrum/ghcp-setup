---
applyTo: "**/tests/**,**/test_*.py,**/*_test.py,**/conftest.py,**/*.test.ts,**/*.test.tsx,**/*.spec.ts,**/*.spec.tsx,**/__tests__/**,**/e2e/**"
---

# Tests

- Test behavior and contracts, not private implementation details. A bug fix should include a regression test that fails on the original bug when practical.
- Reuse the repository's test framework and helpers (pytest fixtures or frontend helpers where present). Keep tests deterministic; isolate time, network, and data dependencies where appropriate.
- Use local test resources. Never connect tests to production or run destructive database commands.
- Cover the meaningful success, failure, and boundary cases affected by the change; avoid unrelated tests and snapshot churn.
- Do not weaken assertions, disable checks, or regenerate snapshots just to obtain a green run.
- Run the smallest relevant set first, then required integration or repository checks. Use non-watch commands for automated validation. Reuse passing evidence only when relevant inputs and environment remain applicable; explain any repeated run.
- Report command, working directory, reviewed revision, exit status and criterion covered. Classify failures as introduced, pre-existing with evidence, environmental or unknown; missing required checks block completion without proving a code defect.
