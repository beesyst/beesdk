# BeeSDK security

## Security boundary

BeeSDK is contracts-only. It must not create execution authority, network egress, subprocess execution, storage access or configuration-driven behavior at import time.

## Capability authority

Modules may provide only a capability name and payload through `CapabilityCaller`. They must not control authority, `module_id`, `run_id`, `session_id` or `case_type`. Hosts must bind and validate that identity and authority server-side. A result object is evidence of an outcome, not execution authority.

## Artifact boundary

`ArtifactPort` is an abstract host port. Hosts are responsible for allowlisted paths, filenames, serialization, retention and access control. BeeSDK must not add a path-based or filesystem implementation without an approved security-sensitive scope.

## Dependencies and input

v0.1 runtime dependencies remain empty. Any runtime dependency addition is security-sensitive and requires review. Treat payloads and protocol implementations as untrusted; consumers validate their own schema, authorization and output handling.
