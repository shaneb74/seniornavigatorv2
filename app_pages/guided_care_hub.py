from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
st.set_page_config(layout='wide', page_title='Guided Care Hub')
inject_theme()
st.markdown('## Guided Care Hub')
