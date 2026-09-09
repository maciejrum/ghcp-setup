# First run and demonstration

## Runtime preflight

Run the static validator and unit tests as described in the [README](../README.md). Then use a disposable copy of the target application. Record VS Code/harness versions, configuration revision and actual model/tool observations using [observability](observability.md).

1. Verify discovery of exactly the intended five roles. Orchestrator is visible; supporting roles are hidden.
2. Confirm Orchestrator has only agent delegation. Confirm Explorer has read/search and no execute/edit. Check effective tool lists for the other roles.
3. Send: "Ask Explorer to inspect this configuration template and identify its validation commands. Do not change files. Include the shared workflow contract's coordination rules if needed."
4. Verify Luna actually ran, the brief cites the existing configuration rather than imaginary application code, and Orchestrator did not browse or execute. Confirm the shared contract reached the coordinator, whether by prompt injection or Explorer's scoped response.
5. Use a small real application change to verify Sonnet implementation → validation → Terra independent review, with revision evidence and truthful reports.
6. Check model availability and parent cost-tier compatibility for all configured roles. Exercise Deep Reviewer only with a real serious question or an explicitly labeled test fixture. Do not manufacture an issue in a normal task.

Repeat after relevant configuration/harness/model changes, not before each task. If agent-only Orchestrator cannot obtain the contract through delegation, record a compatibility failure. Do not silently restore broad tools.

## Behavioral regression scenarios

These are manual runtime tests, not results already achieved by this repository. Record prompt, expected/observed route, trace and outcome. Fixtures may supply deterministic known defects; label them as tests.

| Scenario | Expected evidence |
| --- | --- |
| Investigation only | Explorer; optional bounded reproduction; no unauthorized fix |
| Review only with changes | Reviewer directly; actual diff inspected; no implementation |
| Review only with empty diff | REVIEWED, review_verdict NOT_RUN; no APPROVED |
| Full-stack feature | Usually two scoped Explorer invocations; one writer; shared contract ownership |
| Narrow task with complete current brief | Explorer may be skipped; local implementation inspection remains |
| Missing required test service | BLOCKED/recovery, never a fabricated pass or speculative source repair |
| Confirmed defect plus missing test service | CHANGES REQUIRED with defect and blocker both reported; DONE still impossible until both resolved |
| Repeated confirmed review defect | At most two repair rounds; stop earlier on no progress |
| Persistent tool failure | At most one retry of that operation, within two total recovery attempts |
| Interrupted writer | Confirm termination, inspect partial diff, preserve work, resume missing steps; no concurrent writer |
| Relevant edit after approval | Approval and affected evidence invalidated; assess current task scope |
| REFUTED serious finding | Return to Reviewer for full assessment; no direct DONE from deep review |
| CONFIRMED serious finding | Authorized repair, validation and Reviewer; review-only reports without edits |
| UNRESOLVED serious finding | BLOCKED with missing evidence; no second deep loop |
| Missing model/tool | No generic replacement or widened tools; configured verified fallback only |
| Dirty working tree with overlapping user edits | Before-state preserved; task diff distinguished; user work retained |

The partial-failure drill is detailed in [failure recovery](scenarios/failure-recovery.md).

## Ideal full-stack feature

Use an application with a real list of objects and a validation status. Prepare local test data and agreed baseline checks.

```text
Add status filtering to the API and UI.
Omitting the filter preserves the API contract.
Changing the filter returns the list to page one.
Preserve authorization and handle loading, error and empty states.
Add meaningful backend/frontend tests and independent review.
```

| Stage | What the developer should see |
| --- | --- |
| Planning — Sol | Observable criteria, scope/exclusions, routing reason and initial budget |
| Parallel exploration — Luna ×2 | Backend owns parameter/schema/query discovery and backend tests; frontend owns consumers, URL/cache/pagination and UI tests |
| Brief — Sol | Reconciled API contract, exact paths/symbols, sourced commands/cwd, unknowns; no repeated full exploration |
| Implementation — Sonnet | Captured before-state, one writer, scoped change/tests; extra searches justified by gaps |
| Validation — same Implementer invocation | Criterion-to-check evidence, command results and current revision; only invalidated checks rerun |
| Independent review — Terra | Actual diff/contracts assessed independently; grounded finding IDs and explicit verdict |
| Optional deep review — Sol | Only a precise serious unresolved question; result routes back through the full workflow |
| Final report | Status, criteria/evidence, files, reviewed revision, checks, attempts, actual models/credits if measurable |

A representative transition message (format example, not a measured run):

```text
feature-017 · REVIEW · Reviewer · API/UI diff · independent contract check · repairs remaining: 2
```

Do not run Deep Reviewer simply to display another model. Show a real trace via the built-in debug panel and fill the [scorecard](demo-scorecard.md). A failure/recovery run is a separate labeled demonstration.

## Presentation evidence

Show requirements → scoped handoff → actual diff → validation evidence → independent findings → final verdict. Use [benchmark results](benchmark-results.csv) only when measured; show blocked/failed attempts alongside successes. Before/after claims must distinguish the full model-routing package from the isolated effect of orchestration.

Committing/pushing are separate explicit developer actions. There are no completed Copilot runtime measurements bundled with this template.
