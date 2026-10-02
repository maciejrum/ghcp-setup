# Optional model and workflow experiments

The v4 model policy requests Opus 5.5 for coordination and deep review, GPT-6 Luna for exploration, Sonnet 5 for implementation and GPT-6 Sol for independent review. It retains the v3 workflow contract, five responsibilities, permission boundaries and repair/recovery budgets. This is a configuration hypothesis; it does not establish model availability, actual routing, savings or better code.

GitHub classifies Opus 5.5 and GPT-6 Sol as Powerful, Sonnet 5 as Versatile and GPT-6 Luna as Lightweight. Local subagent routing checks this category against the parent, rather than comparing token prices. The default chain is therefore statically compatible. Still confirm every requested/resolved model in the target VS Code runtime before measured runs. No fallback is enabled. [Copilot categories](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing), [Local model routing](https://code.visualstudio.com/docs/agents/run/subagents).

The trials below are not enabled in the default configuration. Keep the same responsibilities; do not add agents to select a cheaper model. Use a disposable configuration variant and update its validator policy together with the agent files.

## Luna implementation for narrow changes

Test a local low-risk change with a complete current brief and no security/data-integrity boundary changes. Deliberately change Implementer's primary model to GPT-6 Luna, keeping independent Sol review. Run the same acceptance checks as the default Sonnet variant.

Compare credits per externally accepted result, remaining defects, repair rounds and developer interventions. Include failures and retries. Do not infer savings from token prices alone or skip review because the implementer reports HIGH confidence.

## Sol versus Opus coordination

Change only the coordinator from Opus 5.5 to GPT-6 Sol. Keep the workers, brief, instructions, tool permissions, acceptance criteria and budgets identical, including the single evidence-backed Opus deep review allowance. Both coordinators are Powerful, so Sol can request the configured Opus child under the documented category rule. Confirm actual routing in both variants rather than substituting a generic agent after a failure.

Compare total credits per externally accepted result, remaining defects, repair rounds and interventions. A lower coordinator tariff alone does not establish a cheaper completed workflow. Include unsuccessful attempts and repeated trials, and keep this ablation separate from the standard Agent versus team comparison.

A future Versatile coordinator trial would require a different chain without automatic Powerful children. Do not route around the parent's category limit. A manual higher-tier continuation receives the existing brief, revision and counters and remains part of the measured cost/time.

## Confidence calibration

Use HIGH/MEDIUM/LOW as evidence-completeness labels with an explicit reason and unknowns. Compare those labels with externally assessed outcomes across repeated tasks. LOW about missing paths/commands triggers scoped Explorer follow-up; only a serious code-backed question qualifies for Deep Reviewer. Confidence never changes the definition of done.

## Parallel exploration ablation

Compare one scoped Explorer with two disjoint backend/frontend scopes on identical full-stack tasks. Both include their own test impact. Measure elapsed time, tokens, redundant reads, contract mismatches and accepted completion. A third test-impact invocation needs genuinely separate integration/E2E work; a Test Agent is unnecessary unless tools/environment/responsibility materially differ.

Use separate experiment IDs in the [benchmark](benchmark.md) and record the complete configuration variant. If a variant wins consistently, review it before changing the default model policy.
