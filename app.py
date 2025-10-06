from __future__ import annotations

# app.py - Senior Navigator bootstrap with safe, persistent debug + guardrails

import os
import sys
import inspect
from pathlib import Path
import streamlit as st


# =========================
# Streamlit runtime guard
# =========================
def _ensure_navigation_api() -> None:
    """Fail fast with a helpful message when the nav API is unavailable."""

    has_page = hasattr(st, "Page")
    has_nav = hasattr(st, "navigation")
    if has_page and has_nav:
        return

    version = getattr(st, "__version__", "unknown")
    st.set_page_config(page_title="Senior Navigator", layout="wide")
    st.error(
        "Senior Navigator requires Streamlit 1.40 or newer so it can use the"
        " built-in navigation API. The currently running Streamlit version"
        f" is {version!r}. Please upgrade Streamlit (for example:"
        " `pip install --upgrade streamlit>=1.40,<1.41`) and restart the app."
    )
    st.stop()


_ensure_navigation_api()

from senior_nav.navigation import consume_pending_nav


# =========================
# Debug / guardrail toggles
# =========================
def _debug_enabled() -> bool:
    """Return True when lightweight debug logging should be enabled."""

    try:
        qp = str(st.query_params.get("debug", "")).lower()
    except Exception:
        qp = ""
    env = os.environ.get("SN_DEBUG_PAGES", "").lower()
    truthy = {"1", "true", "yes", "on"}
    return qp in truthy or env in truthy

def register_pages(*args, **kwargs):
    # disabled: we register pages solely via INTENDED + st.navigation
    return None

from pathlib import Path

# (removed) legacy auto-registration of subfolder pages
# =========================



# ==========================================
# Sys.path hygiene: keep repo clean & stable
# ==========================================
def _sanitize_sys_path() -> None:
    bad_markers = ("/_graveyard/", "/Designer-Development-8/", "/designer-development-8/", "/ui/pages/")
    keep: list[str] = []
    for p in sys.path:
        s = p.replace("\\", "/")
        if any(m in s for m in bad_markers):
            continue
        keep.append(p)
    sys.path[:] = keep
_sanitize_sys_path()

# ==========================================
# Live import logger (kept on; lightweight)
# Logs any module imported from /pages/ at runtime
# ==========================================
class _PageImportLogger:
    def find_spec(self, fullname, path=None, target=None):  # type: ignore[override]
        from importlib.machinery import PathFinder
        spec = PathFinder.find_spec(fullname, path)
        if spec and getattr(spec, "origin", None):
            origin = str(spec.origin).replace("\\", "/")
            if "/pages/" in origin:
                print(f"📄 import: {origin}")
        return spec



# Install the logger only once when debug mode is active.
if _debug_enabled():
    already_registered = any(isinstance(hook, _PageImportLogger) for hook in sys.meta_path)
    if not already_registered:
        sys.meta_path.insert(0, _PageImportLogger())



# ===============================
# Theme import with safe fallback
# ===============================
try:
    from ui.theme import inject_theme  # preferred path
except Exception:
    def inject_theme() -> None:
        st.markdown(
            """
            <style>
              .block-container{max-width:1160px;padding-top:8px;}
              header[data-testid="stHeader"]{background:transparent;}
              footer{visibility:hidden;}
            </style>
            """,
            unsafe_allow_html=True,
        )

# ==========================================
# Global CSS injection (theme comes in last)
# ==========================================
def _inject_global_css() -> None:
    css_path = Path("static/style.css")
    if css_path.exists():
        try:
            extra = css_path.read_text(encoding="utf-8").strip()
        except Exception:
            extra = css_path.read_bytes().decode(errors="ignore").strip()
        v = int(css_path.stat().st_mtime)
        st.markdown(f"<style>{extra}</style><!-- v:{v} -->", unsafe_allow_html=True)
    inject_theme()
# _inject_global_css()  # moved into pages after set_page_config
# ==========================================
# Pre-flight syntax check for page modules
# (kept: catches bad edits before navigation)
# ==========================================
def _syntax_preflight(paths=("pages",), stop_on_error=True):
    import pathlib, io, tokenize
    errors = []
    for root in paths:
        for p in pathlib.Path(root).rglob("*.py"):
            try:
                src = p.read_text(encoding="utf-8")
            except Exception as e:
                errors.append((p, 0, 0, f"read error: {e}", ""))
                continue
            try:
                tokenize.generate_tokens(io.StringIO(src).readline)
                compile(src, str(p), "exec", dont_inherit=True)
            except SyntaxError as e:
                errors.append((p, e.lineno or 0, e.offset or 0, e.msg, e.text or ""))
            except Exception as e:
                errors.append((p, 0, 0, f"{type(e).__name__}: {e}", ""))
    if errors:
        st.error("Syntax/parse error(s) found. Fix these before running pages.")
        for p, line, col, msg, txt in errors:
            pointer = " " * (max((col or 1) - 1, 0)) + "^" if txt else ""
            st.write(f"**{p}**")
            st.code(f"line {line}, col {col}: {msg}\n{(txt or '').rstrip()}\n{pointer}")
            st.markdown("---")
        if stop_on_error:
            st.stop()
_syntax_preflight()

consume_pending_nav()

# ==========================================
# Session bootstrap (prototype auth flag)
# ==========================================
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False



# ==========================================
# Page registration helpers
# ==========================================
def ensure_page(path: str, title: str, icon: str, default: bool = False):
    p = Path(path)
    if not p.exists():
        return None
    return (
        st.Page(path, title=title, icon=icon, default=True)
        if default else st.Page(path, title=title, icon=icon)
    )

# ==========================================
# Pages to register (controls nav order)
# ==========================================
INTENDED = [
    ("pages/00_welcome.py", "Welcome", "👋", True),
    ("pages/10_audiencing.py", "Choose Entry Type", "🎯", False),
    ("pages/20_hub.py", "Care Planning Hub", "🏠", False),
    ("pages/30_guided_care_plan.py", "Guided Care Plan", "🧭", False),
    ("pages/40_cost_planner.py", "Cost Planner", "💰", False),
    ("pages/50_my_documents.py", "My Documents", "📁", False),
    ("pages/60_pfma.py", "Plan for My Advisor", "🤝", False),
    ("pages/70_ai_advisor.py", "AI Advisor", "🤖", False),
]
# Build the Page objects (ignore missing silently)
pages = []
for path, title, icon, default in INTENDED:
    page = ensure_page(path, title, icon, default)
    if page:
        pages.append(page)


# Render navigation (always sidebar, expanded)
if pages:
    pg = st.navigation(pages, position="sidebar", expanded=True)
    pg.run()
else:
    st.error("No pages available. Check file paths in app.py.")

# ==========================================
# Sidebar tools (Design mode + Auth)
# ==========================================
with st.sidebar:
    st.markdown("---")
    # Design mode toggle
    st.checkbox(
        "Design mode (keep nav visible; skip welcome redirect)",
        key="dev_design_mode",
        help="Enable with ?dev=1 in the URL or SN_DEV=1 in env.",
    )
    # Lightweight pages debug toggle
    st.checkbox(
        "Debug: log page imports (?debug=1)",
        value=_debug_enabled(),
        key="dbg_pages_enabled",
        help="Prints a line in the terminal whenever a /pages/ module is imported.",
        disabled=True,  # state is controlled by query param/env for reproducibility
    )
    st.markdown("---")
    # Prototype auth toggle
    st.caption("Authentication")
    if st.session_state.is_authenticated:
        st.success("Signed in")
        if st.button("Log out", key="sidebar_logout"):
            st.session_state.is_authenticated = False
            st.rerun()
    else:
        st.info("Not signed in")
        if st.button("Log in", key="sidebar_login"):
            st.session_state.is_authenticated = True
            st.rerun()
