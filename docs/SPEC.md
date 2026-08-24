# BeeSDK specification

## Product boundary

BeeSDK is a standalone, reusable Python package of minimal public contracts for Bee ecosystem consumers. It is neither a BeeAgent domain module nor a runtime application.

## Public responsibilities in v0.1

- define module authority, context, result and structural module protocol;
- define a minimal artifact-writing port owned by a host;
- define a module-facing capability caller and bounded result/status;
- publish a stable top-level API from `beesdk`.

## Explicit exclusions

BeeSDK does not own orchestration, runs or sessions, configuration, storage, artifact paths, capability execution, capability gateways, networking, subprocesses, provider/LLM integration, UI, dependency injection or plugin discovery. It contains no ROP-specific or BeeScan-specific contract.

## Authority boundary

`CapabilityCaller.call(capability_name, payload)` is the only module-facing capability call shape in v0.1. A module cannot supply authority, module identity, run identity, session identity or case type. The host/runtime owns that context and enforces policy before any execution. `CapabilityResult.authority` reports host-applied authority; it does not grant authority.

`ModuleContext.artifact_api` preserves the established field name for migration compatibility, but its type is `ArtifactPort | None`; BeeSDK ships no artifact implementation.
