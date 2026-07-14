#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-$HOME/family-photo-cloud/apps/photo-frame-web}"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8092}"

cd "$APP_DIR"
exec uv run uvicorn photo_frame_web.main:app --host "$HOST" --port "$PORT"

