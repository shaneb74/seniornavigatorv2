from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
from pages.seniornav_util import top_nav, safe_switch

st.set_page_config(layout="wide", page_title="Trusted Partners")
inject_theme()
top_nav()

st.markdown("## Trusted Partners")
st.subheader("Meet our vetted partners.")
st.write("We carefully select these services for honesty and senior-first care — no ads, no upsell.")

c1, c2 = st.columns(2)

with c1:
    st.markdown("#### Health Plan One")
    st.caption("A Medicare brokerage offering a one-stop shop to compare over 50 plans. Carrier-agnostic, no pushy calls — just clear options.")
    st.write("• Free enrollment support  \n• Price lock tool")
    st.button("Connect", type="primary", use_container_width=True)

with c2:
    st.markdown("#### Senior Life AI")
    st.caption("AI-driven tests for cognitive decline and fall prediction, using your phone camera for early insights.")
    st.write("• Quick cognitive check  \n• Fall-risk predictor")
    st.button("Start Test", type="primary", use_container_width=True)

with c1:
    st.markdown("#### PillSync")
    st.caption("Medication management with daily reminders, interaction alerts, and one-tap reordering — no spam.")
    st.write("• Custom reminders  \n• Interaction checks")
    st.button("Sign Up Free", type="primary", use_container_width=True)

with c2:
    st.markdown("#### Longevity Link")
    st.caption("Long-term care coverage for home help, memory care, and hospice — lock in rates before they rise.")
    st.write("• Covers home and facility care  \n• Price stability")
    st.button("Get Quote", type="primary", use_container_width=True)

st.divider()
if st.button("Back to Waiting Room", use_container_width=True):
    safe_switch("pages/SeniorNav_waiting_room.py")
