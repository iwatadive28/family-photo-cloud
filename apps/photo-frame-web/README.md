# photo-frame-web

NextcloudサーバーPC上の写真フォルダを、Raspberry Piやスマホのブラウザに配信する最小Webフォトフレームです。

このサンプルはBOOTH本の発展編用です。カメラ連携、RTSP、録画、人物検出などは含めません。

## できること

- 写真フォルダを再帰的に読み取る
- `/photo-frame/api/photos` で写真一覧を返す
- `/photo-frame/photos/...` で元画像を返す
- `/photo-frame/photos-lite/...` で長辺1280px程度の軽量JPEGを返す
- Raspberry Pi kiosk表示向けに `?lite=1` を用意する
- スマホ/PCからも同じURLで見られる

## 起動

```bash
cd apps/photo-frame-web
uv run uvicorn photo_frame_web.main:app --host 0.0.0.0 --port 8092
```

環境変数:

```bash
PHOTO_FRAME_DIR=/path/to/photoframe
BASE_PATH=/photo-frame
LITE_IMAGE_MAX_EDGE=1280
LITE_IMAGE_QUALITY=82
```

## 表示URL

```text
http://127.0.0.1:8092/photo-frame
http://127.0.0.1:8092/photo-frame?lite=1
```

Tailscale Serveを使う場合は、tailnet内だけでHTTPS公開します。

