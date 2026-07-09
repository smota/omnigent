"""Manual Windows evidence capture for psmux browser terminal attach.

Run with ``OMNIGENT_WINDOWS_EVIDENCE=1`` from native Windows. The test writes
screenshots under ``.pi/evidence/windows-parity`` and is intentionally gated so
ordinary browser E2E runs do not update evidence artifacts.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from tests.e2e_ui.conftest import open_right_rail

pytestmark = pytest.mark.skipif(
    os.environ.get("OMNIGENT_WINDOWS_EVIDENCE") != "1",
    reason="set OMNIGENT_WINDOWS_EVIDENCE=1 to capture Windows evidence artifacts",
)

_USER_ZSH_KEY_RE = re.compile(r"^terminal:terminal_zsh_u-")


def _open_shell(page: Page) -> None:
    open_right_rail(page)
    rail = page.get_by_role("complementary", name="Workspace")
    rail.get_by_role("tab", name=re.compile("Shells")).click()
    rail.get_by_role("button", name="New shell").click()


def _connected_terminal(page: Page):
    main_terminal = page.get_by_test_id("main-terminal-view")
    expect(main_terminal).to_be_visible(timeout=60_000)
    expect(main_terminal).to_have_attribute("data-active-terminal", _USER_ZSH_KEY_RE)
    terminal_view = page.get_by_test_id("terminal-view").last
    expect(terminal_view).to_be_visible(timeout=60_000)
    expect(terminal_view).to_have_attribute("data-state", "connected", timeout=20_000)
    return main_terminal, terminal_view


def test_windows_psmux_browser_evidence(page: Page, terminal_session: tuple[str, str]) -> None:
    """Capture attach, input, reconnect, and ANSI limitation screenshots."""
    base_url, session_id = terminal_session
    evidence_dir = Path(".pi/evidence/windows-parity")
    evidence_dir.mkdir(parents=True, exist_ok=True)
    nonce = os.environ.get("OMNIGENT_WINDOWS_EVIDENCE_NONCE", "omnigent-windows-terminal-ok")

    page.set_viewport_size({"width": 1440, "height": 1000})
    page.goto(f"{base_url}/c/{session_id}")
    _open_shell(page)
    main_terminal, terminal_view = _connected_terminal(page)

    textarea = terminal_view.locator("textarea.xterm-helper-textarea")
    textarea.focus()
    page.keyboard.type(f"printf '{nonce}\\n'")
    page.keyboard.press("Enter")
    page.wait_for_timeout(1500)
    expect(terminal_view).to_have_attribute("data-state", "connected")
    page.screenshot(path=str(evidence_dir / "browser-psmux-terminal-attach.png"), full_page=True)
    main_terminal.screenshot(path=str(evidence_dir / "browser-psmux-terminal-panel.png"))

    page.get_by_role("button", name="Close shell").click()
    expect(main_terminal).to_have_count(0)
    page.get_by_role("complementary", name="Workspace").get_by_role(
        "button", name=re.compile("zsh")
    ).first.click()
    main_terminal, terminal_view = _connected_terminal(page)
    page.screenshot(path=str(evidence_dir / "browser-psmux-terminal-reconnect.png"), full_page=True)

    textarea = terminal_view.locator("textarea.xterm-helper-textarea")
    textarea.focus()
    page.keyboard.type("printf '\\033[31mRED\\033[0m cursor-limit-check\\n'")
    page.keyboard.press("Enter")
    page.wait_for_timeout(1500)
    page.screenshot(path=str(evidence_dir / "browser-psmux-terminal-ansi-limitation.png"), full_page=True)

    textarea.focus()
    page.keyboard.type("exit")
    page.keyboard.press("Enter")
    page.wait_for_timeout(2500)
    page.screenshot(path=str(evidence_dir / "browser-psmux-terminal-ended.png"), full_page=True)
