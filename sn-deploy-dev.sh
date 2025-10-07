#!/usr/bin/env bash
set -Eeuo pipefail

BRANCH="Development"
MSG="${1:-chore: sync local changes}"
PY_DIRS=("app_pages" "ui")

echo "▶️  Ensuring on $BRANCH…"
git switch "$BRANCH"
git pull --ff-only

echo "🧪 Running verify…"
./sn-verify.sh

echo "➕ Staging, committing, pushing…"
git add -A
if ! git diff --cached --quiet; then
  git commit -m "$MSG"
else
  echo "ℹ️ No changes to commit."
fi
git push origin HEAD

echo "✅ Pushed to $BRANCH. If Streamlit Cloud tracks this branch, it will redeploy automatically."
