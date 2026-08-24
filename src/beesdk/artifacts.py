"""Minimal host-owned artifact boundary for Bee modules."""

from __future__ import annotations

from typing import Any, Mapping, Protocol, runtime_checkable


@runtime_checkable
class ArtifactPort(Protocol):
    """A host-provided port for a module to write one JSON-safe artifact.

    Storage location, naming policy, lifecycle and returned handle are deliberately owned
    by the host. BeeSDK provides no filesystem or path implementation.
    """

    def write_json(self, filename: str, data: Mapping[str, Any] | list[Any]) -> Any: ...
