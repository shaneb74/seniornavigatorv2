"""Streamlit page shim that redirects to the Welcome flow."""

import streamlit as st
from app_pages.audiencing import *  # noqa: F401,F403

st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

st.switch_page("pages/welcome.py")

st.markdown('</div>', unsafe_allow_html=True)
