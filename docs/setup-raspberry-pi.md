# Raspberry Pi setup

このページは、Raspberry Piへ写真を同期して `feh` でローカル表示する基本編です。

サーバーPCからWebアプリとして配信し、Raspberry Piをブラウザ表示専用端末にする発展編は、次のページを使います。

- `docs/setup-web-photo-frame.md`
- `docs/setup-raspberry-pi-kiosk-web.md`

## 1. Install helpers

```bash
cd family-photo-cloud
bash scripts/pi/install-photoframe.sh
```

## 2. Join Tailscale

```bash
sudo tailscale up
tailscale status
```

Confirm the Windows/Nextcloud machine is visible.

## 3. Configure rclone

Create a Nextcloud app password, then:

```bash
rclone config
```

Use `examples/rclone-nextcloud.example.txt` as a guide.

## 4. Dry-run sync

```bash
~/bin/sync-photoframe.sh --dry-run
```

If the source and destination look right:

```bash
~/bin/sync-photoframe.sh
```

## 5. Test slideshow

```bash
DISPLAY=:0 ~/bin/start-photoframe.sh
```

## 6. Cron example

```cron
*/10 * * * * /home/pi/bin/sync-photoframe.sh
```

Use `copy` first. Do not switch to `sync` until you are sure deletion is safe.
