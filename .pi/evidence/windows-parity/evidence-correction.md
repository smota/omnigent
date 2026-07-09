## Evidence correction (2026-07-09)

The earlier browser/desktop PNG screenshots are withdrawn. They did not show the requested real Omnigent application or terminal state consistently enough for PR review and should not be used as validation evidence.

Authoritative evidence for review is the native Windows terminal/tool output transcripts in this bundle:

- `00_environment.txt` — native Windows/toolchain inventory, including `psmux` / tmux.
- `01_import_cli_smoke.txt` — `import omnigent` and `uv run omnigent --help` output.
- `02_windows_safe_stable.txt` — stable Windows helper run: `21 passed, 6 skipped`.
- `03_runner_transport_tests.txt` — runner transport/routing tests: `18 passed`.
- `04_sandbox_fail_closed_tests.txt` — sandbox fail-closed tests: `6 passed`.
- `05_psmux_diagnostics_test.txt` — missing-`psmux` diagnostic test: `1 passed`.
- `06_precommit_key_windows_docs.txt` — focused pre-commit hooks: `EXIT=0`.
- `07_collect_only.txt` — broad collection: `14709/14725 tests collected`, `EXIT=0`.

If visual evidence is required later, it must be captured from an unlocked interactive Windows desktop showing the real Omnigent terminal/application window, not headless GitHub pages or an empty desktop.
