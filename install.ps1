# Sobok installer. Usage (PowerShell):  irm <url-of-this-file> | iex
# Downloads one exe into the user's folder, adds a Start Menu shortcut, and starts it. No admin rights needed.
# Keep this file ASCII-only: Windows PowerShell 5.1 may misread other characters when the script is piped from the web.
$ErrorActionPreference = 'Stop'
$repo = 'lovejoohero0228/sobok-release'                                             # public repository that holds the release
$url  = if ($env:SOBOK_URL) { $env:SOBOK_URL } else { "https://github.com/$repo/releases/latest/download/sobok.exe" }
$ko   = -join ([char]0xC18C, [char]0xBCF5, [char]0xC18C, [char]0xBCF5)   # the app name in Korean
# Start Menu name: Korean on a Korean Windows, 'Sobok' everywhere else (so it can be typed). SOBOK_LANG=ko|en overrides.
$lang = if ($env:SOBOK_LANG) { $env:SOBOK_LANG } elseif ((Get-UICulture).Name -like 'ko*') { 'ko' } else { 'en' }
$name = if ($lang -eq 'ko') { $ko } else { 'Sobok' }
$dir  = Join-Path $env:LOCALAPPDATA 'Sobok'
$exe  = Join-Path $dir 'sobok.exe'
$lnk  = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\$name.lnk"

Write-Host "Installing $name ..."
Get-Process sobok -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Milliseconds 400
New-Item -ItemType Directory -Force $dir | Out-Null

if (Test-Path -LiteralPath $url) { Copy-Item -LiteralPath $url $exe -Force }      # local file (for testing)
else {
  [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
  $ProgressPreference = 'SilentlyContinue'
  Invoke-WebRequest -Uri $url -OutFile $exe -UseBasicParsing
}
if ((Get-Item $exe).Length -lt 500000) { throw 'Download failed (file too small).' }

$sh = New-Object -ComObject WScript.Shell
$s = $sh.CreateShortcut($lnk)
$s.TargetPath = $exe; $s.WorkingDirectory = $dir; $s.IconLocation = "$exe,0"; $s.Save()
# Remove a shortcut left under the other name by an earlier install.
$other = Join-Path $env:APPDATA ("Microsoft\Windows\Start Menu\Programs\" + $(if ($lang -eq 'ko') { 'Sobok' } else { $ko }) + '.lnk')
if (Test-Path -LiteralPath $other) { Remove-Item -LiteralPath $other -Force -ErrorAction SilentlyContinue }

# The app draws with the WebView2 runtime, which Windows 11 already has.
$wv = '{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}'
$has = (Test-Path "HKLM:\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\$wv") -or (Test-Path "HKLM:\SOFTWARE\Microsoft\EdgeUpdate\Clients\$wv") -or (Test-Path "HKCU:\SOFTWARE\Microsoft\EdgeUpdate\Clients\$wv")
if (-not $has) { Write-Host 'WebView2 runtime was not found. Install it from https://developer.microsoft.com/microsoft-edge/webview2/ and start the app again.' -ForegroundColor Yellow }

if (-not $env:SOBOK_NOLAUNCH) { Start-Process $exe }
Write-Host "Done. Start it again any time from the Start Menu: $name" -ForegroundColor Green
