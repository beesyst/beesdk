from __future__ import annotations

import inspect
from typing import Any, Mapping

from beesdk import AuthorityLevel, CapabilityCaller, CapabilityResult, CapabilityStatus


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
            data=payload,
        )


def test_capability_caller_is_structural() -> None:
    caller = ExampleCapabilityCaller()

    assert isinstance(caller, CapabilityCaller)
    assert caller.call("lookup", {"id": "42"}).status is CapabilityStatus.OK


def test_capability_result_defaults_and_statuses() -> None:
    result = CapabilityResult(
        capability_name="lookup",
        status=CapabilityStatus.REFUSED,
        authority=AuthorityLevel.DRAFT_ONLY,
        summary="policy refused request",
    )

    assert [status.value for status in CapabilityStatus] == ["ok", "refused", "timeout", "error"]
    assert result.data == {}
    assert result.diagnostics == {}


def test_module_facing_call_cannot_receive_host_owned_identity_or_authority() -> None:
    parameters = list(inspect.signature(CapabilityCaller.call).parameters)

    assert parameters == ["self", "capability_name", "payload"]
    assert not {"authority", "module_id", "run_id", "session_id", "case_type"}.intersection(parameters)
