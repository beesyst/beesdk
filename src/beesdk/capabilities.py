"""Module-facing capability contracts with host-owned authority and identity."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Protocol, runtime_checkable

from beesdk.modules import AuthorityLevel


class CapabilityStatus(str, Enum):
    """Bounded outcome of a capability call."""

    OK = "ok"
    REFUSED = "refused"
    TIMEOUT = "timeout"
    ERROR = "error"


@dataclass(frozen=True)
class CapabilityResult:
    """Host-returned result of a module-facing capability call."""

    capability_name: str
    status: CapabilityStatus
    authority: AuthorityLevel
    summary: str
    data: Mapping[str, Any] = field(default_factory=dict)
    diagnostics: Mapping[str, Any] = field(default_factory=dict)


@runtime_checkable
class CapabilityCaller(Protocol):
    """Host-injected caller with authority and runtime identity kept host-owned."""

    def call(
        self,
        capability_name: str,
        payload: Mapping[str, Any],
    ) -> CapabilityResult: ...
