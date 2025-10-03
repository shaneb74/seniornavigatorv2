"""Streamlit page shim that redirects to the Welcome flow."""

import streamlit as st

from audiencing import *  # noqa: F401,F403

st.switch_page("pages/welcome.py")
