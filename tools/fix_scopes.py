#!/usr/bin/env python3
"""
fix_scopes.py - relocate inject_theme() and the scope wrapper to a safe spot in pages/*.py.

- Keeps shebang/encoding and __future__ at the very top.
- Preserves the full import block (including multi-line imports).
- Ensures a single `from ui.theme import inject_theme` in the imports.
- Inserts `inject_theme()` and the opening scope AFTER the imports.
- Ensures a closing </div> at EOF.
"""

from __future__ import annotations
import pathlib, re

PAGES_DIR = pathlib.Path("pages")

TRIPLE_RE = re.compile(r'^\s*[ruRU]?[\'"]{3}')
IMPORT_LINE_RE = re.compile(r'^\s*(from\s+\S+\s+import|import\s+\S+)')
FUTURE_RE = re.compile(r'^\s*from\s+__future__\s+import\s+')

def detect_scope(path: pathlib.Path) -> str:
    name = path.name.lower()
    pstr = str(path).lower().replace("\\", "/")
    return "gcp" if name.startswith("gcp") or "/gcp" in pstr else "dashboard"

def find_header_and_imports(lines: list[str]) -> tuple[int, int]:
    """
    Returns a tuple: (import_start, import_end)
    - import_start: index where the import block starts (may equal import_end if none)
    - import_end: index just after the last line of the import block
    The header (shebang/encoding/__future__/docstring) ends at import_start.
    """
    i = 0
    n = len(lines)

    # Shebang & encoding cookie as first lines if present
    if i < n and lines[i].startswith("#!"):
        i += 1
    if i < n and ("coding:" in lines[i] or "coding=" in lines[i]):
        i += 1

    # __future__ imports must come first if present
    while i < n and FUTURE_RE.match(lines[i]):
        i += 1

    # Top-level module docstring (triple quotes) - keep intact
    if i < n and TRIPLE_RE.match(lines[i]):
        q = '"""' if '"""' in lines[i] else "'''"
        if lines[i].count(q) >= 2 and lines[i].strip().endswith(q):
            i += 1
        else:
            i += 1
            while i < n and q not in lines[i]:
                i += 1
            if i < n:
                i += 1

    # Import block starts here (may be empty)
    import_start = i

    # Consume imports, including multi-line (track paren depth)
    paren_depth = 0
    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Track parentheses for multi-line imports like "from x import (\n a,\n b\n)"
        paren_depth += stripped.count("(") - stripped.count(")")

        is_import = bool(IMPORT_LINE_RE.match(line))
        if is_import or paren_depth > 0:
            i += 1
            continue

        # Allow blank lines *inside* an ongoing import group
        if stripped == "" and (i == import_start or paren_depth > 0 or (i > import_start and (IMPORT_LINE_RE.match(lines[i-1]) or paren_depth > 0))):
            i += 1
            continue

        break

    import_end = i
    return import_start, import_end

def ensure_imports(lines: list[str], import_start: int, import_end: int) -> tuple[list[str], int, int]:
    """Ensure 'import streamlit as st' and 'from ui.theme import inject_theme' exist within import block."""
    import_block = lines[import_start:import_end]
    # Normalize block for checks
    has_st = any(re.match(r'^\s*import\s+streamlit\s+as\s+st\s*$', ln) for ln in import_block)
    has_theme = any("from ui.theme import inject_theme" in ln for ln in import_block)

    new_block = import_block[:]

    # Insert streamlit import at top of block if missing
    if not has_st:
        new_block = ["import streamlit as st"] + ([""] if new_block and new_block[0].strip() else []) + new_block

    # Recompute has_theme after potential change
    has_theme = any("from ui.theme import inject_theme" in ln for ln in new_block)
    if not has_theme:
        # Place theme import *after* streamlit import if present, else at top
        placed = False
        out = []
        for ln in new_block:
            out.append(ln)
            if (not placed) and ln.strip().startswith("import streamlit as st"):
                out.append("from ui.theme import inject_theme")
                placed = True
        if not placed:
            out = ["from ui.theme import inject_theme"] + out
        new_block = out

    # Replace in lines and return new indices (import block length may have changed)
    new_lines = lines[:import_start] + new_block + lines[import_end:]
    delta = len(new_block) - len(import_block)
    new_import_start = import_start
    new_import_end = import_end + delta
    return new_lines, new_import_start, new_import_end

def remove_existing_injections(lines: list[str]) -> list[str]:
    """Strip previously injected theme calls and scope wrappers to avoid duplicates."""
    out = []
    for ln in lines:
        s = ln.strip()
        if s == "inject_theme()":
            continue
        if "st.markdown(" in ln and "sn-scope " in ln and "unsafe_allow_html=True" in ln:
            # remove any scope opener lines we previously added
            continue
        out.append(ln)
    return out

def ensure_closing_div(text: str) -> str:
    # Only add a closing div if missing entirely.
    if "</div>" not in text:
        return text.rstrip() + "\n\nst.markdown('</div>', unsafe_allow_html=True)\n"
    return text

def process_file(p: pathlib.Path) -> bool:
    try:
        s = p.read_text(encoding="utf-8")
    except Exception:
        s = p.read_bytes().decode("utf-8", errors="ignore")

    # Only touch Streamlit pages
    if ("st." not in s) and ("streamlit" not in s):
        return False

    lines = s.splitlines()

    # Remove existing injections (theme call + scope opener) wherever they landed
    lines = remove_existing_injections(lines)

    # Find import block after header
    import_start, import_end = find_header_and_imports(lines)

    # Ensure necessary imports present in the block
    lines, import_start, import_end = ensure_imports(lines, import_start, import_end)

    # Insert injection immediately *after* the full import block
    scope = detect_scope(p)
    inject_block = [
        "",
        "inject_theme()",
        f"st.markdown('<div class=\"sn-scope {scope}\">', unsafe_allow_html=True)",
        "",
    ]
    lines[import_end:import_end] = inject_block

    # Reassemble, ensure a closing </div> once
    new_text = "\n".join(lines)
    new_text = ensure_closing_div(new_text)

    if new_text != s:
        p.write_text(new_text, encoding="utf-8", newline="\n")
        return True
    return False

def main() -> None:
    changed = 0
    for p in PAGES_DIR.rglob("*.py"):
        try:
            if process_file(p):
                print(f"[fixed] {p}")
                changed += 1
        except Exception as e:
            print(f"[skip]  {p}: {e}")
    print(f"\nDone. Updated {changed} file(s).")

if __name__ == "__main__":
    main()
