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
| **Dependency rule**             | Для v0.1 runtime dependency target — Python standard library only.                                                                                           |
| **Typing principle**            | `py.typed` является частью package contract; type signatures рассматриваются как consumer-facing API.                                                        |
| **Versioning principle**        | BeeSDK имеет собственный SemVer lifecycle, независимый от версий BeeAgent, ROP, BeeUI и других consumers.                                                    |
| **Release principle**           | Обычные feature/fix PR не bump-ят version вручную; version/changelog/tag lifecycle ведётся release automation.                                               |
| **Security rule**               | SDK не должен создавать execution, network egress, filesystem access, secret loading или другие runtime side effects только из-за import/use contracts.      |
| **KISS rule**                   | BeeSDK должен оставаться маленьким. Новый framework layer, dependency или abstraction появляется только после реальной необходимости.                        |

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

## Status values

Допустимые статусы iterations:

- **PLANNED** — scope утверждён, implementation ещё не началась;
- **IN PROGRESS** — iteration в работе;
- **DONE** — iteration полностью завершена;
- **DONE (partial)** — завершена с осознанными documented limitations.

Для дальних направлений используется:

- **FUTURE / orientation** — направление известно, но ещё не является утверждённым implementation scope.

`FUTURE / orientation` не означает автоматического одобрения будущей архитектуры.

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

## Change levels for verification

Для lightweight SDLC используются три уровня изменений.

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

После bootstrap release release lifecycle должен управляться `release-please`:

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

| Phase                                      | Status      | What it means                                                                                                                                               |
| ------------------------------------------ | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Phase A — Contract foundation**          | IN PROGRESS | Создаётся standalone typed package, governance, package/release baseline и первые shared module/artifact/capability contracts.                              |
| **Phase B — Consumer adoption validation** | FUTURE      | Existing contracts проверяются реальной миграцией BeeAgent и domain module consumers; SDK меняется только если integration выявляет настоящий contract gap. |
| **Phase C — Scoped capability evolution**  | FUTURE      | Capability contracts уточняются после реального host/module integration evidence; runtime gateway implementation остаётся вне BeeSDK.                       |
| **Phase D — Additional shared contracts**  | FUTURE      | Project/state или другие contracts рассматриваются только после появления реальных consumers и доказанной reusable semantics.                               |

### Stages

- **Stage 1 — Contract foundation:** standalone package, governance, module/artifact/capability contracts, tests, package/release baseline.
- **Stage 2 — Consumer adoption validation:** проверка SDK через реальное потребление BeeAgent и `beeagent-rop`.
- **Stage 3 — Scoped capability evolution:** contract refinement после использования в настоящем host runtime.
- **Stage 4 — Additional shared contracts:** только consumer-proven contracts; никакого заранее утверждённого framework expansion.

---

## Этап 1 — Contract foundation

### Purpose of stage

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

### Итерация 1 — Repository and core contract foundation v0.1.0

**Status:** DONE

#### Goal

Создать standalone BeeSDK v0.1.0 как минимальный typed shared-contract package для Bee ecosystem, достаточный для последующей migration/validation через BeeAgent и `beeagent-rop`, но не содержащий host runtime implementation.

#### Scope

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

#### Excluded

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

#### Deliverable

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
- может быть использован как contract dependency на следующем consumer-adoption этапе.

Expected public contract-module API:

```python
from beesdk.artifacts import ArtifactPort
from beesdk.capabilities import CapabilityCaller, CapabilityResult, CapabilityStatus
from beesdk.modules import AuthorityLevel, ModuleContext, ModuleContract, ModuleResult
```

#### Acceptance criteria

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

#### Checks

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

#### DoD

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
- package is ready to be consumed by the first real consumers;
- SDK-1 delivery is reviewed through PR;
- `v0.1.0` can become the first BeeSDK contract baseline.

---

## Этап 2 — Consumer adoption validation

### Purpose of stage

Stage 2 проверяет, что BeeSDK contract действительно работает в настоящем ecosystem, а не только выглядит правильно внутри isolated repository.

Ключевой принцип:

> Consumer adoption implementation живёт в consumer repositories.

То есть:

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

### Итерация 2 — BeeAgent and ROP contract adoption validation

**Status:** FUTURE / orientation

#### Goal

Проверить BeeSDK v0.1 contracts через реальное потребление BeeAgent и `beeagent-rop`, убрать безопасно устранимое дублирование shared contracts и зафиксировать только реально выявленные compatibility gaps.

Expected sequence:

```text
beesdk v0.1.0
      ↓
BeeAgent adoption
      ↓
beeagent-rop adoption
      ↓
integration evidence
      ↓
BeeSDK change only if proven necessary
```

#### Expected scope

Consumer-side work:

```text
BeeAgent
→ imports shared contracts from beesdk

beeagent-rop
→ imports shared contracts from beesdk where appropriate

duplicated shared definitions
→ removed where compatibility permits
```

BeeSDK-side work допускается только при подтверждённом integration gap.

#### Excluded

SDK-2 заранее не разрешает:

- redesign public API;
- add runtime dependencies;
- add module registry;
- add capability gateway implementation;
- add storage implementation;
- add state framework;
- add config runtime;
- add execution/egress;
- add provider integration;
- add plugin framework.

#### Deliverable

Real consumer evidence that BeeSDK contracts are usable across host and domain-module boundaries without reverse dependencies or private-internal coupling.

#### Acceptance criteria

- BeeAgent can depend on BeeSDK without circular dependency;
- BeeAgent module runtime remains behavior-compatible;
- BeeAgent can provide an implementation compatible with `ArtifactPort`;
- BeeAgent can keep authority/policy/runtime identity host-owned;

- `beeagent-rop` can depend on BeeSDK without importing BeeAgent private internals;
- duplicated module contract definitions can be removed or reduced where safe;

- normal module dispatch remains compatible;
- artifact integration remains compatible;
- capability boundary remains host-owned;
- no domain semantics move into BeeSDK;

- BeeSDK remains independently installable;
- BeeSDK does not need BeeAgent installed;
- BeeSDK does not gain runtime implementation merely to satisfy migration.

#### Checks

Consumer-specific tests run inside each consumer repository.

BeeSDK changes, if any, require:

```bash
uv run pytest -q
uv build
```

Plus affected consumer compatibility tests.

Required review questions:

```text
Did adoption reveal a real SDK gap?
Can the gap be solved consumer-side?
Would the proposed SDK change be reusable by another consumer?
Does the change preserve host-owned authority?
Does it introduce runtime implementation into BeeSDK?
```

#### DoD

- BeeAgent consumes BeeSDK shared contracts where appropriate;
- `beeagent-rop` consumes BeeSDK shared contracts where appropriate;
- duplicate contract ownership is reduced;
- runtime behavior remains compatible;
- no circular dependency appears;
- no consumer implementation is imported into BeeSDK;
- any BeeSDK changes are evidence-driven;
- resulting compatibility boundaries are documented;
- new BeeSDK release is made only if package contract actually changed.

---

## Stage 3 — Scoped capability evolution

### Purpose of stage

Stage 3 возможен только после реального опыта использования `CapabilityCaller` в host/module integration.

До этого текущий v0.1 capability contract считается намеренно минимальным.

---

### Iteration SDK-3 — Scoped capability contract evolution

**Status:** FUTURE / orientation

#### Goal

Уточнить shared capability contract только в том случае, если BeeAgent/ROP adoption докажет, что v0.1 module-facing boundary недостаточна для реального controlled execution flow.

#### Required invariant

Module controls:

```text
capability_name
payload
```

Host controls:

```text
module identity
run identity
session identity
case type
authority
policy
credentials
execution
```

#### Potential scope

Только после evidence могут рассматриваться shared contracts для:

- scoped capability caller binding;
- host-generated invocation context;
- common refusal/result semantics;
- compatibility rules between module intent and host execution boundary.

#### Excluded

Заранее не одобрены:

- `ScopedCapabilityGateway` implementation inside BeeSDK;
- capability runtime;
- network/provider implementation;
- MCP implementation;
- n8n implementation;
- HTTP execution;
- retries;
- credential loading;
- secret/config runtime;
- execution engine;
- policy engine;
- plugin framework.

#### Deliverable

Если integration доказывает необходимость — минимально расширенный contract, который описывает shared boundary, но оставляет implementation host-owned.

Если такой gap не найден, SDK-3 не требуется.

#### Acceptance criteria

Если SDK-3 открывается:

- есть concrete integration evidence;
- существующий `CapabilityCaller` действительно недостаточен;
- новый contract нужен более чем одному implementation path или является стабильной host/module boundary;
- caller не получает возможность self-assign authority;
- credentials остаются host-owned;
- runtime implementation не переносится в SDK;
- public compatibility/migration impact определён;
- negative authority tests существуют.

#### Checks

Expected:

```bash
uv run pytest -q
uv build
```

Required security checks:

```text
SAST
negative authority tests
consumer compatibility tests
SCA only if dependencies change
```

#### DoD

SDK-3 считается выполненной только если реальный integration gap устранён меньшим возможным shared-contract изменением.

---

## Stage 4 — Additional shared contracts

### Purpose of stage

Stage 4 существует только как orientation для будущих reusable contracts.

Он не означает, что BeeSDK обязан получить state/config/project/execution APIs.

---

### Iteration SDK-4 — Project/state contracts when proven necessary

**Status:** FUTURE / orientation

#### Goal

Рассмотреть project/state contracts только если реальные consumers покажут общую stable semantic boundary, которую невозможно корректно поддерживать локально.

#### Candidate areas

Только после evidence могут рассматриваться contracts вроде:

```text
Project identity
State reference
Checkpoint reference
Job identity
```

Но ни один из них не считается заранее approved.

#### Excluded

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

#### Required evidence

Новый contract должен доказать:

- минимум одного непосредственного real consumer;
- предпочтительно несколько consumers или очевидную stable shared boundary;
- отсутствие лучшего consumer-local решения;
- стабильность semantics;
- отсутствие переноса runtime implementation в SDK;
- compatibility/security value.

#### Deliverable

Может быть:

- небольшой shared contract;
- решение оставить contract consumer-local;
- решение вообще не расширять BeeSDK.

Все три результата допустимы.

#### DoD

SDK-4 не обязана быть реализована.

Если реального shared contract need нет, правильный результат:

```text
no SDK change
```

---

## Future contract rule

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

## Related project boundaries

### BeeAgent

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
```

BeeSDK не должен поглощать эту ответственность.

### `beeagent-rop`

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

### BeeScan

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

### BeeUI

BeeUI остаётся отдельным generic presentation package.

Текущий BeeSDK roadmap не требует:

```text
beeui -> beesdk
```

Такая dependency допускается только при отдельном доказанном shared contract need.

### Bee Dev MCP

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

## Related process documents

Для выполнения roadmap iterations вместе с этим ROADMAP используются:

- `docs/SPEC.md` — public product/contract specification;
- `docs/ARCHITECTURE.md` — dependency direction и ownership boundaries;
- `docs/DEV_GUIDE.md` — development, testing, package build и consumer integration;
- `docs/SDLC.md` — lightweight process, change levels, direct-main/PR и release rules;
- `docs/SECURITY.md` — authority, capability, artifact, dependency и trust-boundary rules;
- `AGENTS.md` — repository-level development/AI instructions.

## Summary

BeeSDK развивается по принципу:

```text
extract only what is already needed
→ validate through real consumers
→ fix only proven contract gaps
→ add the next abstraction only when evidence requires it
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
