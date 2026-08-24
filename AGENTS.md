# AGENTS.md — BeeSDK repository guidance

## Purpose and boundary

BeeSDK is a standalone contracts package for Bee consumers. It is not a BeeAgent module and does not own runtime application behavior. Consumers depend on `beesdk`; BeeSDK must never depend on `beeagent`, `beeagent-rop`, `beeui` or `beescan`.

## Sources of truth

- iteration scope: `docs/ROADMAP.md` and the approved Issue;
- public boundary: `docs/SPEC.md` and `docs/ARCHITECTURE.md`;
- delivery/security rules: `docs/SDLC.md` and `docs/SECURITY.md`;
- package metadata and version: `pyproject.toml`.

Read the applicable documents before changes. Cross-project inspection is read-only and needed only for an explicitly consumer-related task.

## Implementation rules

- Stay within approved scope and prefer the smallest complete change.
- Keep runtime dependencies empty unless an approved security-sensitive Issue changes that rule.
- Export public contracts through `src/beesdk/__init__.py`; do not force consumers to import internal modules.
- Do not add runtime config, services, storage implementations, gateways, egress, subprocesses, UI, plugin registries or product-specific contracts without explicit scope.
- Preserve host-owned authority: module-facing capability calls must not accept authority or runtime identity.
- Treat public contract or authority/capability boundary changes as security-sensitive.
- Do not change the version for ordinary work.

## Verification and report

Run verification proportional to `docs/SDLC.md`; use `uv sync`, `uv run pytest -q` and `uv build` for the initial package foundation. Do not run `uv lock --check`.

Reports must include files read, change level, source of truth, architecture assessment, changed files, exact checks/results, security review, known limitations and either `version not changed` or an intentional version-change explanation.
