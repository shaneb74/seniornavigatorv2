"""PFMA Care Plan confirmer."""
from __future__ import annotations

import streamlit as st

from ui.theme import inject_theme

inject_theme()

from ui.pfma import (

apply_pfma_theme,
    chip_multiselect,
    ensure_pfma_state,
    go_to_step,
    render_drawer,
    segmented_control,
    update_section,
)

SECTION_KEY = "care_plan"
ADL_OPTIONS = (
    "Bathing",
    "Dressing",
    "Mobility",
    "Meal prep",
    "Medication",
    "Toileting",
    "Transportation",
)

apply_pfma_theme()
state = ensure_pfma_state()
error_placeholder = st.empty()

def _drawer_body(pfma_state: dict[str, object]) -> dict[str, object]:
    section_data = pfma_state["sections"].get(SECTION_KEY, {}).get("data", {})
    gcp_state = st.session_state.get("gcp", {}) or {}

    recommended = gcp_state.get("recommended_setting") or "Recommendation in progress"
    safety_flags = gcp_state.get("safety_flags") or []

    st.markdown(
        f"<div class='pfma-note'>Current recommendation: <strong>{recommended}</strong></div>",
        unsafe_allow_html=True,
    )
    if safety_flags:
        items = "".join(f"<li>{flag}</li>" for flag in safety_flags)
        st.markdown(
            f"""
            <div class="pfma-note" style="background:rgba(251,192,45,0.12);border-radius:var(--sn-radius);padding:.85rem 1rem;">
              <strong>Recent safety flags</strong>
              <ul style="margin:.4rem 0 0 1.1rem;">{items}</ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    confirmation = segmented_control(
        "TEST Does this plan feel advisor-ready?",
        ("Yes", "Need to discuss", "Not sure"),
        key=f"{SECTION_KEY}_confirmation",
        default=section_data.get("confirmation"),
    )

    default_adls = section_data.get("adls") or gcp_state.get("adl_dependency") or []
    if isinstance(default_adls, str):
        default_adls = [default_adls]
    adls = chip_multiselect(
        "Daily activities we should spotlight",
        ADL_OPTIONS,
        key=f"{SECTION_KEY}_adls",
        default=default_adls,
    )

    notes_key = f"pfma_{SECTION_KEY}_notes"
    if notes_key not in st.session_state:
        st.session_state[notes_key] = section_data.get("notes", "")
    st.text_area(
        "Anything you want your advisor to double-check?",
        key=notes_key,
        max_chars=400,
        height=110,
    )

    return {
        "recommended_setting": recommended,
        "confirmation": confirmation,
        "adls": adls,
        "notes": st.session_state[notes_key],
        "safety_flags": safety_flags,
    }

result = render_drawer(
    step_key=SECTION_KEY,
    title="Care Plan Confirmer 📋",
    badge="Earns the Clarity duck",
    description="Give your advisor a heads-up on the plan elements that are locked in versus ready for discussion.",
    body=_drawer_body,
    footer_note="Need edits? Jump back to Guided Care Plan and come right back.",
)

if result.saved:
    payload = result.payload
    errors: list[str] = []
    if not payload.get("confirmation"):
        errors.append("Let us know if the recommendation is ready or needs a conversation.")
    if errors:
        error_placeholder.error("\n".join(errors))
    else:
        update_section(SECTION_KEY, payload)
        st.toast("Care plan ready for your advisor.")
        if result.next_step:
            go_to_step(result.next_step)
