#!/usr/bin/env bash
set -euo pipefail

echo "This exposes local Nextcloud only inside your tailnet:"
echo "  tailscale serve --bg --https=443 http://127.0.0.1:11000"
echo

tailscale serve --bg --https=443 http://127.0.0.1:11000
tailscale serve status
