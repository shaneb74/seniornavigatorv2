#!/usr/bin/env python3
"""
sanitize_ascii.py - scan and optionally fix non-ASCII punctuation in source files.

Targets the usual gremlins:
  - ' ' " "  (smart quotes)
  - - -      (en/em dashes)
  - ...         (ellipsis)
  - \u00A0    (non-breaking space)
  - \u200B-\u200D (zero-width chars)
Also flags BOMs.

Usage:
  Dry-run scan (recommended first):
    python tools/sanitize_ascii.py

  Auto-fix in place:
    python tools/sanitize_ascii.py --write

  Limit to Python files only:
    python tools/sanitize_ascii.py --ext .py

  Show unified diff for each change:
    python tools/sanitize_ascii.py --write --diff
"""
from __future__ import annotations
import argparse
import pathlib
import sys
import difflib

# File extensions to scan by default (add more if you like)
DEFAULT_EXTS = {
    ".py", ".md", ".txt", ".html", ".css", ".js", ".ts", ".tsx", ".json",
    ".yaml", ".yml",
}

# Replacement map for the most common offenders
# Replacement map for the most common offenders
REPLACEMENTS = {
    # Quotes
    "\u2018": "'",   # left single
    "\u2019": "'",   # right single / apostrophe
    "\u201A": "'",   # single low-9 quote
    "\u201B": "'",   # single high-reversed-9
    "\u201C": '"',   # left double
    "\u201D": '"',   # right double
    "\u201E": '"',   # double low-9 quote
    "\u201F": '"',   # double high-reversed-9

    # Dashes and minus-like
    "\u2010": "-",   # hyphen
    "\u2011": "-",   # non-breaking hyphen
    "\u2012": "-",   # figure dash
    "\u2013": "-",   # en dash
    "\u2014": "-",   # em dash
    "\u2015": "-",   # horizontal bar
    "\u2212": "-",   # minus sign

    # Ellipsis
    "\u2026": "...", # ellipsis

    # Spaces
    "\u00A0": " ",   # NBSP
    "\u202F": " ",   # narrow NBSP
    "\u2000": " ",   # en quad
    "\u2001": " ",   # em quad
    "\u2002": " ",   # en space
    "\u2003": " ",   # em space
    "\u2004": " ",   # three-per-em space
    "\u2005": " ",   # four-per-em space
    "\u2006": " ",   # six-per-em space
    "\u2007": " ",   # figure space
    "\u2008": " ",   # punctuation space
    "\u2009": " ",   # thin space
    "\u200A": " ",   # hair space

    # Zero-width / invisible
    "\u200B": "",    # zero-width space
    "\u200C": "",    # zero-width non-joiner
    "\u200D": "",    # zero-width joiner
    "\uFEFF": "",    # zero-width no-break space / BOM

    # Misc symbols
    "\u2022": "*",   # bullet
    "\u25E6": "*",   # white bullet
}


# Characters we consider problematic (for reporting)
PROBLEMATIC = set(REPLACEMENTS.keys())

# Files/dirs to ignore
IGNORE_DIRS = {".git", ".venv", "venv", "node_modules", ".mypy_cache", ".ruff_cache", "__pycache__"}
IGNORE_FILES = {"package-lock.json"}


def iter_files(root: pathlib.Path, extensions: set[str]) -> list[pathlib.Path]:
    files: list[pathlib.Path] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if p.name in IGNORE_FILES:
            continue
        if any(part in IGNORE_DIRS for part in p.parts):
            continue
        if p.suffix in extensions:
            files.append(p)
    return files


def find_issues(text: str) -> list[tuple[int, int, str]]:
    """Return list of (line_no, col_no, char) for each problematic char or BOM."""
    issues = []
    # Flag BOM at beginning
    if text.startswith("\ufeff"):
        issues.append((1, 1, "BOM(\\ufeff)"))
    for i, line in enumerate(text.splitlines(keepends=False), start=1):
        for j, ch in enumerate(line, start=1):
            if ch in PROBLEMATIC:
                issues.append((i, j, ch))
    return issues


def apply_fixes(text: str) -> str:
    out = text
    # Strip BOM if present
    if out.startswith("\ufeff"):
        out = out.lstrip("\ufeff")
    # Replace mapped chars
    for bad, good in REPLACEMENTS.items():
        out = out.replace(bad, good)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="apply fixes in place")
    ap.add_argument("--ext", action="append", help="restrict to these extensions (repeatable)")
    ap.add_argument("--diff", action="store_true", help="print unified diffs when writing")
    args = ap.parse_args()

    exts = set(args.ext) if args.ext else set(DEFAULT_EXTS)
    root = pathlib.Path(".").resolve()
    files = iter_files(root, exts)

    total_files = 0
    total_issues = 0
    changed_files = 0

    for p in files:
        try:
            raw = p.read_text(encoding="utf-8")
        except Exception as e:
            print(f"[skip] {p}: read error: {e}")
            continue

        issues = find_issues(raw)
        if not issues:
            continue

        total_files += 1
        total_issues += len(issues)
        print(f"\n{p}  ({len(issues)} issue(s))")
        for (ln, col, ch) in issues[:50]:  # cap to avoid spam
            disp = ch if ch != "\ufeff" else "BOM"
            print(f"  line {ln:>4}, col {col:>3}: U+{ord(ch):04X} '{disp}'")

        if args.write:
            fixed = apply_fixes(raw)
            if fixed != raw:
                if args.diff:
                    diff = difflib.unified_diff(
                        raw.splitlines(True),
                        fixed.splitlines(True),
                        fromfile=str(p),
                        tofile=str(p),
                    )
                    sys.stdout.writelines(diff)
                try:
                    p.write_text(fixed, encoding="utf-8", newline="\n")
                    changed_files += 1
                except Exception as e:
                    print(f"[error] {p}: write failed: {e}")

    if not total_files:
        print("No problematic characters found.")
    else:
        print(f"\nScanned {len(files)} files. Found {total_issues} issue(s) in {total_files} file(s).")
        if args.write:
            print(f"Updated {changed_files} file(s).")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
