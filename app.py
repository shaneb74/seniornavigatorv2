
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="CCA Senior Navigator", layout="centered")

def inject_css(path: str):
    css_path = Path(path)
    if css_path.exists():
        mtime = int(css_path.stat().st_mtime)
        st.markdown(f"<style>{css_path.read_text()}</style><!-- v:{mtime} -->", unsafe_allow_html=True)

inject_css("static/style.css")

def safe_page(path: str, title: str, icon: str):
    p = Path(path)
    if not p.exists():
        return None
    return st.Page(path, title=title, icon=icon)

pages = [
    safe_page("pages/welcome.py", "Welcome", "👋"),
    safe_page("pages/tell_us_about_loved_one.py", "Tell Us About Loved One", "ℹ️"),
    safe_page("pages/tell_us_about_you.py", "Tell Us About You", "ℹ️"),
    safe_page("pages/hub.py", "Hub", "🏠"),
    safe_page("pages/gcp.py", "Guided Care Plan", "🗺️"),
    safe_page("pages/gcp_daily_life.py", "GCP — Daily Life & Support", "🗺️"),
    safe_page("pages/gcp_health_safety.py", "GCP — Health & Safety", "🗺️"),
    safe_page("pages/gcp_context_prefs.py", "GCP — Context & Preferences", "🗺️"),
    safe_page("pages/gcp_recommendation.py", "GCP Recommendation", "🗺️"),
    safe_page("pages/cost_planner.py", "Cost Planner: Mode", "💰"),
    safe_page("pages/cost_planner_estimate.py", "Cost Planner: Estimate", "💰"),
    safe_page("pages/cost_planner_estimate_summary.py", "Cost Planner: Quick Summary", "💰"),
    safe_page("pages/cost_planner_modules.py", "Cost Planner: Modules", "📊"),
    safe_page("pages/cost_planner_evaluation.py", "Cost Planner: Evaluation", "🔍"),
    safe_page("pages/pfma.py", "Plan for My Advisor", "🧭"),
    safe_page("pages/ai_advisor.py", "AI Advisor", "🤖"),
]

pages = [p for p in pages if p is not None]
pg = st.navigation(pages)
pg.run()

with st.sidebar:
    st.subheader("AI Advisor")
    st.write("Ask me anything about your plan...")
    st.text_input("Your question", key="ai_question")
    if st.button("Ask", key="ai_ask", type="primary"):
        st.info("Placeholder response: Here's some advice...")
