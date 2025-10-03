"""Debts, other expenses, and custom line items."""
from __future__ import annotations
from ui.theme import inject_theme

import streamlit as st

from cost_planner_shared import add_decision_log, ensure_core_state, format_currency, get_numeric, recompute_costs, set_numeric


inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)


ensure_core_state()
cp = st.session_state["cost_planner"]

st.title("Debts, other expenses, and custom items")
st.caption("Capture debts, miscellaneous spending, and tailor additional line items.")

col_debt1, col_debt2 = st.columns(2)
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
    st.subheader("Add custom line item")
    label = st.text_input("Description", placeholder="Companion membership, private chef, etc.")
    amount = st.number_input("Monthly amount", min_value=0.0, step=25.0)
    submit = st.form_submit_button("Add line item")
    if submit and label.strip() and amount > 0:
        cp["custom_line_items"].append({"label": label.strip(), "amount": float(amount)})
        add_decision_log(f"Custom item added: {label.strip()}")

if cp["custom_line_items"]:
    st.subheader("Custom items")
    removal_keys = []
    for idx, item in enumerate(cp["custom_line_items"]):
        cols = st.columns([3, 1])
        cols[0].write(f"**{item['label']}** - {format_currency(item['amount'])}")
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

# Sync "other" subtotal with base + custom
custom_total = sum(item["amount"] for item in cp["custom_line_items"])
set_numeric("other_miscellaneous", cp.get("other_base", 0.0) + custom_total)

recompute_costs()

other_subtotal = format_currency(cp["subtotals"]["other"])
st.metric("Other & debts subtotal", format_currency(cp["subtotals"]["other"] + cp["subtotals"]["debts"]))
st.caption(f"Other expenses: {other_subtotal}")

st.markdown("---")

col_hub, col_back, col_next = st.columns([1, 1, 1])
with col_hub:
    if st.button("Return to Hub", type="secondary"):
        st.switch_page("pages/hub.py")
with col_back:
    if st.button("Back: Benefits"):
        st.switch_page("pages/cost_planner_benefits.py")
with col_next:
    if st.button("Next: Expert Review", type="primary"):
        st.switch_page("pages/cost_planner_evaluation.py")

st.markdown('</div>', unsafe_allow_html=True)