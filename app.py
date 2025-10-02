
import streamlit as st
from pathlib import Path

# Set page config for centered layout
st.set_page_config(page_title="CCA Senior Navigator", layout="centered")

# CSS Injection for Streamlit Cloud
def inject_css(path: str):
    css_path = Path(path)
    if css_path.exists():
        mtime = int(css_path.stat().st_mtime)
        st.markdown(f"<style>{css_path.read_text()}</style><!-- v:{mtime} -->", unsafe_allow_html=True)
    else:
        st.warning(f"Missing CSS: {path}")

# Load CSS
inject_css("static/style.css")

# Define pages
welcome = st.Page("pages/welcome.py", title="Welcome", icon="👋")

# Use the correct Loved One/You pages (no 'john' file)
tell_us_loved = st.Page("pages/tell_us_about_loved_one.py", title="Tell Us About Loved One", icon="ℹ️")
tell_us_you = st.Page("pages/tell_us_about_you.py", title="Tell Us About You", icon="ℹ️")

hub = st.Page("pages/hub.py", title="Hub", icon="🏠")

# Guided Care Plan flow (entry + 3 subsections + recommendation)
gcp = st.Page("pages/gcp.py", title="Guided Care Plan", icon="🗺️")
gcp_daily = st.Page("pages/gcp_daily_life.py", title="GCP — Daily Life & Support", icon="🗺️")
gcp_health = st.Page("pages/gcp_health_safety.py", title="GCP — Health & Safety", icon="🗺️")
gcp_context = st.Page("pages/gcp_context_prefs.py", title="GCP — Context & Preferences", icon="🗺️")
gcp_reco = st.Page("pages/gcp_recommendation.py", title="GCP Recommendation", icon="🗺️")

# Cost Planner
cost_planner_mode = st.Page("pages/cost_planner.py", title="Cost Planner: Mode", icon="💰")
cost_planner_modules = st.Page("pages/cost_planner_modules.py", title="Cost Planner: Modules", icon="📊")
cost_planner_home_care = st.Page("pages/cost_planner_home_care.py", title="Home Care Support", icon="🏠")
cost_planner_daily_aids = st.Page("pages/cost_planner_daily_aids.py", title="Daily Living Aids", icon="🛠️")
cost_planner_housing = st.Page("pages/cost_planner_housing.py", title="Housing Path", icon="🏡")
cost_planner_benefits = st.Page("pages/cost_planner_benefits.py", title="Benefits Check", icon="💳")
cost_planner_mods = st.Page("pages/cost_planner_mods.py", title="Age-in-Place Upgrades", icon="🔧")
cost_planner_evaluation = st.Page("pages/cost_planner_evaluation.py", title="Cost Planner: Evaluation", icon="🔍")
cost_planner_skipped = st.Page("pages/cost_planner_skipped.py", title="Cost Planner: Skipped", icon="⚠️")

appointment_booking = st.Page("pages/appointment_booking.py", title="Appointment Booking", icon="📞")
appointment_interstitial = st.Page("pages/appointment_interstitial.py", title="Call Scheduled", icon="⏰")

care_plan_confirm = st.Page("pages/care_plan_confirm.py", title="Care Plan Confirmation", icon="✅")
cost_plan_confirm = st.Page("pages/cost_plan_confirm.py", title="Cost Plan Confirmation", icon="💰")
care_needs = st.Page("pages/care_needs.py", title="Care Needs & Support", icon="🩺")
care_prefs = st.Page("pages/care_prefs.py", title="Care Preferences", icon="🎯")
household_legal = st.Page("pages/household_legal.py", title="Household & Legal", icon="🏠")
benefits_coverage = st.Page("pages/benefits_coverage.py", title="Benefits & Coverage", icon="💳")
personal_info = st.Page("pages/personal_info.py", title="Personal Info", icon="👤")

ai_advisor = st.Page("pages/ai_advisor.py", title="AI Advisor", icon="🤖")
waiting_room = st.Page("pages/waiting_room.py", title="Waiting Room", icon="⏳")
risk_navigator = st.Page("pages/risk_navigator.py", title="Risk Navigator", icon="🛡️")
medication_management = st.Page("pages/medication_management.py", title="Medication Management", icon="💊")
trusted_partners = st.Page("pages/trusted_partners.py", title="Trusted Partners", icon="🤝")

export_results = st.Page("pages/export_results.py", title="Export Results", icon="📥")
my_documents = st.Page("pages/my_documents.py", title="My Documents", icon="📁")
my_account = st.Page("pages/my_account.py", title="My Account", icon="👤")

# Optional PFMA page
pfma = st.Page('pages/pfma.py', title='Plan for My Advisor', icon="🧭")

# Configure navigation
pages = [
    # Entry and profile capture
    welcome, tell_us_loved, tell_us_you, hub,

    # Guided Care Plan flow
    gcp, gcp_daily, gcp_health, gcp_context, gcp_reco,

    # Cost Planner
    cost_planner_mode, cost_planner_modules, cost_planner_home_care, cost_planner_daily_aids,
    cost_planner_housing, cost_planner_benefits, cost_planner_mods, cost_planner_evaluation,
    cost_planner_skipped, cost_plan_confirm,

    # Plan confirmation and details
    care_plan_confirm, care_needs, care_prefs, household_legal, benefits_coverage, personal_info,

    # Appointments and PFMA
    appointment_booking, appointment_interstitial, pfma,

    # Tools and extras
    ai_advisor, waiting_room, risk_navigator, medication_management, trusted_partners,

    # Output and account
    export_results, my_documents, my_account,
]

pg = st.navigation(pages)

# Run the selected page
pg.run()

# Common elements: AI Advisor in sidebar
with st.sidebar:
    st.subheader("AI Advisor")
    st.write("Ask me anything about your plan...")
    st.text_input("Your question", key="ai_question")
    if st.button("Ask", key="ai_ask", type="primary"):
        st.info("Placeholder response: Here's some advice...")
