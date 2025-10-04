"""PFMA Household & Legal confirmer."""
from __future__ import annotations

import streamlit as st

from ui.pfma import (
    apply_pfma_theme,
    ensure_pfma_state,
    go_to_step,
    render_drawer,
    segmented_control,
    update_section,
)


SECTION_KEY = "household_legal"
MARITAL_STATUS = ("Single", "Married/partnered", "Widowed", "Divorced")
LIVING_SITUATION = ("Lives alone", "With spouse/partner", "With family", "Community")
YES_NO = ("Yes", "No", "Sometimes")


apply_pfma_theme()
state = ensure_pfma_state()
error_placeholder = st.empty()


def _drawer_body(pfma_state: dict[str, object]) -> dict[str, object]:
    section_data = pfma_state["sections"].get(SECTION_KEY, {}).get("data", {})

    st.markdown(
        "<div class='pfma-note'>These basics help advisors prep paperwork and flag any legal next steps.</div>",
        unsafe_allow_html=True,
    )

    segmented_control(
        "Marital status",
        MARITAL_STATUS,
        key=f"{SECTION_KEY}_marital",
        default=section_data.get("marital_status"),
    )

    segmented_control(
        "Current living situation",
        LIVING_SITUATION,
        key=f"{SECTION_KEY}_living",
        default=section_data.get("living_situation"),
    )

    segmented_control(
        "Any hearing challenges?",
        YES_NO,
        key=f"{SECTION_KEY}_hearing",
        default=section_data.get("hearing"),
    )

    segmented_control(
        "Any vision challenges?",
        YES_NO,
        key=f"{SECTION_KEY}_vision",
        default=section_data.get("vision"),
    )

    segmented_control(
        "Smoking or alcohol use?",
        ("None", "Occasional", "Frequent"),
        key=f"{SECTION_KEY}_habits",
        default=section_data.get("habits"),
    )

    toggle_key = "pfma_household_verified"
    if toggle_key not in st.session_state:
        st.session_state[toggle_key] = bool(section_data.get("household_confirmed"))
    st.checkbox("Household confirmed", key=toggle_key, help="Tick this when you’ve double-checked with your loved one.")

    return {
        "marital_status": st.session_state.get(f"pfma_segment_{SECTION_KEY}_marital"),
        "living_situation": st.session_state.get(f"pfma_segment_{SECTION_KEY}_living"),
        "hearing": st.session_state.get(f"pfma_segment_{SECTION_KEY}_hearing"),
        "vision": st.session_state.get(f"pfma_segment_{SECTION_KEY}_vision"),
        "habits": st.session_state.get(f"pfma_segment_{SECTION_KEY}_habits"),
        "household_confirmed": st.session_state[toggle_key],
    }


result = render_drawer(
    step_key=SECTION_KEY,
    title="Household & Legal 🏠",
    badge="High-fives the Family duck",
    description="Capture the basics advisors use to prep paperwork or vet household fit.",
    body=_drawer_body,
    footer_note="Need legal docs? Your advisor can trigger follow-ups after the call.",
)


if result.saved:
    payload = result.payload
    errors: list[str] = []
    required_fields = [
        payload.get("marital_status"),
        payload.get("living_situation"),
        payload.get("hearing"),
        payload.get("vision"),
    ]
    if not all(required_fields):
        errors.append("Fill in marital, living, hearing, and vision details.")
    if errors:
        error_placeholder.error("\n".join(errors))
    else:
        update_section(SECTION_KEY, payload)
        st.toast("Household snapshot ready.")
        if result.next_step:
            go_to_step(result.next_step)
