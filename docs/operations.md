# Operations

## Monthly checks

Windows / WSL:

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

## Backup reminder

Nextcloud visibility is not backup.

Keep original photos in a separate backup location such as another HDD, NAS, or cloud storage.

## Display-safe photo rule

Only put photos into `photoframe` when they are safe to show in the room:

- Family members are okay with them being displayed
- Visitors seeing them is not a problem
- No address, school, hospital, license plate, delivery label, or private screen notification is visible
- When unsure, do not add the photo
