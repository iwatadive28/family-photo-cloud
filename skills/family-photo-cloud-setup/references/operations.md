# Operations and Troubleshooting

## Monthly Checks

Windows/WSL:

```powershell
docker ps
tailscale serve status
```

Raspberry Pi:

```bash
tailscale status
tail -n 50 ~/photoframe-rclone.log
df -h
ls -lh ~/Pictures/frame | head
```

## If Photos Do Not Show

Check in layers:

1. Source folder contains photos
2. Nextcloud external storage shows `photoframe`
3. Tailscale URL opens from the Pi
4. `rclone lsd nextcloud:` works
5. `~/Pictures/frame` contains files
6. `DISPLAY=:0 ~/bin/start-photoframe.sh` starts `feh`
7. Screen lock / screensaver / DPMS are disabled

## Backup Warning

Nextcloud is not backup. It is the sharing and viewing layer.

Keep original photos separately backed up on another HDD, NAS, or cloud storage.

## Public Documentation Hygiene

Before publishing:

- Replace tailnet FQDNs with `<machine-name>.<tailnet>.ts.net`
- Replace users with `<user>` or `<nextcloud-user>`
- Remove screenshots that include family names, child photos, address, school, hospital, car plate, delivery labels, or notifications
- Avoid committing `.env`, `rclone.conf`, passwords, app passwords, and real logs
