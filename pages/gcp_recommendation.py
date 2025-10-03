"""Guided Care Plan – Financial confidence and recommendation."""

from __future__ import annotations

import streamlit as st

from audiencing import ensure_audiencing_state
from guided_care_plan import (
    ensure_gcp_session,
    evaluate_guided_care,
    get_question_meta,
    render_stepper,
)
from guided_care_plan.state import current_audiencing_snapshot


def _ensure_care_context():
    return st.session_state.setdefault(
        "care_context",
        {
            "person_name": "Your Loved One",
            "gcp_answers": {},
            "gcp_recommendation": None,
            "gcp_cost": None,
        },
    )


answers, gcp_result = ensure_gcp_session()
care_context = _ensure_care_context()
aud_state = ensure_audiencing_state()
snapshot = current_audiencing_snapshot()

st.set_page_config(page_title="GCP – Recommendation", layout="wide")

has_result = bool(gcp_result.get("recommended_setting"))
stepper_placeholder = st.empty()
with stepper_placeholder.container():
    render_stepper(5 if has_result else 4)

if not has_result:
    meta = get_question_meta("funding_confidence")
    option_map = {opt["value"]: opt["label"] for opt in meta["options"]}
    values = list(option_map.keys())
    default_value = answers.get("funding_confidence", values[0])
    if default_value not in values:
        default_value = values[0]

    st.markdown("""
<h2 style="text-transform:uppercase; letter-spacing:0.08em; color:#6b7280; font-size:0.95rem;">Guided Care Plan</h2>
<h1 style="margin-bottom:0.4rem;">Financial confidence</h1>
<p style="max-width:660px; color:#475569;">Share how confident you feel about paying for care so we can tailor next steps.</p>
""", unsafe_allow_html=True)

    st.markdown('<div class="sn-card" style="margin-top:1.4rem;">', unsafe_allow_html=True)
    st.markdown(f"<h3>{meta['label']}</h3>", unsafe_allow_html=True)
    selected_value = st.radio(
        meta["label"],
        options=values,
        index=values.index(default_value),
        key="gcp_funding_confidence",
        label_visibility="collapsed",
        format_func=lambda value, m=option_map: m[value],
    )
    if meta.get("description"):
        st.caption(meta["description"])
    st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="sn-sticky-footer"><div class="sn-footer-inner">', unsafe_allow_html=True)
        footer_cols = st.columns([1, 1, 1])
        skip_clicked = False
        continue_clicked = False
        with footer_cols[0]:
            skip_clicked = st.button(
                "Skip",
                type="secondary",
                use_container_width=True,
                key="gcp_finance_skip",
            )
        with footer_cols[2]:
            continue_clicked = st.button(
                "Continue",
                type="primary",
                use_container_width=True,
                key="gcp_finance_continue",
            )
        st.markdown(
            "</div><div class=\"sn-footer-note\">Respond as a person receiving care even if you’re filling it for someone else.</div></div>",
            unsafe_allow_html=True,
        )

    run_engine = False
    chosen_value = selected_value
    if continue_clicked:
        run_engine = True
    elif skip_clicked:
        run_engine = True
        chosen_value = "unsure"

    if run_engine:
        answers["funding_confidence"] = chosen_value
        result = evaluate_guided_care(answers, aud_state)
        gcp_result.update(result)
        gcp_result["audiencing_snapshot"] = snapshot
        st.session_state["gcp"] = gcp_result
        care_context["gcp_answers"] = answers
        care_context["gcp_recommendation"] = result["recommended_setting"]
        care_context["gcp_cost"] = result.get("care_intensity")
        has_result = True
        stepper_placeholder.empty()
        with stepper_placeholder.container():
            render_stepper(5)

if has_result:
    st.markdown("""
<h2 style="text-transform:uppercase; letter-spacing:0.08em; color:#6b7280; font-size:0.95rem;">Guided Care Plan</h2>
<h1 style="margin-bottom:0.4rem;">Recommendation</h1>
<p style="max-width:660px; color:#475569;">Here’s the care setting that best fits today’s answers plus the key reasons behind it.</p>
""", unsafe_allow_html=True)

    recommendation = gcp_result.get("recommended_setting")
    intensity = gcp_result.get("care_intensity")
    safety_flags = gcp_result.get("safety_flags", [])
    chronic_list = gcp_result.get("chronic_conditions", [])
    decision_trace = gcp_result.get("DecisionTrace", [])

    friendly_setting = {
        "home": "Stay at home with in-home support",
        "assisted": "Assisted living support",
        "memory": "Memory care support",
        "skilled-reserved": "Higher-skilled nursing (reserve)",
    }.get(recommendation, recommendation or "Care setting")

    intensity_copy = {
        "low": "Low support needs",
        "med": "Moderate support needs",
        "high": "High support needs",
    }.get(intensity, intensity or "Support level")

    st.markdown(
        """
<div class="sn-card" style="margin-top:1.8rem; display:flex; flex-direction:column; gap:1rem;">
  <div>
    <span class="sn-chip">Recommendation ready</span>
    <h2 style="margin-top:0.4rem;">{setting}</h2>
    <p style="color:#475569;">{intensity}</p>
  </div>
""".format(setting=friendly_setting, intensity=intensity_copy),
        unsafe_allow_html=True,
    )

    if safety_flags:
        st.markdown("<h4>Safety watchpoints</h4>", unsafe_allow_html=True)
        for flag in safety_flags:
            label = flag.replace("_", " ").title()
            st.markdown(f"<p style='color:#475569;'>⚠️ {label}</p>", unsafe_allow_html=True)

    if chronic_list:
        st.markdown("<h4>Chronic conditions</h4>", unsafe_allow_html=True)
        if chronic_list == ["None"]:
            st.markdown("<p style='color:#475569;'>No chronic conditions noted.</p>", unsafe_allow_html=True)
        else:
            st.markdown(
                f"<p style='color:#475569;'>{', '.join(chronic_list)}</p>",
                unsafe_allow_html=True,
            )

    if decision_trace:
        st.markdown("<h4>DecisionTrace</h4>", unsafe_allow_html=True)
        items = "".join(f"<li>{step}</li>" for step in decision_trace)
        st.markdown(f"<ul style='color:#475569; line-height:1.7;'>{items}</ul>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="sn-sticky-footer"><div class="sn-footer-inner">', unsafe_allow_html=True)
        footer_cols = st.columns([1, 1, 1])
        with footer_cols[0]:
            if st.button("Open Cost Planner", key="gcp_open_cost_planner", use_container_width=True):
                st.switch_page("pages/cost_planner_estimate.py")
        with footer_cols[2]:
            if st.button("Go to Hub", type="primary", use_container_width=True, key="gcp_go_hub"):
                st.switch_page("pages/hub.py")
        st.markdown('</div><div class="sn-footer-note">Your Concierge Care Hub now reflects this recommendation.</div></div>', unsafe_allow_html=True)

with st.expander("Debug: GCP snapshot", expanded=False):
    st.json({"answers": answers, "gcp": gcp_result})
