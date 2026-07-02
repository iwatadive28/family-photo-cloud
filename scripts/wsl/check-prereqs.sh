#!/usr/bin/env bash
set -euo pipefail

PHOTO_ROOT="${PHOTO_ROOT:-/mnt/d/home}"

echo "== basic commands =="
for cmd in docker tailscale; do
  if command -v "$cmd" >/dev/null 2>&1; then
    echo "ok: $cmd"
  else
    echo "missing: $cmd"
  fi
done

echo
echo "== photo root =="
if [ -d "$PHOTO_ROOT" ]; then
  echo "ok: $PHOTO_ROOT exists"
  ls -la "$PHOTO_ROOT" | sed -n '1,20p'
else
  echo "missing: $PHOTO_ROOT"
  echo "Set PHOTO_ROOT=/mnt/<drive>/home or create the folder first."
fi

echo
echo "== docker mount test =="
if command -v docker >/dev/null 2>&1 && [ -d "$PHOTO_ROOT" ]; then
  docker run --rm -v "$PHOTO_ROOT:/test:ro" alpine:latest ls -la /test | sed -n '1,20p'
else
  echo "skipped"
fi

echo
echo "== tailscale status =="
if command -v tailscale >/dev/null 2>&1; then
  tailscale status || true
else
  echo "skipped"
fi
