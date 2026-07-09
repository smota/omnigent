"""Terminal multiplexer backend abstractions.

The current implementation is tmux-backed. This module introduces a small
backend seam so alternative multiplexers can be wired without changing the
registry contract that tools and runners already use.
"""

from __future__ import annotations

import asyncio
import os
import shutil
import tempfile
from pathlib import Path
from typing import Protocol

from omnigent._platform import IS_WINDOWS
from omnigent.inner.datamodel import OSEnvSpec, TerminalEnvSpec
from omnigent.inner.terminal import TerminalInstance, create_terminal_instance


class TerminalMuxBackend(Protocol):
    """Create terminal instances for a registry-managed multiplexer backend."""

    @property
    def name(self) -> str:
        """Stable backend identifier, e.g. ``"tmux"``."""
        ...

    def create(
        self,
        terminal_name: str,
        session_key: str,
        spec: TerminalEnvSpec,
        *,
        parent_os_env: OSEnvSpec | None = None,
        cwd_override: str | None = None,
        sandbox_override: str | None = None,
        conversation_link: str | None = None,
    ) -> tuple[TerminalInstance, Path]:
        """Create an unlaunched terminal instance and its resolved cwd."""
        ...


class PsmuxTerminalInstance(TerminalInstance):
    """Terminal instance launched through psmux on native Windows."""

    backend_name: str = "psmux"

    @property
    def tmux_target(self) -> str:
        safe_name = "".join(ch if ch.isalnum() else "-" for ch in self.name)
        safe_key = "".join(ch if ch.isalnum() else "-" for ch in self.session_key)
        return f"omnigent-{safe_name}-{safe_key}-{abs(hash(self.private_dir)) & 0xFFFF:x}"

    def _tmux_base_cmd(self) -> list[str]:
        return ["psmux", "-S", str(self.socket_path)]

    async def launch(self, *, cwd: Path | None = None) -> None:
        if self.running:
            return
        effective_cwd = str(cwd or self.private_dir)
        env = os.environ.copy() if self.inherit_env else {}
        env.pop("OMNIGENT_TMUX_SOCK", None)
        env.update(self.env)
        for key in self.env_unset:
            env.pop(key, None)

        proc = await asyncio.create_subprocess_exec(
            *self._tmux_base_cmd(),
            "new-session",
            "-d",
            "-s",
            self.tmux_target,
            "-c",
            effective_cwd,
            "--",
            shutil.which(self.command) or self.command,
            *self.args,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.PIPE,
            env=env,
        )
        _, stderr = await proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError(
                f"psmux launch failed (rc={proc.returncode}): {stderr.decode().strip()}"
            )
        self.running = True
        self.launch_cwd = effective_cwd


class TmuxTerminalMuxBackend:
    """Terminal backend that delegates to the existing tmux implementation."""

    @property
    def name(self) -> str:
        return "tmux"

    def create(
        self,
        terminal_name: str,
        session_key: str,
        spec: TerminalEnvSpec,
        *,
        parent_os_env: OSEnvSpec | None = None,
        cwd_override: str | None = None,
        sandbox_override: str | None = None,
        conversation_link: str | None = None,
    ) -> tuple[TerminalInstance, Path]:
        created = create_terminal_instance(
            terminal_name,
            session_key,
            spec,
            parent_os_env_spec=parent_os_env,
            cwd_override=cwd_override,
            sandbox_override=sandbox_override,
            conversation_link=conversation_link,
        )
        return created.instance, created.cwd


class PsmuxTerminalMuxBackend:
    """Windows terminal backend using psmux as a tmux-compatible multiplexer."""

    @property
    def name(self) -> str:
        return "psmux"

    def validate_available(self) -> None:
        """Fail loudly when the psmux backend cannot run on this machine."""
        if not IS_WINDOWS:
            raise RuntimeError("psmux terminal backend is only supported on Windows")
        if shutil.which("psmux") is None:
            raise RuntimeError(
                "psmux is required for Omnigent-managed terminals on native Windows "
                "but was not found on PATH. Install psmux and restart the Omnigent "
                "host, or use WSL/Linux/macOS for the tmux terminal backend."
            )

    def create(
        self,
        terminal_name: str,
        session_key: str,
        spec: TerminalEnvSpec,
        *,
        parent_os_env: OSEnvSpec | None = None,
        cwd_override: str | None = None,
        sandbox_override: str | None = None,
        conversation_link: str | None = None,
    ) -> tuple[TerminalInstance, Path]:
        del parent_os_env, sandbox_override, conversation_link
        self.validate_available()
        private_dir = Path(tempfile.mkdtemp(prefix="omnigent-terminal-"))
        cwd = Path(cwd_override or (spec.os_env.cwd if spec.os_env else os.getcwd())).resolve()
        instance = PsmuxTerminalInstance(
            name=terminal_name,
            session_key=session_key,
            socket_path=private_dir / "psmux.sock",
            private_dir=private_dir,
            command=spec.command,
            args=list(spec.args),
            env=dict(spec.env),
            env_unset=list(spec.env_unset),
            inherit_env=spec.inherit_env,
            scrollback=spec.scrollback,
            tmux_allow_passthrough=spec.tmux_allow_passthrough,
            tmux_start_on_attach=spec.tmux_start_on_attach,
            keep_alive_after_exit=spec.keep_alive_after_exit,
            terminal_transport=spec.terminal_transport,
        )
        return instance, cwd


def default_terminal_mux_backend() -> TerminalMuxBackend:
    """Return the platform default terminal multiplexer backend."""
    if IS_WINDOWS:
        return PsmuxTerminalMuxBackend()
    return TmuxTerminalMuxBackend()
