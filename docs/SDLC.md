# SDLC — BeeSDK

## Purpose

This document defines the lightweight SDLC used in `beesdk`.

Цель процесса:

- сохранять public contracts стабильными;
- не ломать consumers случайными изменениями;
- поддерживать security boundaries;
- иметь воспроизводимые releases;
- не создавать лишнюю бюрократию для небольшого SDK.

BeeSDK использует два уровня workflow:

```text
low-risk maintenance
→ check
→ main
```

и:

```text
significant contract change
→ ROADMAP / Issue
→ branch
→ code
→ tests
→ PR
→ merge
→ release process
```

Kanban / GitHub Project не является обязательной частью BeeSDK process.

## Sources of truth

Документы разделяют ответственность:

- `docs/ROADMAP.md` — куда развивается SDK;
- `docs/SPEC.md` — что является public contract;
- `docs/ARCHITECTURE.md` — dependency/ownership boundaries;
- `Issue` — что требуется сделать в конкретной significant task;
- `PR` — что реально сделано и проверено;
- `docs/SDLC.md` — как проводить изменения;
- `docs/SECURITY.md` — как оценивать trust/security impact;
- `pyproject.toml` — package metadata, dependencies и current version.

## Core principles

Development in `beesdk` follows these rules:

- KISS;
- small changes;
- public API remains explicit;
- consumer need before abstraction;
- compatibility before cosmetic cleanup;
- zero consumer dependencies;
- zero runtime dependencies in v0.1 unless explicitly approved;
- no runtime implementation inside contracts package;
- authority remains host-owned;
- security checks proportional to the actual change;
- no manual version bump in ordinary feature/fix work.

## Two delivery paths

### Path A — low-risk direct maintenance

Direct `main` is acceptable for obvious low-risk changes such as:

- typo/document wording;
- test-only cleanup with no contract behavior change;
- formatting;
- small repository housekeeping;
- non-public refactor with no package/consumer impact.

Issue and PR are optional.

Conditions:

- no public API change;
- no dependency change;
- no package compatibility impact;
- no authority/capability/artifact boundary change;
- no release-related behavior change;
- change is easy to review locally.

Run applicable checks before commit.

### Path B — significant change

Use Issue → branch → PR when change affects:

- public API;
- exported names;
- dataclass/protocol signatures;
- enum values;
- module contract;
- artifact contract;
- capability contract;
- compatibility;
- package/build behavior;
- runtime dependency surface;
- authority/trust boundary;
- release mechanics.

For these changes direct `main` should not be the default path.

## ROADMAP

`docs/ROADMAP.md` contains coherent SDK increments.

A roadmap iteration should describe:

- Goal;
- Scope;
- Excluded;
- Deliverable;
- Acceptance criteria;
- Checks;
- DoD.

Do not create roadmap iterations for:

- typos;
- tiny docs cleanup;
- trivial test maintenance;
- unrelated housekeeping.

## Issue

Significant task should use `.github/ISSUE_TEMPLATE/issue.md`.

Issue explains:

- what is missing;
- why it matters;
- scope;
- deliverable;
- acceptance criteria;
- public API/compatibility impact;
- dependency impact;
- security impact;
- checks.

One implementation repository should normally have one Issue.

## Branch

For significant changes use a separate branch.

Recommended names:

```text
feature/<short-name>
fix/<short-name>
docs/<short-name>
chore/<short-name>
test/<short-name>
```

If useful:

```text
feature/sdk-2-beeagent-adoption-contract
fix/12-artifact-port-compatibility
```

`main` remains stable.

## Code

Implementation rules:

- stay inside approved scope;
- reuse existing contracts;
- do not redesign unrelated APIs;
- do not add speculative framework layers;
- do not add consumer-specific semantics;
- do not introduce dependency without approval;
- do not change version manually;
- preserve public field names unless migration explicitly requires a breaking change.

## Tests

Default test command:

```bash
uv run pytest -q
```

Package/build changes additionally run:

```bash
uv build
```

Import smoke when applicable:

```bash
uv run python -c "import beesdk; print(beesdk.__file__)"
```

Contract changes should include targeted tests for:

- public imports;
- signatures;
- defaults;
- enum values;
- compatibility;
- negative boundary behavior.

## Build artifacts

BeeSDK does not have runtime artifacts like BeeAgent `storage/`.

Relevant project outputs are:

- tests;
- package metadata;
- built wheel;
- source distribution;
- generated package metadata.

Generated build outputs are verification evidence and normally are not committed.

## Pull Request

Significant PR should explain:

- Summary;
- related Issue;
- iteration;
- Scope;
- Changes;
- Package/Public API/Contract impact;
- Verification;
- Security review;
- Version/release decision;
- Limitations/follow-ups.

PR is the primary delivery evidence for significant work.

## Merge

A significant task is ready to merge when:

- acceptance criteria are satisfied;
- public contract is explicit;
- compatibility impact is understood;
- required tests pass;
- package builds when applicable;
- security checks are complete;
- docs match actual behavior;
- no unintended consumer/runtime dependency exists.

## Change levels

Use only three levels.

### low-risk

Examples:

- docs;
- test-only additions;
- formatting;
- internal cleanup with no public impact.

Usually required:

- relevant targeted check;
- full tests only when code/test infrastructure warrants it.

Issue/PR may be skipped when truly trivial.

### runtime-risk

For BeeSDK this means package/consumer behavior risk rather than application runtime ownership.

Examples:

- additive public API;
- compatible module contract addition;
- changed defaults;
- packaging behavior;
- build metadata;
- consumer compatibility adjustment;
- public typing changes without authority/security impact.

Usually required:

```text
targeted contract tests
uv run pytest -q
uv build when packaging/public package is affected
consumer compatibility smoke when relevant
```

### security-sensitive

Examples:

- authority semantics;
- `CapabilityCaller` boundary;
- execution-related contract;
- artifact trust boundary;
- serialization/deserialization of untrusted data;
- dependency addition;
- path/file contract;
- secret/auth contract;
- code that could create execution/egress side effects.

Usually required:

- runtime-risk checks;
- SAST;
- SCA if dependencies changed;
- targeted negative/adversarial tests;
- explicit authority/trust review.

DAST/IAST/fuzzing only when applicable.

## Security-aware check selection

Do not run every security technique for every PR.

Use:

### SAST

Expected for:

- code-heavy contract changes;
- authority/capability changes;
- parsing/validation;
- package code handling untrusted values.

### SCA

Expected when:

```text
pyproject.toml dependency surface changes
uv.lock dependency graph changes
```

### DAST

Normally not applicable because BeeSDK has no network runtime.

DAST becomes relevant only if BeeSDK scope fundamentally changes to include a network-facing runtime, which itself requires architecture review.

### IAST

Not default.

Use only if future SDK functionality introduces a meaningful instrumentable security-sensitive runtime.

### Fuzzing

Useful only if BeeSDK introduces:

- parser;
- serializer/deserializer;
- structured untrusted-input validator;
- fragile normalization logic.

Current simple dataclass/protocol contracts do not require broad fuzzing.

## Public API compatibility rules

A public contract change must evaluate:

- export names;
- constructor fields;
- defaults;
- enum values;
- protocol signatures;
- return types;
- field semantics;
- typing compatibility;
- affected consumers.

Prefer additive compatibility over breaking replacement.

Do not rename a public field only because another name looks cleaner.

## Dependency rules

v0.1 target:

```text
runtime dependencies = []
```

Any runtime dependency addition is significant and security-sensitive.

Before adding one, Issue must answer:

- why stdlib is insufficient;
- which public contract requires it;
- why dependency belongs in BeeSDK rather than consumer;
- maintenance/security impact;
- whether zero-dependency boundary can be preserved.

If dependencies change:

- update `pyproject.toml`;
- update `uv.lock`;
- run SCA/review;
- verify build.

## Versioning

BeeSDK uses SemVer.

Current version source of truth:

```text
pyproject.toml
```

Ordinary feature/fix PR:

```text
do not manually edit version
```

Release automation uses Conventional Commits.

General mapping:

```text
feat:          MINOR
fix:           PATCH
docs:          no version bump
test:          no version bump
refactor:      no version bump
chore:         no version bump
ci:            no version bump
build:         normally no version bump
feat!:         breaking / MAJOR
BREAKING CHANGE: breaking / MAJOR
```

Release-please owns release PR/version/changelog/tag lifecycle after bootstrap release is established.

## CHANGELOG

`CHANGELOG.md` is release history, not an implementation diary.

Do not manually add entries for every local commit unless release workflow explicitly requires it.

Release PR should keep release history synchronized.

## ROADMAP update rules

Update `docs/ROADMAP.md` when:

- iteration status changes;
- iteration contract changes;
- public SDK direction changes;
- significant capability is added/removed;
- planned sequencing changes.

Do not update ROADMAP for tiny implementation details.

## Docs update rules

Check documentation if one of these changes:

- public API;
- compatibility;
- package usage;
- architecture boundary;
- dependency rule;
- authority rule;
- development/release flow.

Do not touch every doc mechanically.

## Definition of Done

For significant contract work:

- implementation matches Issue;
- public API is explicit;
- compatibility has been assessed;
- targeted tests exist;
- `uv run pytest -q` passes;
- `uv build` passes when applicable;
- import smoke passes when applicable;
- dependency direction remains correct;
- required security checks completed;
- docs reflect actual contract;
- version was not manually changed unless task is explicitly release-related;
- PR contains sufficient verification evidence.

For low-risk direct maintenance:

- change is truly low-risk;
- applicable check passes;
- no hidden contract/dependency/release impact exists.

## KISS process rule

Do not require:

- Kanban for every task;
- Issue for typo;
- PR for one-line docs fix;
- release for docs-only change;
- full security suite for simple contract-neutral work.

Do require stronger process when the thing that makes BeeSDK valuable is being changed:

```text
public contract
compatibility
authority
dependencies
```

## Summary

BeeSDK process should remain lighter than BeeAgent runtime process.

The purpose of SDLC here is not bureaucracy.

It is to prevent three expensive problems:

```text
breaking consumers
accidental authority expansion
uncontrolled dependency drift
```
