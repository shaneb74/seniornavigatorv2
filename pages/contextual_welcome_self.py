import streamlit as st
st.set_page_config(layout='wide', page_title='Welcome · For You')

from ui.theme import inject_theme
inject_theme()

# pages/contextual_welcome_self.py
try:
    from pages.contextual_welcome_base import render  # Streamlit package import
except Exception:
    from pages.contextual_welcome_base import render        # fallback when executed directly
render("you")
