# family-photo-cloud

Nextcloud AIO、Tailscale、Raspberry Piで家族写真クラウド兼フォトフレームを作るための公開用テンプレートです。

このリポジトリは、BOOTH本「家族写真を、自宅クラウドとフォトフレームで見返す本」の付録として使う想定です。認証情報、tailnet名、家族名、実IPアドレスは含めません。

## できること

- Windows 11 + Docker Desktop + WSL2でNextcloud AIOを立てる準備を確認する
- Ubuntu ServerでNextcloud AIOをより素直に立てる準備を確認する
- Tailscale ServeでNextcloudをtailnet内だけに公開する
- Raspberry PiでTailscale、rclone、fehを使うフォトフレーム環境を作る
- 発展編として、写真フォルダをWebアプリ化し、Raspberry Piをブラウザ表示専用端末にする
- 同じフォトフレーム画面をスマホやPCのブラウザからも見る
- rcloneは初回 `copy --dry-run` を優先し、削除事故を避ける

## ディレクトリ

```text
scripts/wsl/
  check-prereqs.sh
  nextcloud-aio-run.example.sh
  tailscale-serve.example.ps1

scripts/ubuntu/
  check-prereqs.sh
  install-docker-tailscale.sh
  nextcloud-aio-run.example.sh
  tailscale-serve.sh

scripts/pi/
  install-photoframe.sh
  start-photoframe.sh
  start-web-photoframe.sh
  sync-photoframe.sh

apps/photo-frame-web/
  FastAPIによるWebアプリ版フォトフレーム

assets/figures/
  photo-scattered-folders.png
  prep-checklist.png
  operation-rules-table.png
  backup-flow.png

examples/
  env.example
  photo-frame-web.env.example
  rclone-nextcloud.example.txt

docs/
  setup-wsl.md
  setup-ubuntu-server.md
  setup-raspberry-pi.md
  setup-web-photo-frame.md
  setup-raspberry-pi-kiosk-web.md
  operations.md

demo/
  Webアプリ版フォトフレームの静的サンプル

skills/
  family-photo-cloud-setup/
```

## 使い方

1. `examples/env.example` を参考に、自分の環境値を決めます。
2. Windows PCをそのまま使うなら `docs/setup-wsl.md` を読みます。
3. Ubuntu Serverとして使うなら `docs/setup-ubuntu-server.md` を読みます。
4. Raspberry Pi側は `docs/setup-raspberry-pi.md` を読みます。
5. Webアプリ版フォトフレームを使うなら `docs/setup-web-photo-frame.md` と `docs/setup-raspberry-pi-kiosk-web.md` を読みます。
6. 運用開始後は `docs/operations.md` の月1チェックを使います。

## Windows/WSLとUbuntuの使い分け

家に余っているWindows PCをそのまま活かしたいなら、Windows/WSLルートが現実的です。

サーバー専用機として割り切れるなら、Ubuntu Serverルートの方がシンプルです。Docker、パス、権限、SSH、ログ確認がすべてLinux内で完結します。

## AIスキル

`skills/family-photo-cloud-setup/` に、Codex/ChatGPT向けのセットアップ支援スキルを同梱しています。

使うときの依頼例:

```text
$family-photo-cloud-setup を使って、Windows 11 + Docker Desktop + TailscaleでNextcloud AIOを立てる手順を確認して。
```

```text
$family-photo-cloud-setup を使って、Raspberry Piをフォトフレーム化するためのチェックリストとコマンドを出して。
```

## Webアプリ版フォトフレーム

初版の `rclone + feh` 構成は、Raspberry Piへ写真をコピーしてローカル表示します。

発展編のWebアプリ版では、NextcloudサーバーPC側で写真一覧と軽量画像を配信し、Raspberry Piはブラウザのkiosk表示だけを担当します。Pi側のローカル同期や写真保存容量を減らせるうえ、同じURLをスマホやPCからも開けます。

サンプル:

```text
demo/index.html
```

実アプリ:

```text
apps/photo-frame-web/
```

## 注意

- このテンプレートはバックアップ完成形ではありません。
- Nextcloudで見える状態はバックアップではありません。
- 元写真は別HDD、NAS、クラウドなどに別途バックアップしてください。
- `rclone sync` は削除を伴います。初回は必ず `copy --dry-run` から始めてください。

## ライセンス

この公開テンプレートはMIT Licenseで公開します。スクリプト、設定例、ドキュメント、同梱スキルは自由に利用、変更、再配布できます。

BOOTH本のPDF本文や販売物そのものは、このリポジトリには含めません。
