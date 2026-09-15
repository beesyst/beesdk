# SECURITY — BeeSDK

## Purpose

This document defines practical security rules for `beesdk`.

BeeSDK is a contracts-only library, so its security profile differs from BeeAgent runtime.

BeeSDK does not own:

- credentials;
- servers;
- storage;
- external connectors;
- execution;
- operator sessions.

Its main security responsibilities are:

- preserving authority boundaries;
- preventing caller-controlled privilege escalation;
- keeping contracts narrow;
- avoiding hidden runtime side effects;
- protecting dependency direction;
- keeping supply-chain surface minimal;
- defining safe boundaries for host implementations.

Use this document with:

- `docs/SPEC.md`;
- `docs/ARCHITECTURE.md`;
- `docs/SDLC.md`;
- `docs/ROADMAP.md`.

## Core security principle

BeeSDK must describe authority.

It must not create authority.

The host/runtime is responsible for:

- identity;
- policy;
- authorization;
- execution;
- credentials;
- storage;
- egress.

## What we protect

At minimum BeeSDK should protect:

- module/host trust boundary;
- authority semantics;
- capability caller boundary;
- artifact port boundary;
- stable public contract;
- dependency integrity;
- package integrity;
- consumer isolation.

## Security boundary

Importing:

```python
import beesdk
```

must not:

- access network;
- read environment variables;
- read files;
- create files;
- start threads;
- start services;
- execute subprocesses;
- initialize external SDK clients;
- connect to databases;
- mutate consumer state.

BeeSDK imports should define contracts only.

## Dependency direction

Allowed:

```text
consumer -> beesdk
```

Forbidden:

```text
beesdk -> beeagent
beesdk -> beeagent-rop
beesdk -> beescan
beesdk -> beeui
```

A reverse dependency can create:

- hidden authority coupling;
- circular imports;
- deployment coupling;
- accidental access to runtime implementation;
- second sources of truth.

## Runtime dependencies

v0.1 runtime dependency target:

```text
[]
```

Any runtime dependency addition is security-sensitive.

Before adding a dependency review:

- necessity;
- maintenance quality;
- vulnerability surface;
- transitive dependency graph;
- licensing;
- whether functionality belongs in consumer instead.

Never add a dependency “just in case”.

## Authority model

Public authority values:

```text
read_only
draft_only
execution_capable
```

Authority must be assigned by host/runtime.

Module-controlled payload cannot grant authority.

Never infer execution authority from:

- payload text;
- AI output;
- module result;
- capability result alone;
- arbitrary enum/string restored from untrusted source.

Host must validate and bind authority independently.

## Capability boundary

`CapabilityCaller` is a module-facing port.

Allowed module-controlled values:

```text
capability_name
payload
```

The module-facing call must not accept caller-controlled:

```text
authority
module_id
run_id
session_id
case_type
policy
credential
connector URL
```

Reason:

A module must not be able to create a request such as:

```text
authority=execution_capable
module_id=trusted-admin-module
```

and have the host trust it.

Correct model:

```text
module input
    ↓
host-bound caller
    ↓
host injects identity + authority
    ↓
host applies policy
    ↓
execution
```

## Capability result

`CapabilityResult` represents host-reported outcome.

It does not itself create:

- approval;
- permission;
- execution authority;
- persistent trust.

Consumers must not interpret:

```text
status=ok
```

as permission to perform a different action.

## Artifact boundary

`ArtifactPort` is an abstract host-controlled port.

BeeSDK does not define:

- storage root;
- arbitrary path access;
- filename allowlist;
- filesystem permissions;
- retention;
- artifact visibility;
- serialization implementation.

Host implementations are responsible for those controls.

Do not add path-oriented APIs like:

```text
write(path)
open(path)
delete(path)
glob(path)
```

without explicit security-sensitive scope.

If such functionality is needed, first determine whether it belongs in host runtime rather than SDK.

## External input

Treat module payloads and implementation objects as potentially untrusted.

BeeSDK should not silently deserialize or execute arbitrary values.

Current contracts intentionally keep validation minimal because domain schema validation belongs to consumer/host.

If BeeSDK later adds reusable validation:

- validation must be bounded;
- malformed input must fail predictably;
- validation must not grant authority;
- parser/serialization changes become security-sensitive.

## No secret ownership

BeeSDK does not need:

```text
.env
secret loader
credential model
API token handling
auth headers
```

Do not introduce them without a fundamental architecture change.

Secrets belong to runtime/consumer projects.

BeeSDK tests/docs/examples must not contain real:

- tokens;
- API keys;
- webhook URLs;
- customer credentials;
- private client payloads.

## No logging framework

BeeSDK does not currently need runtime logging.

Do not add a package-level logger simply for consistency with BeeAgent.

If future code needs diagnostics, ensure that:

- no secrets exist in payload examples;
- no unbounded consumer payload is logged;
- no runtime behavior is introduced at import.

## No execution / egress

BeeSDK itself must not perform:

- HTTP requests;
- MCP calls;
- n8n calls;
- subprocess execution;
- shell commands;
- Bitrix calls;
- email access;
- filesystem mutation.

Ports may describe such capabilities abstractly.

Implementations live in host/consumer.

## Consumer-specific data

Do not commit real consumer data into BeeSDK.

Tests should use synthetic generic fixtures.

BeeSDK should not know:

- Welding-specific senders;
- ROP taxonomy;
- BeeScan targets;
- Bitrix portal IDs;
- client routing data.

If a contract requires consumer-specific examples to explain itself, prefer minimal synthetic examples.

## Public API as a security boundary

Because BeeSDK is shared, public API changes can alter trust assumptions across consumers.

Review:

- who controls each field;
- who validates each field;
- who assigns authority;
- whether data is evidence or authority;
- whether a module can impersonate host state;
- whether optional defaults weaken policy.

Security-relevant distinction:

```text
evidence != authority
result != approval
payload != trusted identity
```

## Type contract

BeeSDK ships `py.typed`.

Type annotations therefore affect consumer integration.

Typing must not suggest unsafe ownership.

For example, module-facing contract should not expose an `authority` argument if host owns authority.

Structural protocols should accurately describe what host implementation must provide.

## Security checks

Use only checks appropriate to the change.

## SAST

Use SAST/mindset review for:

- capability contracts;
- authority semantics;
- public protocol changes;
- validation;
- parsing;
- serialization;
- package code with non-trivial logic.

Look for:

- authority supplied by caller;
- hidden I/O;
- dynamic execution;
- consumer imports;
- unsafe path surface;
- overly broad `Any` where it obscures trust ownership;
- accidental runtime side effects.

## SCA

Required when dependencies change.

Review:

```text
pyproject.toml
uv.lock
```

Check:

- direct dependencies;
- transitive dependencies;
- known vulnerabilities;
- package necessity.

## DAST

Normally not applicable.

BeeSDK has no network-facing service.

If a task suddenly requires DAST, first verify that runtime/network functionality has not incorrectly moved into SDK.

## IAST

Not default.

Only relevant if future scope adds a security-sensitive executable runtime, which requires architecture review first.

## Fuzzing

Not default for simple protocols/dataclasses.

Consider fuzzing only if BeeSDK adds:

- parser;
- deserializer;
- normalization engine;
- complex reusable validation of untrusted structures.

## Change levels

### low-risk

Examples:

- docs;
- tests;
- formatting;
- internal non-public cleanup.

Usually:

- normal review;
- applicable tests.

### runtime-risk

In BeeSDK this includes normal package/consumer behavior changes:

- additive public API;
- compatible signature/default changes;
- packaging changes;
- build changes;
- non-authority compatibility changes.

Usually:

- contract tests;
- full tests;
- build/import smoke where relevant;
- compatibility review.

### security-sensitive

Examples:

- authority;
- capability caller shape;
- artifact trust boundary;
- dependency changes;
- execution-related contracts;
- parser/serialization;
- path/file APIs;
- any new runtime side effect.

Usually:

- all applicable runtime-risk checks;
- SAST;
- SCA when dependencies changed;
- targeted negative/adversarial tests;
- explicit security review in PR.

## Minimal developer security checklist

Before significant PR ask:

- can module-controlled input escalate authority?
- can caller control runtime identity?
- did SDK gain hidden I/O?
- did SDK gain consumer dependency?
- did runtime dependencies change?
- does ArtifactPort expose filesystem implementation?
- does a result object accidentally become authority?
- are public signatures compatible?
- are examples synthetic?
- is this functionality really a contract rather than runtime behavior?

## Minimal reviewer checklist

Reviewer should verify:

- ownership remains clear;
- authority remains host-owned;
- dependency direction remains correct;
- no consumer implementation moved into SDK;
- new contract is actually reusable;
- runtime dependencies are justified;
- public API is minimal;
- compatibility impact is documented;
- tests cover negative boundary cases where relevant.

## Supply-chain and release security

Release/package metadata should remain reproducible.

Source of truth:

```text
pyproject.toml
uv.lock
```

Release automation should operate through reviewed repository configuration.

Do not:

- manually upload unknown build artifacts;
- commit generated `.egg-info`;
- commit local virtualenv;
- include consumer source code in package;
- add arbitrary release scripts with hidden network behavior.

Package build should contain only intended BeeSDK package content.

## What not to do

Avoid:

- runtime framework inside SDK;
- generic “execute anything” capability;
- caller-controlled authority;
- arbitrary file/path APIs;
- dynamic import/install of plugins;
- hidden env/config behavior;
- dependencies added for convenience only;
- product/client rules;
- treating AI output as trust/authority;
- security theater requiring every tool for every change.

## Summary

BeeSDK security is primarily boundary security.

Keep it safe by keeping it small:

```text
no execution
no secrets
no hidden I/O
no consumer dependencies
host-owned authority
narrow ports
minimal dependency surface
```
