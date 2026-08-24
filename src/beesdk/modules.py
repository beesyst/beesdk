"""Public module contracts shared by Bee hosts and modules."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Protocol, runtime_checkable

from beesdk.artifacts import ArtifactPort


class AuthorityLevel(str, Enum):
    """Authority granted by a host to a module run."""

    READ_ONLY = "read_only"
    DRAFT_ONLY = "draft_only"
    EXECUTION_CAPABLE = "execution_capable"


@dataclass(frozen=True)
class ModuleContext:
    """Host-provided context for one module invocation.

    ``artifact_api`` remains named for compatibility with existing BeeAgent modules.
    It is an abstract port, never a storage implementation supplied by BeeSDK.
    """

    run_id: str
    case_type: str
    module_id: str
    payload: Mapping[str, Any] = field(default_factory=dict)
    session_id: str = ""
    authority: AuthorityLevel | None = None
    artifact_api: ArtifactPort | None = None


@dataclass(frozen=True)
class ModuleResult:
    """A module's bounded result returned to its host."""

    module_id: str
    case_type: str
    authority: AuthorityLevel
    status: str
    summary: str
    data: Mapping[str, Any] = field(default_factory=dict)


@runtime_checkable
class ModuleContract(Protocol):
    """Structural contract a reusable Bee module implements."""

    @property
    def module_id(self) -> str: ...

    @property
    def authority(self) -> AuthorityLevel: ...

    def supported_case_types(self) -> list[str]: ...

    def handle(self, context: ModuleContext) -> ModuleResult: ...
