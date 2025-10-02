
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="CCA Senior Navigator", layout="centered")

def inject_css(path: str):
    css_path = Path(path)
    if css_path.exists():
        mtime = int(css_path.stat().st_mtime)
        st.markdown(f"<style>{css_path.read_text()}</style><!-- v:{mtime} -->", unsafe_allow_html=True)
    else:
        st.warning(f"Missing CSS: {path}")

inject_css("static/style.css")

# Minimal set shown here for clarity; keep your broader list if you have one.
welcome = st.Page("pages/welcome.py", title="Welcome", icon="👋")
tell_us_loved = st.Page("pages/tell_us_about_loved_one.py", title="Tell Us About Loved One", icon="ℹ️")
tell_us_you = st.Page("pages/tell_us_about_you.py", title="Tell Us About You", icon="ℹ️")
hub = st.Page("pages/hub.py", title="Hub", icon="🏠")

# Guided Care Plan
gcp = st.Page("pages/gcp.py", title="Guided Care Plan", icon="🗺️")
gcp_daily = st.Page("pages/gcp_daily_life.py", title="GCP — Daily Life & Support", icon="🗺️")
gcp_health = st.Page("pages/gcp_health_safety.py", title="GCP — Health & Safety", icon="🗺️")
gcp_context = st.Page("pages/gcp_context_prefs.py", title="GCP — Context & Preferences", icon="🗺️")
gcp_reco = st.Page("pages/gcp_recommendation.py", title="GCP Recommendation", icon="🗺️")

# Cost Planner
cost_planner_mode = st.Page("pages/cost_planner.py", title="Cost Planner: Mode", icon="💰")
cost_planner_estimate = st.Page("pages/cost_planner_estimate.py", title="Cost Planner: Estimate", icon="💰")
cost_planner_estimate_summary = st.Page("pages/cost_planner_estimate_summary.py", title="Cost Planner: Quick Summary", icon="💰")
cost_planner_modules = st.Page("pages/cost_planner_modules.py", title="Cost Planner: Modules", icon="📊")
cost_planner_evaluation = st.Page("pages/cost_planner_evaluation.py", title="Cost Planner: Evaluation", icon="🔍")

# Extras
pfma = st.Page("pages/pfma.py", title="Plan for My Advisor", icon="🧭")
ai_advisor = st.Page("pages/ai_advisor.py", title="AI Advisor", icon="🤖")

pages = [
    welcome, tell_us_loved, tell_us_you, hub,
    gcp, gcp_daily, gcp_health, gcp_context, gcp_reco,
    cost_planner_mode, cost_planner_estimate, cost_planner_estimate_summary, cost_planner_modules, cost_planner_evaluation,
    pfma, ai_advisor
]

pg = st.navigation(pages)
pg.run()

with st.sidebar:
    st.subheader("AI Advisor")
    st.write("Ask me anything about your plan...")
    st.text_input("Your question", key="ai_question")
    if st.button("Ask", key="ai_ask", type="primary"):
        st.info("Placeholder response: Here's some advice...")
