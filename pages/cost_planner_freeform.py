"""Debts, other expenses, and custom line items with unified styling."""

from __future__ import annotations

import streamlit as st

from cost_planner_shared import (
    add_decision_log,
    ensure_core_state,
    format_currency,
    get_numeric,
    recompute_costs,
    set_numeric,
)

ensure_core_state()
cp = st.session_state["cost_planner"]

st.set_page_config(page_title="Cost Planner • Debts", layout="wide")

st.markdown("""
<h2 style="text-transform:uppercase; letter-spacing:0.08em; color:#6b7280; font-size:0.9rem;">Cost Planner</h2>
<h1 style="margin-bottom:0.4rem;">Debts & other expenses</h1>
<p style="max-width:640px; color:#475569;">Capture debts, miscellaneous spending, and tailor additional line items.</p>
""", unsafe_allow_html=True)

st.markdown('<div class="sn-card" style="margin-top:1.2rem;">', unsafe_allow_html=True)
st.markdown("<span class='sn-chip'>Drawer</span>", unsafe_allow_html=True)
st.markdown("<h3 style='margin-top:0.6rem;'>Debt payments</h3>", unsafe_allow_html=True)

col_debt1, col_debt2 = st.columns(2, gap="large")
with col_debt1:
    cc = st.number_input(
        "Credit card payments",
        min_value=0.0,
        step=25.0,
        value=float(get_numeric("debt_credit_cards")),
    )
    set_numeric("debt_credit_cards", cc)
with col_debt2:
    loans = st.number_input(
        "Loan payments",
        min_value=0.0,
        step=25.0,
        value=float(get_numeric("debt_loans")),
    )
    set_numeric("debt_loans", loans)

cp.setdefault("custom_line_items", [])
cp.setdefault("other_base", float(get_numeric("other_miscellaneous")))

st.markdown("<h3 style='margin-top:1.6rem;'>Other expenses</h3>", unsafe_allow_html=True)
base_other = st.number_input(
    "Other monthly expenses",
    min_value=0.0,
    step=25.0,
    value=float(cp.get("other_base", 0.0)),
    help="Transportation, clubs, subscriptions, or other planned amounts.",
)
if base_other != cp.get("other_base"):
    cp["other_base"] = base_other

with st.form("custom_line_item_form", clear_on_submit=True):
    st.markdown("<h3 style='margin-top:1.6rem;'>Add custom line item</h3>", unsafe_allow_html=True)
    label = st.text_input("Description", placeholder="Companion membership, private chef, etc.")
    amount = st.number_input("Monthly amount", min_value=0.0, step=25.0)
    submit = st.form_submit_button("Add line item")
    if submit and label.strip() and amount > 0:
        cp["custom_line_items"].append({"label": label.strip(), "amount": float(amount)})
        add_decision_log(f"Custom item added: {label.strip()}")

if cp["custom_line_items"]:
    st.markdown("<h4 style='margin-top:1rem;'>Custom items</h4>", unsafe_allow_html=True)
    removal_keys = []
    for idx, item in enumerate(cp["custom_line_items"]):
        cols = st.columns([3, 1])
        cols[0].write(f"**{item['label']}** — {format_currency(item['amount'])}")
        if cols[1].button("Remove", key=f"remove_custom_{idx}"):
            removal_keys.append(idx)
    if removal_keys:
        for index in sorted(removal_keys, reverse=True):
            del cp["custom_line_items"][index]

cp.setdefault("notes", "")
notes = st.text_area(
    "Planner notes",
    value=cp.get("notes", ""),
    help="Context for advisors reviewing this estimate.",
)
cp["notes"] = notes

custom_total = sum(item["amount"] for item in cp["custom_line_items"])
set_numeric("other_miscellaneous", cp.get("other_base", 0.0) + custom_total)

recompute_costs()

other_total = cp["subtotals"]["other"] + cp["subtotals"]["debts"]
st.markdown(
    f"<p style='margin-top:1.4rem; font-weight:600;'>Other & debts subtotal: {format_currency(other_total)}</p>",
    unsafe_allow_html=True,
)
st.caption(f"Other expenses: {format_currency(cp['subtotals']['other'])}")

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
    st.switch_page("pages/cost_planner_benefits.py")
if next_clicked:
    st.switch_page("pages/cost_planner_evaluation.py")
