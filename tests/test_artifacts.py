from __future__ import annotations

from typing import Any, Mapping

from beesdk import ArtifactPort, ModuleContext


class MemoryArtifactPort:
    def __init__(self) -> None:
        self.artifacts: dict[str, Mapping[str, Any] | list[Any]] = {}

    def write_json(self, filename: str, data: Mapping[str, Any] | list[Any]) -> str:
        self.artifacts[filename] = data
        return filename


def test_artifact_port_is_structural_and_not_path_based() -> None:
    port = MemoryArtifactPort()
    context = ModuleContext(
        run_id="run-1",
        case_type="example_case",
        module_id="example",
        artifact_api=port,
    )

    assert isinstance(port, ArtifactPort)
    assert context.artifact_api is port
    assert port.write_json("result.json", {"ok": True}) == "result.json"
