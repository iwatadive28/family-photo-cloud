# Windows / WSL / Nextcloud AIO

Use this when helping set up the Windows/WSL side.

## Assumptions

- Windows 11
- Docker Desktop with WSL2 backend
- Tailscale installed
- Photo root such as `D:\home`, visible from WSL as `/mnt/d/home`
- Folders: `picture`, `family`, `photoframe`

## Checks

```bash
PHOTO_ROOT=/mnt/d/home bash books/family-photo-cloud/public-repo/scripts/wsl/check-prereqs.sh
```

If Docker cannot see the photo root:

```bash
docker run --rm -v /mnt/d/home:/test:ro alpine:latest ls -la /test
```

Try `/mnt/<drive>/home` before `/run/desktop/mnt/host/...` on this project.

## Nextcloud AIO

Print the suggested command:

```bash
PHOTO_ROOT=/mnt/d/home bash books/family-photo-cloud/public-repo/scripts/wsl/nextcloud-aio-run.example.sh
```

The command should bind Nextcloud Apache to localhost:

```text
APACHE_PORT=11000
APACHE_IP_BINDING=127.0.0.1
NEXTCLOUD_MOUNT=/mnt/d/home
```

Open:

```text
https://127.0.0.1:8080
```

Save the AIO passphrase in a password manager.

## Tailscale Serve

In PowerShell:

```powershell
tailscale serve --bg --https=443 http://127.0.0.1:11000
tailscale serve status
```

Use the Tailscale FQDN as the AIO domain:

```text
<machine-name>.<tailnet>.ts.net
```

Never publish the real FQDN in public docs.

## External Storage

Map:

```text
/picture     -> /mnt/d/home/picture
/family      -> /mnt/d/home/family
/photoframe  -> /mnt/d/home/photoframe
```

Explain that Nextcloud's external storage "restrict to users" setting controls who sees the storage.
