"""Cost Planner entry screen with unified TurboTax-style design."""

from __future__ import annotations

import streamlit as st

from cost_planner_shared import (
    audiencing_badges,
    ensure_core_state,
    format_currency,
    get_numeric,
    recompute_costs,
    set_numeric,
)

ensure_core_state()
cp = st.session_state["cost_planner"]
aud = st.session_state["audiencing"]
gcp = st.session_state.get("gcp", {})
qualifiers = aud.get("qualifiers", {})

st.set_page_config(page_title="Cost Planner", layout="wide")

st.markdown("""
<h2 style="text-transform:uppercase; letter-spacing:0.08em; color:#6b7280; font-size:0.95rem;">Cost Planner</h2>
<h1 style="margin-bottom:0.4rem;">Understand the costs</h1>
<p style="max-width:660px; color:#475569;">Assess the cost structure across options. The estimate will update as you go.</p>
""", unsafe_allow_html=True)

entry, badges = audiencing_badges()
alert = [f"Planning for <strong>{entry}</strong> audience."]
if badges:
    alert.append("Badges: " + ", ".join(badges))
st.markdown(
    f"<div class='sn-banner'>💡 <div>{' '.join(alert)}</div></div>",
    unsafe_allow_html=True,
)

if qualifiers.get("on_medicaid"):
    st.markdown(
        "<div class='sn-banner'>🩺 <div>Medicaid coverage detected. We’ll default to the Medicaid payment context and log a short-circuit entry.</div></div>",
        unsafe_allow_html=True,
    )

recommended = gcp.get("recommended_setting")
if recommended:
    st.markdown(
        "<div class='sn-banner sn-banner--success'>🧭 <div>Guided Care Plan recommends <strong>{}</strong> with {} care intensity.</div></div>".format(
            recommended.title(), gcp.get("care_intensity", "unknown")
        ),
        unsafe_allow_html=True,
    )

st.markdown('<div class="sn-card" style="margin-top:1.4rem;">', unsafe_allow_html=True)
col_mode, col_household = st.columns(2, gap="large")
with col_mode:
    mode_label = {
        "tinkering": "I’m exploring rough numbers",
        "planning": "I need a real plan with runway",
    }
    selected_mode = st.radio(
        "Planner mode",
        options=["tinkering", "planning"],
        index=["tinkering", "planning"].index(cp.get("mode", "tinkering")),
        format_func=lambda value: mode_label[value],
    )
    cp["mode"] = selected_mode

with col_household:
    household_label = {
        "single": "Single household",
        "split": "Split household",
    }
    disable_partner = not qualifiers.get("has_partner")
    selected_household = st.radio(
        "Household",
        options=["single", "split"],
        index=["single", "split"].index(cp.get("household", "single")),
        format_func=lambda value: household_label[value],
        disabled=disable_partner,
        help="Partners must be enabled in Audiencing to plan for a split household." if disable_partner else None,
    )
    cp["household"] = selected_household if not disable_partner else "single"

st.markdown("<hr style='margin:1.6rem 0;'/>", unsafe_allow_html=True)

if cp["mode"] == "planning":
    assets_default = get_numeric("assets_total")
    assets_value = st.number_input(
        "Liquid assets available for care",
        min_value=0.0,
        step=500.0,
        value=float(assets_default),
        help="Enter savings that could be used to cover care. We’ll calculate runway based on net out-of-pocket.",
    )
    set_numeric("assets_total", assets_value)
else:
    set_numeric("assets_total", 0.0)

recompute_costs()
subtotals = cp["subtotals"]
metric_cols = st.columns(3)
metric_cols[0].metric("Monthly costs", format_currency(cp["monthly_total"]))
metric_cols[1].metric("Offsets", format_currency(subtotals["offsets"]))
metric_cols[2].metric("Net out-of-pocket", format_currency(cp["net_out_of_pocket"]))

st.markdown("</div>", unsafe_allow_html=True)

with st.expander("Debug: Cost Planner session state", expanded=False):
    st.json(
        {
            "mode": cp["mode"],
            "household": cp["household"],
            "audiencing": aud,
            "gcp": gcp,
            "inputs": cp["inputs"],
        }
    )

with st.container():
    st.markdown('<div class="sn-sticky-footer"><div class="sn-footer-inner">', unsafe_allow_html=True)
    footer_cols = st.columns([1, 1, 1])
    back_clicked = False
    next_clicked = False
    with footer_cols[0]:
        back_clicked = st.button("Return to Hub", type="secondary", use_container_width=True)
    with footer_cols[2]:
        next_clicked = st.button("Next step", type="primary", use_container_width=True)
    st.markdown('</div><div class="sn-footer-note">Next step ✺</div></div>', unsafe_allow_html=True)

if back_clicked:
    st.switch_page("pages/hub.py")
if next_clicked:
    st.switch_page("pages/cost_planner_housing.py")
