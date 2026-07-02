# Ubuntu Server / Nextcloud AIO

Use this when the user can dedicate a PC as an Ubuntu Server.

Ubuntu is simpler than Windows + Docker Desktop + WSL2 because Docker, paths, permissions, SSH, logs, and systemd all live in one Linux environment.

## Assumptions

- Ubuntu Server
- Tailscale installed or installable
- Docker installed or installable
- Photo root such as `/srv/family-photo-cloud`
- Folders: `picture`, `family`, `photoframe`

## Folder setup

```bash
sudo mkdir -p /srv/family-photo-cloud/{picture,family,photoframe}
sudo chown -R "$USER:$USER" /srv/family-photo-cloud
```

## Install Docker and Tailscale

Prefer the public repo script when available:

```bash
bash books/family-photo-cloud/public-repo/scripts/ubuntu/install-docker-tailscale.sh
```

Then:

```bash
sudo tailscale up
tailscale status
```

## Checks

```bash
PHOTO_ROOT=/srv/family-photo-cloud bash books/family-photo-cloud/public-repo/scripts/ubuntu/check-prereqs.sh
```

## Nextcloud AIO

Print the suggested command:

```bash
PHOTO_ROOT=/srv/family-photo-cloud bash books/family-photo-cloud/public-repo/scripts/ubuntu/nextcloud-aio-run.example.sh
```

The important values are:

```text
APACHE_PORT=11000
APACHE_IP_BINDING=127.0.0.1
NEXTCLOUD_MOUNT=/srv/family-photo-cloud
```

Open AIO locally:

```text
https://127.0.0.1:8080
```

For a headless server, use SSH forwarding:

```bash
ssh -L 8080:127.0.0.1:8080 <user>@<ubuntu-host>
```

## Tailscale Serve

```bash
bash books/family-photo-cloud/public-repo/scripts/ubuntu/tailscale-serve.sh
```

Use the Tailscale FQDN as the AIO domain:

```text
<machine-name>.<tailnet>.ts.net
```

Never publish the real FQDN.

## External Storage

Map:

```text
/picture     -> /srv/family-photo-cloud/picture
/family      -> /srv/family-photo-cloud/family
/photoframe  -> /srv/family-photo-cloud/photoframe
```

## Tradeoff to explain

Ubuntu is cleaner for a server, but less convenient if the same PC must remain a family Windows PC.
