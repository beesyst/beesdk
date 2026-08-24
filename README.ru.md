# BeeSDK

BeeSDK — самостоятельный минимальный Python SDK с публичными contracts для Bee ecosystem. Он предназначен для того, чтобы host-проекты и доменные модули использовали одни и те же малые интерфейсы без зависимости друг от друга через внутренности BeeAgent.

## Что входит в v0.1

- contracts для Bee modules: context, result, authority и structural protocol;
- минимальный host-owned `ArtifactPort`;
- module-facing `CapabilityCaller`, его bounded result и status;
- typed package marker `py.typed`.

## Что не входит

BeeSDK не является runtime application и не содержит конфигурации, сервисного entrypoint, CLI, хранилища, capability runtime/gateway, subprocess execution, HTTP-клиентов, LLM/provider integrations, UI, plugin registry или contracts, специфичных для ROP и BeeScan.

## Направление зависимостей

`beesdk` зависит только от Python standard library на runtime. Потребители зависят от `beesdk`; BeeSDK никогда не зависит от `beeagent`, `beeagent-rop`, `beeui` или `beescan`.

```text
beesdk
  ↑
  ├── beeagent
  ├── beeagent-rop
  ├── beescan
  └── future Bee consumers
```

BeeAgent остаётся host/orchestrator; ROP и BeeScan остаются consumer/domain products; BeeUI не является частью SDK.

## Установка и разработка

Для разработки в корне repository:

```bash
uv sync
uv run pytest -q
uv build
```

Публикуемый distribution называется `beesdk`, import package — тоже `beesdk`.

## Public API

```python
from typing import Any, Mapping

from beesdk import (
    AuthorityLevel,
    CapabilityCaller,
    CapabilityResult,
    ModuleContext,
    ModuleResult,
)


def handle(context: ModuleContext, caller: CapabilityCaller) -> ModuleResult:
    capability: CapabilityResult = caller.call("customer.lookup", {"id": "42"})
    return ModuleResult(
        module_id=context.module_id,
        case_type=context.case_type,
        authority=context.authority or AuthorityLevel.READ_ONLY,
        status=capability.status.value,
        summary=capability.summary,
        data=capability.data,
    )
```

`CapabilityCaller.call()` принимает только имя capability и payload. Authority, `module_id`, `run_id`, `session_id` и `case_type` принадлежат host/runtime и не могут задаваться модулем через этот API.

## Versioning

BeeSDK использует SemVer. Источник правды версии — package metadata в `pyproject.toml`; `CHANGELOG.md` описывает опубликованные изменения. Изменение public contract требует оценки compatibility и security boundary.
