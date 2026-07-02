#!/usr/bin/env bash
set -euo pipefail

REMOTE="${REMOTE:-nextcloud:photoframe}"
FRAME_DIR="${FRAME_DIR:-$HOME/Pictures/frame}"
LOG_FILE="${LOG_FILE:-$HOME/photoframe-rclone.log}"

mkdir -p "$FRAME_DIR"

if [ "${1:-}" = "--dry-run" ]; then
  exec rclone copy "$REMOTE" "$FRAME_DIR" --dry-run --log-file="$LOG_FILE" --log-level INFO
fi

exec rclone copy "$REMOTE" "$FRAME_DIR" --log-file="$LOG_FILE" --log-level INFO
