
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="CCA Senior Navigator", layout="centered")

# ------------------------------
# Global CSS styling for buttons
# ------------------------------
STYLES = """
<style>
/* Primary CTA button: Blue */
div.stButton > button:first-child {
    background-color: #0B5CD8;
    color: white;
    font-size: 20px;
    font-weight: 600;
    border-radius: 12px;
    padding: 0.6em 1.2em;
    border: none;
}

/* Secondary button: Black */
div.stButton.secondary > button:first-child {
    background-color: #000000;
    color: white;
    font-size: 20px;
    font-weight: 600;
    border-radius: 12px;
    padding: 0.6em 1.2em;
    border: none;
}

/* Hover effect */
div.stButton > button:first-child:hover {
    opacity: 0.9;
}
</style>
"""
st.markdown(STYLES, unsafe_allow_html=True)

# ------------------------------
# Auth flag placeholder
# ------------------------------
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False

def ensure_page(path: str, title: str, icon: str, default: bool=False):
    p = Path(path)
    if not p.exists():
        return None, path
    page = st.Page(path, title=title, icon=icon, default=bool(default)) if default else st.Page(path, title=title, icon=icon)
    return page, None

INTENDED = [
    ("pages/welcome.py", "Welcome", "👋", True),
    ("pages/hub.py", "Hub", "🏠", False),
    ("pages/gcp.py", "Guided Care Plan", "🗺️", False),
    ("pages/gcp_daily_life.py", "GCP — Daily Life & Support", "🗺️", False),
    ("pages/gcp_health_safety.py", "GCP — Health & Safety", "🗺️", False),
    ("pages/gcp_context_prefs.py", "GCP — Context & Preferences", "🗺️", False),
    ("pages/gcp_recommendation.py", "GCP Recommendation", "🗺️", False),
    ("pages/cost_planner.py", "Cost Planner: Mode", "💰", False),
    ("pages/cost_planner_modules.py", "Cost Planner: Modules", "📊", False),
    ("pages/expert_review.py", "Expert Review", "🔎", False),
    ("pages/pfma.py", "Plan for My Advisor", "🧭", False),
    ("pages/appointment_booking.py", "Appointment Booking", "📞", False),
    ("pages/login.py", "Login", "🔐", False),
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

# Sidebar login toggle
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
