#!/bin/bash
# Sobok uninstaller for macOS.  Usage:  curl -fsSL <url-of-this-file> | bash
pkill -x sobok 2>/dev/null || true
sleep 1
for APP in "$HOME/Applications"/*.app; do
  if [ -x "$APP/Contents/MacOS/sobok" ]; then rm -rf "$APP"; fi
done
rm -rf "$HOME/Library/Application Support/com.sobok.widget" "$HOME/Library/Caches/com.sobok.widget" "$HOME/Library/WebKit/com.sobok.widget"
echo "Sobok was removed."
