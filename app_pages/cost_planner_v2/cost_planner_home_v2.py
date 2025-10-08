# Cost Planner · Home & Housing (v2)
from __future__ import annotations

import streamlit as st

from ui.cost_planner_data import MODULE_FIELD_MAP
from ui.cost_planner_forms import compute_gap, cp_state, render_fields, set_value

OWNER_KEYS = {"home_mortgage", "home_property_tax", "home_insurance", "home_move_plan"}
RENTER_KEYS = {"home_rent", "home_insurance", "home_move_plan"}
FAMILY_KEYS = {"home_move_plan"}


def _clear_keys(keys: set[str]) -> None:
    for key in keys:
        set_value(key, 0)


def render() -> None:
    st.header("Home & Housing")
    st.caption("Document where you live today, housing costs, and whether a move is on the horizon.")

    fields = MODULE_FIELD_MAP["home"]
    status_field = fields[0]

    valid, _ = render_fields([status_field])
    status = cp_state().get("home_status", status_field.default or "Own")

    if status == "Own":
        owner_fields = [f for f in fields if f.key in OWNER_KEYS and f.key != "home_status"]
        valid_owner, _ = render_fields(owner_fields)
        valid = valid and valid_owner
        _clear_keys({"home_rent"})
    elif status == "Rent":
        renter_fields = [f for f in fields if f.key in RENTER_KEYS and f.key != "home_status"]
        valid_renter, _ = render_fields(renter_fields)
        valid = valid and valid_renter
        _clear_keys({"home_mortgage", "home_property_tax"})
    else:
        family_fields = [f for f in fields if f.key in FAMILY_KEYS and f.key != "home_status"]
        valid_family, _ = render_fields(family_fields)
        valid = valid and valid_family
        _clear_keys({"home_mortgage", "home_property_tax", "home_rent"})

    st.markdown("---")
    if st.button("Save & back to Modules", type="primary", disabled=not valid):
        compute_gap(cp_state())
        try:
            st.switch_page("app_pages/cost_planner_v2/cost_planner_modules_hub_v2.py")
        except Exception:
            st.session_state["nav_target"] = "app_pages/cost_planner_v2/cost_planner_modules_hub_v2.py"
            st.rerun()


render()
