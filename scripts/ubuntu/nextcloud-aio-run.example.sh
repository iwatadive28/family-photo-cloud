#!/usr/bin/env bash
set -euo pipefail

PHOTO_ROOT="${PHOTO_ROOT:-/srv/family-photo-cloud}"

cat <<EOF
This script prints the Ubuntu Server Nextcloud AIO docker run command.
Review it before running. It does not execute docker automatically.

docker run --init --sig-proxy=false \\
  --name nextcloud-aio-mastercontainer \\
  --restart always \\
  --publish 8080:8080 \\
  --env APACHE_PORT=11000 \\
  --env APACHE_IP_BINDING=127.0.0.1 \\
  --env NEXTCLOUD_MOUNT=$PHOTO_ROOT \\
  --volume nextcloud_aio_mastercontainer:/mnt/docker-aio-config \\
  --volume /var/run/docker.sock:/var/run/docker.sock:ro \\
  ghcr.io/nextcloud-releases/all-in-one:latest

After startup:
  1. Open https://127.0.0.1:8080 from the Ubuntu machine,
     or use SSH port forwarding:
       ssh -L 8080:127.0.0.1:8080 <user>@<ubuntu-host>
       then open https://127.0.0.1:8080 locally.
  2. Save the AIO passphrase in a password manager.
  3. Set the domain to your Tailscale FQDN.
EOF
