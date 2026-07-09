"""Tests for sandbox capability metadata."""

from __future__ import annotations

from omnigent.inner.sandbox_capabilities import (
    default_sandbox_backend_for_platform,
    sandbox_capabilities,
)


def test_windows_jobobject_capabilities_are_process_only() -> None:
    """Windows metadata is explicit about containment but no egress isolation."""
    caps = sandbox_capabilities("windows_jobobject")

    assert caps.platform == "windows"
    assert caps.process_containment is True
    assert caps.filesystem_isolation is False
    assert caps.network_isolation is False
    assert caps.egress_policy is False
    assert "Job Object" in caps.notes


def test_egress_capable_backends_are_marked() -> None:
    """Linux/macOS hardened backends advertise egress-policy support."""
    assert sandbox_capabilities("linux_bwrap").egress_policy is True
    assert sandbox_capabilities("darwin_seatbelt").egress_policy is True


def test_unknown_backend_fails_closed() -> None:
    """Unknown backend metadata must not imply any isolation capability."""
    caps = sandbox_capabilities("future_backend")

    assert caps.backend == "future_backend"
    assert caps.process_containment is False
    assert caps.filesystem_isolation is False
    assert caps.network_isolation is False
    assert caps.egress_policy is False


def test_default_windows_backend() -> None:
    """Native Windows defaults to process containment metadata."""
    assert default_sandbox_backend_for_platform("nt") == "windows_jobobject"
