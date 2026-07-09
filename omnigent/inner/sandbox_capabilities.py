"""Sandbox capability metadata by platform/backend."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class SandboxCapabilities:
    """Security capabilities advertised by an OS sandbox backend.

    :param backend: Sandbox backend identifier.
    :param platform: Platform family the backend runs on.
    :param process_containment: Whether child process cleanup/containment is
        provided.
    :param filesystem_isolation: Whether read/write path policy is hard-enforced.
    :param network_isolation: Whether network deny/isolation can be hard-enforced.
    :param egress_policy: Whether L7 egress rules can be enforced by forcing all
        traffic through the Omnigent egress proxy.
    :param notes: Short human-readable support boundary.
    """

    backend: str
    platform: str
    process_containment: bool
    filesystem_isolation: bool
    network_isolation: bool
    egress_policy: bool
    notes: str


_CAPABILITIES: dict[str, SandboxCapabilities] = {
    "linux_bwrap": SandboxCapabilities(
        backend="linux_bwrap",
        platform="linux",
        process_containment=True,
        filesystem_isolation=True,
        network_isolation=True,
        egress_policy=True,
        notes="bubblewrap enforces filesystem, process, and network isolation",
    ),
    "darwin_seatbelt": SandboxCapabilities(
        backend="darwin_seatbelt",
        platform="darwin",
        process_containment=True,
        filesystem_isolation=True,
        network_isolation=True,
        egress_policy=True,
        notes="seatbelt profile enforces filesystem and network policy",
    ),
    "windows_job_object": SandboxCapabilities(
        backend="windows_job_object",
        platform="windows",
        process_containment=True,
        filesystem_isolation=False,
        network_isolation=False,
        egress_policy=False,
        notes=(
            "Windows Job Object support contains and cleans up process trees but "
            "does not provide filesystem isolation or network/egress policy"
        ),
    ),
    "none": SandboxCapabilities(
        backend="none",
        platform="any",
        process_containment=False,
        filesystem_isolation=False,
        network_isolation=False,
        egress_policy=False,
        notes="no OS sandbox isolation",
    ),
}


def sandbox_capabilities(backend: str) -> SandboxCapabilities:
    """Return capability metadata for *backend*.

    Unknown backends are treated as unsupported/no-isolation so policy callers
    can fail closed instead of assuming a secure default.
    """
    return _CAPABILITIES.get(
        backend,
        SandboxCapabilities(
            backend=backend,
            platform="unknown",
            process_containment=False,
            filesystem_isolation=False,
            network_isolation=False,
            egress_policy=False,
            notes="unknown sandbox backend; no capabilities advertised",
        ),
    )


def default_sandbox_backend_for_platform(platform: str | None = None) -> str:
    """Return the default sandbox backend name for a platform family."""
    name = platform or os.name
    if name == "nt":
        return "windows_job_object"
    if name == "posix":
        if os.uname().sysname == "Darwin":
            return "darwin_seatbelt"
        return "linux_bwrap"
    return "none"


__all__ = [
    "SandboxCapabilities",
    "default_sandbox_backend_for_platform",
    "sandbox_capabilities",
]
