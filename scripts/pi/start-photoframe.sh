#!/usr/bin/env bash
set -euo pipefail

FRAME_DIR="${FRAME_DIR:-$HOME/Pictures/frame}"
DELAY="${SLIDESHOW_DELAY:-20}"

xset s off || true
xset -dpms || true
xset s noblank || true
unclutter -idle 0.5 -root &

exec feh --fullscreen --hide-pointer --slideshow-delay "$DELAY" --randomize --auto-zoom "$FRAME_DIR"
