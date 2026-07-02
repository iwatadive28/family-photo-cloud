#!/usr/bin/env bash
set -euo pipefail

sudo apt update
sudo apt install -y ca-certificates curl gnupg lsb-release

if ! command -v docker >/dev/null 2>&1; then
  curl -fsSL https://get.docker.com | sh
  sudo usermod -aG docker "$USER"
  echo "Docker installed. Log out and log back in so group membership is applied."
else
  echo "Docker already installed."
fi

if ! command -v tailscale >/dev/null 2>&1; then
  curl -fsSL https://tailscale.com/install.sh | sh
else
  echo "Tailscale already installed."
fi

echo "Next:"
echo "  sudo tailscale up"
echo "  PHOTO_ROOT=/srv/family-photo-cloud bash scripts/ubuntu/check-prereqs.sh"
