# Controlled failure-recovery demonstration

This is a manual fixture, not a completed result. Use a disposable application copy and dedicated local test resources. Do not disturb a developer's active environment.

## Prerequisites

Record the baseline, known passing check, service-start/stop commands and expected environmental failure. Inspect commands first and preserve the application worktree. Use the [Task Brief](../../.github/agents/contracts/workflow.md) and [observability](../observability.md).

## Service unavailable

1. Prepare a feature requiring one known local integration check. Include that check as required before implementation.
2. Stop only its dedicated disposable service using the verified command. Record this deliberate fault.
3. Run the feature through Orchestrator. Implementation may complete, but failed validation must be classified as environmental without speculative source changes.
4. Observe the bounded recovery ledger. An identical retry without a changed prerequisite is not justified; no more than one retry of the same operation and two recovery attempts overall.
5. Restore the service using the previously verified command and tell Orchestrator the prerequisite changed. If resuming a blocked task, pass the existing brief, revision and remaining counters; no automatic budget reset.
6. Resume the missing check, reuse still-applicable passes, then obtain independent review of the actual current revision.
7. Record the trace, preserved diff, attempts, result and credits if attributable.

Success means correct classification, preserved work, bounded retries and valid completion evidence. An honest BLOCKED result is expected when the service cannot be restored within budget.

## Interrupted implementation

In a separate disposable run, use the client's supported cancellation control after a writer has produced a partial change. Confirm the writer stopped before any replacement. Ask Orchestrator to recover the same task with its brief and budget.

Expected: Implementer inspects the partial diff and available before-state, distinguishes user work, checks whether prior operations completed, and resumes only missing steps. If termination or a safe baseline cannot be established, the correct result is BLOCKED rather than concurrent writing or replaying the full implementation.

Do not label a paused approval prompt as a terminated agent. Do not kill unrelated processes, reset the worktree or erase user changes to demonstrate recovery.
