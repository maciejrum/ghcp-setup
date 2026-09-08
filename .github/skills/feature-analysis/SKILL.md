---
name: feature-analysis
description: Analyze a requested feature or scoped refactoring before implementation, identifying existing patterns, contracts, affected files, and validation.
---

# Feature analysis

1. Translate the request into observable acceptance criteria; retain compatibility and scope constraints. Separate assumptions from requirements.
2. Locate the existing entry point and follow data through the relevant layers. For cross-application changes, identify request/response schemas and consumers.
3. Find the closest existing implementation to reuse and the tests that describe its behavior.
4. Identify the smallest affected file set, contract changes, meaningful edge cases, and regression risks. For refactoring, name the behavior that must remain unchanged.
5. Read manifests, test configuration, and documentation to identify actual validation commands and their working directories. Do not invent paths or scripts.
6. Return a concise implementation brief with acceptance criteria, file paths/symbols, patterns to reuse, tests, commands, and unresolved questions. Flag missing application code or contradictory requirements.

This skill performs analysis, not implementation. Respect the current agent's tools; pass execution needs to the coordinator.

