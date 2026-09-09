# Observing an Engineering Team run

Start with VS Code's built-in Agent Debug Logs; a separate telemetry service or dashboard is unnecessary. Record the harness and configuration revision because available fields differ across clients.

## Developer-facing progress

Orchestrator emits one short message per stage transition with task ID, stage, role, scope, routing reason and remaining budget. The final report links validation/review evidence. Avoid narrating every read or asking a model to estimate its own cost.

## Local evidence

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
| Credits | Actual attributable Copilot usage; leave blank if unavailable/delayed |
| Recovery and review | Ledger attempts, stable finding IDs, revision and final verdict |

Tool call count is a proxy for overhead, not a credit bill. Cache and output tokens also affect cost. A Reviewer's independent read is ordinarily necessary verification. Metadata-only traces may not identify paths/ranges; mark read metrics unavailable rather than enabling full content capture automatically.

For cache investigation use the built-in Cache Explorer; stabilize instructions, models and tool sets during a run. Treat cache metrics as runtime observations, not assumed savings. [Cache Explorer](https://code.visualstudio.com/docs/agents/agent-troubleshooting/cache-explorer).

A cost/replay presentation uses the exported trace plus the [scorecard](demo-scorecard.md), not another agent invocation. Keep telemetry opt-in; the repository's shared approval settings remain unchanged.
