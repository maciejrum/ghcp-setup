# First run and presentation

## Check the configuration before working on the application

1. Run `scripts/validate_config.py` as described in the README.
2. In VS Code, open Chat and select Orchestrator. If it is missing, check discovery of `.github/agents/` and frontmatter errors in Chat diagnostics; reload the window if needed.
3. Check the availability of the configured models and each role's tools. A missing tool or model is a configuration blocker, not a reason to expand another role's permissions.
4. Send: `Ask Explorer to analyze this repository's structure. Identify the agent files and validation command. Do not change anything.`
5. Verify that Explorer was actually invoked with its configured model and read/search tools. The expected report identifies the repository as a configuration template and does not invent backend/frontend code.
6. Run a small implementation task in a copy of the target application. Check the Explorer → Implementer → Reviewer sequence, models, pending approvals, and test report.

Passing the static validator does not replace steps 2–6. No runtime results are included in this repository as completed measurements.

## Single-feature demo

Choose a working application that actually has a list of objects with a validation status. Prepare local data and a baseline test suite.

```text
Add list filtering by validation status in the API and UI.
Omitting the filter must preserve the existing API contract.
Changing the filter must return the list to the first page.
Handle loading, error, and empty states.
Add tests for the changed behavior and conduct an independent review.
```

Show separate backend/frontend analysis, the coordinator's plan, Sonnet's implementation, test results, and Terra's review. If there are no serious concerns, Deep Reviewer should remain unused. Do not manufacture a problem just to demonstrate escalation.

Finish by showing the diff, validation report, and actual benchmark data. Committing and pushing remain separate developer actions.

## Presentation narrative

1. **Problem:** developers manually manage context, model selection, implementation, and review.
2. **Idea:** engineering roles with separate models and tools.
3. **Workflow:** Orchestrator → Explorer → Implementer → Reviewer; a specific escalation triggers Deep Reviewer.
4. **Costs:** repository research delegated to Luna, limited repair rounds, and no automatic Astra/Opus use.
5. **Control:** one agent writes at a time, explicit tool lists, terminal approvals, and no automatic publishing. The reviewer's terminal is not a read-only sandbox.
6. **Demo:** one request, code, tests, and review.
7. **Results:** actual time, credits, interventions, completed tasks, and failures for A/B; acknowledge the small sample.
8. **Next steps:** after evaluating the POC, consider MCP for tickets/documentation and integrations allowed by the organization.

The “before/after” slide: before, the developer directs each step; after, the developer defines the task, the team analyzes, implements, tests, and reviews it, and the developer verifies the result.

## Five-day plan

| Day | What to verify |
| --- | --- |
| 1 | Instructions and correct Explorer/Implementer behavior on a small task |
| 2 | Orchestrator delegation and independent analysis of different areas |
| 3 | Review, concrete fixes, and another review |
| 4 | Skills, prompts, model routing, and credit usage |
| 5 | Five benchmark pairs, results analysis, and demo preparation |
