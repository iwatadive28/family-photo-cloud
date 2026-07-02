# Raspberry Pi Photoframe

Use this when helping set up the Raspberry Pi display side.

## Assumptions

- Raspberry Pi with GUI session
- Tailscale can join the same tailnet
- `rclone`, `feh`, and `unclutter` are used
- Local frame folder: `~/Pictures/frame`

## Install

```bash
bash books/family-photo-cloud/public-repo/scripts/pi/install-photoframe.sh
```

If the repo is cloned on the Pi, run from the cloned repo root.

## Tailscale

```bash
sudo tailscale up
tailscale status
```

Confirm the Nextcloud machine is visible.

## rclone

Use a Nextcloud app password, not the normal login password.

Remote URL:

```text
https://<machine-name>.<tailnet>.ts.net/remote.php/dav/files/<nextcloud-user>/
```

Initial test:

```bash
rclone lsd nextcloud:
~/bin/sync-photoframe.sh --dry-run
```

If correct:

```bash
~/bin/sync-photoframe.sh
```

## Slideshow

```bash
DISPLAY=:0 ~/bin/start-photoframe.sh
```

Autostart file:

```text
~/.config/autostart/photoframe.desktop
```

## Cron

```cron
*/10 * * * * /home/pi/bin/sync-photoframe.sh
```

Use `copy`, not `sync`, until deletion behavior is intentionally accepted.
