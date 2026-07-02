# Ubuntu Server setup

Ubuntu Server can be simpler than Windows + Docker Desktop + WSL2 because Docker, paths, permissions, SSH, and systemd all live in one Linux environment.

Use this route when the machine can be dedicated to server use.

Use the Windows/WSL route when you want to keep using the PC as a normal Windows machine.

## 1. Prepare folders

Example:

```bash
sudo mkdir -p /srv/family-photo-cloud/{picture,family,photoframe}
sudo chown -R "$USER:$USER" /srv/family-photo-cloud
```

Roles:

```text
/srv/family-photo-cloud/picture
  Original photos. Do not casually delete.

/srv/family-photo-cloud/family
  Photos shared with family.

/srv/family-photo-cloud/photoframe
  Photos safe to show on the room display.
```

## 2. Install Docker and Tailscale

```bash
bash scripts/ubuntu/install-docker-tailscale.sh
```

Log out and log back in if Docker was newly installed.

Join Tailscale:

```bash
sudo tailscale up
tailscale status
```

## 3. Check prerequisites

```bash
PHOTO_ROOT=/srv/family-photo-cloud bash scripts/ubuntu/check-prereqs.sh
```

## 4. Start Nextcloud AIO

Print the command:

```bash
PHOTO_ROOT=/srv/family-photo-cloud bash scripts/ubuntu/nextcloud-aio-run.example.sh
```

Read it, then run the printed `docker run` command manually.

## 5. Open AIO admin

If you have a browser on the Ubuntu machine:

```text
https://127.0.0.1:8080
```

If the machine is headless, use SSH port forwarding:

```bash
ssh -L 8080:127.0.0.1:8080 <user>@<ubuntu-host>
```

Then open this on your local PC:

```text
https://127.0.0.1:8080
```

Save the AIO passphrase in a password manager.

## 6. Serve through Tailscale

```bash
bash scripts/ubuntu/tailscale-serve.sh
```

Use the Tailscale FQDN as the Nextcloud AIO domain:

```text
<machine-name>.<tailnet>.ts.net
```

Do not publish the real FQDN.

## 7. External storage

Map:

```text
/picture     -> /srv/family-photo-cloud/picture
/family      -> /srv/family-photo-cloud/family
/photoframe  -> /srv/family-photo-cloud/photoframe
```

## Why Ubuntu is easier

- No Windows/WSL/Docker Desktop path translation
- Docker runs directly on Linux
- SSH operation is natural
- systemd and logs are easier to inspect
- Raspberry Pi side uses the same Linux mental model

## Tradeoffs

- The PC becomes closer to a dedicated server
- Windows apps are no longer available on that machine
- OS installation and basic Linux administration are required
- Family-shared Windows PC use is less practical
