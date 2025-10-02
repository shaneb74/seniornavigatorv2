
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="CCA Senior Navigator", layout="centered")

def inject_css(path: str):
    p = Path(path)
    if p.exists():
        mtime = int(p.stat().st_mtime)
        st.markdown(f"<style>{p.read_text()}</style><!-- v:{mtime} -->", unsafe_allow_html=True)

inject_css("static/style.css")

def ensure_page(path: str, title: str, icon: str, default: bool=False):
    """Return (Page|None, missing_path|None). Accepts optional default flag."""
    p = Path(path)
    if not p.exists():
        return None, path
    page = st.Page(path, title=title, icon=icon, default=bool(default)) if default else st.Page(path, title=title, icon=icon)
    return page, None

INTENDED = [
    ("pages/welcome.py", "Welcome", "👋", True),
    ("pages/tell_us_about_loved_one.py", "Tell Us About Loved One", "ℹ️", False),
    ("pages/tell_us_about_you.py", "Tell Us About You", "ℹ️", False),
    ("pages/hub.py", "Hub", "🏠", False),
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
    ("pages/expert_review.py", "Expert Review", "🔎", False),
    ("pages/cost_planner_evaluation.py", "Cost Planner: Evaluation", "🔍", False),
    ("pages/cost_planner_home_care.py", "Home Care Support", "🏠", False),
    ("pages/cost_planner_daily_aids.py", "Daily Living Aids", "🛠️", False),
    ("pages/cost_planner_housing.py", "Housing Path", "🏡", False),
    ("pages/cost_planner_benefits.py", "Benefits Check", "💳", False),
    ("pages/cost_planner_mods.py", "Age-in-Place Upgrades", "🔧", False),
    ("pages/cost_planner_skipped.py", "Cost Planner: Skipped", "⚠️", False),
    # PFMA & confirmations
    ("pages/pfma.py", "Plan for My Advisor", "🧭", False),
    ("pages/pfma_confirm_care_plan.py", "PFMA • Care Plan Confirmer", "✅", False),
    ("pages/pfma_confirm_cost_plan.py", "PFMA • Cost Plan Confirmer", "💰", False),
    ("pages/pfma_confirm_care_needs.py", "PFMA • Care Needs", "🩺", False),
    ("pages/pfma_confirm_care_prefs.py", "PFMA • Care Preferences", "🎯", False),
    ("pages/pfma_confirm_household_legal.py", "PFMA • Household & Legal", "🏠", False),
    ("pages/pfma_confirm_benefits_coverage.py", "PFMA • Benefits & Coverage", "💳", False),
    ("pages/pfma_confirm_personal_info.py", "PFMA • Personal Info", "👤", False),
    # Appointments & extras
    ("pages/appointment_booking.py", "Appointment Booking", "📞", False),
    ("pages/appointment_interstitial.py", "Call Scheduled", "⏰", False),
    ("pages/ai_advisor.py", "AI Advisor", "🤖", False),
    ("pages/waiting_room.py", "Waiting Room", "⏳", False),
    ("pages/risk_navigator.py", "Risk Navigator", "🛡️", False),
    ("pages/medication_management.py", "Medication Management", "💊", False),
    ("pages/trusted_partners.py", "Trusted Partners", "🤝", False),
    ("pages/export_results.py", "Export Results", "📥", False),
    ("pages/my_documents.py", "My Documents", "📁", False),
    ("pages/my_account.py", "My Account", "👤", False),
]

pages = []
missing = []
for args in INTENDED:
    page, miss = ensure_page(*args)  # accepts 4-tuple
    if page:
        pages.append(page)
    if miss:
        missing.append(miss)

if missing:
    st.sidebar.warning("Missing pages detected:\n" + "\n".join(f"- {m}" for m in missing))

if not pages:
    st.error("No pages available. Check file paths in app.py.")
else:
    pg = st.navigation(pages)
    pg.run()

with st.sidebar:
    st.subheader("AI Advisor")
    st.write("Ask me anything about your plan...")
    st.text_input("Your question", key="ai_question")
    if st.button("Ask", key="ai_ask", type="primary"):
        st.info("Placeholder response: Here's some advice...")
