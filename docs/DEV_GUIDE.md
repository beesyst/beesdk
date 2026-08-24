# BeeSDK development guide

## Setup and checks

From the repository root:

```bash
uv sync
uv run pytest -q
uv build
```

Run Python through `uv run`; no runtime service or configuration is required for BeeSDK.

## Contract discipline

Keep top-level re-exports in `beesdk.__init__` stable. Add only reusable, consumer-proven contracts. Do not import consumer projects or implement host runtime behavior in this package. Update documentation and compatibility tests whenever public API changes.

`pyproject.toml` is the source of truth for the version and dependencies. Commit `uv.lock` with dependency changes; do not run dedicated lockfile validation.
