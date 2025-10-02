
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="CCA Senior Navigator", layout="centered")

# ============== Global CSS ==============
STYLES = """
<style>
:root {
  --cca-blue: #0B5CD8;
  --cca-black: #000000;
}

/* Primary CTA button: Blue */
div.stButton > button:first-child {
  background-color: var(--cca-blue);
  color: #fff;
  font-size: 20px;
  font-weight: 600;
  border-radius: 12px;
  padding: 0.6rem 1.2rem;
  border: none;
}

/* Secondary button: Black */
div.stButton.secondary > button:first-child {
  background-color: var(--cca-black);
  color: #fff;
  font-size: 20px;
  font-weight: 600;
  border-radius: 12px;
  padding: 0.6rem 1.2rem;
  border: none;
}

/* Hover effect */
div.stButton > button:first-child:hover {
  opacity: 0.92;
}

/* Radios & checkboxes accent color */
input[type="radio"], input[type="checkbox"] {
  accent-color: var(--cca-blue);
}

/* Segmented control: pill buttons */
div[data-testid="stSegmentedControl"] > div {
  gap: 10px;
}
div[data-testid="stSegmentedControl"] button {
  border-radius: 9999px !important;
  padding: 10px 16px !important;
  font-weight: 600 !important;
  border: 1px solid rgba(0,0,0,0.08) !important;
  background: #f8fafc !important;
  color: #1f2937 !important;
}
div[data-testid="stSegmentedControl"] button[aria-checked="true"] {
  background: var(--cca-blue) !important;
  color: #fff !important;
  border-color: var(--cca-blue) !important;
}
</style>
"""
st.markdown(STYLES, unsafe_allow_html=True)

# Simple prototype auth flag
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False

def ensure_page(path: str, title: str, icon: str, default: bool=False):
    p = Path(path)
    if not p.exists():
        return None, path
    page = st.Page(path, title=title, icon=icon, default=bool(default)) if default else st.Page(path, title=title, icon=icon)
    return page, None

# Register broad set so nav isn't truncated
INTENDED = [
    # Entry & Hub
    ("pages/welcome.py", "Welcome", "👋", True),
    ("pages/hub.py", "Your Concierge Care Hub", "🏠", False),

    # Tell-us flows
    ("pages/tell_us_about_you.py", "Tell Us About You", "ℹ️", False),
    ("pages/tell_us_about_loved_one.py", "Tell Us About Loved One", "ℹ️", False),
    ("pages/professional_mode.py", "Professional Mode", "🧑‍⚕️", False),

    # Guided Care Plan
    ("pages/gcp.py", "Guided Care Plan", "🗺️", False),
    ("pages/gcp_daily_life.py", "GCP — Daily Life & Support", "🗺️", False),
    ("pages/gcp_health_safety.py", "GCP — Health & Safety", "🗺️", False),
    ("pages/gcp_context_prefs.py", "GCP — Context & Preferences", "🗺️", False),
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
    if page: pages.append(page)
    if miss: missing.append(miss)

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
