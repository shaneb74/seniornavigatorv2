
import streamlit as st
from pathlib import Path
import re

st.set_page_config(page_title="CCA Senior Navigator", layout="centered")

def inject_css(path: str):
    css_path = Path(path)
    if css_path.exists():
        mtime = int(css_path.stat().st_mtime)
        st.markdown(f"<style>{css_path.read_text()}</style><!-- v:{mtime} -->", unsafe_allow_html=True)

inject_css("static/style.css")

# ---------- Safe registration ----------
def ensure_page(path: str, title: str, icon: str):
    p = Path(path)
    if not p.exists():
        return None
    return st.Page(path, title=title, icon=icon)

INTENDED = [
    ("pages/welcome.py", "Welcome", "👋"),
    ("pages/tell_us_about_loved_one.py", "Tell Us About Loved One", "ℹ️"),
    ("pages/tell_us_about_you.py", "Tell Us About You", "ℹ️"),
    ("pages/hub.py", "Hub", "🏠"),
    # GCP
    ("pages/gcp.py", "Guided Care Plan", "🗺️"),
    ("pages/gcp_daily_life.py", "GCP — Daily Life & Support", "🗺️"),
    ("pages/gcp_health_safety.py", "GCP — Health & Safety", "🗺️"),
    ("pages/gcp_context_prefs.py", "GCP — Context & Preferences", "🗺️"),
    ("pages/gcp_recommendation.py", "GCP Recommendation", "🗺️"),
    # Cost Planner
    ("pages/cost_planner.py", "Cost Planner: Mode", "💰"),
    ("pages/cost_planner_estimate.py", "Cost Planner: Estimate", "💰"),
    ("pages/cost_planner_estimate_summary.py", "Cost Planner: Quick Summary", "💰"),
    ("pages/cost_planner_modules.py", "Cost Planner: Modules", "📊"),
    ("pages/expert_review.py", "Expert Review", "🔎"),  # NEW
    ("pages/cost_planner_evaluation.py", "Cost Planner: Evaluation", "🔍"),
    ("pages/cost_planner_home_care.py", "Home Care Support", "🏠"),
    ("pages/cost_planner_daily_aids.py", "Daily Living Aids", "🛠️"),
    ("pages/cost_planner_housing.py", "Housing Path", "🏡"),
    ("pages/cost_planner_benefits.py", "Benefits Check", "💳"),
    ("pages/cost_planner_mods.py", "Age-in-Place Upgrades", "🔧"),
    ("pages/cost_planner_skipped.py", "Cost Planner: Skipped", "⚠️"),
    # PFMA & extras
    ("pages/appointment_booking.py", "Appointment Booking", "📞"),
    ("pages/appointment_interstitial.py", "Call Scheduled", "⏰"),
    ("pages/pfma.py", "Plan for My Advisor", "🧭"),
    ("pages/ai_advisor.py", "AI Advisor", "🤖"),
    ("pages/waiting_room.py", "Waiting Room", "⏳"),
    ("pages/risk_navigator.py", "Risk Navigator", "🛡️"),
    ("pages/medication_management.py", "Medication Management", "💊"),
    ("pages/trusted_partners.py", "Trusted Partners", "🤝"),
    ("pages/export_results.py", "Export Results", "📥"),
    ("pages/my_documents.py", "My Documents", "📁"),
    ("pages/my_account.py", "My Account", "👤"),
]

pages = [p for p in (ensure_page(*triple) for triple in INTENDED) if p is not None]
pg = st.navigation(pages)
pg.run()

with st.sidebar:
    st.subheader("AI Advisor")
    st.write("Ask me anything about your plan...")
    st.text_input("Your question", key="ai_question")
    if st.button("Ask", key="ai_ask", type="primary"):
        st.info("Placeholder response: Here's some advice...")
