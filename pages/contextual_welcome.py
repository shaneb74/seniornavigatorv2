import streamlit as st

from ui.theme import inject_theme

st.set_page_config(layout="wide")

inject_theme()

# pages/contextual_welcome.py
from pages.contextual_welcome_base import render

# Keep old links working by showing the "For You" variant.
# (Change to render("loved") if you ever want it to default to the Loved Ones view.)
render("you")
