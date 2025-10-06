"""PFMA Care Needs confirmer."""
from __future__ import annotations

import streamlit as st

from senior_nav.ui import configure_page
from ui.theme import inject_theme

configure_page(page_title="PFMA · Care Needs")

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

SECTION_KEY = "care_needs"
BEHAVIORAL_OPTIONS = (
    "Memory changes",
    "Wandering",
    "Agitation",
    "Sleep disruption",
    "Hallucinations",
    "Mood shifts",
)
DIETARY_OPTIONS = (
    "Low-sodium",
    "Diabetic",
    "Pureed",
    "Vegetarian",
    "Gluten-free",
    "High-calorie",
)
COGNITION_LEVELS = ("Intact", "Mild", "Moderate", "Severe")

apply_pfma_theme()
state = ensure_pfma_state()
error_placeholder = st.empty()

def _drawer_body(pfma_state: dict[str, object]) -> dict[str, object]:
    section_data = pfma_state["sections"].get(SECTION_KEY, {}).get("data", {})
    care_state = st.session_state.get("care_context", {}) or {}
    needs_state = care_state.get("care_needs") if isinstance(care_state.get("care_needs"), dict) else {}

    st.markdown(
        "<div class='pfma-note'>Focus on the daily support that keeps things running smoothly. Advisors love concrete examples.</div>",
        unsafe_allow_html=True,
    )

    behavioral = chip_multiselect(
        "Behavioral or memory symptoms",
        BEHAVIORAL_OPTIONS,
        key=f"{SECTION_KEY}_behavioral",
        default=section_data.get("behavioral") or needs_state.get("behavioral") or [],
    )

    notes_key = f"pfma_{SECTION_KEY}_mental_health"
    if notes_key not in st.session_state:
        st.session_state[notes_key] = section_data.get("mental_health") or needs_state.get("mental_health") or ""
    st.text_area(
        "Mental health notes",
        key=notes_key,
        max_chars=400,
        height=100,
    )

    dietary = chip_multiselect(
        "Dietary needs",
        DIETARY_OPTIONS,
        key=f"{SECTION_KEY}_dietary",
        default=section_data.get("dietary") or needs_state.get("dietary") or [],
    )

    cognition_default = section_data.get("cognition") or needs_state.get("cognition")
    segmented_control(
        "Cognition level",
        COGNITION_LEVELS,
        key=f"{SECTION_KEY}_cognition",
        default=cognition_default,
    )

    return {
        "behavioral": behavioral,
        "mental_health": st.session_state[notes_key],
        "dietary": dietary,
        "cognition": st.session_state.get(f"pfma_segment_{SECTION_KEY}_cognition"),
    }

result = render_drawer(
    step_key=SECTION_KEY,
    title="Care Needs & Support 🩺",
    badge="Unlocks the Care duck",
    description="Capture the rhythms of each day so your advisor sees where support is non-negotiable.",
    body=_drawer_body,
    footer_note="You can always keep notes in the Follow-Up Drawer after the call, too.",
)

if result.saved:
    payload = result.payload
    errors: list[str] = []
    if not payload.get("cognition"):
        errors.append("Choose a cognition level to help with care-matching.")
    if errors:
        error_placeholder.error("\n".join(errors))
    else:
        update_section(SECTION_KEY, payload)
        st.toast("Daily support ready to share.")
        if result.next_step:
            go_to_step(result.next_step)
