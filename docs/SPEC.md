# SPEC — BeeSDK

## 0. Terms

- Repository: `beesdk`
- Python distribution: `beesdk`
- Python import package: `beesdk`
- Consumer: project/package that depends on BeeSDK
- Host: runtime that provides module context and port implementations, currently primarily BeeAgent
- Module: domain component implementing the shared module contract
- Contract: public type/protocol/enum that defines interoperability
- Port: abstract host-provided capability described by a `Protocol`
- Authority: host-owned permission level
- Artifact: host-owned persisted output exposed to module through an abstract port
- Capability: bounded host-owned way for a module to request data/action
- Public API: contracts imported from explicit public contract modules
- Runtime implementation: executable/storage/network/orchestration code that is explicitly outside BeeSDK

## 1. Goal

BeeSDK provides a small, reusable and typed public contract layer for Bee ecosystem projects.

The goal is to prevent this pattern:

```text
BeeAgent defines contract A
ROP copies contract A'
BeeScan copies contract A''
future product copies contract A'''
```

and replace it with:

```text
BeeSDK defines contract A
     ↑
     ├── BeeAgent
     ├── ROP
     ├── BeeScan
     └── future consumers
```

BeeSDK should allow shared integration without exposing BeeAgent internals.

## 2. Product principles

- KISS;
- contracts before frameworks;
- consumer-proven abstractions only;
- stable public imports;
- clear ownership;
- compatibility matters;
- host owns runtime identity and authority;
- consumers own domain logic;
- BeeSDK owns no execution;
- zero runtime dependencies in v0.1;
- no hidden I/O;
- no product-specific semantics.

## 3. Dependency rule

Required direction:

```text
consumer -> beesdk
```

BeeSDK must not depend on:

```text
beeagent
beeagent-rop
beeui
beescan
future consumer implementations
```

v0.1 runtime rule:

```text
beesdk -> Python standard library only
```

## 4. Public API v0.1

Supported public contract-module imports:

```python
from beesdk.artifacts import ArtifactPort
from beesdk.capabilities import CapabilityCaller, CapabilityResult, CapabilityStatus
from beesdk.modules import AuthorityLevel, ModuleContext, ModuleContract, ModuleResult
```

`src/beesdk/__init__.py` remains empty. `beesdk.artifacts`, `beesdk.capabilities` and `beesdk.modules` are stable public contract modules; no `__all__` re-export layer is used.

## 5. AuthorityLevel

`AuthorityLevel` defines host-assigned module authority.

Values:

```text
read_only
draft_only
execution_capable
```

Semantics:

### `read_only`

Module/runtime path may inspect/read through capabilities allowed by host policy but must not perform mutations merely because this enum value exists.

### `draft_only`

Module may produce draft/intention/recommendation outputs but does not automatically receive external mutation rights.

### `execution_capable`

Host may permit bounded execution through separately enforced policy/capability implementation.

Important:

> The enum represents authority assigned by host. It does not implement or enforce authority by itself.

## 6. ModuleContext

`ModuleContext` represents one host-provided module invocation.

Current public fields:

```text
run_id
case_type
module_id
payload
session_id
authority
artifact_api
```

Semantics:

### `run_id`

Host-owned identifier of the invocation/run context.

Module must not treat an arbitrary payload value as a replacement for host-supplied `run_id`.

### `case_type`

Case/scenario selected by host for the module invocation.

### `module_id`

Host-known module identity for the invocation.

### `payload`

Input data for the domain module.

BeeSDK does not validate product-specific payload schema.

Consumer/domain module owns domain validation.

### `session_id`

Optional/empty host-provided session identifier.

### `authority`

Authority assigned by host.

May be absent where host has not bound it into the context yet.

### `artifact_api`

Optional host-provided `ArtifactPort`.

The field name `artifact_api` is intentionally retained for compatibility with existing BeeAgent/module integration.

BeeSDK does not ship an artifact implementation.

## 7. ModuleResult

`ModuleResult` is the bounded result returned from module to host.

Fields:

```text
module_id
case_type
authority
status
summary
data
```

Semantics:

- `module_id` — module returning the result;
- `case_type` — handled scenario;
- `authority` — authority associated with the host invocation/result;
- `status` — bounded consumer-defined/host-readable status string;
- `summary` — concise result summary;
- `data` — structured result payload.

`ModuleResult` does not grant authority for another operation.

## 8. ModuleContract

`ModuleContract` is a structural protocol.

Required surface:

```python
module_id
authority
supported_case_types()
handle(context)
```

Conceptually:

```python
class ModuleContract(Protocol):
    @property
    def module_id(self) -> str: ...

    @property
    def authority(self) -> AuthorityLevel: ...

    def supported_case_types(self) -> list[str]: ...

    def handle(self, context: ModuleContext) -> ModuleResult: ...
```

BeeSDK does not require inheritance from a framework base class.

No plugin system is required.

## 9. ArtifactPort

`ArtifactPort` defines the minimal host-owned artifact boundary currently required by consumers.

Current v0.1 operation:

```text
write_json(filename, data)
```

It intentionally does not expose:

```text
artifact root
Path
filesystem implementation
delete
glob
arbitrary path
retention
storage database
```

Host is responsible for:

- filename validation;
- storage location;
- access policy;
- retention;
- serialization implementation;
- operator visibility;
- security/redaction.

BeeSDK only defines the port shape.

## 10. CapabilityStatus

`CapabilityStatus` defines bounded result status.

Values:

```text
ok
refused
timeout
error
```

Semantics:

### `ok`

Host reports successful bounded capability execution.

### `refused`

Host policy or capability boundary refused the request.

### `timeout`

Bounded execution did not complete within host-defined limit.

### `error`

Execution failed for another controlled reason.

Status is outcome evidence, not new authority.

## 11. CapabilityResult

`CapabilityResult` contains bounded host-returned capability evidence.

Fields:

```text
capability_name
status
authority
summary
data
diagnostics
```

Semantics:

- `capability_name` — capability that was requested;
- `status` — bounded outcome;
- `authority` — host-applied authority context;
- `summary` — bounded human-readable summary;
- `data` — structured result;
- `diagnostics` — bounded diagnostic metadata.

Consumers must not treat diagnostics or result data as execution authority.

## 12. CapabilityCaller

`CapabilityCaller` is the module-facing capability request port.

Public call shape:

```python
caller.call(
    capability_name,
    payload,
)
```

The caller must not expose module-controlled parameters for:

```text
authority
module_id
run_id
session_id
case_type
host policy
credentials
```

This ensures host/runtime remains responsible for identity and authority binding.

Correct ownership:

```text
module:
    capability_name
    payload

host:
    module identity
    run identity
    session identity
    authority
    policy
    connector implementation
    credentials
```

## 13. Capability execution is not part of v0.1

BeeSDK v0.1 does not define:

- `CapabilityRuntime`;
- `ScopedCapabilityGateway`;
- provider registry;
- MCP execution;
- HTTP execution;
- retries;
- rate limits;
- credential loading.

It only defines module-facing/public result contracts.

Runtime implementation belongs to host.

## 14. Artifact implementation is not part of v0.1

BeeSDK does not define:

- storage directory;
- `Path`;
- run directories;
- JSON writer implementation;
- artifact reading;
- allowlists;
- retention.

BeeAgent may implement `ArtifactPort` using its own artifact lifecycle.

Other hosts may implement it differently.

## 15. No configuration contract in v0.1

BeeSDK has no runtime configuration.

Therefore it does not provide:

```text
config/settings.yml
.env
config loader
secret loader
runtime settings model
```

Package/tool configuration remains in:

```text
pyproject.toml
```

Future reusable config contracts require actual evidence from multiple consumers before entering SDK.

## 16. No state contract in v0.1

BeeSDK v0.1 does not define:

- project state;
- session storage;
- cross-run state;
- checkpoints;
- persistence backend.

State contracts may be considered later only when actual consumers require a shared boundary.

## 17. No UI contract

BeeSDK has no UI responsibility.

It does not define:

- HTML;
- routes;
- API endpoints;
- components;
- forms;
- sessions;
- authentication;
- BeeUI adapters.

Therefore BeeSDK does not require `docs/WEB_UI.md`.

## 18. Consumer responsibilities

A consumer must:

- depend on a compatible BeeSDK version;
- validate its own domain payload;
- implement host/runtime ports where required;
- enforce authority;
- protect credentials;
- manage storage;
- own product-specific behavior.

BeeSDK does not replace those responsibilities.

## 19. BeeAgent relationship

BeeAgent is expected to become a primary host consumer.

BeeAgent owns implementations such as:

```text
module runtime
module registry
ArtifactAPI
capability runtime
policy
context creation
storage
state
execution
```

BeeSDK owns only the portable public contract those implementations conform to.

## 20. Domain module relationship

Domain modules may depend on BeeSDK for integration contracts.

Example responsibilities remain outside SDK:

### `beeagent-rop`

- lead classification;
- duplicate semantics;
- ROP taxonomy;
- ROP summary;
- recommendations.

### `beescan`

- security scanning domain;
- scan definitions;
- findings;
- domain policy/results.

Shared domain-neutral contracts may move into BeeSDK only when reuse is real and semantics are genuinely common.

## 21. Compatibility rules

Public compatibility includes:

- import names;
- enum values;
- dataclass fields;
- defaults;
- protocol signatures;
- ownership semantics;
- type annotations.

Prefer additive change.

Examples of potentially breaking change:

```text
removing public export
renaming field
removing enum value
changing required constructor parameter
changing protocol method signature
moving authority ownership from host to caller
```

Such changes require explicit migration review.

## 22. Public field naming

Existing public names should not be changed only for style.

Example:

```text
artifact_api
```

may not be the most abstract future name, but it is intentionally preserved for compatibility during extraction/adoption.

A rename should occur only through an explicit compatibility/migration task.

## 23. Versioning

BeeSDK uses SemVer.

Source of truth:

```text
pyproject.toml
```

Versions are independent of consumer versions.

Example:

```text
beesdk 0.1.0
beeagent 0.53.2
beeagent-rop 0.19.6
beeui 0.26.1
```

Consumers choose a compatible BeeSDK release.

Ordinary feature/fix PR does not manually bump package version.

Release automation manages release version lifecycle.

## 24. Package guarantees

BeeSDK should remain:

- importable without BeeAgent;
- importable without ROP;
- importable without BeeUI;
- importable without BeeScan;
- stdlib-only at runtime in v0.1;
- typed through `py.typed`;
- free from runtime side effects at import.

## 25. Maturity rule

BeeSDK is developing correctly when:

- consumer contracts stop being copied;
- BeeAgent can implement contracts without SDK importing BeeAgent;
- domain modules depend only on public contracts;
- adding another real module requires less integration duplication;
- security/authority ownership remains host-side;
- SDK itself remains small.

BeeSDK is developing incorrectly when:

- it becomes a second orchestrator;
- it accumulates product-specific models;
- it gains arbitrary execution;
- it adds abstractions without consumers;
- every Bee project is forced to depend on it without need.

## 26. Current v0.1 boundary

Current v0.1 is intentionally limited to:

```text
module contracts
artifact port
capability caller/result/status
stable public contract-module API
typed package
```

Everything else requires separate evidence and roadmap work.

## Summary

BeeSDK answers one question:

> What is the smallest stable public contract Bee components can share without sharing runtime implementation?

Everything outside that question belongs somewhere else until proven otherwise.
