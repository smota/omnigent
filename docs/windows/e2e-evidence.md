# Windows native E2E evidence package

Use this package to collect review evidence for native Windows parity PRs. It is
intended to be filled from a fresh Windows machine against either a specific PR
branch or the fork-only integration branch.

## Scope

Validate the integrated Windows path:

1. PowerShell installer or manual `uv` setup.
2. Native smoke/unit checks.
3. Server and host startup from PowerShell.
4. psmux-backed terminal creation and browser attach.
5. Runner transport selection/fallback diagnostics.
6. Sandbox/egress fail-closed diagnostics for unsupported Windows policies.

## Environment inventory

Record this at the start of the transcript:

```powershell
$PSVersionTable
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsArchitecture
where.exe git
where.exe uv
where.exe python
where.exe node
where.exe npm
where.exe psmux
uv --version
python --version
node --version
npm --version
psmux --version
```

## Checkout and setup

```powershell
git clone https://github.com/smota/omnigent.git
cd omnigent
git switch windows-parity/integration
uv sync --extra all --extra dev
```

If validating a single PR, replace `windows-parity/integration` with the PR
branch under test.

## Automated validation

```powershell
uv run python -c "import omnigent; print('import omnigent OK')"
uv run omnigent --help
uv run pytest tests/inner/test_proc_and_platform.py tests/runtime/test_process_manager.py -p no:cacheprovider -q
uv run pytest -m "not posix_only" --collect-only -q
```

For PR-specific validation, include the targeted test command from the PR body.

## Manual server/host validation

Terminal 1:

```powershell
uv run omnigent server
```

Terminal 2:

```powershell
uv run omnigent host --server http://localhost:6767
```

Browser:

1. Open the local server URL.
2. Create a new session using the Windows host.
3. Create an Omnigent-managed terminal.
4. Confirm logs identify the Windows terminal backend.
5. Attach to the terminal and run:

```powershell
$PSVersionTable.PSVersion
pwd
Write-Output "omnigent-windows-terminal-ok"
```

Capture a screenshot or short recording showing browser attach and command
output.

## Runner transport evidence

When testing TCP runner transport wiring, capture startup logs that identify the
selected transport. Include any relevant env/config values and prove UDS-only
configuration on native Windows fails with an actionable TCP fallback message.

## Sandbox/egress fail-closed evidence

Run or document a spec that requests unsupported Windows network denial, for
example:

```yaml
spec_version: 1
name: windows-network-deny
os_env:
  type: caller_process
  sandbox:
    type: windows_jobobject
    allow_network: false
```

Expected result: validation fails before runtime with a message explaining that
Windows Job Objects do not hard-enforce network denial and that Linux/macOS
hardened sandboxes are required for network isolation.

## Evidence checklist for PRs

- [ ] PowerShell transcript attached.
- [ ] Environment inventory included.
- [ ] Automated validation commands included.
- [ ] Browser attach screenshot/recording attached for terminal/UI work.
- [ ] Runner transport selection logs included for transport work.
- [ ] Sandbox fail-closed output included for policy work.
- [ ] Known gaps listed explicitly.

## Known limitations to call out

- Windows Job Objects provide process containment, not bwrap/seatbelt-equivalent
  filesystem or network isolation.
- POSIX-only PTY/tmux/pexpect coverage remains Linux/macOS/WSL-only.
- The broad Windows test sweep should remain non-blocking until execution, not
  just collection, is deterministic on `windows-latest`.
