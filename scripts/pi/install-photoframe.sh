#!/usr/bin/env bash
set -euo pipefail

FRAME_DIR="${FRAME_DIR:-$HOME/Pictures/frame}"
BIN_DIR="${BIN_DIR:-$HOME/bin}"

sudo apt update
sudo apt install -y rclone feh unclutter

mkdir -p "$FRAME_DIR" "$BIN_DIR" "$HOME/.config/autostart"

install -m 0755 "$(dirname "$0")/start-photoframe.sh" "$BIN_DIR/start-photoframe.sh"
install -m 0755 "$(dirname "$0")/sync-photoframe.sh" "$BIN_DIR/sync-photoframe.sh"

cat > "$HOME/.config/autostart/photoframe.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Photoframe
Exec=$BIN_DIR/start-photoframe.sh
X-GNOME-Autostart-enabled=true
EOF

echo "Installed photoframe helpers."
echo "Next:"
echo "  1. Join Tailscale: sudo tailscale up"
echo "  2. Configure rclone: rclone config"
echo "  3. Test sync: $BIN_DIR/sync-photoframe.sh --dry-run"
echo "  4. Test display: DISPLAY=:0 $BIN_DIR/start-photoframe.sh"
