#!/usr/bin/env python3
"""
lint.py - light-weight linter (no external deps).
Checks:
- line length > 120
- tabs instead of spaces
- trailing whitespace
- final newline
- mixed line endings
"""
from __future__ import annotations

import pathlib, sys

MAXLEN = 120
IGNORE_DIRS = {'.git','venv','.venv','__pycache__'}

def lint_file(p: pathlib.Path) -> list[str]:
    msgs = []
    try:
        data = p.read_bytes()
    except Exception as e:
        return [f"[read-error] {p}: {e}"]
    # line ending check
    if b'\r\n' in data and b'\n' in data.replace(b'\r\n', b''):
        msgs.append("mixed line endings (CRLF and LF)")
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError as e:
        msgs.append(f"not utf-8: {e}")
        return msgs
    lines = text.splitlines()
    for i, ln in enumerate(lines, 1):
        if '\t' in ln:
            msgs.append(f"line {i}: contains TAB")
        if len(ln) > MAXLEN:
            msgs.append(f"line {i}: longer than {MAXLEN} chars")
        if ln.rstrip() != ln:
            msgs.append(f"line {i}: trailing whitespace")
    if not text.endswith('\n'):
        msgs.append("file does not end with newline")
    return msgs

def main() -> int:
    bad = 0
    for p in pathlib.Path('.').rglob('*.py'):
        if any(part in IGNORE_DIRS for part in p.parts):
            continue
        msgs = lint_file(p)
        if msgs:
            bad += 1
            print(p)
            for m in msgs:
                print(" ", m)
    if bad:
        return 1
    print("✅ Lint clean.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
