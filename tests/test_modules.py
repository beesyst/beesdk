from __future__ import annotations

from collections.abc import Mapping
from typing import Any, get_type_hints

from beesdk.capabilities import CapabilityCaller, CapabilityResult, CapabilityStatus
from beesdk.modules import AuthorityLevel, ModuleContext, ModuleContract, ModuleResult


class ExampleModule:
    module_id = "example"
    authority = AuthorityLevel.READ_ONLY

    def supported_case_types(self) -> list[str]:
        return ["example_case"]

    def handle(self, context: ModuleContext) -> ModuleResult:
        return ModuleResult(
            module_id=self.module_id,
            case_type=context.case_type,
            authority=self.authority,
            status="ok",
            summary="handled",
            data=context.payload,
        )


def test_module_context_preserves_compatibility_artifact_api_field() -> None:
    context = ModuleContext(
        run_id="run-1", case_type="example_case", module_id="example"
    )

    assert context.payload == {}
    assert context.session_id == ""
    assert context.authority is None
    assert context.artifact_api is None
    assert context.capability_caller is None


class ExampleCapabilityCaller:
    def call(
        self,
        capability_name: str,
        payload: Mapping[str, Any],
    ) -> CapabilityResult:
        return CapabilityResult(
            capability_name=capability_name,
            status=CapabilityStatus.OK,
            authority=AuthorityLevel.READ_ONLY,
            summary="completed",
            data=dict(payload),
        )


def test_module_context_accepts_host_provided_capability_caller() -> None:
    caller = ExampleCapabilityCaller()
    context = ModuleContext(
        run_id="run-1",
        case_type="example_case",
        module_id="example",
        capability_caller=caller,
    )

    assert isinstance(context.capability_caller, CapabilityCaller)
    assert context.capability_caller is caller


def test_module_contract_is_structural() -> None:
    module = ExampleModule()
    context = ModuleContext(
        run_id="run-1",
        case_type="example_case",
        module_id="example",
        payload={"key": "value"},
    )

    assert isinstance(module, ModuleContract)
    assert module.handle(context).data == {"key": "value"}


def test_module_contract_matches_beeagent_extraction_types() -> None:
    module_hints = get_type_hints(ModuleContext)
    result_hints = get_type_hints(ModuleResult)

    assert module_hints["payload"] == dict[str, Any]
    assert result_hints["data"] == dict[str, Any]
