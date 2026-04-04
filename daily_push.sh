#!/bin/bash
# Daily GitHub streak push script
# Runs at 11:30 PM IST via cron: 30 23 * * *

REPO="/Users/avik17/PythonProjects/FastApi"
LOG_DIR="$REPO/learning-log"
DATE=$(TZ='Asia/Calcutta' date +%Y-%m-%d)
LOG_FILE="$LOG_DIR/$DATE.md"

cd "$REPO" || exit 1

# If there are uncommitted local changes, commit them first
if ! git diff --quiet || ! git diff --cached --quiet; then
  git add -A
  git commit -m "chore: daily progress $DATE"
fi

# Ensure a learning-log entry exists for today (guarantees streak even on no-code days)
if [ ! -f "$LOG_FILE" ]; then
  mkdir -p "$LOG_DIR"
  cat > "$LOG_FILE" <<EOF
# Learning Log — $DATE

Daily streak entry — FastAPI / Python / AI Engineering track.
EOF
  git add "$LOG_FILE"
  git commit -m "chore: daily learning log $DATE"
fi

# Push everything
git push
