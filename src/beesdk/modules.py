from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol, runtime_checkable

from beesdk.artifacts import ArtifactPort


class AuthorityLevel(str, Enum):
    READ_ONLY = "read_only"
    DRAFT_ONLY = "draft_only"
    EXECUTION_CAPABLE = "execution_capable"


@dataclass(frozen=True)
class ModuleContext:
    run_id: str
    case_type: str
    module_id: str
    payload: dict[str, Any] = field(default_factory=dict)
    session_id: str = ""
    authority: AuthorityLevel | None = None
    artifact_api: ArtifactPort | None = None


@dataclass(frozen=True)
class ModuleResult:
    module_id: str
    case_type: str
    authority: AuthorityLevel
    status: str
    summary: str
    data: dict[str, Any] = field(default_factory=dict)


@runtime_checkable
class ModuleContract(Protocol):
    @property
    def module_id(self) -> str: ...

    @property
    def authority(self) -> AuthorityLevel: ...

    def supported_case_types(self) -> list[str]: ...

    def handle(self, context: ModuleContext) -> ModuleResult: ...
