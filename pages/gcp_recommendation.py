"""Guided Care Plan - Medical conditions and recommendation."""

from __future__ import annotations

import streamlit as st

from audiencing import ensure_audiencing_state
from guided_care_plan import ensure_gcp_session, evaluate_guided_care, get_question_meta, render_stepper
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


def _render_chronic_selector(current_values):
    meta = get_question_meta("chronic_conditions")
    options = meta["options"]
    default = current_values or ("None" in options and ["None"] or [])
    with st.form("gcp_chronic_conditions_form"):
        selections = st.multiselect(
            meta["label"],
            options=options,
            default=default,
            help=meta.get("description"),
        )
        submitted = st.form_submit_button("Generate my recommendation", type="primary")
    return submitted, selections


answers, gcp_result = ensure_gcp_session()
care_context = _ensure_care_context()
aud_state = ensure_audiencing_state()
snapshot = current_audiencing_snapshot()

has_result = bool(gcp_result.get("recommended_setting"))
stepper_placeholder = st.empty()
with stepper_placeholder.container():
    render_stepper(5 if has_result else 4)

st.title("Guided Care Plan - Medical Check & Recommendation")
st.caption("Confirm medical conditions so we can finalize your plan.")

submitted, selections = _render_chronic_selector(answers.get("chronic_conditions"))

if submitted:
    chosen = selections or ["None"]
    answers["chronic_conditions"] = chosen
    result = evaluate_guided_care(answers, aud_state)
    gcp_result.update(result)
    gcp_result["audiencing_snapshot"] = snapshot
    st.session_state["gcp"] = gcp_result
    care_context["gcp_answers"] = answers
    care_context["gcp_recommendation"] = result["recommended_setting"]
    care_context["gcp_cost"] = result.get("care_intensity")
    st.success("Recommendation updated.")
    has_result = True
    stepper_placeholder.empty()
    with stepper_placeholder.container():
        render_stepper(5)

if has_result:
    recommendation = gcp_result["recommended_setting"]
    intensity = gcp_result.get("care_intensity")
    safety_flags = gcp_result.get("safety_flags", [])
    chronic_conditions = gcp_result.get("chronic_conditions", [])
    decision_trace = gcp_result.get("DecisionTrace", [])

    friendly_setting = {
        "home": "Stay at home with in-home support",
        "assisted": "Assisted living support",
        "memory": "Memory care support",
    }.get(recommendation, recommendation)

    intensity_copy = {
        "low": "Low support needs",
        "med": "Moderate support needs",
        "high": "High support needs",
    }.get(intensity, intensity)

    st.markdown("---")
    st.subheader("Your personalized recommendation")
    st.markdown(f"### {friendly_setting}")
    st.caption(intensity_copy)

    if safety_flags:
        st.markdown("#### Safety watchpoints")
        for flag in safety_flags:
            icon = "✅"
            description = ""
            if flag in {"falls", "fall"}:
                icon = "⚠️"
                description = "Recent falls call for supervision or home adjustments."
            elif flag in {"behaviors"}:
                icon = "⚠️"
                description = "Behavior changes suggest a memory care environment."
            elif flag in {"med_mgmt"}:
                icon = "⚠️"
                description = "Medication management support can reduce risk."
            elif flag in {"cognition"}:
                icon = "⚠️"
                description = "Cognition changes benefit from structured support."
            elif flag in {"supervision"}:
                icon = "⚠️"
                description = "Extended supervision needs signal higher care intensity."
            st.write(f"{icon} {flag.replace('_', ' ').title()} - {description}")

    if chronic_conditions:
        st.markdown("#### Chronic conditions to plan for")
        if chronic_conditions == ["None"]:
            st.write("No chronic conditions noted.")
        else:
            st.write(", ".join(chronic_conditions))

    if decision_trace:
        st.markdown("#### DecisionTrace")
        for step in decision_trace:
            st.write(f"• {step}")

    st.markdown("---")
    if st.button("Go to Hub", type="primary"):
        st.switch_page("pages/hub.py")
    if st.button("Open Cost Planner", key="open_cost_planner"):
        st.switch_page("pages/cost_planner.py")

with st.expander("Debug: GCP snapshot", expanded=False):
    st.json({"answers": answers, "gcp": gcp_result})
