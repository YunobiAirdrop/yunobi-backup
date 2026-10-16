#!/bin/bash
# Hourly auto-backup: sync projects -> commit if changed -> push
set -euo pipefail

BACKUP_DIR="$HOME/workspace/backup-yunobi-backup"
cd "$BACKUP_DIR"

# Sync projects (exclude media and sensitive files)
for proj in youtube-otomatis Yunobi_project_backup yunobi-dashboard yunobi-apk custom-skills your_files; do
  if [ -d "$HOME/workspace/$proj" ]; then
    rsync -a --delete \
      --exclude='.git/' --exclude='__pycache__/' --exclude='*.pyc' \
      --exclude='.env' --exclude='*secret*' --exclude='*token*' \
      --exclude='*.key' --exclude='*.pem' --exclude='node_modules/' \
      --exclude='*.mp4' --exclude='*.wav' --exclude='*.mp3' \
      "$HOME/workspace/$proj/" "./$proj/"
  fi
done

# Check for changes
if [ -z "$(git status --porcelain)" ]; then
  exit 0  # No changes, stay silent
fi

# Commit and push
git add -A
CHANGED=$(git diff --cached --stat | tail -1)
git commit -qm "auto-backup: $(TZ=Asia/Jakarta date '+%Y-%m-%d %H:%M WIB') — $CHANGED"
git push -q origin main 2>&1 | tail -3
