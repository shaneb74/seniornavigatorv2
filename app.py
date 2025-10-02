
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="CCA Senior Navigator", layout="centered")

def inject_css(path: str):
    css_path = Path(path)
    if css_path.exists():
        mtime = int(css_path.stat().st_mtime)
        st.markdown(f"<style>{css_path.read_text()}</style><!-- v:{mtime} -->", unsafe_allow_html=True)

inject_css("static/style.css")

def ensure_page(path: str, title: str, icon: str):
    p = Path(path)
    if not p.exists():
        return None
    return st.Page(path, title=title, icon=icon)

pages = [p for p in [
    ensure_page("pages/welcome.py", "Welcome", "👋"),
    ensure_page("pages/tell_us_about_loved_one.py", "Tell Us About Loved One", "ℹ️"),
    ensure_page("pages/tell_us_about_you.py", "Tell Us About You", "ℹ️"),
    ensure_page("pages/hub.py", "Hub", "🏠"),
    ensure_page("pages/gcp.py", "Guided Care Plan", "🗺️"),
    ensure_page("pages/gcp_daily_life.py", "GCP — Daily Life & Support", "🗺️"),
    ensure_page("pages/gcp_health_safety.py", "GCP — Health & Safety", "🗺️"),
    ensure_page("pages/gcp_context_prefs.py", "GCP — Context & Preferences", "🗺️"),
    ensure_page("pages/gcp_recommendation.py", "GCP Recommendation", "🗺️"),
    ensure_page("pages/cost_planner.py", "Cost Planner: Mode", "💰"),
    ensure_page("pages/cost_planner_estimate.py", "Cost Planner: Estimate", "💰"),
    ensure_page("pages/cost_planner_estimate_summary.py", "Cost Planner: Quick Summary", "💰"),
    ensure_page("pages/cost_planner_modules.py", "Cost Planner: Modules", "📊"),
    ensure_page("pages/expert_review.py", "Expert Review", "🔎"),
    ensure_page("pages/cost_planner_evaluation.py", "Cost Planner: Evaluation", "🔍"),
    ensure_page("pages/care_plan_confirm.py", "Care Plan Confirmation", "✅"),
    ensure_page("pages/care_needs.py", "Care Needs & Support", "🩺"),
    ensure_page("pages/care_prefs.py", "Care Preferences", "🎯"),
    ensure_page("pages/household_legal.py", "Household & Legal", "🏠"),
    ensure_page("pages/benefits_coverage.py", "Benefits & Coverage", "💳"),
    ensure_page("pages/personal_info.py", "Personal Info", "👤"),
    ensure_page("pages/pfma.py", "Plan for My Advisor", "🧭"),
    ensure_page("pages/pfma_confirm_care_plan.py", "PFMA • Care Plan Confirmer", "✅"),
    ensure_page("pages/pfma_confirm_cost_plan.py", "PFMA • Cost Plan Confirmer", "💰"),
    ensure_page("pages/pfma_confirm_care_needs.py", "PFMA • Care Needs", "🩺"),
    ensure_page("pages/pfma_confirm_care_prefs.py", "PFMA • Care Preferences", "🎯"),
    ensure_page("pages/pfma_confirm_household_legal.py", "PFMA • Household & Legal", "🏠"),
    ensure_page("pages/pfma_confirm_benefits_coverage.py", "PFMA • Benefits & Coverage", "💳"),
    ensure_page("pages/pfma_confirm_personal_info.py", "PFMA • Personal Info", "👤"),
    ensure_page("pages/appointment_booking.py", "Appointment Booking", "📞"),
    ensure_page("pages/appointment_interstitial.py", "Call Scheduled", "⏰"),
    ensure_page("pages/pfma.py", "Plan for My Advisor", "🧭"),
    ensure_page("pages/ai_advisor.py", "AI Advisor", "🤖"),
    ensure_page("pages/waiting_room.py", "Waiting Room", "⏳"),
    ensure_page("pages/risk_navigator.py", "Risk Navigator", "🛡️"),
    ensure_page("pages/medication_management.py", "Medication Management", "💊"),
    ensure_page("pages/trusted_partners.py", "Trusted Partners", "🤝"),
    ensure_page("pages/export_results.py", "Export Results", "📥"),
    ensure_page("pages/my_documents.py", "My Documents", "📁"),
    ensure_page("pages/my_account.py", "My Account", "👤"),
] if p is not None]

pg = st.navigation(pages)
pg.run()

with st.sidebar:
    st.subheader("AI Advisor")
    st.write("Ask me anything about your plan...")
    st.text_input("Your question", key="ai_question")
    if st.button("Ask", key="ai_ask", type="primary"):
        st.info("Placeholder response: Here's some advice...")
