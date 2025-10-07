from __future__ import annotations
import streamlit as st
from app_pages.seniornav_util import top_nav, safe_switch
top_nav()

st.markdown("## Your Waiting Room")
st.subheader("Relax, explore, get ready.")
st.write("While you wait for your call, check out these options.")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("#### Trivia Time")
    st.caption("Fun fact: Did you know 1 in 5 seniors miss a med dose? Click for a tip!")
    st.button("Get Tip", width="stretch")

with c2:
    st.markdown("#### Partner Spotlight")
    st.caption("Explore our trusted partners — vetted for your peace of mind.")
    if st.button("See All Partners", width="stretch"):
        safe_switch("pages/SeniorNav_trusted_partners.py")

with c3:
    st.markdown("#### Second Opinion")
    st.caption("Get a quick geriatrics review before your call — no cost.")
    st.button("Chat Now", width="stretch")

st.divider()
if st.button("Back to Hub", width="stretch"):
    safe_switch("pages/guided_care_hub.py")
