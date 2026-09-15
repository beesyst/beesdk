from __future__ import annotations

import inspect
from collections.abc import Mapping
from typing import Any, get_type_hints

from beesdk.capabilities import CapabilityCaller, CapabilityResult, CapabilityStatus
from beesdk.modules import AuthorityLevel


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

    assert [status.value for status in CapabilityStatus] == [
        "ok",
        "refused",
        "timeout",
        "error",
    ]
    assert result.data == {}
    assert result.diagnostics == {}


def test_module_facing_call_cannot_receive_host_owned_identity_or_authority() -> None:
    parameters = list(inspect.signature(CapabilityCaller.call).parameters)

    assert parameters == ["self", "capability_name", "payload"]
    assert not {
        "authority",
        "module_id",
        "run_id",
        "session_id",
        "case_type",
    }.intersection(parameters)


def test_capability_result_data_and_diagnostics_are_dicts() -> None:
    hints = get_type_hints(CapabilityResult)

    assert hints["data"] == dict[str, Any]
    assert hints["diagnostics"] == dict[str, Any]


def test_capability_caller_payload_remains_mapping() -> None:
    hints = get_type_hints(CapabilityCaller.call)

    assert hints["payload"] == Mapping[str, Any]
