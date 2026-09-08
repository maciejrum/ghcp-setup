# POC benchmark: Agent Mode vs Engineering Team

Compare **A: standard Copilot Agent Mode** with **B: Orchestrator and four supporting roles** on five tasks from a real project. Do not replace measurements with estimates or sample results.

## Tasks

| ID | Type | Example to adapt | Acceptance criteria |
| --- | --- | --- | --- |
| bug | Small bug | Filtering on a later page returns an empty result | Reproduction, fix, and regression test |
| backend | Backend feature | Optional status filter in the API | Correct filtering; omitting the filter preserves the contract |
| frontend | Frontend feature | Filter control for an existing API | Keyboard access, correct URL state, and error handling |
| fullstack | Full-stack feature | New filter from the API to the view | Consistent contract, cache, pagination, and tests for both applications |
| refactor | Refactoring | Remove local duplication in validation | Preserved behavior and a limited set of affected files |

Record the exact prompts and criteria before running either variant. Each task should have its own starting point; an earlier task must not provide a ready-made solution for a later measurement.

## A/B procedure

1. Prepare two separate copies or worktrees at the same application commit. Keep test data, dependency versions, and the environment identical. Do not reset a directory containing the user's work.
2. To measure the effect of orchestration, keep the same instructions and skills in A and B. In A, use standard Agent Mode without the custom team or prompts that select Orchestrator; in B, select Orchestrator. Record any use of built-in subagents in A.
3. Use identical task wording and explicitly record the main model in A. Record the role models in B, the VS Code version, Copilot/harness version, reasoning mode, context, and approval settings. If you compare the full package against a clean configuration in A, describe it as a different experiment.
4. Start new conversations without history from the previous variant. Record the start time and credit usage counter. Do not run other paid sessions on the same account during the measurement.
5. Run the task and record interventions. When it finishes, inspect the code and run the same predefined acceptance tests in both variants. Record the end of the measurement after this verification.
6. Read the final usage, accounting for reporting delays. If usage cannot be attributed reliably, leave the field blank and explain why. Missing data does not mean zero.
7. Fill in [benchmark-results.csv](benchmark-results.csv). Keep failed and blocked attempts as well. Alternate the A/B execution order between tasks; for a larger sample, repeat measurements and report the median and spread.

## Metrics and worksheet

| Column | Meaning |
| --- | --- |
| task_id, variant, run | Task, A/B variant, and repetition number |
| base_commit | Shared application commit for the pair |
| prompt, acceptance_criteria | Exact task and criteria for both attempts |
| environment, models | Versions, harness, settings, and models actually used |
| started_at, finished_at | ISO 8601 timestamps with a time zone offset |
| elapsed_minutes | Time from prompt submission to result verification, including approval waits |
| credits_before, credits_after | Cumulative counter of **consumed** credits, using the same unit |
| credits_used | `credits_after - credits_before`; if using a remaining-credit balance, convert it and explain in notes |
| human_interventions | Additional instructions, corrections, and manual edits; the initial prompt does not count |
| approval_prompts | Tool approvals, counted separately from substantive interventions |
| tests | PASS, FAIL, NOT_RUN, or PARTIAL for the previously agreed required checks |
| validation_evidence | Commands, working directories, and results, or a path to the report |
| review_critical, review_major, review_minor | Number of unique confirmed findings; do not count the same issue again in a later round |
| rework_rounds | Number of repair rounds after review |
| files_touched, unrelated_files | Number of unique added/modified/deleted files and files outside the scope; exclude caches and dependency installation artifacts |
| review_verdict | APPROVED, CHANGES REQUIRED, DEEP REVIEW REQUIRED, or NOT_RUN |
| status | NOT_RUN, DONE, FAILED, or BLOCKED |
| notes | Blocker reasons, missing data, escalations, deviations, and observations |

If A has no automated review, leave its review metrics blank and enter `NOT_RUN`; zeros would imply a completed review with no findings. Compare quality using the same tests and an independent human review for both variants. More findings alone do not demonstrate a better solution.

Five pairs provide pilot results. Present differences in time, cost, and interventions alongside completion rates, validation, and change scope. Do not claim savings based on incomplete or incomparable attempts.
