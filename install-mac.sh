#!/bin/bash
# Sobok installer for macOS.  Usage:  curl -fsSL <url-of-this-file> | bash
set -e
URL="${SOBOK_URL:-https://github.com/lovejoohero0228/sobok-release/releases/latest/download/sobok-mac.zip}"
DEST="$HOME/Applications"
TMP="$(mktemp -d)"
echo "Installing Sobok ..."
pkill -x sobok 2>/dev/null || true
curl -fsSL "$URL" -o "$TMP/sobok-mac.zip"
mkdir -p "$DEST"
ditto -x -k "$TMP/sobok-mac.zip" "$TMP/out"
APP="$(ls -d "$TMP/out"/*.app | head -1)"
NAME="$(basename "$APP")"
if [ -d "$DEST/$NAME" ]; then rm -rf "$DEST/$NAME"; fi
mv "$APP" "$DEST/$NAME"
xattr -dr com.apple.quarantine "$DEST/$NAME" 2>/dev/null || true
open "$DEST/$NAME"
echo "Done. It lives in ~/Applications. Quit from the menu bar icon."
