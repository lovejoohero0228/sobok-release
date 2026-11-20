# Sobok uninstaller. Usage (PowerShell):  irm <url-of-this-file> | iex
# Removes the exe, the Start Menu shortcut, and saved settings. ASCII-only on purpose (see install.ps1).
$name = -join ([char]0xC18C, [char]0xBCF5, [char]0xC18C, [char]0xBCF5)
Get-Process sobok -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Milliseconds 800
$targets = @(
  (Join-Path $env:LOCALAPPDATA 'Sobok'),
  (Join-Path $env:LOCALAPPDATA 'com.sobok.widget'),
  (Join-Path $env:APPDATA 'com.sobok.widget'),
  (Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\$name.lnk")
)
foreach ($t in $targets) { if (Test-Path -LiteralPath $t) { Remove-Item -LiteralPath $t -Recurse -Force -ErrorAction SilentlyContinue } }
Write-Host "$name was removed." -ForegroundColor Green
