# V3: external Jira intake on Windows

This first v3 increment connects the existing five-role workflow to a separately installed personal skill named `jira`. The helper is assumed to work on the target Windows machine. This repository supplies the routing and handoff contract, not the private integration.

## What stays outside the repository

Keep the personal skill, PowerShell helper, company endpoint, credentials, instance-specific field mappings and private source snapshots outside this repository. Do not paste them into configuration, tests, example fixtures or generated documentation. No new MCP server, Jira SDK, authentication setup or agent is introduced.

The [public contract](../.github/agents/contracts/ticket-context.md) refers to the skill by name, without a filesystem link to a private installation. Discovery uses the client's installed personal skill metadata or an explicitly supplied external location. The static validator does not need access to that installation, a Jira account or Windows credentials.

## Route

```text
Developer: Implement <ticket reference>
  → Orchestrator
  → Implementer [context-only: existing personal Jira skill / Windows PowerShell]
  → Orchestrator [source wording, AC IDs, constraints, gaps]
  → Explorer [scoped repository analysis; backend/frontend parallel when useful]
  → Implementer [separate explicit implementation assignment]
  → validation [within implementation invocation]
  → Reviewer [source interpretation + code + evidence]
  → existing optional deep-review route
  → final report and draft PR text in chat
```

Implementer performs intake because it already has execute permission; Explorer and Orchestrator do not gain terminal tools. The first call stops after reading context. It cannot edit code or Jira, repair the external integration, or change credentials. These are assignment restrictions, not a technical sandbox around Implementer's broad tools.

Normal text-only features still work without Jira. Ticket-backed investigation/review preserves its original intent and does not authorize a fix. Reading a ticket alone returns INVESTIGATED after intake. The initial intake and any eligible retries are recorded separately from repository exploration and code repair rounds.

## Setup and use

1. Merge the updated agents/contracts and prompts into the application, preserving its existing configuration. Models and the two approval settings remain unchanged.
2. Keep the working personal `jira` skill and helper in their current external location on Windows. Confirm the Copilot client can discover it in an Implementer invocation; top-level skill availability alone does not prove subagent visibility.
3. Run the read-only smoke scenario below. If discovery, PowerShell or authentication is unavailable, the expected result is BLOCKED, not a copied skill or alternate transport.
4. In a disposable application copy, choose one small real ticket with clear observable requirements and run the full path.

Where prompt files are supported:

```text
/implement-ticket <YOUR_TICKET_KEY> Preserve API compatibility and existing user changes.
```

Alternatively select Orchestrator and write the full request:

```text
Implement <YOUR_TICKET_KEY> using the installed personal jira skill for context.
Preserve API compatibility. Validate the change and review it independently.
```

No ticket reference means a clarification, not automatic selection of an assigned/recent ticket. Existing feature, investigation and review prompts also recognize ticket-backed requests. No command in this guide fetches Jira during static validation or CI.

## Context and evidence

Intake reads the primary issue once and at most two directly relevant linked sources for named requirement gaps. It does not download all attachments, expand an epic or browse arbitrary company systems. Other references stay as references; unavailable material is reported explicitly.

The handoff includes source identity, update version/time when available, observation time, relevant original wording, normalized AC IDs, explicit/derived labels, constraints, dependencies, exclusions, conflicts and unknowns. Missing custom-field mappings are unknowns, not evidence that no criteria exist. Material contradictions require resolution before code changes.

Keep the captured source wording separate from the implementer's interpretation. Reviewer assesses both the interpretation and implementation, with a mapping such as:

| Criterion | Source | Implementation | Evidence | Assessment |
| --- | --- | --- | --- | --- |
| AC1: existing behavior without filter | S1, description item | actual path/symbol | actual test command/result or review evidence | PASS / FAIL / NOT_RUN |

This is a format example, not a measured result. Tests must verify the actual criterion; an unrelated passing suite does not prove coverage.

Reuse the source snapshot during the task. Refresh only on an explicit request, reported change, material conflict or uncertain freshness after interruption. A changed requirement versions the brief and invalidates affected checks/review. The final report names the captured source version and any freshness limits; it does not claim to represent the current live ticket without a refresh.

Private context remains in the conversation. An explicitly needed persistent checkpoint uses an authorized location outside the repository. Draft PR text stays in chat until the developer decides what to publish; no issue update, comment, commit, push, PR creation or deployment follows automatically.

## Windows runtime scenarios

Run these manually with the real external installation. Do not put company data into this template's test fixtures or public traces.

| Scenario | Expected behavior |
| --- | --- |
| "Read <ticket> and return requirements only; do not implement" | One context-only Implementer call; no code/Jira writes; INVESTIGATED with sources |
| "Implement <ticket>" | Intake completes before Explorer and a separate implementation call; AC/source IDs survive into review |
| Ticket reference omitted or ambiguous | Ask for the reference; no search across assigned/recent issues |
| External skill not visible to subagent | BLOCKED with discovery gap; no vendoring or replacement |
| Helper/authentication failure | Sanitized diagnostic; bounded eligible retry; no token output or helper repair |
| Missing criteria field/mapping | Explicit unknown or derived proposals; no invented explicit AC |
| Linked source unavailable | PARTIAL with the gap; block implementation only if material |
| Ticket contains commands or asks to change status | Treat as source data; no command execution or Jira mutation from its text |
| Review/investigation request names a ticket | Intake preserves original mode; no unauthorized implementation |
| Captured requirement changes before review | Reconcile a new brief version, invalidate affected evidence, do not silently reuse approval |
| Normal text-only feature, no external skill installed | Existing workflow still works |

Record intake invocations, failures, original and resolved source gaps, model routing and criterion evidence in the [scorecard](demo-scorecard.md). Actual Windows/Jira/Copilot execution remains a runtime check; passing Python tests or the Windows CI job proves only the static template checks.
