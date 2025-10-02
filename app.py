
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="CCA Senior Navigator", layout="centered")

# ------------------------------
# Global safe switch_page wrapper
# ------------------------------
def _safe_switch_page(target: str, fallback: str = "pages/hub.py"):
    """Wrap st.switch_page to avoid hard crashes when a page isn't registered or missing."""
    # Normalize: only allow pages/ targets
    if not isinstance(target, str):
        st.error("Invalid navigation target.")
        return
    if not target.startswith("pages/"):
        # Don't allow jumping to root stray files
        target = fallback

    # If target file doesn't exist on disk, prefer fallback
    if not Path(target).exists():
        if Path(fallback).exists():
            target = fallback
        else:
            st.error("Navigation target is unavailable in this build.")
            return

    # Try the original switch_page; fall back to Hub if registration is missing
    try:
        st._orig_switch_page(target)  # type: ignore[attr-defined]
    except Exception:
        if target != fallback and Path(fallback).exists():
            try:
                st._orig_switch_page(fallback)  # type: ignore[attr-defined]
                return
            except Exception:
                pass
        st.error("Could not navigate. Use the sidebar to reach the Hub.")

# Monkey‑patch once
if not hasattr(st, "_orig_switch_page"):
    st._orig_switch_page = st.switch_page  # type: ignore[attr-defined]
    st.switch_page = _safe_switch_page     # type: ignore[assignment]

# ------------------------------
# Prototype auth flag
# ------------------------------
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False

def ensure_page(path: str, title: str, icon: str, default: bool=False):
    p = Path(path)
    if not p.exists():
        return None, path
    page = st.Page(path, title=title, icon=icon, default=bool(default)) if default else st.Page(path, title=title, icon=icon)
    return page, None

# Register the pages you navigate to from Hub and Welcome
INTENDED = [
    ("pages/welcome.py", "Welcome", "👋", True),
    ("pages/hub.py", "Your Concierge Care Hub", "🏠", False),
    ("pages/gcp.py", "Guided Care Plan", "🗺️", False),
    ("pages/gcp_daily_life.py", "GCP — Daily Life & Support", "🗺️", False),
    ("pages/gcp_health_safety.py", "GCP — Health & Safety", "🗺️", False),
    ("pages/gcp_context_prefs.py", "GCP — Context & Preferences", "🗺️", False),
    ("pages/gcp_recommendation.py", "GCP Recommendation", "🗺️", False),
    ("pages/tell_us_about_you.py", "Tell Us About You", "ℹ️", False),
    ("pages/tell_us_about_loved_one.py", "Tell Us About Loved One", "ℹ️", False),
    ("pages/professional_mode.py", "Professional Mode", "🧑‍⚕️", False),
    ("pages/cost_planner.py", "Cost Planner: Mode", "💰", False),
    ("pages/cost_planner_modules.py", "Cost Planner: Modules", "📊", False),
    ("pages/cost_planner_estimate.py", "Cost Planner: Estimate", "💰", False),
    ("pages/cost_planner_estimate_summary.py", "Cost Planner: Quick Summary", "💰", False),
    ("pages/expert_review.py", "Expert Review", "🔎", False),
    ("pages/pfma.py", "Plan for My Advisor", "🧭", False),
    ("pages/appointment_booking.py", "Appointment Booking", "📞", False),
    ("pages/appointment_interstitial.py", "Call Scheduled", "⏰", False),
    ("pages/ai_advisor.py", "AI Advisor", "🤖", False),
    ("pages/medication_management.py", "Medication Management", "💊", False),
    ("pages/risk_navigator.py", "Risk Navigator", "🛡️", False),
]

pages = []
missing = []
for args in INTENDED:
    page, miss = ensure_page(*args)
    if page:
        pages.append(page)
    if miss:
        missing.append(miss)

if missing:
    st.sidebar.warning("Missing pages detected:\n" + "\n".join(f"- " + m for m in missing))

if pages:
    pg = st.navigation(pages)
    pg.run()
else:
    st.error("No pages available. Check file paths in app.py.")

# Sidebar auth toggle at bottom
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
