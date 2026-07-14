# Webアプリ版フォトフレーム setup

この手順では、NextcloudサーバーPC側で写真フォルダをWebアプリとして配信し、Raspberry Piやスマホのブラウザから表示します。

初版の `rclone + feh` 方式では、Raspberry Piへ写真をコピーしてローカル表示します。Webアプリ版では、Raspberry Piはブラウザ表示専用端末になり、写真の読み込み・縮小配信はサーバーPC側で行います。

## 構成

```text
Nextcloud / 写真HDDのあるPC
  └─ photo-frame-web
       ├─ /photo-frame
       ├─ /photo-frame/api/photos
       └─ /photo-frame/photos-lite/...

Raspberry Pi
  └─ Firefox / Chromium kiosk

スマホ / PC
  └─ 同じURLをブラウザで開く
```

## 1. アプリを起動する

```bash
cd family-photo-cloud/apps/photo-frame-web
cp ../../examples/photo-frame-web.env.example .env
```

`.env` の `PHOTO_FRAME_DIR` を自分の写真フォルダに変更します。

```bash
PHOTO_FRAME_DIR=/mnt/photos/photoframe
BASE_PATH=/photo-frame
LITE_IMAGE_MAX_EDGE=1280
LITE_IMAGE_QUALITY=82
```

起動します。

```bash
uv run uvicorn photo_frame_web.main:app --host 0.0.0.0 --port 8092
```

確認します。

```bash
curl http://127.0.0.1:8092/photo-frame/api/photos
```

## 2. Tailscale Serveで公開する

tailnet内だけで見られるようにします。

```bash
tailscale serve --bg --set-path /photo-frame http://127.0.0.1:8092/photo-frame
tailscale serve status
```

表示URLは環境に合わせて変わります。

```text
https://<your-machine>.<your-tailnet>.ts.net/photo-frame
```

Raspberry Piでは軽量表示を使います。

```text
https://<your-machine>.<your-tailnet>.ts.net/photo-frame?lite=1
```

## 3. なぜlite表示を使うか

スマホ写真は1枚数MBになることがあります。そのままRaspberry Piの7インチ画面で表示すると、通信、画像デコード、描画が重くなります。

`?lite=1` では、写真URLとして `/photos-lite/...` を使います。サーバー側で長辺1280px程度に縮小したJPEGを返すため、Raspberry Pi側の負荷を下げられます。

## 4. feh方式との違い

| 方式 | 写真の置き場所 | Piの役割 | 長所 | 注意 |
|---|---|---|---|---|
| rclone + feh | Piローカル | 写真同期と表示 | ネットワーク不調でも表示しやすい | rclone設定とローカル容量が必要 |
| Webアプリ版 | サーバーPC | ブラウザ表示 | Piが軽い。スマホでも同じURLを見られる | サーバーPCとネットワークに依存 |

## 5. 注意

- このWebアプリは家庭内/tailnet内利用を想定しています。
- 写真をインターネットへ直接公開しないでください。
- Nextcloudで見える状態はバックアップではありません。元写真は別途バックアップしてください。

