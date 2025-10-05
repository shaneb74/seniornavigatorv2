from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
from pages.seniornav_util import ensure_aud, safe_switch, top_nav

st.set_page_config(layout="wide", page_title="Senior Navigator")
inject_theme()
ensure_aud()
top_nav()

st.markdown('<div class="sn-hero">', unsafe_allow_html=True)
st.markdown("## Welcome to Senior Navigator")
st.caption("Find care options, build plans, and get expert guidance.")
st.image("static/images/hero_pfma.jpg", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

cols = st.columns(3)
def card(title, blurb, dest, aria):
    with st.container():
        st.markdown('<div class="sn-card">', unsafe_allow_html=True)
        st.markdown(f"### {title}")
        st.write(blurb)
        if st.button("Open", use_container_width=True):
            safe_switch(dest)
        st.markdown('</div>', unsafe_allow_html=True)

with cols[0]:
    card("Looking for Yourself?", "Find personalized care options for your needs.", "pages/SeniorNav_welcome_self.py", "Start for yourself")
with cols[1]:
    card("Helping a Loved One?", "Support a loved one with a tailored plan.", "pages/SeniorNav_welcome_someone_else.py", "Start for someone else")
with cols[2]:
    card("I’m a Professional", "Manage care plans for your clients.", "pages/SeniorNav_welcome_professional.py", "Start as a professional")
