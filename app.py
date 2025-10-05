from __future__ import annotations
import streamlit as st
import os
import sys
from pathlib import Path
import pathlib
import io
import tokenize

# Streamlit configuration
st.set_page_config(page_title="Senior Navigator", layout="wide")

# =========================
# Debug and Design Mode Toggles
# =========================
def _debug_enabled() -> bool:
    """Check if debug mode is enabled via query param or environment variable."""
    qp_flag = str(st.query_params.get("debug", "")).lower() in ("1", "true", "yes")
    env_flag = os.environ.get("SN_DEBUG_PAGES", "") == "1"
    return qp_flag or env_flag

def _design_mode_enabled() -> bool:
    """Check if design mode is enabled via query param, env, or session state."""
    qp_flag = str(st.query_params.get("dev", "")).lower() in ("1", "true", "yes")
    env_flag = os.environ.get("SN_DEV", "") == "1"
    ss_flag = bool(st.session_state.get("dev_design_mode"))
    return qp_flag or env_flag or ss_flag

# =========================
# System Path Hygiene
# =========================
def _sanitize_sys_path() -> None:
    """Remove problematic paths from sys.path to maintain a clean environment."""
    bad_markers = ("/_graveyard/", "/Designer-Development-8/", "/designer-development-8/", "/ui/pages/")
    keep = []
    for p in sys.path:
        path = Path(p).as_posix()
        if any(marker in path for marker in bad_markers):
            continue
        keep.append(p)
    sys.path[:] = keep
_sanitize_sys_path()

# =========================
# Page Import Logger
# =========================
class _PageImportLogger:
    """Log imports of modules from the /pages/ directory when debug is enabled."""
    def find_spec(self, fullname, path=None, target=None):
        from importlib.machinery import PathFinder
        spec = PathFinder.find_spec(fullname, path)
        if spec and getattr(spec, "origin", None):
            origin = Path(spec.origin).as_posix()
            if "/pages/" in origin:
                print(f"📄 import: {origin}")
        return spec

if _debug_enabled():
    sys.meta_path.insert(0, _PageImportLogger())

# =========================
# Theme and CSS Injection
# =========================
try:
    from ui.theme import inject_theme
except ImportError:
    def inject_theme() -> None:
        """Fallback theme if ui.theme import fails."""
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

def _inject_global_css() -> None:
    """Inject global CSS from static/style.css, with fallback if missing."""
    css_path = Path("static/style.css")
    if css_path.exists():
        try:
            extra = css_path.read_text(encoding="utf-8").strip()
        except Exception as e:
            st.warning(f"Failed to read CSS file with UTF-8 encoding: {e}. Falling back.")
            extra = css_path.read_bytes().decode(errors="ignore").strip()
        try:
            v = int(css_path.stat().st_mtime)
        except Exception:
            v = 0
        st.markdown(f"<style>{extra}</style><!-- v:{v} -->", unsafe_allow_html=True)
    else:
        st.warning("CSS file (static/style.css) not found. Using default styling.")
    inject_theme()
_inject_global_css()

# =========================
# Syntax Preflight Check
# =========================
def _syntax_preflight(paths=("pages",), stop_on_error=True) -> None:
    """Check syntax of Python files in specified paths, run only in debug mode."""
    if not _debug_enabled():
        return
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

# =========================
# Session Bootstrap
# =========================
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False

# =========================
# Page Registration
# =========================
def ensure_page(path: str, title: str, icon: str, default: bool = False) -> st.Page | None:
    """Create a Streamlit Page object if the path exists."""
    p = Path(path)
    if not p.exists():
        return None
    return st.Page(path, title=title, icon=icon, default=default)

def discover_pages() -> list[st.Page]:
    """Discover and validate pages from INTENDED list, avoiding duplicates."""
    pages = []
    seen_paths = set()
    for path, title, icon, default in INTENDED:
        if path in seen_paths:
            st.warning(f"Duplicate page path detected: {path}")
            continue
        seen_paths.add(path)
        page = ensure_page(path, title, icon, default)
        if page:
            pages.append(page)
    return pages

def _force_welcome_once() -> None:
    """Redirect to Welcome page on first session load, unless in design mode."""
    if _design_mode_enabled():
        return
    if st.session_state.get("_boot_forced_welcome"):
        return
    st.session_state["_boot_forced_welcome"] = True
    try:
        st.query_params.clear()
    except Exception:
        st.warning("Failed to clear query parameters; navigation may be affected.")
    st.rerun()

# Defined pages (controls navigation order)
INTENDED = [
    ("pages/welcome.py", "Welcome", "👋", True),
    ("pages/hub.py", "Your Concierge Care Hub", "🏠", False),
    ("pages/contextual_welcome_self.py", "Contextual Welcome - For You", "ℹ️", False),
    ("pages/contextual_welcome_loved_one.py", "Contextual Welcome - For Loved Ones", "ℹ️", False),
    ("pages/professional_mode.py", "Professional Mode", "🧑", False),
    ("pages/gcp.py", "Guided Care Plan", "🗺️", False),
    ("pages/gcp_daily_life.py", "GCP - Daily Life & Support", "🗺️", False),
    ("pages/gcp_health_safety.py", "GCP - Health & Safety", "🗺️", False),
    ("pages/gcp_context_prefs.py", "GCP - Context & Preferences", "🗺️", False),
    ("pages/gcp_recommendation.py", "GCP Recommendation", "🗺️", False),
    ("pages/cost_planner.py", "Cost Planner: Mode", "💰", False),
    ("pages/cost_planner_estimate.py", "Cost Planner: Estimate", "💰", False),
    ("pages/cost_planner_estimate_summary.py", "Cost Planner: Quick Summary", "💰", False),
    ("pages/cost_planner_modules.py", "Cost Planner: Modules", "📊", False),
    ("pages/cost_planner_home_care.py", "Home Care Support", "🏠", False),
    ("pages/cost_planner_daily_aids.py", "Daily Living Aids", "🛠️", False),
    ("pages/cost_planner_housing.py", "Housing Path", "🏡", False),
    ("pages/cost_planner_benefits.py", "Benefits Check", "💳", False),
    ("pages/cost_planner_mods.py", "Age-in-Place Upgrades", "🔧", False),
    ("pages/expert_review.py", "Expert Review", "🔎", False),
    ("pages/cost_planner_evaluation.py", "Cost Planner: Evaluation", "🔍", False),
    ("pages/cost_planner_skipped.py", "Cost Planner: Skipped", "⚠️", False),
    ("pages/pfma.py", "Plan for My Advisor", "🧭", False),
    ("pages/pfma_confirm_care_plan.py", "PFMA * Care Plan Confirmer", "✅", False),
    ("pages/pfma_confirm_cost_plan.py", "PFMA * Cost Plan Confirmer", "💰", False),
    ("pages/pfma_confirm_care_needs.py", "PFMA * Care Needs", "🩺", False),
    ("pages/pfma_confirm_care_prefs.py", "PFMA * Care Preferences", "🎯", False),
    ("pages/pfma_confirm_household_legal.py", "PFMA * Household & Legal", "🏠", False),
    ("pages/pfma_confirm_benefits_coverage.py", "PFMA * Benefits & Coverage", "💳", False),
    ("pages/pfma_confirm_personal_info.py", "PFMA * Personal Info", "👤", False),
    ("pages/cost_planner_v2/cost_planner_landing_v2.py", "Cost Planner v2 · Landing", "💰", False),
    ("pages/cost_planner_v2/cost_planner_modules_hub_v2.py", "Cost Planner v2 · Modules", "🧰", False),
    ("pages/cost_planner_v2/cost_planner_income_v2.py", "Cost Planner v2 · Income", "🧾", False),
    ("pages/cost_planner_v2/cost_planner_expenses_v2.py", "Cost Planner v2 · Expenses", "🧮", False),
    ("pages/cost_planner_v2/cost_planner_benefits_v2.py", "Cost Planner v2 · Benefits", "🎖️", False),
    ("pages/cost_planner_v2/cost_planner_home_v2.py", "Cost Planner v2 · Home", "🏠", False),
    ("pages/cost_planner_v2/cost_planner_home_mods_v2.py", "Cost Planner v2 · Home Mods", "🔧", False),
    ("pages/cost_planner_v2/cost_planner_liquidity_v2.py", "Cost Planner v2 · Liquidity", "💵", False),
    ("pages/cost_planner_v2/cost_planner_caregiver_v2.py", "Cost Planner v2 · Caregiver", "👥", False),
    ("pages/cost_planner_v2/cost_planner_assets_v2.py", "Cost Planner v2 · Assets", "🏦", False),
    ("pages/cost_planner_v2/cost_planner_timeline_v2.py", "Cost Planner v2 · Timeline", "📈", False),
]

# Register and navigate pages
pages = discover_pages()
_force_welcome_once()

if pages:
    pg = st.navigation(pages, position="sidebar", expanded=True)
    pg.run()
else:
    st.error("No pages available. Check file paths in app.py.")

# =========================
# Sidebar Tools
# =========================
with st.sidebar:
    st.markdown("---")
    st.checkbox(
        "Design mode (keep nav visible; skip welcome redirect)",
        key="dev_design_mode",
        help="Enable with ?dev=1 in the URL or SN_DEV=1 in env."
    )
    st.checkbox(
        "Debug: log page imports",
        key="dbg_pages_enabled",
        help="Prints a line in the terminal whenever a /pages/ module is imported.",
        on_change=lambda: sys.meta_path.insert(0, _PageImportLogger()) if st.session_state.dbg_pages_enabled else sys.meta_path.remove(_PageImportLogger())
    )
    st.markdown("---")
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