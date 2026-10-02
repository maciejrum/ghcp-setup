# Observing an Engineering Team run

Start with VS Code's built-in Agent Debug Logs; a separate telemetry service or dashboard is unnecessary. Record the harness and configuration revision because available fields differ across clients.

## Developer-facing progress

Orchestrator emits one short message per stage transition with task ID, stage, role, scope, routing reason and remaining budget. The final report links validation/review evidence. Avoid narrating every read or asking a model to estimate its own cost.

## Local evidence

The shared workspace settings enable `chat.subagents.showCreditUsage`. In supported VS Code Local sessions this exposes subagent credits in the response pill and hover details. This adds visibility; it is not an export, a complete session bill or proof that the installed client supports the setting. Capture the client/extension versions and verify the display during a separate smoke test. Keep that smoke test outside measured task runs. [Subagent credit display](https://code.visualstudio.com/docs/agents/run/subagents).

Open Agent Debug Logs from Chat and select the task session. Inspect delegations, prompts/results and effective model/tool routing. Export a session for offline inspection and reimport it for a presentation. Raw exports can contain code or prompts; keep them locally under the gitignored `.local/engineering-team/` directory and review them before sharing. [Debug logs](https://code.visualstudio.com/docs/agents/agent-troubleshooting/chat-debug-view).

Optional metadata-only OTel configuration for a local development profile (replace the absolute output path for your machine; do not commit it to shared workspace settings):

```json
{
  "github.copilot.chat.otel.enabled": true,
  "github.copilot.chat.otel.exporterType": "file",
  "github.copilot.chat.otel.outfile": "/absolute/local/path/engineering-team-trace.jsonl",
  "github.copilot.chat.otel.captureContent": false
}
```

OTel exposes parent/child spans, requested/resolved model fields, token usage and durations. Use `gen_ai.request.model` versus `gen_ai.response.model` to compare requested and actual routing. Fields absent from a runtime stay unknown. Debug content capture can differ by harness and OTel configuration; inspect what an export contains before treating it as metadata-only. [VS Code OTel](https://code.visualstudio.com/docs/agents/guides/monitoring-agents).

## Measurement rules

| Observation | How to record it |
| --- | --- |
| Task and delegation identity | Session/span IDs plus Task Brief task_id and version |
| Model routing | Requested/resolved model from runtime, never agent self-identification |
| Tool/delegation counts | Count unique relevant execution spans; separate errors/retries |
| Token totals | Sum non-overlapping leaf model calls or use one authoritative session total; do not sum inclusive parent and child totals together |
| Repeated reads | Same path/range and content revision read again |
| Redundant reads | Classify repeated reads with no changed evidence or independent verification need; record the reason and sampling limits |
| Credits | Actual attributable Copilot usage with source, precision and whether it includes children; leave blank if unavailable/delayed |
| Recovery and review | Ledger attempts, stable finding IDs, revision and final verdict |

Tool call count is a proxy for overhead, not a credit bill. Cache and output tokens also affect cost. A Reviewer's independent read is ordinarily necessary verification. Metadata-only traces may not identify paths/ranges; mark read metrics unavailable rather than enabling full content capture automatically.

Use one authoritative complete session credit total when available. If reconstructing a total from component usage, include the coordinator and every child exactly once; do not add child credits to an inclusive parent total. Record the evidence for the inclusion rule. A subagent pill alone omits coordinator cost, and a rounded/delayed or account-wide change is not automatically attributable to one task. Keep unrelated Copilot activity out of the measurement window. Report unavailable credits as unknown; a tariff calculation is an estimate in a separate field. [Copilot billing](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing).

Agent frontmatter is the requested configuration. Validate effective parent and child models from runtime logs; an agent's statement of its model is not proof. A successful static validation confirms the selected names/categories and permission metadata, not that VS Code obeyed them. Record any routing mismatch or unavailable model and keep that run visible as a deviation/failure instead of silently replacing it.

For cache investigation use the built-in Cache Explorer; stabilize instructions, models and tool sets during a run. Treat cache metrics as runtime observations, not assumed savings. [Cache Explorer](https://code.visualstudio.com/docs/agents/agent-troubleshooting/cache-explorer).

A cost/replay presentation uses the exported trace plus the [scorecard](demo-scorecard.md), not another agent invocation. Keep telemetry opt-in; the repository's shared approval settings remain unchanged.
