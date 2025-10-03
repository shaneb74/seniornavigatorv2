#!/usr/bin/env python3
"""
dead_imports.py - find potentially unused imports across the repo.
Heuristic AST-based (safe to run; no execution). Excludes star-imports.
"""
from __future__ import annotations

import ast, pathlib, sys

IGNORE_DIRS = {'.git','venv','.venv','__pycache__'}

def analyze_file(p: pathlib.Path) -> list[tuple[str,int]]:
    try:
        src = p.read_text(encoding='utf-8')
    except Exception:
        return []
    try:
        tree = ast.parse(src, filename=str(p))
    except SyntaxError:
        return []
    imported: dict[str, int] = {}
    used: set[str] = set()

    class Visitor(ast.NodeVisitor):
        def visit_Import(self, node: ast.Import) -> None:
            for alias in node.names:
                name = alias.asname or alias.name.split('.')[0]
                imported[name] = node.lineno
        def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
            if node.module is None:
                return
            for alias in node.names:
                if alias.name == '*':
                    continue
                name = alias.asname or alias.name
                imported[name] = node.lineno
        def visit_Name(self, node: ast.Name) -> None:
            used.add(node.id)

    Visitor().visit(tree)

    unused = []
    for name, lineno in imported.items():
        if name not in used:
            unused.append((name, lineno))
    return unused

def main() -> int:
    any_unused = False
    for p in pathlib.Path('.').rglob('*.py'):
        if any(part in IGNORE_DIRS for part in p.parts):
            continue
        unused = analyze_file(p)
        if unused:
            any_unused = True
            print(f"{p}:")
            for name, ln in sorted(unused, key=lambda x: x[1]):
                print(f"  line {ln}: unused import '{name}'")
    if any_unused:
        return 1
    print("✅ No unused imports detected.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
