"""Cost Planner v2 · Income — PFMA-styled income module"""

from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme

# If you have these helpers, import them; otherwise simple fallbacks below.
try:
    from ui.cost_planner_template import (
        section_header,
        money_input,
        subtotal_row,
        nav_buttons,
    )
except Exception:
    # --- Simple inline fallbacks so this page works even without the helpers ---
    def section_header(title: str, subtitle: str = ""):
        st.markdown(f"### {title}")
        if subtitle:
            st.caption(subtitle)

    def money_input(label: str, key: str):
        return st.number_input(label, min_value=0.0, step=50.0, key=key, format="%.2f")

    def subtotal_row(label: str, value: float):
        st.markdown(
            f"<div style='display:flex;justify-content:space-between;"
            f"font-weight:700;padding:.5rem 0;border-top:1px solid rgba(0,0,0,.08)'>"
            f"<span>{label}</span><span>${value:,.2f}</span></div>",
            unsafe_allow_html=True,
        )

    def nav_buttons(prev: str | None = None, nxt: str | None = None):
        c1, c2 = st.columns(2)
        with c1:
            if prev and st.button("← Back", type="secondary", use_container_width=True):
                try:
                    st.switch_page(prev)  # type: ignore[attr-defined]
                except Exception:
                    st.query_params["next"] = prev
                    st.experimental_rerun()
        with c2:
            if nxt and st.button("Next →", type="primary", use_container_width=True):
                try:
                    st.switch_page(nxt)  # type: ignore[attr-defined]
                except Exception:
                    st.query_params["next"] = nxt
                    st.experimental_rerun()

# Page config MUST be first Streamlit call
st.set_page_config(page_title="Cost Planner v2 · Income", layout="wide")
inject_theme()

st.markdown('<div class="sn-scope cost-planner-v2">', unsafe_allow_html=True)

# ---------------------------------
# Header
# ---------------------------------
section_header("Income Sources", "Estimate monthly income available for care costs.")

with st.container(border=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        ss = money_input("Social Security", key="income_ss")
        pension = money_input("Pension / Annuity", key="income_pension")
        wages = money_input("Employment Income", key="income_wages")

    with col2:
        va = money_input("VA Benefits", key="income_va")
        rental = money_input("Rental Income", key="income_rental")
        investment = money_input("Investment Income", key="income_investment")

    with col3:
        family = money_input("Family Support", key="income_family")
        other = money_input("Other Income", key="income_other")
        note = st.text_area(
            "Notes or details",
            key="income_notes",
            placeholder="Describe any irregular income or seasonal sources...",
        )

total = sum(
    st.session_state.get(k, 0.0)
    for k in [
        "income_ss",
        "income_pension",
        "income_wages",
        "income_va",
        "income_rental",
        "income_investment",
        "income_family",
        "income_other",
    ]
)

subtotal_row("Estimated Total Monthly Income", total)

st.divider()

nav_buttons(
    prev="pages/cost_planner_v2/cost_planner_landing_v2.py",
    nxt="pages/cost_planner_v2/cost_planner_expenses_v2.py",
)
