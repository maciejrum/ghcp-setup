---
name: implement-ticket
description: Implement a Jira ticket using an external personal skill, sourced requirements, validation, and independent review.
agent: Orchestrator
argument-hint: Provide the ticket key or URL and any additional scope or compatibility constraints.
---

Implement the ticket explicitly identified in the user's message, preserving additional user constraints. If the reference is missing or ambiguous, ask which ticket before fetching anything; never choose an assigned or recent issue automatically.

Follow the [external ticket context contract](../agents/contracts/ticket-context.md). First delegate a context-only read to Implementer using the externally installed personal skill `jira` on the target Windows machine. Do not copy the skill/helper into the repository, change Jira, edit code or begin implementation during this intake call.

Build the versioned Task Brief from retrieved source wording and criteria with source IDs. Resolve material gaps/conflicts, then use the normal scoped Explorer → Implementer → validation → independent Reviewer workflow and existing budgets. Do not treat FETCHED as implementation approval or bypass missing required evidence.

Finish with the existing final status, ticket/source versions, criterion-to-evidence mapping, review verdict and a draft PR title/description in chat. Publishing or Jira mutations require a separate explicit request.
