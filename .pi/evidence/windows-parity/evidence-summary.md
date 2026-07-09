## Controlled user evidence results (2026-07-09)

Executed on native Windows 10 Home ARM64 from the integration branch after syncing the open PR stack.

Artifacts are stored locally under `.pi/evidence/windows-parity/`:

- `00_environment.txt` — Windows/toolchain inventory (`uv 0.11.23`, Python `3.11.15`, Node `v24.16.0`, npm `11.18.0`, `psmux` / tmux `3.3.6`).
- `01_import_cli_smoke.txt` — `import omnigent` and `uv run omnigent --help` succeeded.
- `02_windows_safe_stable.txt` — stable Windows helper result: `21 passed, 6 skipped`.
- `03_runner_transport_tests.txt` — runner routing/transport tests: `18 passed`.
- `04_sandbox_fail_closed_tests.txt` — sandbox fail-closed tests: `6 passed`.
- `05_psmux_diagnostics_test.txt` — missing-`psmux` diagnostic test: `1 passed`.
- `06_precommit_key_windows_docs.txt` — whitespace/newline hooks over changed Windows docs: `EXIT=0`.
- `07_collect_only.txt` — broad collection check: `14709/14725 tests collected`, `EXIT=0`.
- `desktop-evidence-summary.png` — local desktop print screen captured for reviewer evidence pack.

Key transcript excerpts:

```text
# stable Windows helper
21 passed, 6 skipped in 2.30s

# runner transport/routing
18 passed in 2.27s

# sandbox fail-closed
6 passed in 0.38s

# psmux diagnostic
1 passed in 0.14s

# broad collect-only
14709/14725 tests collected (16 deselected) in 11.47s
```

Notes:

- This is the executed follow-up to the `Controlled user evidence plan` already added to the open PRs.
- The psmux-specific review path includes terminal `attach/reconnect` coverage in the evidence plan; this run collected CLI/test evidence and a local print screen, while browser attach/reconnect screenshots remain the only manual visual item to capture if reviewers require them.
