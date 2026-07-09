$ErrorActionPreference = 'Continue'
$root = Resolve-Path "."
$out = Join-Path $root ".pi/evidence/windows-parity"
New-Item -ItemType Directory -Force -Path $out | Out-Null
function Run-Step($Name, [scriptblock]$Block) {
  $safeName = $Name -replace '[^A-Za-z0-9_.-]', '_'
  $file = Join-Path $out "$safeName.txt"
  "==> $Name" | Tee-Object -FilePath $file
  try {
    & $Block *>&1 | Tee-Object -FilePath $file -Append
    "EXIT=$LASTEXITCODE" | Tee-Object -FilePath $file -Append
  } catch {
    "ERROR=$($_.Exception.Message)" | Tee-Object -FilePath $file -Append
  }
}
Run-Step "00_environment" { $PSVersionTable; Get-ComputerInfo | Select WindowsProductName,WindowsVersion,OsArchitecture; where.exe git; where.exe uv; where.exe python; where.exe node; where.exe npm; where.exe psmux; uv --version; python --version; node --version; npm --version; psmux --version }
Run-Step "01_import_cli_smoke" { uv run python -c "import omnigent; print('import omnigent OK')"; uv run omnigent --help }
Run-Step "02_windows_safe_stable" { pwsh -NoProfile -File scripts/windows_safe_pytest.ps1 -StableOnly }
Run-Step "03_runner_transport_tests" { uv run pytest tests/server/test_runner_transport.py tests/runner/test_routing.py -q }
Run-Step "04_sandbox_fail_closed_tests" { uv run pytest tests/inner/test_sandbox_capabilities.py tests/spec/test_parser.py::test_parse_windows_jobobject_rejects_network_deny tests/spec/test_validator.py::test_os_env_windows_jobobject_rejects_network_deny -q }
Run-Step "05_psmux_diagnostics_test" { uv run pytest tests/terminals/test_registry.py::test_psmux_backend_missing_binary_error_is_actionable -q }
Run-Step "06_precommit_key_windows_docs" { uv run pre-commit run trailing-whitespace --files docs/windows-e2e-evidence.md docs/windows-test-execution.md docs/windows-sandbox-isolation-design.md README.md; uv run pre-commit run end-of-file-fixer --files docs/windows-e2e-evidence.md docs/windows-test-execution.md docs/windows-sandbox-isolation-design.md README.md }
Run-Step "07_collect_only" { pwsh -NoProfile -File scripts/windows_safe_pytest.ps1 -CollectOnly }
