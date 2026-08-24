from __future__ import annotations

from beesdk import AuthorityLevel, ModuleContext, ModuleContract, ModuleResult


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
    context = ModuleContext(run_id="run-1", case_type="example_case", module_id="example")

    assert context.payload == {}
    assert context.session_id == ""
    assert context.authority is None
    assert context.artifact_api is None


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
