#!/usr/bin/env python3
"""
check_future_imports.py - verify that `from __future__ import annotations` is in the correct spot.
Rules:
- May follow: shebang, encoding, top-level module docstring.
- Must precede: all other imports and code.
"""
from __future__ import annotations

import pathlib
import re
import sys

TARGET = "from __future__ import annotations"
TRIPLE_RE = re.compile(r'^\s*[ruRU]?[\'\"]{3}')

def expected_index(lines: list[str]) -> int:
    i = 0
    n = len(lines)
    if i < n and lines[i].startswith("#!"):
        i += 1
    if i < n and ("coding:" in lines[i] or "coding=" in lines[i]):
        i += 1
    if i < n and TRIPLE_RE.match(lines[i]):
        q = '"""' if '"""' in lines[i] else "'''"
        # single-line docstring
        if lines[i].strip().endswith(q) and lines[i].count(q) >= 2:
            i += 1
        else:
            j = i + 1
            while j < n and q not in lines[j]:
                j += 1
            i = min(j + 1, n)
    return i

def check_file(p: pathlib.Path) -> tuple[bool, str]:
    lines = p.read_text(encoding="utf-8").splitlines()
    fut = None
    for idx, ln in enumerate(lines):
        if ln.strip() == TARGET:
            fut = idx
            break
    if fut is None:
        return True, ""  # no future import = OK (we only enforce placement when present)
    want = expected_index(lines)
    return fut == want, f"{p} (line {fut+1}) should be at line {want+1}"

def main() -> int:
    bad = []
    for py in pathlib.Path('.').rglob('*.py'):
        if any(part in {'.git','venv','.venv','__pycache__'} for part in py.parts):
            continue
        ok, msg = check_file(py)
        if not ok:
            bad.append(msg)
    if bad:
        print("❌ Found __future__ imports in the wrong place:")
        for m in bad:
            print(" ", m)
        return 1
    print("✅ All __future__ imports are in the correct place.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
