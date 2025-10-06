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
INTENDED = [    ("pages/welcome.py", "Welcome", "👋", True),
    ("pages/hub.py", "Your Concierge Care Hub", "🏠", False),
    ("pages/SeniorNav_terms.py", "Terms of Use", "📄", False),
    ("pages/SeniorNav_privacy.py", "Privacy Policy", "🔒", False),

    ("pages/SeniorNav_welcome_self.py", "Welcome · For You", "🙂", False),
    ("pages/SeniorNav_welcome_someone_else.py", "Welcome · Someone Else", "👥", False),
    ("pages/SeniorNav_welcome_professional.py", "Welcome · Professional", "🩺", False),
                ("pages/SeniorNav_professional_hub.py", "Professional Hub", "🧰", False),
    ("pages/SeniorNav_ai_advisor.py", "AI Advisor", "🤖", False),
    ("pages/SeniorNav_login.py", "Login", "🔐", False),
    ("pages/SeniorNav_waiting_room.py", "Waiting Room", "⏳", False),
    ("pages/SeniorNav_trusted_partners.py", "Trusted Partners", "🤝", False),
    ("pages/SeniorNav_export_details.py", "Export Details", "📤", False),
    ("pages/SeniorNav_my_documents.py", "My Documents", "📁", False),
    ("pages/SeniorNav_my_account.py", "My Account", "👤", False),
    
    ("pages/gcp_v2/gcp_landing_v2.py", "Guided Care Plan · Start", "🗺️", False),
    ("pages/gcp_v2/gcp_daily_life_v2.py", "GCP · Daily Life & Support", "🧭", False),
    ("pages/gcp_v2/gcp_health_safety_v2.py", "GCP · Health & Safety", "🩺", False),
    ("pages/gcp_v2/gcp_context_prefs_v2.py", "GCP · Context & Preferences", "🎯", False),
    ("pages/gcp_v2/gcp_recommendation_v2.py", "GCP · Recommendation", "✅", False),
    ("pages/professional_mode.py", "Professional Mode", "🧑", False),
    ("pages/expert_review.py", "Expert Review", "🔎", False),
    ("pages/pfma.py", "Plan for My Advisor", "🧭", False),
    ("pages/pfma_confirm_care_plan.py", "PFMA * Care Plan Confirmer", "✅", False),
    ("pages/pfma_confirm_cost_plan.py", "PFMA * Cost Plan Confirmer", "💰", False),
    ("pages/pfma_confirm_care_needs.py", "PFMA * Care Needs", "🩺", False),
    ("pages/pfma_confirm_care_prefs.py", "PFMA * Care Preferences", "🎯", False),
    ("pages/pfma_confirm_household_legal.py", "PFMA * Household & Legal", "🏠", False),
    ("pages/pfma_confirm_benefits_coverage.py", "PFMA * Benefits & Coverage", "💳", False),
    ("pages/pfma_confirm_personal_info.py", "PFMA * Personal Info", "👤", False),
    ("pages/ai_advisor.py", "AI Advisor", "🤖", False),
    ("pages/export_results.py", "Export Results", "📥", False),
    ("pages/my_documents.py", "My Documents", "📁", False),
    ("pages/my_account.py", "My Account", "👤", False),
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
# --- Cost Planner v2 diagnostics (non-blocking) ---
_CP_V2_PREFIX = "pages/cost_planner_v2/"
_cp_entries = [entry for entry in INTENDED if entry[0].startswith(_CP_V2_PREFIX)]
_cp_missing: list[str] = []
_cp_failed: list[tuple[str, str]] = []
for path, title, icon, default in _cp_entries:
    page_path = Path(path)
    if not page_path.exists():
        _cp_missing.append(path)
        continue
    try:
        st.Page(path, title=title, icon=icon, default=default)
    except Exception as exc:  # pragma: no cover - Streamlit runtime only
        _cp_failed.append((path, f"{type(exc).__name__}: {exc}"))

if _cp_missing or _cp_failed:
    st.warning("Cost Planner v2 diagnostics detected issues. See details below.")
    if _cp_missing:
        st.write("**Missing on disk:**")
        st.write("\n".join(f"• {p}" for p in sorted(_cp_missing)))
    if _cp_failed:
        st.write("**Failed to build:**")
        for path, message in _cp_failed:
            st.code(f"{path}\n{message}")
else:
    st.caption(f"Cost Planner v2 diagnostics: {len(_cp_entries)} page(s) ready.")
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
