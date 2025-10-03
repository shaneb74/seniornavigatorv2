# app.py - header + global CSS injector (full replacement for the opening block)

from __future__ import annotations
import streamlit as st
from pathlib import Path

# ---- Import the theme injector with a safe fallback ----
try:
    # preferred: provided by ui/theme.py
    from ui.theme import inject_theme  # exposes the real CSS and tokens
except Exception:
    # belt-and-suspenders: keep the app running even if ui/theme.py is missing/broken
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

# ========= Global CSS (single source of truth) =========
def _inject_global_css() -> None:
    # Inject the theme once
    inject_theme()

    # Optionally layer a repo-level stylesheet (if present)
    css_path = Path("static/style.css")
    if css_path.exists():
        try:
            extra = css_path.read_text(encoding="utf-8").strip()
        except Exception:
            # If encoding is weird, read bytes and decode permissively
            extra = css_path.read_bytes().decode(errors="ignore").strip()
        # cache-bust by appending file mtime as a comment
        v = int(css_path.stat().st_mtime)
        st.markdown(f"<style>{extra}</style><!-- v:{v} -->", unsafe_allow_html=True)

# Call once on startup (before you render anything)
_inject_global_css()


# ---- PRE-FLIGHT SYNTAX CHECK FOR PAGES ----
def _syntax_preflight(paths=("pages",), stop_on_error=True):
    import pathlib, io, tokenize, ast, streamlit as st
    errors = []
    for root in paths:
        for p in pathlib.Path(root).rglob("*.py"):
            try:
                src = p.read_text(encoding="utf-8")
            except Exception as e:
                errors.append((p, 0, 0, f"read error: {e}", ""))
                continue
            try:
                # Tokenize first to flush out invisible bad chars, then compile
                tokenize.generate_tokens(io.StringIO(src).readline)
                compile(src, str(p), "exec", dont_inherit=True)
            except SyntaxError as e:
                errors.append((p, e.lineno or 0, e.offset or 0, e.msg, e.text or ""))
            except Exception as e:
                # Not syntax, but still fatal at import time
                errors.append((p, 0, 0, f"{type(e).__name__}: {e}", ""))
    if errors:
        st.error("Syntax/parse error(s) found. Fix these before running pages.")
        for p, line, col, msg, txt in errors:
            st.write(f"**{p}**")
            st.code(f"line {line}, col {col}: {msg}\n{txt.rstrip()}\n{' '*(max(col-1,0))}^")
            st.markdown("---")
        if stop_on_error:
            st.stop()

# run it once at startup
_syntax_preflight()

# ========= Simple prototype auth flag (keep your original logic below) =========
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False

# ========= Navigation helpers =========
def ensure_page(path: str, title: str, icon: str, default: bool = False):
    p = Path(path)
    if not p.exists():
        return None, path
    page = (
        st.Page(path, title=title, icon=icon, default=True)
        if default
        else st.Page(path, title=title, icon=icon)
    )
    return page, None

# ========= Pages to register (order controls left-nav order) =========
INTENDED = [
    # Entry & Hub
    ("pages/welcome.py", "Welcome", "👋", True),
    ("pages/hub.py", "Your Concierge Care Hub", "🏠", False),

    # Tell-us flows
    ("pages/tell_us_about_you.py", "Tell Us About You", "ℹ️", False),
    ("pages/tell_us_about_loved_one.py", "Tell Us About Loved One", "ℹ️", False),
    ("pages/professional_mode.py", "Professional Mode", "🧑", False),

    # Guided Care Plan
    ("pages/gcp.py", "Guided Care Plan", "🗺️", False),
    ("pages/gcp_daily_life.py", "GCP - Daily Life & Support", "🗺️", False),
    ("pages/gcp_health_safety.py", "GCP - Health & Safety", "🗺️", False),
    ("pages/gcp_context_prefs.py", "GCP - Context & Preferences", "🗺️", False),
    ("pages/gcp_recommendation.py", "GCP Recommendation", "🗺️", False),

    # Cost Planner
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

    # PFMA + booking
    ("pages/pfma.py", "Plan for My Advisor", "🧭", False),
    ("pages/appointment_booking.py", "Appointment Booking", "📞", False),
    ("pages/appointment_interstitial.py", "Call Scheduled", "⏰", False),
    ("pages/pfma_confirm_care_plan.py", "PFMA • Care Plan Confirmer", "✅", False),
    ("pages/pfma_confirm_cost_plan.py", "PFMA • Cost Plan Confirmer", "💰", False),
    ("pages/pfma_confirm_care_needs.py", "PFMA • Care Needs", "🩺", False),
    ("pages/pfma_confirm_care_prefs.py", "PFMA • Care Preferences", "🎯", False),
    ("pages/pfma_confirm_household_legal.py", "PFMA • Household & Legal", "🏠", False),
    ("pages/pfma_confirm_benefits_coverage.py", "PFMA • Benefits & Coverage", "💳", False),
    ("pages/pfma_confirm_personal_info.py", "PFMA • Personal Info", "👤", False),

    # Misc
    ("pages/login.py", "Login", "🔐", False),
    ("pages/ai_advisor.py", "AI Advisor", "🤖", False),
    ("pages/waiting_room.py", "Waiting Room", "⏳", False),
    ("pages/trusted_partners.py", "Trusted Partners", "🤝", False),
    ("pages/export_results.py", "Export Results", "📥", False),
    ("pages/my_documents.py", "My Documents", "📁", False),
    ("pages/my_account.py", "My Account", "👤", False),
]

pages, missing = [], []
for args in INTENDED:
    page, miss = ensure_page(*args)
    if page:
        pages.append(page)
    if miss:
        missing.append(miss)

if missing:
    st.sidebar.warning("Missing pages detected:\n" + "\n".join(f"- {m}" for m in missing))

if pages:
    pg = st.navigation(pages)
    pg.run()
else:
    st.error("No pages available. Check file paths in app.py.")

# ========= Sidebar login toggle (prototype) =========
with st.sidebar:
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
