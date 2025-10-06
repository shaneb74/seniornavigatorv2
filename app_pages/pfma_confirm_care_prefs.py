"""PFMA Care Preferences confirmer."""
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
    update_section,
)

SECTION_KEY = "care_prefs"
PET_OPTIONS = ("Yes", "No", "Allergic", "Service animal only")
ACTIVITY_OPTIONS = (
    "Gardening",
    "Live music",
    "Arts & crafts",
    "Faith services",
    "Outdoors",
    "Volunteering",
    "Games",
)
SETTING_OPTIONS = (
    "Stay at home",
    "Senior community",
    "Assisted living",
    "Memory care",
    "Skilled nursing",
)

apply_pfma_theme()
state = ensure_pfma_state()
error_placeholder = st.empty()

def _drawer_body(pfma_state: dict[str, object]) -> dict[str, object]:
    section_data = pfma_state["sections"].get(SECTION_KEY, {}).get("data", {})

    st.markdown(
        "<div class='pfma-note'>Little preferences make a big difference. Capture what sparks joy or what's a dealbreaker.</div>",
        unsafe_allow_html=True,
    )

    pet_key = "pfma_care_prefs_pets"
    if pet_key not in st.session_state:
        st.session_state[pet_key] = section_data.get("pets") or PET_OPTIONS[0]
    st.selectbox("Pets okay?", PET_OPTIONS, key=pet_key)

    activities = chip_multiselect(
        "Activities that matter",
        ACTIVITY_OPTIONS,
        key=f"{SECTION_KEY}_activities",
        default=section_data.get("activities") or [],
    )

    radius_key = "pfma_care_prefs_radius"
    if radius_key not in st.session_state:
        st.session_state[radius_key] = section_data.get("radius", 15)
    st.slider("Preferred radius from home (miles)", 5, 50, key=radius_key, help="We'll expand if there are limited matches.")

    settings = chip_multiselect(
        "Preferred care settings",
        SETTING_OPTIONS,
        key=f"{SECTION_KEY}_settings",
        default=section_data.get("settings") or [],
    )

    return {
        "pets": st.session_state[pet_key],
        "activities": activities,
        "radius": st.session_state[radius_key],
        "settings": settings,
    }

result = render_drawer(
    step_key=SECTION_KEY,
    title="Care Preferences ⭐",
    badge="Celebrates the Joy duck",
    description="Flag lifestyle non-negotiables so your advisor can shortlist matches you'll feel good about.",
    body=_drawer_body,
    footer_note="Preference tweaks? Update anytime-even after the advisor call.",
)

if result.saved:
    payload = result.payload
    errors: list[str] = []
    if not payload.get("settings"):
        errors.append("Pick at least one setting so we know your baseline.")
    if errors:
        error_placeholder.error("\n".join(errors))
    else:
        update_section(SECTION_KEY, payload)
        st.toast("Preferences saved-your ducks are delighted.")
        if result.next_step:
            go_to_step(result.next_step)
