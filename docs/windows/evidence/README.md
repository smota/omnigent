# Windows evidence package

Collected on native Windows for the bounded Windows first-class support ADR.

## Environment

See [`environment-inventory.txt`](environment-inventory.txt).

## Browser psmux terminal attach

Evidence was collected by running the existing browser E2E fixture flow on native
Windows with Chromium headed mode and the psmux terminal backend installed.

Command used:

```powershell
$env:PATH="C:\Users\samue\AppData\Local\hermes\node;" + $env:PATH
uv run pytest tests/e2e_ui/test_windows_terminal_evidence_tmp.py::test_windows_psmux_browser_evidence -q --headed --browser chromium --ui-skip-build
```

The temporary evidence test used the same `terminal_session` fixture and web UI
flow as `tests/e2e_ui/shells/test_new_shell.py`: open the Shells rail, create a
new shell, wait for `data-state="connected"`, type a nonce command into xterm,
verify the bridge stays connected, and capture screenshots.

Artifacts:

- [`browser-psmux-terminal-attach.png`](browser-psmux-terminal-attach.png) — full-page screenshot of Omnigent web terminal attach with typed nonce command.
- [`browser-psmux-terminal-panel.png`](browser-psmux-terminal-panel.png) — focused terminal panel screenshot.

Nonce typed in the terminal:

```text
omnigent-windows-terminal-ok-20260709
```

Validation output:

```text
Running 1 items in this shard
.
1 passed in 18.56s
```

## Notes

The screenshot demonstrates browser attach and input delivery for the documented
capture/send bridge. It does not claim POSIX tmux PTY/control fidelity parity;
that limitation remains documented in `../psmux-browser-attach.md`.
