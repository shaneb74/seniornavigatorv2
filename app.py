from __future__ import annotations

import os
import sys
from pathlib import Path
import streamlit as st

# ✅ Always set page config first
st.set_page_config(page_title="Senior Navigator", layout="wide")

# =========================
# Streamlit runtime guard
# =========================
def _ensure_navigation_api() -> None:
    has_page = hasattr(st, "Page")
    has_nav = hasattr(st, "navigation")
    if has_page and has_nav:
        return
    version = getattr(st, "__version__", "unknown")
    st.error(
        "Senior Navigator requires Streamlit 1.40+ for the built-in navigation API. "
        f"Detected version: {version!r}. Please upgrade (`pip install -U 'streamlit>=1.40,<1.41'`)."
    )
    st.stop()

_ensure_navigation_api()

# OPTIONAL: your CSS/theme injector can stay as-is, but run it later on each page.

# ------------------------------------------
# Preflight check (safe now that session is up)
# ------------------------------------------
def _syntax_preflight(paths=("app_pages",), stop_on_error=True):  # 🔁 updated folder name
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

# ------------------------------------------
# Session bootstrap
# ------------------------------------------
st.session_state.setdefault("is_authenticated", False)

# ------------------------------------------
# Page builder
# ------------------------------------------
def ensure_page(path: str, title: str, icon: str, default: bool = False):
    p = Path(path)
    if not p.exists():
        return None
    return st.Page(path, title=title, icon=icon, default=default)

# 🔁 Rename your folder from `pages/` ➜ `app_pages/` and update paths here
INTENDED = [
    ("app_pages/welcome.py", "Welcome", "👋", True),

    # Home & Welcome
    ("app_pages/SeniorNav_welcome_self.py", "Welcome · For You", "🙂", False),
    ("app_pages/SeniorNav_welcome_someone_else.py", "Welcome · Someone Else", "👥", False),
    ("app_pages/SeniorNav_welcome_professional.py", "Welcome · Professional", "🩺", False),
    ("app_pages/professional_mode.py", "Professional Mode", "🧑", False),

    # Concierge Care Hub
    ("app_pages/hub.py", "Your Concierge Care Hub", "🏠", False),
    ("app_pages/SeniorNav_professional_hub.py", "Professional Hub", "🧰", False),

    # Guided Care Plan
    ("app_pages/gcp_v2/gcp_landing_v2.py", "Guided Care Plan · Start", "🗺️", False),
    ("app_pages/gcp_v2/gcp_daily_life_v2.py", "GCP · Daily Life & Support", "🧭", False),
    ("app_pages/gcp_v2/gcp_health_safety_v2.py", "GCP · Health & Safety", "🩺", False),
    ("app_pages/gcp_v2/gcp_context_prefs_v2.py", "GCP · Context & Preferences", "🎯", False),
    ("app_pages/gcp_v2/gcp_recommendation_v2.py", "GCP · Recommendation", "✅", False),

    # Cost Planner
    ("app_pages/cost_planner_v2/cost_planner_landing_v2.py", "Cost Planner v2 · Landing", "💰", False),
    ("app_pages/cost_planner_v2/cost_planner_modules_hub_v2.py", "Cost Planner v2 · Modules", "🧰", False),
    ("app_pages/cost_planner_v2/cost_planner_income_v2.py", "Cost Planner v2 · Income", "🧾", False),
    ("app_pages/cost_planner_v2/cost_planner_expenses_v2.py", "Cost Planner v2 · Expenses", "🧮", False),
    ("app_pages/cost_planner_v2/cost_planner_benefits_v2.py", "Cost Planner v2 · Benefits", "🎖️", False),
    ("app_pages/cost_planner_v2/cost_planner_home_v2.py", "Cost Planner v2 · Home", "🏠", False),
    ("app_pages/cost_planner_v2/cost_planner_home_mods_v2.py", "Cost Planner v2 · Home Mods", "🔧", False),
    ("app_pages/cost_planner_v2/cost_planner_liquidity_v2.py", "Cost Planner v2 · Liquidity", "💵", False),
    ("app_pages/cost_planner_v2/cost_planner_caregiver_v2.py", "Cost Planner v2 · Caregiver", "👥", False),
    ("app_pages/cost_planner_v2/cost_planner_assets_v2.py", "Cost Planner v2 · Assets", "🏦", False),
    ("app_pages/cost_planner_v2/cost_planner_timeline_v2.py", "Cost Planner v2 · Timeline", "📈", False),
    ("app_pages/expert_review.py", "Expert Review", "🔎", False),

    # PFMA
    ("app_pages/pfma.py", "Plan for My Advisor", "🧭", False),
    ("app_pages/pfma_confirm_care_plan.py", "PFMA * Care Plan Confirmer", "✅", False),
    ("app_pages/pfma_confirm_cost_plan.py", "PFMA * Cost Plan Confirmer", "💰", False),
    ("app_pages/pfma_confirm_care_needs.py", "PFMA * Care Needs", "🩺", False),
    ("app_pages/pfma_confirm_care_prefs.py", "PFMA * Care Preferences", "🎯", False),
    ("app_pages/pfma_confirm_household_legal.py", "PFMA * Household & Legal", "🏠", False),
    ("app_pages/pfma_confirm_benefits_coverage.py", "PFMA * Benefits & Coverage", "💳", False),
    ("app_pages/pfma_confirm_personal_info.py", "PFMA * Personal Info", "👤", False),

    # AI + Waiting Room
    ("app_pages/SeniorNav_ai_advisor.py", "AI Advisor", "🤖", False),
    ("app_pages/SeniorNav_waiting_room.py", "Waiting Room", "⏳", False),

    # Utilities
    ("app_pages/SeniorNav_login.py", "Login", "🔐", False),
    ("app_pages/SeniorNav_trusted_partners.py", "Trusted Partners", "🤝", False),
    ("app_pages/SeniorNav_export_details.py", "Export Details", "📤", False),
    ("app_pages/SeniorNav_my_documents.py", "My Documents", "📁", False),
    ("app_pages/SeniorNav_my_account.py", "My Account", "👤", False),
    ("app_pages/SeniorNav_terms.py", "Terms of Use", "📄", False),
    ("app_pages/SeniorNav_privacy.py", "Privacy Policy", "🔒", False),
]

pages = [p for (path, title, icon, default) in INTENDED if (p := ensure_page(path, title, icon, default))]

if pages:
    nav = st.navigation(pages, position="sidebar", expanded=True)
    nav.run()
else:
    st.error("No pages available. Check file paths in app.py.")

# ------------------------------------------
# Sidebar Auth Mock (fixed indentation)
# ------------------------------------------
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
