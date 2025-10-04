"""Cost planner hi-fi shell with wizard wiring."""
from __future__ import annotations

import streamlit as st

from senior_nav.components import layout, theme
from senior_nav.cost_planner import state, wizard
from senior_nav.navi import agent as navi_agent

state.ensure_state()
st.set_page_config(layout="wide")
theme.inject_theme()

copy = state.get_copy()
app_copy = copy["app"]
steps = wizard.get_steps()
current_step = wizard.get_current_step()
current_index = wizard.get_step_index(current_step)
progress_ratio = current_index / (len(steps) - 1) if len(steps) > 1 else 0
mode_badge = app_copy["mode_badges"].get(
    state.get_state().get("mode", "exploring"),
    app_copy["mode_badges"]["exploring"],
)

layout.render_header(
    app_copy["title"],
    mode_badge,
    [step.label for step in steps],
    current_index,
    progress=progress_ratio,
    progress_label=app_copy["progress_label"],
)

main_col, sidebar_col = st.columns([3, 1])
with main_col:
    wizard.run_step(current_step)

with sidebar_col:
    sidebar = app_copy["sidebar"]
    layout.render_sidebar(
        sidebar["totals_title"],
        sidebar["totals_rows"],
        sidebar["navi_title"],
        sidebar["navi_body"],
    )

navi_agent.render(current_step.drawer_key)
