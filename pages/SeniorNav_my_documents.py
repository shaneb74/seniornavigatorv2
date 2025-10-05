from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
from pages.seniornav_util import top_nav

st.set_page_config(layout="wide", page_title="My Documents")
inject_theme()
top_nav()
st.markdown("## My Documents")
for i in range(1,6):
    st.markdown('<div class="sn-card">', unsafe_allow_html=True)
    st.markdown(f"**Document {i}**")
    st.caption("Uploaded recently")
    cols = st.columns(2)
    cols[0].button("Open", key=f"open_{i}", use_container_width=True)
    cols[1].button("Delete", key=f"del_{i}", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
