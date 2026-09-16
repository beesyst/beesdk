# ROADMAP — BeeSDK (SDLC-light, shared contracts)

## Purpose

Этот документ фиксирует маршрут развития `beesdk` по этапам и итерациям.

ROADMAP в проекте используется как lightweight SDLC-артефакт:

- задаёт направление развития shared SDK;
- фиксирует цель каждой значимой итерации;
- определяет ожидаемые public contracts, compatibility expectations и проверки;
- помогает связывать Issue → Code → Tests → Package → PR → Merge → Release;
- не позволяет превращать BeeSDK в speculative framework без реальных consumers.

ROADMAP не заменяет Issue и PR:

- **Issue** объясняет, что именно нужно сделать в рамках конкретной значимой задачи;
- **PR** фиксирует, что реально было сделано и как это проверялось;
- **ROADMAP** показывает, куда развивается SDK и что считается готовностью iteration-level contract.

Значимая roadmap iteration закрывается через PR.

Мелкие low-risk изменения, которые не затрагивают public API, compatibility, dependencies, package/release behavior или security boundaries, могут выполняться напрямую в `main` согласно `docs/SDLC.md` и не требуют отдельной roadmap iteration.

ROADMAP не дублирует полные правила проекта:

- public contract и границы продукта описываются в `docs/SPEC.md`;
- dependency direction и ownership — в `docs/ARCHITECTURE.md`;
- development process, change levels и delivery rules — в `docs/SDLC.md`;
- authority/trust/security rules — в `docs/SECURITY.md`;
- практическая разработка, package build и consumer integration — в `docs/DEV_GUIDE.md`.

---

## Vision

| Block                           | Statement                                                                                                                                                    |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Product identity**            | `beesdk` развивается как небольшой standalone typed Python package с reusable public contracts для Bee ecosystem.                                            |
| **Primary objective**           | Убрать дублирование общих integration contracts между BeeAgent, domain modules и будущими Bee consumers без переноса runtime implementation в SDK.           |
| **Dependency principle**        | Consumers могут зависеть от BeeSDK; BeeSDK никогда не зависит от `beeagent`, `beeagent-rop`, `beescan`, `beeui` или другого consumer implementation.         |
| **Contract principle**          | В SDK попадают только небольшие, стабильные и реально необходимые shared contracts.                                                                          |
| **Consumer-evidence principle** | Новый contract добавляется только при доказанном consumer need, а не потому, что потенциально может пригодиться.                                             |
| **Runtime principle**           | BeeSDK определяет contracts и ports, но не владеет orchestration, runtime state, storage implementation, capability execution, connectors, providers или UI. |
| **Authority principle**         | Runtime identity, policy и execution authority принадлежат host. Module-facing API не должен позволять caller самостоятельно назначать себе authority.       |
| **Artifact principle**          | SDK определяет минимальный artifact port; paths, retention, serialization implementation и access policy остаются host-owned.                                |
| **Capability principle**        | Module-facing capability contract остаётся narrow: module передаёт capability intent/payload, host добавляет identity, authority и policy.                   |
| **Compatibility principle**     | Public imports, fields, enums, signatures, defaults и ownership semantics являются compatibility surface и не меняются ради косметики.                       |
| **Package principle**           | BeeSDK должен устанавливаться и импортироваться независимо от всех consumer projects.                                                                        |
| **Dependency rule**             | Runtime dependency target — Python standard library only, пока реальная contract need не докажет иное.                                                       |
| **Typing principle**            | `py.typed` является частью package contract; type signatures рассматриваются как consumer-facing API.                                                        |
| **Versioning principle**        | BeeSDK имеет собственный SemVer lifecycle, независимый от версий BeeAgent, ROP, BeeUI и других consumers.                                                    |
| **Release principle**           | Обычные feature/fix PR не bump-ят version вручную; version/changelog/tag lifecycle ведётся release automation.                                               |
| **Security rule**               | SDK не должен создавать execution, network egress, filesystem access, secret loading или другие runtime side effects только из-за import/use contracts.      |
| **KISS rule**                   | BeeSDK должен оставаться маленьким. Новый framework layer, dependency или abstraction появляется только после реальной необходимости.                        |

---

## Development principles

Делаем маленькие contract-sized изменения.

Каждая значимая roadmap iteration должна:

- иметь конкретного consumer или подтверждённый architecture gap;
- оставаться внутри declared scope;
- сохранять dependency direction:

```text
consumer -> beesdk
```

- сохранять независимую installability BeeSDK;
- сохранять explicit public API через public contract modules;
- включать compatibility assessment;
- иметь contract tests;
- проходить package build, когда затрагивается package/public surface;
- проходить required quality/security checks из `docs/SDLC.md` и `docs/SECURITY.md`;
- не переносить host runtime implementation в SDK;
- не добавлять consumer-specific domain semantics;
- не добавлять runtime dependencies без отдельного обоснования;
- не менять package version вручную в обычной implementation task.

Для BeeSDK особенно важно:

```text
shared contract
!=
shared implementation
```

и:

```text
evidence
!=
authority
```

---

## KISS roadmap rule

ROADMAP BeeSDK намеренно должен оставаться коротким.

Не нужно заранее создавать десятки iterations для:

```text
state
config
execution
egress
plugins
providers
storage
networking
UI
```

только потому, что такие abstractions существуют в других SDK.

Новый roadmap item появляется, когда есть хотя бы одно из условий:

1. contract уже существует в consumer и начинает дублироваться;
2. два или более consumers требуют одинаковую semantic boundary;
3. новый реальный consumer невозможно корректно подключить существующим API;
4. integration выявила compatibility/security gap в текущем contract;
5. отсутствие shared contract приводит к реальному architecture drift.

Недостаточные причины:

```text
"может пригодиться"
"будет красивее"
"так делают большие SDK"
"давайте сразу заложим на будущее"
```

---

## SDLC workflow for roadmap items

Значимая BeeSDK iteration проходит по упрощённому циклу:

1. **Planning**

   Определяется реальный consumer/gap и необходимость изменения BeeSDK.

2. **Requirements**

   Определяются:
   - Goal;
   - Scope;
   - Excluded;
   - Deliverable;
   - Acceptance criteria;
   - compatibility impact;
   - dependency impact;
   - security impact;
   - Checks;
   - DoD.

3. **Issue**

   Significant public-contract work оформляется как Issue.

4. **Implementation**

   Изменение выполняется в отдельной branch.

5. **Verification**

   Выполняются:
   - targeted contract tests;
   - full tests;
   - package build, если применимо;
   - import/public API checks;
   - consumer compatibility checks, если применимо;
   - required quality/security checks.

6. **Review / PR**

   В PR фиксируются actual implementation и verification evidence.

7. **Merge**

   Изменение попадает в `main`.

8. **Release**

   Если изменение требует нового package release, version/changelog/tag lifecycle выполняется через принятую release automation.

Tiny low-risk docs/test/chore maintenance может использовать сокращённый путь из `docs/SDLC.md`.

Kanban / GitHub Project не является обязательной частью BeeSDK workflow.

---

## Status values

Допустимые статусы iterations:

- **PLANNED** — scope утверждён, implementation ещё не началась;
- **IN PROGRESS** — iteration в работе;
- **DONE** — iteration полностью завершена;
- **DONE (partial)** — завершена с осознанными documented limitations.

Для дальних направлений используется:

- **FUTURE / orientation** — направление известно, но ещё не является утверждённым implementation scope.

`FUTURE / orientation` не означает автоматического одобрения будущей архитектуры.

---

## Roadmap item format

Новые iterations используют компактную структуру:

- `Goal`
- `Scope`
- `Excluded`
- `Deliverable`
- `Acceptance criteria`
- `Checks`
- `DoD`

ROADMAP фиксирует iteration-level contract.

Подробные implementation requirements, конкретные файлы, полные payload examples, расширенные test matrices и verification evidence принадлежат Issue, implementation handoff и PR.

---

## Global Definition of Done

Значимая BeeSDK iteration считается завершённой, если:

- declared scope реализован;
- public API является явным и минимальным;
- public contract-module imports согласованы;
- compatibility impact проверен;
- type contract согласован с runtime/consumer expectations;
- dependency direction остаётся `consumer -> beesdk`;
- BeeSDK не импортирует consumer projects;
- package не получил runtime implementation без явного architecture decision;
- runtime dependency surface не изменился без approved scope;
- targeted contract tests проходят;
- `uv run pytest -q` проходит;
- `uv build` проходит, если iteration затрагивает package/public contract;
- package import smoke проходит;
- package остаётся usable без установленных BeeAgent/ROP/BeeScan/BeeUI;
- `py.typed` присутствует в built package;
- required quality/security checks выполнены;
- docs обновлены, если изменился public contract, architecture, security или development flow;
- package version не изменена вручную, если задача не является release-related;
- significant iteration delivery зафиксирован в PR.

---

## Change levels for verification

### low-risk

Изменения без public/consumer impact.

Примеры:

- docs;
- formatting;
- test-only additions;
- internal cleanup без public API change.

Обычно достаточно:

- relevant targeted checks;
- full tests, если затрагивается Python/test infrastructure.

Tiny low-risk maintenance может не иметь Issue/PR.

### runtime-risk

Для BeeSDK это package/consumer behavior risk, а не application runtime ownership.

Примеры:

- additive public contract;
- compatible public signature/default change;
- public contract-module import change;
- packaging/build behavior;
- compatibility fix;
- typed API change без trust/authority impact.

Обычно требуется:

- targeted contract tests;
- `uv run pytest -q`;
- `uv build`, когда затрагивается package/public surface;
- import/public API smoke;
- affected consumer compatibility check, если применимо.

### security-sensitive

Изменения trust boundary.

Примеры:

- authority semantics;
- capability contract;
- caller/host identity ownership;
- artifact trust boundary;
- parser/serialization of untrusted input;
- path/file API;
- execution-related contract;
- runtime dependency addition;
- secret/auth contract;
- code с runtime side effects или egress implications.

Обычно требуется:

- applicable runtime-risk checks;
- SAST;
- SCA, если dependencies изменились;
- explicit negative/adversarial boundary tests;
- security review по `docs/SECURITY.md`.

DAST/IAST/fuzzing применяются только если изменение реально создаёт соответствующую поверхность.

---

## Versioning and release rule

BeeSDK имеет собственный SemVer lifecycle.

Source of truth:

```text
pyproject.toml
```

Версии BeeSDK независимы от consumer versions.

Например:

```text
beesdk        0.1.x
beeagent      0.53.x
beeagent-rop  0.19.x
beeui         0.26.x
```

Roadmap iteration и package release — не одно и то же.

Например:

- consumer adoption может подтвердить текущий SDK contract без нового BeeSDK release;
- один additive contract может привести к MINOR release;
- compatible contract bugfix может привести к PATCH release;
- docs-only maintenance может не требовать нового package release.

Ordinary implementation PR не должен вручную менять:

```text
pyproject.toml -> project.version
```

BeeSDK использует Conventional Commits и release automation.

Базовая SemVer mapping:

| Commit             | Release impact           |
| ------------------ | ------------------------ |
| `feat:`            | MINOR                    |
| `fix:`             | PATCH                    |
| `docs:`            | no release bump          |
| `test:`            | no release bump          |
| `refactor:`        | no release bump          |
| `chore:`           | no release bump          |
| `ci:`              | no release bump          |
| `build:`           | normally no release bump |
| `feat!:` / `fix!:` | breaking / MAJOR         |
| `BREAKING CHANGE:` | breaking / MAJOR         |

Release lifecycle управляется `release-please`:

```text
commit history
→ Release PR
→ version
→ CHANGELOG
→ Git tag
→ GitHub Release
```

Expected repository baseline:

```text
.github/release-please/config.json
.github/release-please/manifest.json
.github/workflows/release-please.yml
```

Первый `v0.1.0` является contract baseline SDK-1.

Breaking public contract change требует:

- explicit compatibility analysis;
- migration strategy;
- SemVer-compatible release decision.

---

## Product phases

| Phase                                              | Status  | What it means                                                                                                                                                   |
| -------------------------------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Phase A — Contract foundation**                  | DONE    | Создан standalone typed package, governance, package/release baseline и первые shared module/artifact/capability contracts.                                     |
| **Phase B — Scoped capability integration**        | PLANNED | Реальный BeeDrill/BeeAgent integration выявил минимальный shared-contract gap: host должен иметь public способ передать существующий `CapabilityCaller` модулю. |
| **Phase C — Broader consumer adoption validation** | FUTURE  | Existing contracts проверяются более широкой миграцией BeeAgent, `beeagent-rop` и других consumers; дублирование сокращается только где это реально оправдано.  |
| **Phase D — Additional shared contracts**          | FUTURE  | Project/state или другие contracts рассматриваются только после появления реальных consumers и доказанной reusable semantics.                                   |

### Stages

- **Stage 1 — Contract foundation:** standalone package, governance, module/artifact/capability contracts, tests, package/release baseline.
- **Stage 2 — Scoped capability integration:** минимальное contract evolution, уже доказанное BeeDrill/BeeAgent integration need.
- **Stage 3 — Broader consumer adoption validation:** дальнейшая migration existing consumers и reduction duplicated shared contracts.
- **Stage 4 — Additional shared contracts:** только consumer-proven contracts; никакого заранее утверждённого framework expansion.

---

# Этап 1 — Contract foundation

## Purpose of stage

Stage 1 создаёт минимальный самостоятельный BeeSDK.

Фокус:

- standalone repository/package;
- independent package lifecycle;
- typed public API;
- module contracts;
- artifact port;
- capability caller/result contract;
- compatibility/security boundaries;
- project governance;
- tests/build;
- SemVer/release baseline.

Stage 1 не пытается реализовать runtime.

Основной architecture invariant:

```text
BeeSDK = contracts

BeeAgent / another host = implementations
```

---

## Итерация 1 — Repository and core contract foundation v0.1.0

**Status:** DONE

### Goal

Создать standalone BeeSDK v0.1.0 как минимальный typed shared-contract package для Bee ecosystem, достаточный для последующей consumer validation через BeeAgent и domain modules, но не содержащий host runtime implementation.

### Scope

**Included**

- standalone repository:
  - `beesdk`;

- Python distribution:
  - `beesdk`;

- Python import package:
  - `beesdk`;

- Python:
  - `>=3.14`;

- package management:
  - `uv`;

- standard `src` layout;
- `py.typed`;
- independent package version:
  - `0.1.0`;

- zero runtime dependencies;
- stable public contract-module API:

```python
from beesdk.artifacts import ArtifactPort

from beesdk.capabilities import CapabilityCaller, CapabilityResult, CapabilityStatus

from beesdk.modules import AuthorityLevel, ModuleContext, ModuleContract, ModuleResult
```

- module contracts:
  - `AuthorityLevel`;
  - `ModuleContext`;
  - `ModuleResult`;
  - `ModuleContract`;

- artifact contract:
  - minimal `ArtifactPort`;

- capability contracts:
  - `CapabilityCaller`;
  - `CapabilityResult`;
  - `CapabilityStatus`;

- host-owned authority semantics;
- module-facing capability API without caller-controlled runtime identity/authority;
- compatibility-oriented extraction of existing BeeAgent module contracts;
- contract/public API tests;
- dependency-direction tests;
- zero-runtime-dependency tests;
- consumer-import guard tests;
- capability authority-boundary tests;
- package build verification;
- project governance:
  - `AGENTS.md`;
  - `docs/ROADMAP.md`;
  - `docs/SPEC.md`;
  - `docs/ARCHITECTURE.md`;
  - `docs/SDLC.md`;
  - `docs/SECURITY.md`;
  - `docs/DEV_GUIDE.md`;

- project-local development workflow:
  - `.agents/prompts/01-planning.md`;
  - `.agents/prompts/02-implementation-tests.md`;
  - `.agents/prompts/03-final-review.md`;
  - corresponding BeeSDK-local skills;

- GitHub Issue template;
- GitHub PR template;
- `CHANGELOG.md`;
- SemVer/release baseline:
  - Conventional Commits;
  - release-please config;
  - release-please manifest;
  - release-please workflow;
  - first `v0.1.0` contract baseline after SDK-1 completion.

### Excluded

Не входит в SDK-1:

- migration BeeAgent to BeeSDK;
- migration `beeagent-rop` to BeeSDK;
- BeeScan implementation;
- BeeUI integration;
- capability runtime implementation;
- `ScopedCapabilityGateway` implementation;
- module registry implementation;
- orchestration;
- run/session lifecycle implementation;
- state engine;
- project state implementation;
- config runtime;
- `.env` handling;
- storage implementation;
- filesystem artifact implementation;
- logging framework;
- network clients;
- MCP execution;
- n8n execution;
- HTTP execution;
- subprocess execution;
- provider/LLM integrations;
- CLI application runtime;
- FastAPI/web runtime;
- UI;
- plugin marketplace/discovery framework;
- dependency injection framework;
- ROP-specific contracts;
- BeeScan-specific contracts;
- client-specific business semantics;
- execution/egress implementation.

### Deliverable

Standalone package:

```text
beesdk 0.1.0
```

который:

- устанавливается самостоятельно;
- импортируется самостоятельно;
- публикует minimal typed public contract;
- не требует BeeAgent или другого Bee project at runtime;
- не создаёт execution/storage/network side effects;
- может быть использован как contract dependency следующими real consumers.

Expected public contract-module API:

```python
from beesdk.artifacts import ArtifactPort

from beesdk.capabilities import CapabilityCaller, CapabilityResult, CapabilityStatus

from beesdk.modules import AuthorityLevel, ModuleContext, ModuleContract, ModuleResult
```

### Acceptance criteria

- repository является самостоятельным Git repository;
- package name = `beesdk`;
- import package = `beesdk`;
- `requires-python >= 3.14`;
- current version source of truth находится в `pyproject.toml`;
- runtime `dependencies` пусты;
- `py.typed` входит в built package;
- public contracts are available through explicit public contract modules;
- `src/beesdk/__init__.py` remains empty;
- BeeSDK не импортирует:
  - `beeagent`;
  - `beeagent-rop`;
  - `beeui`;
  - `beescan`;

- extracted module contracts сохраняют compatibility с реальным BeeAgent contract в пределах declared extraction scope;
- existing public field types/signatures не расширяются или сужаются без отдельного compatibility decision;
- public field names не переименовываются только ради cleanup;
- `artifact_api` сохраняется как compatibility field name в `ModuleContext`;
- `ArtifactPort` остаётся minimal protocol;
- `ArtifactPort` не раскрывает filesystem/path implementation;
- `CapabilityCaller.call(...)` принимает только module-controlled capability intent/payload;
- module-facing `CapabilityCaller` не принимает:
  - `authority`;
  - `module_id`;
  - `run_id`;
  - `session_id`;
  - `case_type`;

- `CapabilityResult` является result/evidence contract, а не grant of execution authority;
- import BeeSDK не создаёт:
  - network calls;
  - storage access;
  - subprocess execution;
  - env/secret loading;
  - runtime service initialization;

- tests покрывают positive public contract и critical negative boundaries;
- package собирается через `uv build`;
- package импортируется в собственном BeeSDK environment без consumer projects;
- governance/docs согласованы между собой;
- prompts/skills являются BeeSDK-local и не зависят от `.agents` другого repository;
- Issue/PR templates отражают package/public API/compatibility/security impact;
- release/version policy описана;
- release-please baseline присутствует;
- обычная implementation task не требует manual package version bump.

### Checks

Required:

```bash
uv sync
uv run pytest -q
uv build
uv run python -c "import beesdk; print(beesdk.__file__)"
```

Contract/public API checks:

```text
public contract-module imports
empty package __init__.py
AuthorityLevel values
ModuleContext shape
ModuleResult shape
ModuleContract structural compatibility
ArtifactPort structural compatibility
CapabilityCaller signature
CapabilityResult shape
CapabilityStatus values
```

Negative boundary checks:

```text
CapabilityCaller has no authority argument
CapabilityCaller has no module_id argument
CapabilityCaller has no run_id argument
CapabilityCaller has no session_id argument
CapabilityCaller has no case_type argument
BeeSDK imports no consumer project
runtime dependency list remains empty
import has no runtime side effects
```

Package checks:

```text
wheel builds
sdist builds
py.typed is included
consumer source code is not packaged
generated build metadata is not tracked as source
```

Compatibility review:

```text
compare extracted module contracts against current BeeAgent usage
verify field/signature/default compatibility
verify structural typing compatibility
verify ArtifactPort against real host implementation shape
```

Governance review:

```text
AGENTS.md
docs/ROADMAP.md
docs/SPEC.md
docs/ARCHITECTURE.md
docs/SDLC.md
docs/SECURITY.md
docs/DEV_GUIDE.md
Issue template
PR template
three project prompts
four BeeSDK skills
```

Release baseline:

```text
release-please config uses package-name beesdk
manifest represents the actual released baseline
workflow targets main
pyproject.toml is version source of truth
ordinary feature/fix work does not manually bump version
```

Quality/security:

```text
SAST/security review for authority/capability boundary
SCA only if dependency surface changes
DAST not applicable
IAST not applicable
fuzzing not required for simple dataclass/protocol contracts
```

Repository hygiene:

```bash
git diff --check
```

### DoD

- BeeSDK exists as a standalone package/repository;
- public API v0.1 is explicit;
- package builds successfully;
- tests pass;
- import smoke passes;
- package is typed through `py.typed`;
- runtime dependencies remain empty;
- no consumer imports exist;
- module/artifact/capability contracts are minimal and documented;
- extracted contracts are compatibility-reviewed against current consumer reality;
- host owns runtime identity and authority;
- module-facing capability API cannot self-assign authority;
- no runtime/storage/network/provider implementation is included;
- docs, AGENTS, prompts, skills and GitHub templates are aligned;
- SemVer/release baseline is defined;
- release-please baseline is ready;
- required security checks are complete;
- package is ready to be consumed by real consumers;
- SDK-1 delivery is reviewed through PR;
- `v0.1.0` is the first BeeSDK contract baseline.

---

# Этап 2 — Scoped capability integration

## Purpose of stage

Stage 2 выполняет первое evidence-driven расширение BeeSDK после появления реального consumer integration need.

BeeDrill Iteration 4 и соответствующий BeeAgent host integration выявили конкретный gap:

```text
CapabilityCaller exists
+
ModuleContract.handle(context) exists
+
ModuleContext has no public host-provided CapabilityCaller field
```

Сам `CapabilityCaller` остаётся достаточным и намеренно narrow.

Проблема находится не в его signature, а в отсутствии shared public injection point между host и module.

Основной invariant:

```text
module supplies intent
host supplies authority
```

Stage 2 не создаёт runtime implementation.

## Итерация 2 — Host-provided capability caller injection

**Status:** DONE

### Goal

Закрыть конкретный shared-contract gap, доказанный BeeDrill/BeeAgent integration:

> host должен иметь public typed способ передать существующий `CapabilityCaller` модулю через `ModuleContext`, не раскрывая и не передавая модулю контроль над runtime identity, authority, policy или credentials.

Целевой flow:

```text
BeeAgent host
→ creates ModuleContext
→ injects host-bound CapabilityCaller
→ module receives context
→ module calls capability_name + payload
→ host executes/refuses according to host policy
```

### Scope

**Included**

Добавить один backward-compatible optional host-provided field в `ModuleContext`:

```python
capability_caller: CapabilityCaller | None = None
```

Сохранить существующие public contracts:

```text
CapabilityCaller.call(capability_name, payload)
ModuleContract.handle(context)
CapabilityResult
CapabilityStatus
```

Required ownership invariant:

```text
Module controls:

capability_name
payload
```

```text
Host controls:

module identity
run identity
session identity
case type
authority
policy
credentials
execution
```

Изменение должно оставаться additive:

- existing `ModuleContext(...)` construction без capability caller продолжает работать;
- `capability_caller` defaults to `None`;
- `ModuleContract.handle(context)` не меняется;
- существующие public imports сохраняются;
- existing artifact contract не меняется;
- `CapabilityCaller.call(...)` не получает host-owned arguments.

### Excluded

Не входит в SDK-2:

- capability runtime implementation;
- `ScopedCapabilityGateway` implementation;
- BeeAgent runtime implementation;
- Surfpool implementation;
- Solana implementation;
- subprocess execution;
- network/RPC implementation;
- execution engine;
- policy engine;
- authority engine;
- credential loading;
- secret/config runtime;
- retries;
- module registry;
- orchestration;
- generic dependency injection;
- generic provider abstraction;
- HTTP/MCP/n8n execution;
- changing:

```text
handle(context)
```

to:

```text
handle(context, caller)
```

- adding module-controlled:
  - `authority`;
  - `module_id`;
  - `run_id`;
  - `session_id`;
  - `case_type`;
  - credentials;
  - policy.

### Deliverable

BeeSDK exposes one additive module-context contract:

```python
ModuleContext(
    ...,
    capability_caller=host_provided_caller,
)
```

through which a host can provide an implementation of the already-existing public `CapabilityCaller` protocol.

Expected consumer relationship:

```text
BeeDrill
→ imports BeeSDK contracts only

BeeAgent
→ implements/provides CapabilityCaller
→ injects it through ModuleContext

BeeSDK
→ knows neither BeeAgent nor BeeDrill implementation
```

Existing consumers that do not use capabilities continue constructing and consuming `ModuleContext` unchanged.

### Acceptance criteria

- `ModuleContext` exposes optional host-provided `CapabilityCaller`;
- field defaults to `None`;
- existing `ModuleContext` constructor usages remain valid;
- `ModuleContract.handle(context)` remains unchanged;
- `CapabilityCaller.call()` still accepts only:

```text
capability_name
payload
```

- caller API does not accept:
  - authority;
  - module identity;
  - run identity;
  - session identity;
  - case type;
  - credentials;
  - policy;

- modules cannot self-assign host authority through the shared API;
- `CapabilityResult` remains result/evidence, not authority grant;
- BeeAgent can provide a structurally compatible caller;
- BeeDrill can consume the caller without importing BeeAgent private internals;
- no consumer-specific type enters BeeSDK;
- BeeSDK adds no runtime implementation;
- BeeSDK adds no I/O;
- BeeSDK adds no network execution;
- BeeSDK adds no subprocess behavior;
- runtime dependency list remains empty;
- existing public contract-module imports remain stable;
- package remains independently installable.

### Checks

Required:

```bash
uv run pytest -q
uv build
```

Contract tests:

```text
legacy ModuleContext construction without capability caller
ModuleContext construction with capability caller
capability_caller default is None
structurally compatible CapabilityCaller is accepted
ModuleContract.handle(context) signature unchanged
CapabilityCaller.call signature unchanged
CapabilityResult shape unchanged
CapabilityStatus values unchanged
public imports remain stable
runtime dependencies remain empty
```

Negative authority tests:

```text
CapabilityCaller has no authority argument
CapabilityCaller has no module_id argument
CapabilityCaller has no run_id argument
CapabilityCaller has no session_id argument
CapabilityCaller has no case_type argument
CapabilityCaller has no credentials argument
CapabilityCaller has no policy argument
CapabilityResult does not mutate ModuleContext authority
```

Consumer compatibility checks:

```text
BeeAgent can inject a host-owned caller
BeeDrill can consume caller through BeeSDK contract
BeeDrill requires no BeeAgent private import
legacy consumers without caller remain compatible
```

Package checks:

```text
package import smoke
wheel build
sdist build
py.typed remains included
zero runtime dependency check
consumer import guard
```

Quality/security:

```text
SAST
explicit authority-boundary review
negative authority tests
consumer compatibility verification
SCA only if dependency surface unexpectedly changes
DAST not applicable
IAST not applicable
fuzzing not required for this bounded dataclass/protocol change
```

Repository hygiene:

```bash
git diff --check
```

### DoD

- additive `ModuleContext.capability_caller` contract exists;
- field defaults to `None`;
- existing module consumers remain source-compatible;
- `CapabilityCaller.call(...)` remains narrow;
- module cannot provide host authority or runtime identity through shared capability API;
- BeeAgent can provide a host-bound implementation;
- BeeDrill can consume that implementation through BeeSDK only;
- BeeSDK contains no BeeAgent/BeeDrill implementation;
- no runtime implementation moved into BeeSDK;
- no runtime dependencies were added;
- tests pass;
- package builds;
- import smoke passes;
- security/authority negative tests pass;
- affected consumer compatibility is verified;
- docs describing module/capability boundary are updated where required;
- `pyproject.toml.version` is not manually changed;
- SDK-2 delivery is reviewed through PR.

---

# Этап 3 — Broader consumer adoption validation

## Purpose of stage

Stage 3 проверяет более широкое применение BeeSDK в существующем ecosystem после того, как первый real capability integration уже доказал работоспособность shared host/module boundary.

Ключевой принцип:

> Consumer adoption implementation живёт в consumer repositories.

Например:

```text
BeeAgent migration
→ BeeAgent Issue / branch / PR

beeagent-rop migration
→ beeagent-rop Issue / branch / PR
```

BeeSDK repository меняется только если integration evidence показывает, что существующий shared contract:

- несовместим;
- недостаточен;
- небезопасен;
- заставляет consumer зависеть от private host internals;
- требует duplicate contract workaround.

Consumer adoption не является разрешением расширять SDK заранее.

SDK-3 не является prerequisite для BeeDrill Iteration 4 или BeeAgent Iteration 43.

Эти integration paths относятся к конкретному capability work, уже покрытому SDK-2.

---

## Итерация 3 — Broader consumer contract adoption validation

**Status:** FUTURE / orientation

### Goal

Проверить BeeSDK contracts через более широкое реальное потребление BeeAgent, `beeagent-rop` и других подходящих consumers, убрать безопасно устранимое дублирование shared contracts и зафиксировать только реально выявленные compatibility gaps.

Possible sequence:

```text
current BeeSDK contract
      ↓
selected BeeAgent shared-contract adoption
      ↓
selected beeagent-rop shared-contract adoption
      ↓
integration evidence
      ↓
BeeSDK change only if separately proven necessary
```

### Scope

Future consumer-side work may include:

```text
BeeAgent
→ broader migration from duplicated shared contracts to BeeSDK

beeagent-rop
→ adopt BeeSDK shared contracts where appropriate

duplicated shared definitions
→ remove where compatibility permits
```

Potential candidate areas may include:

- shared module contracts;
- artifact port compatibility;
- authority enums/semantics;
- capability result/caller usage;
- removal of duplicate public/shared definitions.

Каждая migration должна выполняться только там, где dependency direction и compatibility действительно улучшаются.

### Excluded

SDK-3 заранее не разрешает:

- redesign public API;
- speculative BeeSDK expansion;
- add runtime dependencies без отдельного доказанного need;
- add module registry;
- add capability gateway implementation;
- add storage implementation;
- add state framework;
- add config runtime;
- add execution/egress;
- add provider integration;
- add plugin framework;
- переносить domain semantics из consumer в BeeSDK;
- forcing migration только ради удаления похожего кода;
- менять уже стабильные contracts без concrete compatibility reason.

### Deliverable

Real consumer evidence that BeeSDK contracts can be adopted across host and domain-module boundaries without:

```text
reverse dependencies
private-internal coupling
authority leakage
runtime ownership drift
unnecessary duplicate contracts
```

Результатом iteration может быть:

- consumer migration без BeeSDK code changes;
- уменьшение duplicated shared definitions;
- documented compatibility evidence;
- отдельный новый BeeSDK roadmap item, если integration выявит новый доказанный shared-contract gap.

### Acceptance criteria

When SDK-3 is scheduled:

- selected BeeAgent contracts consume BeeSDK where appropriate;
- BeeAgent module runtime remains behavior-compatible;
- BeeAgent keeps authority/policy/runtime identity host-owned;
- `beeagent-rop` consumes BeeSDK only where shared semantics действительно совпадают;
- `beeagent-rop` does not need BeeAgent private internals for shared contracts;
- duplicated definitions are reduced only where safe;
- normal module dispatch remains compatible;
- artifact integration remains compatible;
- capability boundary remains host-owned;
- no domain semantics move into BeeSDK;
- no circular dependency appears;
- BeeSDK remains independently installable;
- BeeSDK does not need consumers installed;
- no consumer implementation is imported into BeeSDK;
- BeeSDK does not gain runtime implementation merely to simplify migration.

### Checks

Consumer-specific tests run inside each affected consumer repository.

BeeSDK changes, if any are separately approved, require:

```bash
uv run pytest -q
uv build
```

Plus affected consumer compatibility tests.

Required review questions:

```text
Did adoption reveal a real SDK gap?
Can the gap be solved consumer-side?
Would a proposed SDK change represent stable shared semantics?
Would another consumer reasonably use the same contract?
Does the change preserve host-owned authority?
Does it introduce runtime implementation into BeeSDK?
Can duplicate ownership be removed without increasing coupling?
```

Quality/security:

```text
consumer compatibility tests
dependency-direction review
authority-boundary review where applicable
SAST for security-sensitive shared-contract changes
SCA only if dependency surface changes
```

### DoD

SDK-3 считается завершённой, когда approved broader consumer-adoption scope выполнен и доказано, что:

- selected consumers use BeeSDK shared contracts where appropriate;
- duplicated shared contract ownership is reduced where safe;
- runtime behavior remains compatible;
- no circular dependencies appear;
- no consumer implementation moves into BeeSDK;
- authority ownership remains host-side;
- resulting compatibility boundaries are documented;
- any additional BeeSDK change is evidence-driven and отдельно approved;
- new BeeSDK release is made only if package contract actually changed.

---

# Этап 4 — Additional shared contracts

## Purpose of stage

Stage 4 существует только как orientation для будущих reusable contracts.

Он не означает, что BeeSDK обязан получить state/config/project/execution APIs.

---

## Итерация 4 — Project/state contracts when proven necessary

**Status:** FUTURE / orientation

### Goal

Рассмотреть project/state или другие shared contracts только если реальные consumers покажут общую stable semantic boundary, которую невозможно корректно поддерживать локально.

### Candidate areas

Только после evidence могут рассматриваться contracts вроде:

```text
Project identity
State reference
Checkpoint reference
Job identity
```

Но ни один из них не считается заранее approved.

### Excluded

До отдельного evidence BeeSDK не должен определять:

```text
Project runtime
Session engine
StateStore implementation
CheckpointStore implementation
Job runner
ExecutionPlan runtime
Egress engine
Config loader
Database
filesystem state backend
```

Также не должны появляться автоматически:

```text
generic execution framework
provider framework
network runtime
plugin marketplace
workflow engine
secret manager
```

### Required evidence

Новый contract должен доказать:

- минимум одного непосредственного real consumer;
- предпочтительно несколько consumers или очевидную stable shared boundary;
- отсутствие лучшего consumer-local решения;
- стабильность semantics;
- отсутствие переноса runtime implementation в SDK;
- compatibility/security value.

### Deliverable

Может быть:

- небольшой shared contract;
- решение оставить contract consumer-local;
- решение вообще не расширять BeeSDK.

Все три результата допустимы.

### DoD

SDK-4 не обязана быть реализована.

Если реального shared contract need нет, правильный результат:

```text
no SDK change
```

---

# Future contract rule

После SDK-1 новые roadmap iterations не создаются автоматически по номеру.

Правильный flow:

```text
real consumer gap
→ architecture evidence
→ necessity verdict
→ BeeSDK roadmap item
→ Issue
→ implementation
→ compatibility/security verification
→ PR
→ release if needed
```

Пример текущей последовательности:

```text
SDK-1
→ minimal contracts established

BeeDrill/BeeAgent integration need appears
→ concrete ModuleContext capability injection gap proven

SDK-2
→ minimal additive contract change

later broader ecosystem adoption
→ SDK-3 when actually scheduled

new reusable contract need
→ SDK-4 only if separately proven
```

Неправильный flow:

```text
SDK-1
→ SDK-2
→ SDK-3
→ SDK-4
→ SDK-5
→ SDK-6
```

только потому, что номера можно продолжать.

BeeSDK считается успешным не по количеству iterations, а по тому, насколько маленьким и стабильным остаётся shared contract surface.

---

# Related project boundaries

## BeeAgent

BeeAgent остаётся primary host/runtime и владеет:

```text
orchestration
module registry
runtime context creation
artifact implementation
state
policy
capability execution
approvals
connectors
execution/egress
process lifecycle
timeouts
cleanup
credentials
```

BeeSDK не должен поглощать эту ответственность.

BeeAgent может реализовывать BeeSDK protocols и передавать host-owned implementations через shared contracts.

---

## BeeDrill

BeeDrill является domain module consumer BeeSDK contracts.

BeeDrill может владеть:

```text
drill domain contracts
scenario semantics
expected controls
evidence interpretation
metrics
deterministic verdicts
```

BeeDrill не должен получать через BeeSDK:

```text
arbitrary execution authority
host identity control
runtime policy control
credentials
process lifecycle ownership
RPC endpoint ownership
```

BeeDrill Iteration 4 является concrete integration evidence для SDK-2.

---

## `beeagent-rop`

`beeagent-rop` остаётся domain consumer и владеет:

```text
ROP domain contracts
classification
duplicate semantics
taxonomy
fixtures
summaries
recommendations
```

BeeSDK не должен содержать ROP-specific taxonomy или business rules.

Broader `beeagent-rop` contract adoption относится к SDK-3, когда эта migration будет отдельно scheduled.

---

## BeeScan

BeeScan может стать future consumer shared contracts.

Это не означает, что BeeScan-specific:

```text
scan models
findings taxonomy
security rules
tool execution
```

автоматически принадлежат BeeSDK.

Shared contract должен сначала доказать reusable semantics.

---

## BeeUI

BeeUI остаётся отдельным generic presentation package.

Текущий BeeSDK roadmap не требует:

```text
beeui -> beesdk
```

Такая dependency допускается только при отдельном доказанном shared contract need.

---

## Bee Dev MCP

Bee Dev MCP остаётся отдельным development/orchestration tool.

Его отсутствие package-version lifecycle не является моделью для BeeSDK:

```text
Bee Dev MCP
→ development service/tool

BeeSDK
→ reusable package dependency + public compatibility contract
```

Поэтому BeeSDK имеет собственный SemVer/release lifecycle.

---

# Related process documents

Для выполнения roadmap iterations вместе с этим ROADMAP используются:

- `docs/SPEC.md` — public product/contract specification;
- `docs/ARCHITECTURE.md` — dependency direction и ownership boundaries;
- `docs/DEV_GUIDE.md` — development, testing, package build и consumer integration;
- `docs/SDLC.md` — lightweight process, change levels, direct-main/PR и release rules;
- `docs/SECURITY.md` — authority, capability, artifact, dependency и trust-boundary rules;
- `AGENTS.md` — repository-level development/AI instructions.

---

# Summary

BeeSDK развивается по принципу:

```text
extract only what is already needed
→ validate through real consumers
→ fix only proven contract gaps
→ add the next abstraction only when evidence requires it
```

Текущая последовательность:

```text
SDK-1 — Repository and core contract foundation
DONE

        ↓

SDK-2 — Host-provided capability caller injection
PLANNED

        ↓

SDK-3 — Broader consumer contract adoption validation
FUTURE / orientation

        ↓

SDK-4 — Project/state contracts when proven necessary
FUTURE / orientation
```

Целевое состояние — не большой framework.

Целевое состояние:

```text
small
typed
stable
independent
secure
boring
useful
```
