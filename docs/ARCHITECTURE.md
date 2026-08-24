# BeeSDK architecture

## Dependency direction

```text
beesdk
  ↑
  ├── beeagent
  ├── beeagent-rop
  ├── beescan
  └── future Bee consumers
```

Consumers depend on BeeSDK; BeeSDK never depends on a consumer. In v0.1 the runtime dependency rule is explicit:

```text
beesdk -> stdlib only
```

## Ownership

BeeSDK owns only portable contracts. A host such as BeeAgent owns orchestration, run/session context, authority enforcement, capability routing and artifact lifecycle. A domain product owns its own business taxonomy and rules. BeeUI owns generic presentation.

## Ports, not implementations

`ArtifactPort` and `CapabilityCaller` are host-provided ports. BeeSDK supplies neither a filesystem implementation nor a capability runtime/gateway. This keeps contracts portable and prevents an SDK import from creating execution or egress behavior.
