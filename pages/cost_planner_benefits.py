"""Insurance costs and benefit offsets drawer with unified styling."""

from __future__ import annotations

import streamlit as st

from cost_planner_shared import (
    ensure_core_state,
    format_currency,
    get_numeric,
    recompute_costs,
    set_numeric,
)

ensure_core_state()
cp = st.session_state["cost_planner"]
aud = st.session_state["audiencing"]
quals = aud.get("qualifiers", {})

st.set_page_config(page_title="Cost Planner • Insurance", layout="wide")

st.markdown("""
<h2 style="text-transform:uppercase; letter-spacing:0.08em; color:#6b7280; font-size:0.9rem;">Cost Planner</h2>
<h1 style="margin-bottom:0.4rem;">Insurance & offsets</h1>
<p style="max-width:640px; color:#475569;">Log insurance premiums and the income or benefits that offset monthly costs.</p>
""", unsafe_allow_html=True)

st.markdown('<div class="sn-card" style="margin-top:1.2rem;">', unsafe_allow_html=True)
st.markdown("<span class='sn-chip'>Drawer</span>", unsafe_allow_html=True)
st.markdown("<h3 style='margin-top:0.6rem;'>Insurance premiums</h3>", unsafe_allow_html=True)

col_1, col_2, col_3 = st.columns(3, gap="large")
with col_1:
    health = st.number_input(
        "Health insurance premiums",
        min_value=0.0,
        step=25.0,
        value=float(get_numeric("insurance_health")),
        help="Medicare, Advantage, Medigap, or supplemental health premiums.",
    )
    set_numeric("insurance_health", health)
with col_2:
    ltc = st.number_input(
        "Long-term care insurance premiums",
        min_value=0.0,
        step=25.0,
        value=float(get_numeric("insurance_ltc")),
        help="Monthly payment due for active LTC policies.",
    )
    set_numeric("insurance_ltc", ltc)
with col_3:
    other_ins = st.number_input(
        "Other insurance premiums",
        min_value=0.0,
        step=25.0,
        value=float(get_numeric("insurance_other")),
        help="Dental, vision, life, umbrella, or other recurring premiums.",
    )
    set_numeric("insurance_other", other_ins)

st.markdown("<h3 style='margin-top:1.6rem;'>Income & benefits</h3>", unsafe_allow_html=True)

col_income1, col_income2 = st.columns(2, gap="large")
with col_income1:
    inc_ss = st.number_input(
        "Social Security income",
        min_value=0.0,
        step=50.0,
        value=float(get_numeric("offset_ss_income")),
    )
    set_numeric("offset_ss_income", inc_ss)
    inc_pension = st.number_input(
        "Pension income",
        min_value=0.0,
        step=50.0,
        value=float(get_numeric("offset_pension_income")),
    )
    set_numeric("offset_pension_income", inc_pension)
with col_income2:
    inc_annuity = st.number_input(
        "Annuity income",
        min_value=0.0,
        step=50.0,
        value=float(get_numeric("offset_annuity_income")),
    )
    set_numeric("offset_annuity_income", inc_annuity)
    inc_other = st.number_input(
        "Other recurring income",
        min_value=0.0,
        step=50.0,
        value=float(get_numeric("offset_other_income")),
        help="Family contributions, trust distributions, or gig income.",
    )
    set_numeric("offset_other_income", inc_other)

col_benefit1, col_benefit2, col_benefit3 = st.columns(3, gap="large")
with col_benefit1:
    if quals.get("is_veteran"):
        va = st.number_input(
            "VA benefits",
            min_value=0.0,
            step=25.0,
            value=float(get_numeric("offset_va_benefits")),
            help="VA Aid & Attendance or other VA programs applied to care costs.",
        )
        set_numeric("offset_va_benefits", va)
    else:
        set_numeric("offset_va_benefits", 0.0)
        st.caption("VA benefits hidden — not eligible per Audiencing.")
with col_benefit2:
    medicaid = st.number_input(
        "Medicaid coverage",
        min_value=0.0,
        step=25.0,
        value=float(get_numeric("offset_medicaid_benefits")),
        help="State Medicaid offsets covering monthly care expenses.",
        disabled=not quals.get("on_medicaid"),
    )
    set_numeric("offset_medicaid_benefits", medicaid if quals.get("on_medicaid") else 0.0)
with col_benefit3:
    ltc_payout = st.number_input(
        "LTC insurance payouts",
        min_value=0.0,
        step=25.0,
        value=float(get_numeric("offset_ltc_benefits")),
        help="Monthly payout from LTC policy benefit triggers.",
    )
    set_numeric("offset_ltc_benefits", ltc_payout)

recompute_costs()
st.markdown(
    f"<p style='margin-top:1.4rem; font-weight:600;'>Offsets subtotal: {format_currency(cp['subtotals']['offsets'])}</p>",
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="sn-sticky-footer"><div class="sn-footer-inner">', unsafe_allow_html=True)
    footer_cols = st.columns([1, 1, 1])
    back_clicked = False
    next_clicked = False
    with footer_cols[0]:
        back_clicked = st.button("Back", type="secondary", use_container_width=True)
    with footer_cols[2]:
        next_clicked = st.button("Next step", type="primary", use_container_width=True)
    st.markdown('</div><div class="sn-footer-note">Next step ✺</div></div>', unsafe_allow_html=True)

if back_clicked:
    st.switch_page("pages/cost_planner_daily_aids.py")
if next_clicked:
    st.switch_page("pages/cost_planner_freeform.py")
