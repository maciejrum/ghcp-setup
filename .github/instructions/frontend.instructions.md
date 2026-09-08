---
applyTo: "**/*.ts,**/*.tsx"
---

# React / Next.js / TypeScript

- Follow the installed framework versions, router, folder structure, and component conventions.
- Keep the existing Next.js server/client boundary. Add `use client` only where interactivity requires it; keep secrets and server-only code out of client bundles.
- Prefer precise types over `any`; preserve the API contract and handle optional fields explicitly.
- If RTK Query is present, extend existing API slices and cache tags. Keep server data in its cache rather than duplicating it in component state or adding a second fetching stack.
- Use the existing approach for URL filters and pagination. Consider stale requests, cache invalidation, and resetting pagination when filters change.
- Handle loading, empty, success, and error states. Preserve keyboard access, semantic controls, and accessible labels.
- Reuse the existing component library and design conventions.
- Test observable behavior with the configured test runner and React Testing Library or existing equivalent. Use the repository's lint and typecheck scripts and package manager.

