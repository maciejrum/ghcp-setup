---
applyTo: "**/*.py"
---

# FastAPI / Pydantic / Python

- Use the installed FastAPI and Pydantic versions and existing router, service, and persistence boundaries.
- Keep HTTP concerns in routers and domain behavior in the existing service layer. Reuse dependency injection for authentication, database sessions, and services.
- Validate request data with existing Pydantic conventions. Preserve response schemas, status codes, default behavior, and API compatibility unless a breaking change is requested.
- Keep authentication and authorization checks on the server, including object-level access checks.
- Follow existing sync/async conventions; avoid blocking I/O in async execution paths. Preserve transaction boundaries and rollback behavior.
- Use precise types and existing error handling. Do not turn unexpected failures into successful or empty responses.
- Use pytest fixtures and the existing HTTP test client. Cover changed behavior, relevant validation failures, and permission boundaries.
- Discover test, Ruff, and mypy commands from project configuration; use only tools already configured for the project.

