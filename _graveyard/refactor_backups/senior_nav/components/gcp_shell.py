import streamlit as st

from senior_nav.components.theme import inject_theme
from senior_nav.components.card import card_panel
from senior_nav.components.stepper import render as render_stepper

GCP_STEPS = [
    ("Financial", "ui/pages/gcp.py"),
    ("Daily Life & Support", "ui/pages/gcp_daily_life.py"),
    ("Health & Safety", "ui/pages/gcp_health_safety.py"),
    ("Context & Preferences", "ui/pages/gcp_context_prefs.py"),
    ("Recommendation", "ui/pages/gcp_recommendation.py"),
]


def centered_container():
    return st.columns([1, 2, 1])[1]


def gcp_header(current_index: int):
    inject_theme()
    st.markdown("")
    titles = [label for label, _ in GCP_STEPS]
    render_stepper(titles, current_index)


def gcp_section(title: str, subtitle: str, body_render_fn):
    with centered_container():
        card_panel(title=title, subtitle=subtitle, body=body_render_fn)


def primary_secondary(
    primary_label: str,
    on_primary,
    secondary_label: str | None = None,
    on_secondary=None,
    disabled: bool = False,
):
    cols = st.columns([1, 1])
    with cols[0]:
        if st.button(primary_label, type="primary", use_container_width=True, disabled=disabled):
            on_primary()
    if secondary_label and on_secondary:
        with cols[1]:
            if st.button(secondary_label, use_container_width=True):
                on_secondary()
