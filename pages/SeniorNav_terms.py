from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
from pages.seniornav_util import top_nav

st.set_page_config(layout="wide", page_title="Terms & Conditions")
inject_theme()
top_nav()

st.markdown("## Terms & Conditions")
st.write("These are placeholder Terms & Conditions for Senior Navigator.")
st.write("Replace this text with your actual terms, including acceptable use, warranties, and limitations of liability.")
