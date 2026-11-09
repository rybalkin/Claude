#!/usr/bin/env bash
# Replaces Capacitor's default launcher icon with the app's own icon.
# Run from android-test-app/ after `npx cap add android`.
set -euo pipefail
RES=android/app/src/main/res
rm -rf "$RES/mipmap-anydpi-v26"   # drop the adaptive icon so the PNGs below are used
for dir in "$RES"/mipmap-*dpi; do
  cp www/icons/icon-192.png "$dir/ic_launcher.png"
  cp www/icons/icon-192.png "$dir/ic_launcher_round.png"
done
echo "Launcher icon replaced."
