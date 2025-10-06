from __future__ import annotations

import streamlit as st

from cost_planner_v2.cp_nav import goto
from pages.cost_planner_v2 import _shared as shared
from senior_nav.components import buttons
from ui.theme import inject_theme


st.set_page_config(page_title="Cost Planner · Plan the Cost of Care", layout="wide")


def main() -> None:
    inject_theme()
    shared.cp_state()
    buttons.page_start()

    with shared.page_container():
        st.markdown(
            """
            <div class="sn-hero" style="margin:2rem 0 1.5rem;">
              <h1 style="margin:0 0 .5rem 0;">Plan the Cost of Care</h1>
              <p style="margin:0;color:var(--ink-muted);max-width:640px;">
                Estimate the dollars behind your care decisions. This walkthrough uses what you’ve already
                shared and takes about 5–10 minutes.
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.info("We’ll use your earlier answers to pre-fill where we can.")

        st.markdown("""<div style='height:1rem'></div>""", unsafe_allow_html=True)

        cols = st.columns([1, 1], gap="medium")
        with cols[0]:
            if buttons.primary(
                "Start Cost Planner",
                key="cp_start",
                use_container_width=True,
            ):
                goto("pages/cost_planner_v2/cost_planner_modules_hub_v2.py")
        with cols[1]:
            if buttons.link(
                "View modules",
                key="cp_view_modules",
                use_container_width=True,
            ):
                goto("pages/cost_planner_v2/cost_planner_modules_hub_v2.py")

    buttons.page_end()


if __name__ == "__main__":
    main()
