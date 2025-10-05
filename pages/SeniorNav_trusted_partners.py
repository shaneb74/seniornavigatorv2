from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
from pages.seniornav_util import top_nav

st.set_page_config(layout="wide", page_title="Trusted Partners")
inject_theme()
top_nav()
st.markdown("## Trusted Partners")
cols = st.columns(2)
for i in range(1,5):
    with cols[i%2]:
        st.markdown('<div class="sn-card">', unsafe_allow_html=True)
        st.markdown(f"### Partner {i}")
        st.caption("Services and contact details")
        st.button("View", key=f"partner_{i}", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
