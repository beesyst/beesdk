from __future__ import annotations

import ast
import importlib.metadata
from pathlib import Path

import beesdk


def test_top_level_public_api_is_stable() -> None:
    from beesdk import (
        ArtifactPort,
        AuthorityLevel,
        CapabilityCaller,
        CapabilityResult,
        CapabilityStatus,
        ModuleContext,
        ModuleContract,
        ModuleResult,
    )

    assert beesdk.__all__ == [
        "ArtifactPort",
        "AuthorityLevel",
        "CapabilityCaller",
        "CapabilityResult",
        "CapabilityStatus",
        "ModuleContext",
        "ModuleContract",
        "ModuleResult",
    ]
    assert all(
        item is not None
        for item in (
            ArtifactPort,
            AuthorityLevel,
            CapabilityCaller,
            CapabilityResult,
            CapabilityStatus,
            ModuleContext,
            ModuleContract,
            ModuleResult,
        )
    )


def test_distribution_has_no_runtime_dependencies() -> None:
    metadata = importlib.metadata.metadata("beesdk")
    assert metadata.get_all("Requires-Dist") in (None, [])


def test_package_does_not_import_consumer_projects() -> None:
    package_root = Path(beesdk.__file__).parent
    forbidden = {"beeagent", "beeagent_rop", "beeui", "beescan"}

    for source_file in package_root.glob("*.py"):
        tree = ast.parse(source_file.read_text(encoding="utf-8"))
        imported = {
            alias.name.split(".", maxsplit=1)[0]
            for node in ast.walk(tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
            for alias in (
                node.names
                if isinstance(node, ast.Import)
                else (() if node.module is None else [ast.alias(name=node.module)])
            )
        }
        assert not forbidden.intersection(imported), source_file
