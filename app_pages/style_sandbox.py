import streamlit as st

from ui.theme import inject_theme

inject_theme()

from ui.pfma import render_drawer as pfma_drawer, segmented_control as pfma_seg, ensure_pfma_state
from ui.cost_planner_template import render_drawer as cp_drawer, segmented_control as cp_seg, ensure_cp_state, NavButton, render_nav_buttons

st.title("Style Sandbox")

st.subheader("Tokens")
import ui.theme as ut

st.json(ut.TOKENS)

st.divider()
st.subheader("PFMA Drawer")
ensure_pfma_state()
def _pfma_body(state):
    d = state.get("sections", {}).get("demo", {}).get("data", {})
    pfma_seg("Marital status", ("Single","Married/partnered","Widowed","Divorced"),
             key="demo_marital", default=d.get("marital_status"))
    return {"marital_status": st.session_state.get("pfma_segment_demo_marital")}
r1 = pfma_drawer(step_key="demo", title="Household & Legal 🏠",
                 description="PFMA drawer demo", body=_pfma_body,
                 footer_note="Shared visual chrome from theme.")
st.write(dict(saved=r1.saved, payload=r1.payload, next=r1.next_step))

st.divider()
st.subheader("Cost Planner Drawer")
ensure_cp_state()
def _cp_body(state):
    d = state.get("sections", {}).get("demo", {}).get("data", {})
    cp_seg("Care level", ("Companion","HHA","LPN","RN"), key="demo_level", default=d.get("level"))
    return {"level": st.session_state.get("cp_segment_demo_level")}
r2 = cp_drawer(step_key="demo", title="Care staffing & services",
               description="CP drawer demo", body=_cp_body, badge="Draft estimate")
st.write(dict(saved=r2.saved, payload=r2.payload, next=r2.next_step))

st.divider()
st.subheader("Nav Buttons")
render_nav_buttons(buttons=[
    NavButton("Back", "nav_back", type="secondary"),
    NavButton("Next", "nav_next", type="primary", icon="➡️"),
])
