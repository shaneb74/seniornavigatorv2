#!/usr/bin/env python3
"""
finish_scope_insertion.py - nudge inject_theme()/scope below any dangling multi-line import
and ensure `from __future__ import annotations` sits at the very top (after docstring).
"""

from __future__ import annotations
import pathlib, re

PAGES = pathlib.Path("pages")

TRIPLE_RE = re.compile(r'^\s*[ruRU]?[\'"]{3}')

def move_future_to_top(lines: list[str]) -> list[str]:
    """Ensure from __future__ import annotations is right after module docstring / header."""
    future_idx = None
    for i, ln in enumerate(lines):
        if ln.strip().startswith("from __future__ import annotations"):
            future_idx = i
            break
    if future_idx is None:
        return lines

    i = 0
    n = len(lines)
    # shebang/encoding
    if i < n and lines[i].startswith("#!"): i += 1
    if i < n and ("coding:" in lines[i] or "coding=" in lines[i]): i += 1

    # module docstring (triple quotes)
    if i < n and TRIPLE_RE.match(lines[i]):
        q = '"""' if '"""' in lines[i] else "'''"
        if lines[i].count(q) >= 2 and lines[i].strip().endswith(q):
            i += 1
        else:
            i += 1
            while i < n and q not in lines[i]: i += 1
            if i < n: i += 1

    # If already in place, nothing to do
    if future_idx == i:
        return lines

    # Relocate
    future_line = lines.pop(future_idx)
    lines[i:i] = [future_line, ""]
    return lines

def paren_depth(s: str) -> int:
    return s.count("(") - s.count(")")

def relocate_injection(lines: list[str]) -> list[str]:
    """Find inject_theme() + scope opener; if they sit before a closing ) of a multi-line import,
    move both lines to the first safe spot where paren depth returns to 0.
    """
    # find injection block indices
    inj_i = None
    scope_i = None
    for i, ln in enumerate(lines):
        if inj_i is None and ln.strip() == "inject_theme()":
            inj_i = i
        if scope_i is None and 'st.markdown(' in ln and 'sn-scope ' in ln and 'unsafe_allow_html=True' in ln:
            scope_i = i
        if inj_i is not None and scope_i is not None:
            break
    if inj_i is None or scope_i is None:
        return lines

    # compute cumulative depth from top to the injection point
    depth = 0
    for j in range(inj_i):
        depth += paren_depth(lines[j])

    if depth <= 0:
        # already safe (not inside parens)
        return lines

    # find first line at/after injection where depth returns to 0
    k = inj_i
    while k < len(lines):
        depth += paren_depth(lines[k])
        if depth <= 0:
            break
        k += 1

    # Move the two lines (keep order) to AFTER line k
    block = [lines[inj_i], lines[scope_i]]
    # delete in reverse index order
    for idx in sorted([inj_i, scope_i], reverse=True):
        del lines[idx]
        if idx < k:
            k -= 1
    insert_at = min(k + 1, len(lines))
    lines[insert_at:insert_at] = block + [""]  # trailing blank for breathing room
    return lines

def process_file(p: pathlib.Path) -> bool:
    s = p.read_text(encoding="utf-8")
    lines = s.splitlines()

    before = lines[:]
    lines = move_future_to_top(lines)
    lines = relocate_injection(lines)

    new = "\n".join(lines) + ("\n" if s.endswith("\n") else "")
    if new != s:
        p.write_text(new, encoding="utf-8", newline="\n")
        print(f"[nudged] {p}")
        return True
    return False

def main():
    changed = 0
    for p in PAGES.rglob("*.py"):
        try:
            if process_file(p):
                changed += 1
        except Exception as e:
            print(f"[skip]  {p}: {e}")
    print(f"Done. Updated {changed} file(s).")

if __name__ == "__main__":
    main()
