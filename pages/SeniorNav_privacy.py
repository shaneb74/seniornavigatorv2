from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
from pages.seniornav_util import top_nav

st.set_page_config(layout="wide", page_title="Privacy Policy")
inject_theme()
top_nav()

st.markdown("## Privacy Policy")
st.write("This is a placeholder Privacy Policy for Senior Navigator.")
st.write("Replace this text with your actual policy covering data collection, use, storage, and user rights.")
