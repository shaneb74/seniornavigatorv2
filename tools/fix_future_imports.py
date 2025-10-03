#!/usr/bin/env python3
"""
fix_future_imports.py - move `from __future__ import annotations` to the correct spot.
Rules:
- May come after: shebang, encoding line, top-level module docstring.
- Must come before any other imports or code.
"""
from __future__ import annotations

import pathlib
import re

TARGET = "from __future__ import annotations"
TRIPLE_RE = re.compile(r'^\s*[ruRU]?[\'\"]{3}')

def desired_index(lines: list[str]) -> int:
    i = 0
    n = len(lines)
    if i < n and lines[i].startswith("#!"):
        i += 1
    if i < n and ("coding:" in lines[i] or "coding=" in lines[i]):
        i += 1
    if i < n and TRIPLE_RE.match(lines[i]):
        q = '"""' if '"""' in lines[i] else "'''"
        if lines[i].strip().endswith(q) and lines[i].count(q) >= 2:
            i += 1
        else:
            j = i + 1
            while j < n and q not in lines[j]:
                j += 1
            i = min(j + 1, n)
    return i

def fix_file(p: pathlib.Path) -> bool:
    text = p.read_text(encoding="utf-8")
    lines = text.splitlines()
    cur = None
    for idx, ln in enumerate(lines):
        if ln.strip() == TARGET:
            cur = idx
            break
    if cur is None:
        return False
    want = desired_index(lines)
    if cur == want:
        return False
    # remove and insert
    lines.pop(cur)
    lines.insert(want, TARGET)
    out = "\n".join(lines)
    if text.endswith("\n") and not out.endswith("\n"):
        out += "\n"
    p.write_text(out, encoding="utf-8", newline="\n")
    return True

def main() -> int:
    changed = 0
    for py in pathlib.Path('.').rglob('*.py'):
        if any(part in {'.git','venv','.venv','__pycache__'} for part in py.parts):
            continue
        try:
            if fix_file(py):
                print(f"[fixed] {py}")
                changed += 1
        except Exception as e:
            print(f"[skip] {py}: {e}")
    print(f"Done. Updated {changed} file(s).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
