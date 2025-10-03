#!/usr/bin/env python3
"""
sanitize_ascii.py - scan and optionally fix non-ASCII punctuation in source files.
Targets: smart quotes, en/em dashes, ellipsis, NBSP, zero-width chars.
"""
from __future__ import annotations

import argparse
import pathlib
import sys
import difflib

DEFAULT_EXTS = {".py",".md",".txt",".html",".css",".js",".ts",".tsx",".json",".yaml",".yml"}

REPLACEMENTS = {
    "\u2018": "'", "\u2019": "'",
    "\u201C": '"', "\u201D": '"',
    "\u2013": "-", "\u2014": "-",
    "\u2026": "...",
    "\u00A0": " ",
    "\u200B": "", "\u200C": "", "\u200D": "",
    "\uFEFF": "",
}

IGNORE_DIRS = {".git",".venv","venv","node_modules",".mypy_cache",".ruff_cache","__pycache__"}

def iter_files(root: pathlib.Path, extensions: set[str]) -> list[pathlib.Path]:
    files: list[pathlib.Path] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in IGNORE_DIRS for part in p.parts):
            continue
        if p.suffix in extensions:
            files.append(p)
    return files

def apply_fixes(text: str) -> str:
    out = text
    for bad, good in REPLACEMENTS.items():
        out = out.replace(bad, good)
    return out

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--ext", action="append")
    ap.add_argument("--diff", action="store_true")
    args = ap.parse_args()

    exts = set(args.ext) if args.ext else set(DEFAULT_EXTS)
    root = pathlib.Path(".").resolve()
    files = iter_files(root, exts)

    changed = 0
    for p in files:
        try:
            raw = p.read_text(encoding="utf-8")
        except Exception as e:
            print(f"[skip] {p}: read error: {e}")
            continue
        fixed = apply_fixes(raw)
        if args.write and fixed != raw:
            p.write_text(fixed, encoding="utf-8", newline="\n")
            print(f"[fixed] {p}")
            changed += 1

    if args.write:
        print(f"Done. Updated {changed} file(s).")
    else:
        print("Scan complete. Use --write to apply fixes.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
