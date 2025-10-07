#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

BRANCH="feat/gcp-behavior-risks-and-ux"
BASE="Development"
MSG="feat(gcp): behavior-risks multi-select, scoring, rec summary + primary button theming"

echo "🔍 Checking repo status..."
git rev-parse --show-toplevel >/dev/null || { echo "✖ Not a git repo"; exit 1; }
git fetch --all --tags

echo "📦 Switching to base branch: $BASE"
git checkout "$BASE"
git pull --rebase origin "$BASE"

echo "🧪 Quick compile check..."
python3 -m compileall . || { echo "✖ compileall failed"; exit 1; }

echo "🌿 Creating or updating feature branch: $BRANCH"
if git show-ref --quiet refs/heads/"$BRANCH"; then
  git switch "$BRANCH"
  git rebase "$BASE"
else
  git switch -c "$BRANCH"
fi

echo "💾 Staging and committing changes..."
git add -A
git commit -m "$MSG" || echo "ℹ Nothing new to commit"

echo "🚀 Pushing branch to origin..."
git push -u origin "$BRANCH"

echo "📤 Creating Pull Request (to $BASE)..."
if command -v gh >/dev/null 2>&1; then
  gh pr create --base "$BASE" --head "$BRANCH" \
    --title "$MSG" \
    --body "Implements GCP behavior-risks multi-select + scoring and UX polish. Maintains accessibility/theming. Please review and merge."
  echo "✅ PR created. Open GitHub to review & merge."
else
  REPO_URL="$(git config --get remote.origin.url | sed 's/.git$//')"
  REPO_URL="${REPO_URL/ssh:\/\/git@/https:\/\/}"
  REPO_URL="${REPO_URL/:/\//}"
  echo "👉 Create a PR here: $REPO_URL/compare/$BASE...$BRANCH"
fi

echo ""
read -p "🕓 Press Enter AFTER merging the PR in GitHub…"

echo "🔄 Syncing local $BASE with origin..."
git checkout "$BASE"
git pull --rebase origin "$BASE"
git branch -D "$BRANCH" 2>/dev/null || true

echo ""
echo "✅ Sync complete. Latest on origin/$BASE:"
git log -1 --oneline --decorate origin/"$BASE"

echo ""
echo "💡 Local smoke test:"
echo "  streamlit run app.py"
echo ""
echo "🚚 To push the merged Development to demo:"
echo "  git push origin $BASE:demo -f"
