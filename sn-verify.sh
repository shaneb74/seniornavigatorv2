#!/usr/bin/env bash
set -Eeuo pipefail

echo "== SeniorNav verify =="
PY_DIRS=("app_pages" "ui")

# helper: run if command exists
run_if() {
  local cmd="$1"; shift
  if command -v "$cmd" >/dev/null 2>&1; then
    "$cmd" "$@"
  else
    echo "⚠️  $cmd not installed — skipping."
  fi
}

echo "• Python version:"
python -V || true

echo "• Checking paths exist:"
for d in "${PY_DIRS[@]}"; do
  if [ ! -d "$d" ]; then
    echo "⚠️  missing dir: $d (will continue)"
  fi
done

echo "• Static checks (format/lint/type) ..."
# Format (check-only)
if command -v black >/dev/null 2>&1; then
  black --check "${PY_DIRS[@]}" || { echo "❌ black check failed"; exit 1; }
else
  echo "⚠️  black not installed — skipping."
fi

# Lint
if command -v ruff >/dev/null 2>&1; then
  ruff check "${PY_DIRS[@]}" || { echo "❌ ruff lint failed"; exit 1; }
else
  echo "⚠️  ruff not installed — skipping."
fi

# Type-check (soft-fail allowed if mypy.ini/pyproject not present)
if command -v mypy >/dev/null 2>&1; then
  if [ -f "mypy.ini" ] || grep -q "mypy" pyproject.toml 2>/dev/null; then
    mypy "${PY_DIRS[@]}" || { echo "❌ mypy failed"; exit 1; }
  else
    echo "⚠️  mypy config not found — skipping."
  fi
else
  echo "⚠️  mypy not installed — skipping."
fi

echo "• Unit tests (if present) ..."
if [ -d "tests" ]; then
  if command -v pytest >/dev/null 2>&1; then
    pytest -q || { echo "❌ pytest failed"; exit 1; }
  else
    echo "⚠️  pytest not installed — skipping."
  fi
else
  echo "ℹ️  no tests/ directory — skipping pytest."
fi

echo "• Byte-compile sanity ..."
python -m compileall "${PY_DIRS[@]}" || { echo "❌ compileall failed"; exit 1; }

echo "✅ verify OK"
