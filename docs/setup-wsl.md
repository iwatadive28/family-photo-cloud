# Windows / WSL setup

## 1. Decide folders

Example:

```text
D:\home
  picture
  family
  photoframe
```

From WSL/Docker Desktop, this may appear as:

```text
/mnt/d/home
```

## 2. Check prerequisites

```bash
cd family-photo-cloud-kit
PHOTO_ROOT=/mnt/d/home bash scripts/wsl/check-prereqs.sh
```

## 3. Start Nextcloud AIO

Print the docker command:

```bash
PHOTO_ROOT=/mnt/d/home bash scripts/wsl/nextcloud-aio-run.example.sh
```

Read the command, then run it manually.

## 4. Configure Tailscale Serve

In PowerShell:

```powershell
tailscale serve --bg --https=443 http://127.0.0.1:11000
tailscale serve status
```

Use the Tailscale FQDN as the Nextcloud domain in AIO.

## 5. Add external storage

In Nextcloud, enable External storage support and map:

```text
/picture     -> /mnt/d/home/picture
/family      -> /mnt/d/home/family
/photoframe  -> /mnt/d/home/photoframe
```

Do not publish real tailnet names, IP addresses, user names, or passwords.
