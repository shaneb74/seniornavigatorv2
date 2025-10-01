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
cost_planner = st.Page("pages/cost_planner.py", title="Cost Planner", icon="💰")
smart_review = st.Page("pages/smart_review.py", title="Smart Review", icon="🔍")
pfma = st.Page("pages/pfma.py", title="Plan for My Advisor", icon="📅")
exports = st.Page("pages/exports.py", title="Exports", icon="📤")

# Configure navigation
pages = [welcome, hub, gcp, cost_planner, smart_review, pfma, exports]
pg = st.navigation(pages)

# Run the selected page
pg.run()

# Common elements: AI Advisor in sidebar
with st.sidebar:
    st.subheader("AI Advisor")
    st.write("Ask me anything about your plan...")
    st.text_input("Your question", key="ai_question")
    if st.button("Ask", type="primary"):
        st.info("Placeholder response: Here's some advice...")
