---
name: feature-analysis
description: Analyze a requested feature or scoped refactoring, identifying reusable evidence, affected contracts, and validation.
---

# Feature analysis

1. Translate the request into observable acceptance criteria; preserve compatibility and exclusions. Separate assumptions from requirements.
2. Start with the supplied brief and named paths. Locate entry points and relevant data flow; for cross-application work identify schemas and consumers. Respect assigned shared-contract ownership.
3. Find the closest reusable implementation and behavior tests. Include test impact in the assigned area, not a separate repository-wide inventory.
4. Identify the smallest change boundary, contract changes, meaningful edge cases and regressions. For refactoring state what must remain unchanged.
5. Reuse sourced validation commands if their configuration remains current. Otherwise inspect relevant manifests/configuration/docs for actual commands and cwd. Do not read every lockfile or invent scripts.
6. Return the Explorer result in the [workflow contract](../../agents/contracts/workflow.md), mapping requirements to paths, evidence and checks. Flag missing code, contradictions and the smallest unresolved question. Stop when the assigned questions are covered.

Analysis does not authorize implementation or execution beyond the active role's tools.
