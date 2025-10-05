
set -euo pipefail

echo "➡️  Starting deprecated appointment pages cleanup…"

if [ ! -f "app.py" ] || [ ! -d "pages" ]; then
  echo "❌ Run this from your repo root (where app.py and /pages live)."
  exit 1
fi

BOOKING="pages/appointment_booking.py"
INTERSTITIAL="pages/appointment_interstitial.py"

TS="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="_graveyard/deleted_pages/$TS"
mkdir -p "$BACKUP_DIR"

move_file() {
  local f="$1"
  if [ -f "$f" ]; then
    if git ls-files --error-unmatch "$f" >/dev/null 2>&1; then
      git mv "$f" "$BACKUP_DIR"/
    else
      mv "$f" "$BACKUP_DIR"/
    fi
    echo "🗂️  Backed up: $f → $BACKUP_DIR/"
  else
    echo "ℹ️  Not present (skipped): $f"
  fi
}

move_file "$BOOKING"
move_file "$INTERSTITIAL"

python3 - <<'PY'
from pathlib import Path
p = Path("app.py")
src = p.read_text(encoding="utf-8")
targets = ("pages/appointment_booking.py", "pages/appointment_interstitial.py")
out = [line for line in src.splitlines() if not any(t in line for t in targets)]
new = "\n".join(out) + "\n"
if new != src:
    p.write_text(new, encoding="utf-8")
    print("🧹 app.py: removed appointment_* entries from INTENDED.")
else:
    print("ℹ️  app.py: no appointment_* entries found.")
PY

if [ -f "pages/expert_review.py" ]; then git add pages/expert_review.py || true; fi

echo "🔎 Scanning for lingering references…"
if grep -RInE 'switch_page\("pages/(appointment_booking|appointment_interstitial)\.py"\)' pages senior_nav app.py run.py 2>/dev/null | sort; then
  echo "⚠️  Found references above. Update/remove them and re-run."
  exit 1
else
  echo "✅ No lingering switch_page() references."
fi

echo "🧪 Running pre-commit (non-fatal)…"
pre-commit run --all-files || true

echo "🧪 Compiling app.py and pages…"
python3 -m py_compile app.py
python3 - <<'PY'
import pathlib, py_compile, sys
ok = True
for f in pathlib.Path("pages").glob("*.py"):
    try: py_compile.compile(str(f), doraise=True)
    except Exception as e:
        ok = False; print(f"❌ {f}: {e}")
if not ok: sys.exit(1)
print("✅ pages compile")
PY

git add -A
if git diff --cached --quiet; then
  echo "ℹ️  Nothing to commit."
else
  git commit -m "chore: remove deprecated appointment pages; Expert Review is finish handoff to PFMA"
  git push
fi

echo "🎉 Done."
echo "📦 Backups are in: $BACKUP_DIR"
