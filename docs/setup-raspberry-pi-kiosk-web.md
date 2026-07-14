# Raspberry Pi kiosk setup for Web Photo Frame

Raspberry Piをブラウザ表示専用端末として使う手順です。

## 1. SSHで入れるようにする

```bash
ssh-copy-id <user>@<raspberry-pi-ip>
ssh <user>@<raspberry-pi-ip>
```

状況を確認します。

```bash
hostname
hostname -I
cat /etc/os-release
systemctl get-default
command -v chromium-browser || command -v firefox
```

## 2. ブラウザを用意する

Chromiumが使えるならChromiumを優先します。

```bash
sudo apt update
sudo apt install -y chromium-browser unclutter x11-xserver-utils
```

Chromiumが使えない環境ではFirefoxでも動きます。

```bash
sudo apt install -y firefox unclutter x11-xserver-utils
```

## 3. 起動スクリプトを置く

```bash
mkdir -p ~/bin
install -m 0755 scripts/pi/start-web-photoframe.sh ~/bin/start-web-photoframe.sh
```

自分のURLに変更します。

```bash
PHOTO_FRAME_URL='https://<your-machine>.<your-tailnet>.ts.net/photo-frame?lite=1'
```

## 4. 自動起動にする

```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/web-photoframe.desktop <<EOF
[Desktop Entry]
Type=Application
Name=Web Photo Frame
Exec=$HOME/bin/start-web-photoframe.sh
Terminal=false
X-GNOME-Autostart-enabled=true
EOF
```

## 5. 画面スリープを止める

X11環境では起動スクリプト内で以下を実行します。

```bash
xset s off
xset -dpms
xset s noblank
```

デスクトップ環境によっては、スクリーンセーバーや画面ロックも別途無効化してください。

## 6. テスト

```bash
DISPLAY=:0 ~/bin/start-web-photoframe.sh
```

再起動後、自動でフォトフレーム画面が出ることを確認します。

