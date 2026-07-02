---
name: family-photo-cloud-setup
description: Guide Codex through setting up a private family photo cloud and Raspberry Pi photoframe using Windows/WSL, Docker Desktop, Nextcloud AIO, Tailscale, rclone, and feh. Use when the user asks to build, troubleshoot, document, or simplify the BOOTH book's family-photo-cloud setup, including creating commands, checking prerequisites, configuring Raspberry Pi slideshow operation, or turning the public repository template into a working local setup.
---

# Family Photo Cloud Setup

Use this skill to help a reader reproduce the family photo cloud from the BOOTH book without exposing private data.

## Rules

- Do not ask for secrets unless the task cannot proceed without them.
- Never include real tailnet names, IP addresses, passwords, app passwords, family names, or child photos in public files.
- Treat Nextcloud visibility as sharing, not backup.
- Prefer `rclone copy --dry-run` before any real transfer.
- Do not suggest `rclone sync` until the user explicitly accepts deletion semantics.
- Keep commands environment-variable based or placeholder based.

## Workflow

1. Identify the user's target:
   - Windows/WSL + Nextcloud AIO setup
   - Ubuntu Server + Nextcloud AIO setup
   - Raspberry Pi photoframe setup
   - rclone/WebDAV setup
   - operations/troubleshooting
   - public repo or documentation updates

2. Load only the needed reference:
   - For Windows/WSL: read `references/wsl-nextcloud.md`
   - For Ubuntu Server: read `references/ubuntu-server.md`
   - For Raspberry Pi: read `references/raspberry-pi.md`
   - For troubleshooting/operations: read `references/operations.md`

3. Produce a short checklist first, then commands.

4. Use the public repo template when available:
   - `books/family-photo-cloud/public-repo/`
   - Prefer adapting those scripts instead of inventing new ones.

5. End with validation commands and rollback notes.

## Expected Output Shape

For setup guidance, respond with:

- Assumptions
- Files or commands to run
- What success looks like
- What to check if it fails
- Privacy/backups warning when photos or credentials are involved

For editing the repo/book, update the relevant files and regenerate artifacts when needed.
