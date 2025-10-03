#!/usr/bin/env python3
"""
compile_pages.py - fast compile of pages/*.py to catch syntax errors.
"""
from __future__ import annotations

import pathlib
import sys

def main() -> int:
    ok = True
    for p in pathlib.Path("pages").rglob("*.py"):
        try:
            src = p.read_text(encoding="utf-8")
            compile(src, str(p), "exec", dont_inherit=True)
        except SyntaxError as e:
            ok = False
            print(f"❌ {p}: line {e.lineno}, col {e.offset}: {e.msg}")
    if not ok:
        return 1
    print("✅ No syntax errors in pages/")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
