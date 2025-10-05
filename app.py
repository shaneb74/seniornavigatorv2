from __future__ import annotations
import os
import sys
import inspect
from pathlib import Path
import streamlit as st

# --- Must be first Streamlit command ---
st.set_page_config(page_title="Senior Navigator", layout="wide")

# ==========================================
# Debug toggles
# ==========================================
def _debug_enabled() -> bool:
    try:
        qp_flag = str(st.query_params.get("debug", "")).lower() in ("1", "true", "yes")
    except Exception:
        qp_flag = False
    env_flag = os.environ.get("SN_DEBUG_PAGES", "") == "1"
    return qp_flag or env_flag


def _design_mode_enabled() -> bool:
    try:
        qp_flag = str(st.query_params.get("dev", "")).lower() in ("1", "true", "yes")
    except Exception:
        qp_flag = False
    env_flag = os.environ.get("SN_DEV", "") == "1"
    ss_flag = bool(st.session_state.get("dev_design_mode"))
    return qp_flag or env_flag or ss_flag


# ==========================================
# Pages guard (disabled for Streamlit Cloud)
# ==========================================
def _enforce_single_pages_dir() -> None:
    """Disabled on Streamlit Cloud"""
    return


# ==========================================
# Path cleanup
# ==========================================
def _sanitize_sys_path() -> None:
    bad_markers = (
        "/_graveyard/",
        "/Designer-Development-8/",
        "/designer-development-8/",
        "/ui/pages/",
    )
    keep: list[str] = []
    for p in sys.path:
        s = p.replace("\\", "/")
        if any(m in s for m in bad_markers):
            continue
        keep.append(p)
    sys.path[:] = keep


_sanitize_sys_path()


# ==========================================
# Import logging (optional)
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


if _debug_enabled():
    sys.meta_path.insert(0, _PageImportLogger())


# ==========================================
# Theme fallback
# ==========================================
try:
    from ui.theme import inject_theme  # preferred
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
# Global CSS
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


_inject_global_css()


# ==========================================
# Syntax preflight check
# ==========================================
def _syntax_preflight(paths=("pages",), stop_on_error=True):
    import pathlib, io, tokenize
    errors = []
    for root in paths:
        for p in pathlib.Path(root).rglob("*.py"):
            try:
                src = p.read_text(encoding="utf-8")
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


# ==========================================
# Session bootstrap
# ==========================================
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False


# ==========================================
# Force Welcome page (unless in design mode)
# ==========================================
def _force_welcome_once() -> None:
    if _design_mode_enabled():
        return
    if st.session_state.get("_boot_forced_welcome"):
        return
    st.session_state["_boot_forced_welcome"] = True
    try:
        st.query_params.clear()  # Streamlit >= 1.33
    except Exception:
        try:
            st.experimental_set_query_params()
        except Exception:
            pass
    st.rerun()


# ==========================================
# Page registration
# ==========================================
def ensure_page(path: str, title: str, icon: str, default: bool = False):
    p = Path(path)
    if not p.exists():
        return None
    return (
        st.Page(path, title=title, icon=icon, default=True)
        if default
        else st.Page(path, title=title, icon=icon)
    )


# ==========================================
# Pages order
# ==========================================
INTENDED = [
    ("pages/welcome.py", "Welcome", "👋", True),
    ("pages/hub.py", "Your Concierge Care Hub", "🏠", False),
    ("pages/contextual_welcome_self.py", "Contextual Welcome - For You", "ℹ️", False),
    ("pages/contextual_welcome_loved_one.py", "Contextual Welcome - For Loved Ones", "ℹ️", False),
    ("pages/gcp.py", "Guided Care Plan", "🗺️", False),
    ("pages/cost_planner_v2/cost_planner_landing_v2.py", "Cost Planner v2 · Landing", "💰", False),
    ("pages/pfma.py", "Plan for My Advisor", "🧭", False),
]

# ==========================================
# Navigation
# ==========================================
pages = [ensure_page(p, t, i, d) for p, t, i, d in INTENDED if ensure_page(p, t, i, d)]

_force_welcome_once()

if pages:
    pg = st.navigation(pages, position="sidebar", expanded=True)
    pg.run()
else:
    st.error("No pages available. Check file paths in app.py.")


# ==========================================
# Sidebar (debug + auth)
# ==========================================
with st.sidebar:
    st.markdown("---")
    st.checkbox(
        "Design mode (keep nav visible; skip welcome redirect)",
        key="dev_design_mode",
        help="Enable with ?dev=1 or SN_DEV=1.",
    )
    st.checkbox(
        "Debug: log page imports (?debug=1)",
        value=_debug_enabled(),
        key="dbg_pages_enabled",
        disabled=True,
    )
    st.markdown("---")
    st.caption("Authentication")
    if st.session_state.is_authenticated:
        st.success("Signed in")
        if st.button("Log out"):
            st.session_state.is_authenticated = False
            st.rerun()
    else:
        st.info("Not signed in")
        if st.button("Log in"):
            st.session_state.is_authenticated = True
            st.rerun()