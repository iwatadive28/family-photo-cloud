$ErrorActionPreference = "Stop"

if (-not $env:NEXTCLOUD_FQDN) {
  Write-Host "Set NEXTCLOUD_FQDN first, for example:"
  Write-Host '$env:NEXTCLOUD_FQDN="your-machine.your-tailnet.ts.net"'
}

Write-Host "This command exposes local Nextcloud only inside your tailnet:"
Write-Host "tailscale serve --bg --https=443 http://127.0.0.1:11000"
Write-Host ""
Write-Host "Run:"
Write-Host "tailscale serve --bg --https=443 http://127.0.0.1:11000"
Write-Host "tailscale serve status"
