# DEV_GUIDE — BeeSDK development and consumer integration

## Purpose

Этот документ описывает:

- как разрабатывать `beesdk`;
- как работать с Python environment через `uv`;
- как запускать tests/build;
- как добавлять public contracts;
- как сохранять compatibility;
- как подключать SDK к Bee consumers;
- как работать с version/release lifecycle;
- как не превратить SDK в runtime framework.

## Related project docs

Используй этот документ вместе с:

- `docs/ROADMAP.md` — направление и текущие SDK iterations;
- `docs/SPEC.md` — public contract и product boundary;
- `docs/ARCHITECTURE.md` — ownership и dependency direction;
- `docs/SDLC.md` — lightweight delivery process;
- `docs/SECURITY.md` — trust/authority/dependency rules.

Правило:

> `DEV_GUIDE` объясняет, как работать с проектом. Он не заменяет `SPEC`, `ROADMAP`, `SDLC` или `SECURITY`.

## Requirements

- Python 3.14+
- `uv`
- Git

## Repository

Основной repository:

```text
/home/bee/Pro/beesdk
```

Python distribution:

```text
beesdk
```

Python import:

```python
import beesdk
```

## Development setup

Из repository root:

```bash
uv sync
```

Активация `.venv` вручную не требуется.

Запускай Python/tool commands через:

```bash
uv run ...
```

## Basic commands

| Что сделать                 | Команда                                                    |
| --------------------------- | ---------------------------------------------------------- |
| установить dev environment  | `uv sync`                                                  |
| запустить tests             | `uv run pytest -q`                                         |
| собрать package             | `uv build`                                                 |
| import smoke                | `uv run python -c "import beesdk; print(beesdk.__file__)"` |
| показать dependencies       | `uv tree`                                                  |
| добавить dev dependency     | `uv add --dev <pkg>`                                       |
| добавить runtime dependency | только через approved Issue                                |
| удалить dependency          | `uv remove <pkg>`                                          |

## Dependency source of truth

Source of truth:

```text
pyproject.toml
uv.lock
```

Правила:

- runtime dependencies для v0.1 остаются пустыми;
- dev dependencies разрешены только когда нужны для development/testing;
- dependency addition должна быть минимальной и обоснованной;
- при dependency change обновляются `pyproject.toml` и `uv.lock`;
- не использовать `uv lock --check`;
- не менять dependency surface случайно при unrelated task.

## Package structure

Текущий public package:

```text
src/beesdk/
├── __init__.py
├── modules.py
├── artifacts.py
├── capabilities.py
└── py.typed
```

Не создавай новые package directories только для красоты.

Добавляй новый слой, если:

- текущий файл стал реально перегруженным;
- появился отдельный coherent public contract family;
- есть доказанный consumer need.

## Stable public contract-module API

Public imports должны идти через explicit public contract modules:

```python
from beesdk.artifacts import ArtifactPort
from beesdk.capabilities import CapabilityCaller, CapabilityResult, CapabilityStatus
from beesdk.modules import AuthorityLevel, ModuleContext, ModuleContract, ModuleResult
```

Если появляется новый public contract:

1. реализуй его в подходящем module;
2. добавь его в explicit public contract module;
3. добавь contract-module import tests;
4. обнови `docs/SPEC.md`;
5. проверь compatibility;
6. обнови `README.ru.md`, если consumer-facing usage изменился.

`src/beesdk/__init__.py` остаётся пустым. Не заставляй consumers зависеть от private internal paths.

## Current public API

Текущий v0.1 surface:

```python
from beesdk.artifacts import ArtifactPort
from beesdk.capabilities import CapabilityCaller, CapabilityResult, CapabilityStatus
from beesdk.modules import AuthorityLevel, ModuleContext, ModuleContract, ModuleResult
```

## Adding a contract

Перед добавлением нового contract ответь:

```text
Кто его consumer?
Какой реальный duplication/gap он закрывает?
Почему contract должен жить в BeeSDK?
Почему он не принадлежит BeeAgent runtime?
Почему он не принадлежит domain module?
Можно ли закрыть задачу существующим contract?
```

Если на эти вопросы нет убедительных ответов, contract пока не нужен.

## Module contract discipline

BeeSDK определяет module interface, но не module implementation.

Не добавляй в SDK:

- module registry;
- module discovery;
- dynamic loading;
- plugin installation;
- module lifecycle manager;
- domain rules.

`ModuleContract` должен оставаться маленьким structural protocol.

## Artifact contract discipline

`ArtifactPort` является host-owned port.

SDK не должен:

- создавать directories;
- принимать arbitrary filesystem paths;
- владеть storage layout;
- определять retention;
- читать BeeAgent storage;
- вводить собственный artifact database.

Если consumer требует новую artifact operation, сначала проверь реальный use case.

Не копируй весь BeeAgent `ArtifactAPI` в SDK автоматически.

## Capability contract discipline

Module-facing capability boundary должна оставаться narrow.

Разрешённая module input shape:

```text
capability_name
payload
```

Не добавляй module-controlled:

```text
authority
module_id
run_id
session_id
case_type
execution policy
connector credentials
```

Эти значения принадлежат host/runtime.

## Consumer integration

### Local development

Consumer repository может подключить sibling BeeSDK через `uv`.

Например:

```toml
[tool.uv.sources]
beesdk = { path = "../beesdk", editable = true }
```

Exact consumer dependency declaration определяется в consumer repository.

### Important rule

Каждый repository проверяется в собственном environment.

Для BeeSDK:

```bash
cd /home/bee/Pro/beesdk
uv sync
uv run pytest -q
uv build
```

Не используй BeeAgent `.venv` как доказательство, что BeeSDK самостоятельно работает.

Это может скрыть accidental dependencies.

## Consumer compatibility

При изменении public contract нужно определить affected consumers.

Минимально проверить:

- старый import surface;
- constructor/signature compatibility;
- enum values;
- protocol shape;
- defaults;
- field names;
- dependency direction.

Если изменение касается BeeAgent/ROP integration, consumer smoke выполняется отдельно в соответствующем repository.

BeeSDK tests не должны требовать установленный BeeAgent.

## Tests

Основной command:

```bash
uv run pytest -q
```

### Что должно тестироваться в BeeSDK

- public contract-module imports;
- public enums;
- dataclass contract;
- structural protocols;
- defaults;
- signature shape;
- negative authority boundaries;
- zero runtime dependencies;
- absence of consumer imports;
- backward compatibility when public API changes.

### Что не тестируется как responsibility BeeSDK

- BeeAgent orchestration;
- BeeAgent storage;
- BeeAgent capability runtime;
- ROP classification;
- BeeScan scanning logic;
- BeeUI rendering;
- external connectors.

Эти checks принадлежат соответствующим consumers.

## Package build

Если package/public metadata затрагивается, выполнить:

```bash
uv build
```

После build проверь как минимум:

- wheel создаётся;
- source distribution создаётся;
- `beesdk` importable;
- `py.typed` включён;
- consumer projects не попали в package;
- runtime dependencies не появились случайно.

Generated directories вроде:

```text
dist/
build/
*.egg-info/
```

не являются source files и должны оставаться ignored.

## Typing contract

BeeSDK публикует:

```text
py.typed
```

Поэтому type annotations являются частью developer-facing public contract.

Не меняй signatures только как cosmetic refactor.

При изменении protocol/dataclass types оцени:

- runtime compatibility;
- structural typing compatibility;
- consumer impact.

## Docs

При public contract change обычно проверить:

```text
README.ru.md
docs/SPEC.md
docs/ARCHITECTURE.md
docs/DEV_GUIDE.md
docs/ROADMAP.md
docs/SECURITY.md
```

Не надо менять каждый документ при каждой задаче.

Меняй только тот, source-of-truth которого реально затронут.

## Versioning

Source of truth текущей package version:

```text
pyproject.toml
```

BeeSDK использует SemVer.

Обычный implementation PR **не должен вручную менять version**.

Используются Conventional Commits:

```text
feat:      public/additive capability → release candidate MINOR
fix:       compatible bugfix         → PATCH
docs:      docs only                  → no release bump
test:      tests only                 → no release bump
refactor:  no behavior change         → no release bump
chore:     maintenance                → no release bump
ci:        CI                         → no release bump
build:     build tooling              → normally no release bump
```

Breaking changes:

```text
feat!: ...
fix!: ...
```

или:

```text
BREAKING CHANGE: ...
```

Release-please управляет release PR, changelog/version update и tag.

Не bump version вручную для обычного feature/fix task.

## Lightweight contribution flow

Для существенного изменения:

```text
ROADMAP / task
→ Issue
→ branch
→ implementation
→ tests
→ PR
→ merge
→ release-please when applicable
```

Для очевидного low-risk maintenance:

```text
docs / test / small chore
→ local check
→ main
```

Issue/PR не обязательны для tiny low-risk изменения, если:

- нет public API change;
- нет compatibility impact;
- нет dependency change;
- нет security/authority impact;
- изменение легко проверить.

Если есть сомнение — используй normal Issue/PR path.

## What not to do

Не надо:

- создавать runtime config;
- добавлять `.env`;
- создавать `start.sh`;
- создавать web service;
- добавлять storage;
- добавлять plugin framework;
- делать provider integration;
- переносить BeeAgent runtime в SDK;
- добавлять product-specific contracts;
- копировать весь consumer implementation;
- добавлять dependencies “на будущее”;
- повышать version вручную в обычном PR.

## Before significant PR

Проверь:

```bash
uv sync
uv run pytest -q
uv build
```

Плюс task-specific checks из:

```text
docs/SDLC.md
docs/SECURITY.md
```

Перед PR reviewer должен понимать:

- какой public contract изменился;
- зачем он нужен;
- backward compatible ли изменение;
- affected consumers;
- dependency impact;
- authority/security impact;
- какие проверки выполнены;
- почему решение остаётся KISS.

## Summary

Работа с BeeSDK должна быть проще, чем работа с BeeAgent runtime.

Основные правила:

```text
small contract
stable public import
zero accidental dependencies
consumer-proven need
explicit compatibility
host-owned authority
```
