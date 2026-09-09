# Benchmark: Agent Mode versus Engineering Team v2

Compare **A: standard Copilot Agent Mode** with **B: the configured Engineering Team** on real application tasks. This measures the complete workflow/model-routing package. Keep failures and blocked attempts; never substitute estimates or sample results for measurements.

## Tasks

| ID | Type | Example to adapt | Acceptance criteria |
| --- | --- | --- | --- |
| bug | Small bug | Filtering on a later page returns an empty result | Reproduction, fix, meaningful regression test |
| backend | Backend feature | Optional status filter | Correct filtering; omission preserves the API contract |
| frontend | Frontend feature | Control for an existing filter API | Keyboard access, URL state, error handling |
| fullstack | Full-stack feature | New filter from query to view | Consistent contract, authorization, cache, pagination, tests for both apps |
| refactor | Refactoring | Remove local validation duplication | Preserved behavior and limited scope |

Freeze exact prompts, acceptance checks and quality criteria before either run. Each task starts independently; earlier tasks must not provide a solution to later measurements. Predefined external acceptance tests must not be generated from the submitted patch.

## Experiments and repetitions

- `package-v2`: A versus B with their recorded model policies. This is a comparison of complete approaches, not isolated orchestration.
- `orchestration-control`: a separate experiment using the same model(s) and shared instructions/skills in both variants where feasible. Record all model assignments and any remaining differences. Change model-policy validation explicitly in a disposable variant; the default validator intentionally pins the production roles.
- `v1-v2`: optional comparison of configuration revisions with otherwise identical tasks and environment.
- Model/confidence/parallelism trials are separate IDs described in [experiments](experiments.md).

Five pairs are a pilot. For stronger evidence, use at least three repetitions per task/variant as an initial plan, then expand if variability warrants it. Randomize paired A/B order and record it. Report per-task results, medians and spread; do not claim statistical certainty from a small sample.

## Procedure

1. Prepare separate copies/worktrees at the same application commit and equivalent initial state. Keep fixtures, dependencies and services identical; never reset user work.
2. Keep common instructions/skills identical for the package comparison. A uses standard Agent Mode without team-selection prompts; B selects Orchestrator. Record any built-in subagents in A.
3. Record exact prompt/criteria, application baseline, configuration revision (including local patch identity if uncommitted), VS Code/harness versions, requested models, reasoning/context and approval settings.
4. Start clean conversations without cross-variant history. Record start time and consumed-credit counter; avoid other paid sessions on the same account during attribution.
5. Execute and record interventions, approvals, delegations, routing deviations and attempts. Use [observability](observability.md) rather than model estimates.
6. Have an assessor run identical external acceptance checks and review anonymized changes where practical. Record final remaining defects and whether the result meets the agreed acceptance/quality gate. Automated team review findings are not this external score.
7. End timing after external verification. Capture attributable credits after reporting delay. Keep unmeasurable fields blank with reasons; missing is not zero.
8. Fill the [worksheet](benchmark-results.csv), including blocked/failed runs. Store raw traces locally and link an appropriate evidence reference; review them before sharing.

## Worksheet fields

| Column | Meaning |
| --- | --- |
| task_id, variant, run, experiment, execution_order | Task, A/B variant, repetition, experiment ID, randomized order within pair |
| base_commit, configuration_revision | Application baseline and exact agent configuration identity |
| prompt, acceptance_criteria | Identical wording/criteria fixed before runs |
| environment, models | Client/harness/dependency/settings details; human-readable model policy summary |
| requested_models, resolved_models | Runtime-backed requested versus actual routing; blank if unavailable |
| started_at, finished_at, elapsed_minutes | ISO timestamps with timezone and end-to-end time including approval waits/external verification |
| credits_before, credits_after, credits_used | Consumed-credit counter and difference in a consistent unit; document conversions |
| human_interventions, approval_prompts | Corrections/manual edits separately from tool approvals; initial prompt excluded |
| tests | PASS, FAIL, NOT_RUN or PARTIAL for the fixed required checks |
| validation_evidence | Commands, cwd, revision, outcomes or evidence reference |
| review_critical, review_major, review_minor | Unique confirmed automated findings, not repeated counts across repair rounds |
| review_verdict | APPROVED, CHANGES REQUIRED, DEEP REVIEW REQUIRED, BLOCKED or reporting-only NOT_RUN |
| rework_rounds, recovery_attempts, deep_reviews | Attempts from the task ledger, never reset across resumptions |
| delegations, tool_calls | Unique runtime invocation/execution counts; include failed operations |
| repeated_reads, redundant_reads | Repeated same-content reads; subset adjudicated unnecessary; explain method/coverage |
| input_tokens, output_tokens, cache_read_tokens, cache_write_tokens | Non-overlapping runtime totals; unavailable fields blank |
| repair_credits, recovery_credits | Attributable subsets of total credits, not additional amounts to add again |
| routing_violations | Count of confirmed deviations from that variant's declared role/model/tool policy |
| remaining_defects | Unique defects from external final assessment, not just the team's own findings |
| accepted | YES/NO from the external acceptance and quality gate; blank if not assessed |
| files_touched, unrelated_files | Unique changed files and out-of-scope subset, excluding disposable tool artifacts |
| trace_ref | Local trace or shareable redacted evidence reference |
| status | NOT_RUN, DONE, FAILED or BLOCKED for the attempted task |
| notes | Blockers, missing data, protocol deviations, measurement limitations and assessor details |

If A has no automated review, its review counts stay blank and verdict is NOT_RUN. Zero implies an actual completed assessment finding no issues. Both variants still receive the same external review.

Independent Reviewer reads are not redundant merely because Implementer read the same path. Classify unjustified duplicate discovery separately. Tool counts alone are not credit costs. Do not double-count inclusive parent/child token totals or cache categories; state the runtime metric definitions.

## Reporting

Primary outcomes: externally accepted completion rate, remaining defects, total attributable credits per accepted task, elapsed time and human interventions.

For credits per accepted task, divide credits across **all measured attempts including failures** by externally accepted results. If no result is accepted, the ratio is undefined; show total spend and zero accepted results. If attribution is incomplete, do not present this ratio as complete.

Show per-task paired results before aggregates: small tasks may favor standard Agent Mode while complex tasks benefit from the team. Include scope drift, validation and routing correctness alongside speed/cost. Confidence labels and more findings alone do not prove higher quality.

The worksheet starts with ten NOT_RUN rows. No runtime performance or credit savings are claimed by the template.
