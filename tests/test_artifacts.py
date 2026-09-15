from __future__ import annotations

from typing import Any, get_type_hints

from beesdk.artifacts import ArtifactPort
from beesdk.modules import ModuleContext


class MemoryArtifactPort:
    def __init__(self) -> None:
        self.artifacts: dict[str, dict[str, Any] | list[Any]] = {}

    def write_json(self, filename: str, data: dict[str, Any] | list[Any]) -> str:
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


def test_artifact_port_write_json_data_type() -> None:
    hints = get_type_hints(ArtifactPort.write_json)

    assert hints["data"] == dict[str, Any] | list[Any]
