"""Entry point for the Senior Care Navigator Streamlit app."""
from __future__ import annotations

import streamlit as st

st.set_page_config(page_title="Senior Care Navigator", layout="wide")

st.page_link("pages/welcome.py", label="Welcome", icon="✨")
st.page_link("pages/welcome.py", label="Start", icon="🏠")
st.page_link("pages/contextual_welcome.py", label="Contextual Welcome", icon="👋")
st.page_link("pages/hub.py", label="Care Planning Hub", icon="🧭")
st.page_link("pages/gcp.py", label="Guided Care Plan", icon="🩺")
st.page_link("pages/gcp_recommendation.py", label="Recommendation", icon="✅")
st.page_link("ui/pages/03_cost_planner.py", label="Cost Planner", icon="💰")
st.page_link("ui/pages/04_smart_review.py", label="Smart Review", icon="🧠")
st.page_link("pages/pfma.py", label="Plan for My Advisor", icon="📘")
