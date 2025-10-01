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
hub = st.Page("pages/hub.py", title="Hub", icon="🏠")
gcp = st.Page("pages/gcp.py", title="Guided Care Plan", icon="🗺️")
cost_planner_mode = st.Page("pages/cost_planner_mode.py", title="Cost Planner: Mode", icon="💰")
cost_planner_modules = st.Page("pages/cost_planner_modules.py", title="Cost Planner: Modules", icon="📊")
cost_planner_home_care = st.Page("pages/cost_planner_home_care.py", title="Home Care Support", icon="🏠")
cost_planner_daily_aids = st.Page("pages/cost_planner_daily_aids.py", title="Daily Living Aids", icon="🛠️")
cost_planner_housing = st.Page("pages/cost_planner_housing.py", title="Housing Path", icon="🏡")
cost_planner_benefits = st.Page("pages/cost_planner_benefits.py", title="Benefits Check", icon="💳")
cost_planner_mods = st.Page("pages/cost_planner_mods.py", title="Age-in-Place Upgrades", icon="🔧")
cost_planner_evaluation = st.Page("pages/cost_planner_evaluation.py", title="Cost Planner: Evaluation", icon="🔍")
cost_planner_skipped = st.Page("pages/cost_planner_skipped.py", title="Cost Planner: Skipped", icon="⚠️")
pfma = st.Page("pages/pfma.py", title="Plan for My Advisor", icon="📅")
exports = st.Page("pages/exports.py", title="Exports", icon="📤")

# Configure navigation
pages = [welcome, hub, gcp, cost_planner_mode, cost_planner_modules, cost_planner_home_care, cost_planner_daily_aids, cost_planner_housing, cost_planner_benefits, cost_planner_mods, cost_planner_evaluation, cost_planner_skipped, pfma, exports]
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
