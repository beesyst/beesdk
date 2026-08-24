# BeeSDK SDLC

## Change levels

- **low-risk**: documentation, internal tests or non-public implementation details;
- **runtime-risk**: packaging or build behavior that changes package consumption;
- **security-sensitive**: public contracts, authority boundaries, capability interfaces, dependency additions, serialization/parsing or artifact boundaries.

Changes must state their level in the Issue and PR, remain within approved scope and use the smallest complete solution. Public contract changes require compatibility assessment, documentation and contract tests.

## Required verification

All changes run relevant tests. Packaging changes additionally run `uv build`. Contract and security-sensitive changes test the affected API shape and its negative boundaries. Do not use `uv lock --check`; when dependencies change, update and review both `pyproject.toml` and `uv.lock`.

## Delivery

Use the project workflow: planning, implementation plus tests, then final review. The final evidence states changed files, change level, public API/compatibility impact, dependency impact, exact commands/results, security review, known limitations and confirms that the version was or was not changed intentionally.
