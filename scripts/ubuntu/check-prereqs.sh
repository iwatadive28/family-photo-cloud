#!/usr/bin/env bash
set -euo pipefail

PHOTO_ROOT="${PHOTO_ROOT:-/srv/family-photo-cloud}"

echo "== OS =="
if [ -f /etc/os-release ]; then
  . /etc/os-release
  echo "${PRETTY_NAME:-unknown}"
fi

echo
echo "== commands =="
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
  echo "Create it with:"
  echo "  sudo mkdir -p $PHOTO_ROOT/{picture,family,photoframe}"
  echo "  sudo chown -R $USER:$USER $PHOTO_ROOT"
fi

echo
echo "== docker =="
if command -v docker >/dev/null 2>&1; then
  docker ps >/dev/null
  echo "ok: docker is usable by current user"
else
  echo "skipped"
fi

echo
echo "== tailscale =="
if command -v tailscale >/dev/null 2>&1; then
  tailscale status || true
else
  echo "skipped"
fi
