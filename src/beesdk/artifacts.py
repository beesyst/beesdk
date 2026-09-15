from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ArtifactPort(Protocol):
    def write_json(self, filename: str, data: dict[str, Any] | list[Any]) -> Any: ...
