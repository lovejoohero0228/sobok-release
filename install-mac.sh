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
# App name: Korean on a Korean Mac, "Sobok" everywhere else (so it can be typed in Spotlight). SOBOK_LANG=ko|en overrides.
UILANG="${SOBOK_LANG:-$(defaults read -g AppleLanguages 2>/dev/null | sed -n '2p' | tr -d ' ",')}"
case "$UILANG" in ko*) ;; *) NAME="Sobok.app" ;; esac
# Remove any earlier copy, whichever name it was installed under.
for OLD in "$DEST"/*.app; do
  if [ -x "$OLD/Contents/MacOS/sobok" ]; then rm -rf "$OLD"; fi
done
mv "$APP" "$DEST/$NAME"
xattr -dr com.apple.quarantine "$DEST/$NAME" 2>/dev/null || true
open "$DEST/$NAME"
echo "Done. It lives in ~/Applications. Quit from the menu bar icon."
