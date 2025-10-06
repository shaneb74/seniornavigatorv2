from __future__ import annotations

import math
import streamlit as st

from pages.cost_planner_v2 import _shared as shared
from senior_nav.components import buttons
from ui.theme import inject_theme


st.set_page_config(page_title="Cost Planner · Modules", layout="wide")


CARD_COLUMNS = 3


DESCRIPTIONS = {
    "income": "Capture Social Security, pensions, wages, and more.",
    "expenses": "List living costs, care services, and medical spending.",
    "benefits": "Track Medicaid, VA, and insurance offsets.",
    "home": "Note mortgage, rent, and housing expenses.",
    "home_mods": "Add accessibility projects or safety upgrades.",
    "liquidity": "Record available cash and coverage buffers.",
    "caregiver": "Share unpaid support and respite plans.",
    "assets": "Log assets that support the long-term plan.",
    "timeline": "Review a 12-month projection of your plan.",
}


def main() -> None:
    inject_theme()
    shared.cp_state()
    buttons.page_start()

    with shared.page_container():
        st.markdown(
            """
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin:2rem 0 1.5rem;gap:1rem;">
              <div>
                <h1 style="margin:0 0 .5rem 0;">Cost Planner Modules</h1>
                <p style="margin:0;color:var(--ink-muted);max-width:640px;">
                  Work through the sections at your own pace. We’ll save as you go and show a quick summary for each module.
                </p>
              </div>
              <div style="font-size:.9rem;">
                <a href="pages/hub.py" style="text-decoration:none;color:var(--brand);">← Return to Hub</a>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        shared.legend_row()

        st.markdown("""<div style='height:1.5rem'></div>""", unsafe_allow_html=True)

        modules = list(shared.modules_data())
        rows = math.ceil(len(modules) / CARD_COLUMNS)
        for row_index in range(rows):
            cols = st.columns(CARD_COLUMNS, gap="large")
            for col_index in range(CARD_COLUMNS):
                idx = row_index * CARD_COLUMNS + col_index
                if idx >= len(modules):
                    continue
                module_key, module_meta = modules[idx]
                with cols[col_index]:
                    with st.container(border=True):
                        st.markdown(
                            f"<h3 style='margin:0 0 .5rem 0;'>{module_meta['title']}</h3>",
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f"<p style='margin:0 0 .75rem 0;color:var(--ink-muted);'>{DESCRIPTIONS.get(module_key, module_meta['description'])}</p>",
                            unsafe_allow_html=True,
                        )
                        shared.render_status_pill(module_key)

                        summary = shared.module_summary(module_key)
                        st.caption(summary)

                        st.markdown("---")

                        open_key = f"open_{module_key}"
                        if buttons.primary(
                            "Open module",
                            key=open_key,
                            use_container_width=True,
                        ):
                            shared.goto_module(module_key)

                        if buttons.link("Reset module", key=f"reset_card_{module_key}", use_container_width=True):
                            shared.reset_module(module_key)
                            st.experimental_rerun()

    buttons.page_end()


if __name__ == "__main__":
    main()
