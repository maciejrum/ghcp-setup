---
version: 2
review_verdicts: ['APPROVED', 'CHANGES REQUIRED', 'DEEP REVIEW REQUIRED', 'BLOCKED']
deep_results: ['CONFIRMED', 'REFUTED', 'UNRESOLVED']
final_statuses: ['DONE', 'INVESTIGATED', 'REVIEWED', 'BLOCKED']
check_results: ['PASS', 'FAIL', 'NOT_RUN']
---

# Engineering Team workflow contract

This is the shared v2 protocol, not an agent or a skill. Load relevant sections once and reuse them until configuration changes. Skills contain procedures; agent definitions grant tools. These instructions guide a model, not a deterministic execution engine.

## Task brief

Orchestrator owns a versioned brief in the conversation. Do not create a shared file on every turn. Each invocation is self-contained: a new subagent cannot be assumed to remember earlier work. Send only its scope, applicable constraints, evidence, remaining budgets and expected output. Repairs need relevant prior state plus the delta; a bare "continue" is insufficient.

Required fields (use unknown with a reason instead of inventing values):

```yaml
task_id: feature-017
brief_version: 1
mode: implement # investigate | reproduce | review | validate | recover
request: <original outcome and user constraints>
scope: <assigned area, paths, exclusions, and shared-contract owner>
acceptance_criteria:
  - id: AC1
    requirement: <observable behavior>
baseline: <base/head or initial working-tree evidence; pending capture if unknown>
findings:
  - path: <exact path>
    symbol: <symbol or lines>
    evidence: <fact and source, distinct from hypothesis>
    relevance: <why this matters>
validation_plan:
  - id: V1
    covers: [AC1]
    cwd: <actual directory>
    command: <discovered non-watch command>
    source: <manifest, configuration, or documentation>
    required: true
unknowns: []
confidence:
  level: MEDIUM # HIGH | MEDIUM | LOW
  reason: <evidence completeness and unverified assumptions>
budget:
  repair_rounds_remaining: <counter from Orchestrator>
  recovery_attempts_remaining: <counter from Orchestrator>
  deep_reviews_remaining: <counter from Orchestrator>
  supplementary_research_remaining: <counter from Orchestrator>
  operation_retries: <operation ID to retries already spent>
expected_output: <role result and scope-specific questions>
```

Do not copy whole files, transcripts, secrets or unrelated findings. Include short snippets only when paths/symbols are insufficient. Confidence measures evidence completeness, not the probability that code is correct. LOW confidence about a path/command calls for scoped research, not deep review. It never replaces tests or approval.

## Role results

- Explorer: task/brief IDs, scope, evidence with paths/symbols, reusable patterns, affected contracts, sourced validation plan, unknowns, confidence with reason and smallest change boundary. Stop when assigned questions are answered.
- Implementer: task/brief IDs, baseline/result revision evidence, changed files and factual summary, criterion evidence, validation records, finding IDs addressed/disputed, attempts spent, unfinished work and blockers.
- Reviewer: reviewed revision/scope, independently inspected paths/contracts, findings, validation evidence assessed, outstanding blockers and exactly one review verdict.
- Deep Reviewer: finding ID, revision, precise question, severity, evidence, correction or missing evidence and exactly one deep result. It never approves the complete change.

Validation record: check ID, criterion IDs, command, cwd, revision, relevant environment identity, exit code (null if not executed), PASS/FAIL/NOT_RUN, concise result and accessible evidence reference. Classify failures as introduced, pre-existing (with evidence), environmental or unknown. An assertion failure is not automatically caused by the patch.

## Revision evidence

Before its first edit, Implementer records the base commit if available, staged/unstaged changes and relevant untracked files. Preserve an accessible scoped before-state where user work overlaps the task. A filename list or HEAD alone cannot distinguish these edits. Use read-only Git inspection and local temporary artifacts; do not stage, stash, reset or commit to create a baseline. Do not capture secrets or unrelated untracked files.

Identify each result with its base, scoped diff/before-state, and hashes or equivalent snapshot of reviewed files, including additions/deletions. A digest identifies a revision but does not replace reviewable contents. Verify the referenced state before validation and review; reconcile external edits without overwriting them.

Reuse passing checks only when relevant code, tests, configuration, dependencies and environment remain applicable, and explain reuse. Relevant edits invalidate approval and affected validation evidence. After repairs, Reviewer assesses the complete current task scope using still-valid prior evidence; no unconditional full rerun is needed.

For review-only work without an implementation baseline, Reviewer captures the requested current scope and does not claim authorship of existing edits. An empty diff means no changes to review, not APPROVED.

## Review decisions

Severity: CRITICAL means exploitable security failure, data loss/corruption or comparable severe harm; MAJOR means incorrect behavior, a broken contract, significant regression or a demonstrated material coverage gap; MINOR means a concrete non-blocking improvement. Each finding has a stable ID, severity, location, trigger, impact, evidence and recommended correction. Do not manufacture findings or block on style preferences.

| Review verdict | Condition | Coordinator action |
| --- | --- | --- |
| APPROVED | No blocking defect or serious unresolved concern; required validation passed for this revision | Check definition of done |
| CHANGES REQUIRED | Confirmed blocking defect in code/tests | Authorized repair if budget remains |
| DEEP REVIEW REQUIRED | Evidence-backed serious unresolved correctness, security, architecture, concurrency, data-integrity or regression question | Delegate the precise question if budget remains |
| BLOCKED | Required evidence, environment, tool, permission, baseline or decision is unavailable | Eligible recovery or blocked report |

Report all concurrent findings/blockers. Choose the verdict in this order: confirmed defect → CHANGES REQUIRED; serious uncertainty requiring deeper analysis → DEEP REVIEW REQUIRED; other missing required evidence → BLOCKED; otherwise APPROVED. Orchestrator handles unavailable escalation/exhausted budgets as BLOCKED. Missing/failed required checks without a confirmed patch defect are BLOCKED, not speculative repair requests. MINOR alone does not block.

Deep results: CONFIRMED routes authorized fixes through Implementer, validation and Reviewer; REFUTED returns evidence to Reviewer to finish the complete assessment; UNRESOLVED ends in BLOCKED with missing evidence. Review-only mode reports confirmed defects without repairs. Deep Reviewer never returns APPROVED or recursively escalates.

## Completion and recovery

DONE requires evidence for every acceptance criterion, all agreed required checks passing for the current state, latest complete review APPROVED, no outstanding blocker and preserved user changes. Agree required checks before implementation; never silently drop a failed/unavailable check. Any justified validation-plan change is explicit, versioned and reviewed; changing a user-required check needs the user's decision.

INVESTIGATED reports diagnosis/reproduction without claiming a fix. REVIEWED reports the verdict/findings without implying approval; confirmed defects are valid review-only outcomes. An inability to finish the requested investigation/review is BLOCKED. With no changes to inspect use REVIEWED with review_verdict NOT_RUN in the report only; NOT_RUN is not an approval verdict.

Orchestrator owns the numeric budgets in its agent instructions and passes remaining counters. New invocations, fallback models and deep review never reset counters. Retry only with evidence of a transient cause or changed prerequisite; permission denials/missing configuration do not justify identical retries. Check whether an edit already happened before retrying it.

If a writer stops returning results, first confirm termination. Without confirmation, return BLOCKED and do not start another writer. A bounded Implementer recovery inspects the actual partial diff and evidence, preserves completed/user work, and resumes only missing steps. Never blindly replay implementation. Reviewers may retry inspection/validation; environment setup or edits belong to Implementer within authorization. Persist a small local checkpoint only for session interruption/resumption: brief, revision references, counters, findings and next action. Orchestrator asks an authorized execution-capable role to save it; it has no file tools.

## Progress and final report

At stage transitions emit one short line: task ID, stage, role, scope, routing reason and remaining relevant budget. Report requested/resolved models, time, tokens, calls and credits only from runtime evidence; otherwise unknown. Model self-identification is not telemetry. Avoid per-read narration.

Final report: status; criteria/evidence; changed/inspected files; commands/cwd/results including NOT_RUN; reviewed revision/verdict; escalation result; repair/recovery counts; risks and concrete next action for blockers. Link evidence rather than pasting logs. Never invent measurements.
