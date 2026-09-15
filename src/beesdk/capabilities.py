from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol, runtime_checkable

from beesdk.modules import AuthorityLevel


class CapabilityStatus(str, Enum):
    OK = "ok"
    REFUSED = "refused"
    TIMEOUT = "timeout"
    ERROR = "error"


@dataclass(frozen=True)
class CapabilityResult:
    capability_name: str
    status: CapabilityStatus
    authority: AuthorityLevel
    summary: str
    data: dict[str, Any] = field(default_factory=dict)
    diagnostics: dict[str, Any] = field(default_factory=dict)


@runtime_checkable
class CapabilityCaller(Protocol):
    def call(
        self,
        capability_name: str,
        payload: Mapping[str, Any],
    ) -> CapabilityResult: ...
