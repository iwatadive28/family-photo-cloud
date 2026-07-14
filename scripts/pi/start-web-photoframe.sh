#!/usr/bin/env bash
set -euo pipefail

PHOTO_FRAME_URL="${PHOTO_FRAME_URL:-https://your-server.example.ts.net/photo-frame?lite=1}"
export DISPLAY="${DISPLAY:-:0}"
export XAUTHORITY="${XAUTHORITY:-$HOME/.Xauthority}"

if [ -z "${DBUS_SESSION_BUS_ADDRESS:-}" ] && [ -S "/run/user/$(id -u)/bus" ]; then
  export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus"
fi

xset s off || true
xset -dpms || true
xset s noblank || true
unclutter -idle 0.5 -root >/tmp/photo-frame-unclutter.log 2>&1 &

if command -v chromium-browser >/dev/null 2>&1; then
  exec chromium-browser \
    --kiosk \
    --noerrdialogs \
    --disable-infobars \
    --disable-session-crashed-bubble \
    --overscroll-history-navigation=0 \
    "$PHOTO_FRAME_URL"
fi

exec firefox --kiosk "$PHOTO_FRAME_URL"

