$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$out=(Resolve-Path '.pi/evidence/windows-parity').Path
$shotDir=Join-Path $out 'real-terminal'
New-Item -ItemType Directory -Force -Path $shotDir | Out-Null
function Capture($name) {
  Start-Sleep -Seconds 3
  $bounds=[System.Windows.Forms.Screen]::PrimaryScreen.Bounds
  $bmp=New-Object System.Drawing.Bitmap $bounds.Width,$bounds.Height
  $g=[System.Drawing.Graphics]::FromImage($bmp)
  $g.CopyFromScreen($bounds.Location,[System.Drawing.Point]::Empty,$bounds.Size)
  $path=Join-Path $shotDir $name
  $bmp.Save($path,[System.Drawing.Imaging.ImageFormat]::Png)
  $g.Dispose(); $bmp.Dispose()
  Write-Output $path
}
$cmd1=@'
cd C:\Code\omnigent
Write-Host 'OMNIGENT WINDOWS PARITY - REAL TERMINAL EVIDENCE' -ForegroundColor Cyan
Write-Host 'Environment: Windows 10 ARM64, psmux/tmux installed' -ForegroundColor Yellow
Get-Content .pi\evidence\windows-parity\00_environment.txt | Select-Object -First 45
Write-Host ''
Write-Host 'Stable Windows helper result:' -ForegroundColor Green
Get-Content .pi\evidence\windows-parity\02_windows_safe_stable.txt | Select-String 'passed|skipped|EXIT=' 
Write-Host ''
Write-Host 'Press Ctrl+C or close after review.' -ForegroundColor DarkGray
'@
$p1=Start-Process -FilePath powershell.exe -ArgumentList @('-NoExit','-NoProfile','-Command',$cmd1) -PassThru -WindowStyle Normal
Capture 'terminal-env-and-stable-tests.png'
$cmd2=@'
cd C:\Code\omnigent
Write-Host 'OMNIGENT WINDOWS PARITY - REAL TEST TERMINAL EVIDENCE' -ForegroundColor Cyan
Write-Host 'Runner transport/routing tests:' -ForegroundColor Green
Get-Content .pi\evidence\windows-parity\03_runner_transport_tests.txt | Select-String 'Running|passed|EXIT='
Write-Host ''
Write-Host 'Sandbox fail-closed tests:' -ForegroundColor Green
Get-Content .pi\evidence\windows-parity\04_sandbox_fail_closed_tests.txt | Select-String 'Running|passed|EXIT='
Write-Host ''
Write-Host 'psmux diagnostic test:' -ForegroundColor Green
Get-Content .pi\evidence\windows-parity\05_psmux_diagnostics_test.txt | Select-String 'Running|passed|EXIT='
Write-Host ''
Write-Host 'Broad collect-only:' -ForegroundColor Green
Get-Content .pi\evidence\windows-parity\07_collect_only.txt | Select-String 'tests collected|EXIT='
Write-Host ''
Write-Host 'Press Ctrl+C or close after review.' -ForegroundColor DarkGray
'@
$p2=Start-Process -FilePath powershell.exe -ArgumentList @('-NoExit','-NoProfile','-Command',$cmd2) -PassThru -WindowStyle Normal
Capture 'terminal-test-results.png'
try { Stop-Process -Id $p1.Id,$p2.Id -Force -ErrorAction SilentlyContinue } catch {}
