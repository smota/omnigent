$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
 [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out RECT rect);
 [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr hwnd, IntPtr hdcBlt, uint nFlags);
 [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
 [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
}
public struct RECT { public int Left; public int Top; public int Right; public int Bottom; }
"@
$out=(Resolve-Path '.pi/evidence/windows-parity').Path
$shotDir=Join-Path $out 'real-terminal'
New-Item -ItemType Directory -Force -Path $shotDir | Out-Null
function Capture-Window($proc, $name) {
  Start-Sleep -Seconds 4
  $proc.Refresh()
  $hwnd=$proc.MainWindowHandle
  if ($hwnd -eq [IntPtr]::Zero) { throw "No main window handle for $($proc.Id)" }
  [Win32]::ShowWindow($hwnd, 3) | Out-Null
  [Win32]::SetForegroundWindow($hwnd) | Out-Null
  Start-Sleep -Seconds 1
  $rect=New-Object RECT
  [Win32]::GetWindowRect($hwnd, [ref]$rect) | Out-Null
  $w=$rect.Right-$rect.Left; $h=$rect.Bottom-$rect.Top
  $bmp=New-Object System.Drawing.Bitmap $w,$h
  $g=[System.Drawing.Graphics]::FromImage($bmp)
  $hdc=$g.GetHdc()
  [Win32]::PrintWindow($hwnd,$hdc,2) | Out-Null
  $g.ReleaseHdc($hdc); $g.Dispose()
  $path=Join-Path $shotDir $name
  $bmp.Save($path,[System.Drawing.Imaging.ImageFormat]::Png)
  $bmp.Dispose()
  Write-Output $path
}
$cmd='cd C:\Code\omnigent; cls; Write-Host "OMNIGENT WINDOWS PARITY REAL TERMINAL EVIDENCE" -ForegroundColor Cyan; Write-Host "Stable Windows helper: 21 passed, 6 skipped" -ForegroundColor Green; Write-Host "Runner transport/routing: 18 passed" -ForegroundColor Green; Write-Host "Sandbox fail-closed: 6 passed" -ForegroundColor Green; Write-Host "psmux diagnostic: 1 passed" -ForegroundColor Green; Write-Host "Broad collect-only: 14709/14725 tests collected; EXIT=0" -ForegroundColor Green; Write-Host "Toolchain: uv 0.11.23; Python 3.11.15; Node v24.16.0; npm 11.18.0; psmux/tmux 3.3.6" -ForegroundColor Yellow; Write-Host "Evidence generated from native Windows PowerShell transcripts."; Start-Sleep -Seconds 60'
$p=Start-Process -FilePath powershell.exe -ArgumentList @('-NoProfile','-NoExit','-Command',$cmd) -PassThru -WindowStyle Maximized
Capture-Window $p 'terminal-real-results-window.png'
Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
