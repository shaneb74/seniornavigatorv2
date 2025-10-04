#!/usr/bin/env bash
set -euo pipefail

# Detect default branch
BASE_BRANCH="$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@')"
if [[ -z "${BASE_BRANCH:-}" ]]; then
  BASE_BRANCH="Development"
fi

echo "→ Using base branch: $BASE_BRANCH"

git fetch --prune

# Switch to base branch
if git switch "$BASE_BRANCH" 2>/dev/null || git checkout "$BASE_BRANCH"; then
  git pull origin "$BASE_BRANCH" || true
else
  echo "⚠️ Could not switch to $BASE_BRANCH. Make sure it exists."
fi

branches=(
  "codex/redesign-streamlit-app-visuals-4e1qoe"
  "codex/redesign-streamlit-app-visuals-1nm6nm"
  "codex/redesign-streamlit-app-visuals-us5sv2"
  "codex/redesign-streamlit-app-visuals-z0yb74"
  "codex/redesign-streamlit-app-visuals-t6ccxk"
)

delete_local_if_exists () {
  local b="$1"
  if git rev-parse --verify --quiet "refs/heads/$b" >/dev/null; then
    echo "🧹 Deleting LOCAL branch: $b"
    git branch -D "$b"
  else
    echo "✓ Local branch not present: $b"
  fi
}

delete_remote_if_exists () {
  local b="$1"
  if git ls-remote --exit-code --heads origin "$b" >/dev/null 2>&1; then
    echo "🧼 Deleting REMOTE branch: $b"
    git push origin --delete "$b"
  else
    echo "✓ Remote branch not present: $b"
  fi
}

for branch in "${branches[@]}"; do
  delete_local_if_exists  "$branch"
  delete_remote_if_exists "$branch"
done

echo "✅ Cleanup complete."
