from __future__ import annotations

from typing import Any, Dict, List, Tuple

import streamlit as st

from ui.cost_planner_data import Field


def cp_state() -> Dict[str, Any]:
    st.session_state.setdefault("cp_answers", {})
    return st.session_state["cp_answers"]


def get_value(key: str, default: Any = None) -> Any:
    return cp_state().get(key, default)


def set_value(key: str, value: Any) -> None:
    cp_state()[key] = value


def currency_input(label: str, key: str, help: str = "", step: float = 50.0) -> float:
    value = float(get_value(key, 0) or 0)
    result = st.number_input(
        label,
        min_value=0.0,
        value=value,
        step=step,
        help=help or None,
        key=f"num_{key}",
    )
    set_value(key, float(result))
    return float(result)


def _choice_index(choices: List[str], current: Any) -> int:
    if not choices:
        return 0
    try:
        return choices.index(current)
    except ValueError:
        return 0


def render_fields(fields: List[Field]) -> Tuple[bool, Dict[str, str]]:
    """
    Returns (is_valid, errors). Writes values into cp_answers.
    """
    errors: Dict[str, str] = {}

    for field in fields:
        key = field.key
        default = field.default
        current_value = get_value(key, default)

        if field.type == "money":
            value = currency_input(field.label, key, field.help)
        elif field.type == "int":
            value = st.number_input(
                field.label,
                min_value=0,
                value=int(current_value or 0),
                step=1,
                help=field.help or None,
                key=f"int_{key}",
            )
            set_value(key, int(value))
        elif field.type == "percent":
            value = st.number_input(
                field.label,
                min_value=0.0,
                max_value=100.0,
                value=float(current_value or 0),
                step=1.0,
                help=field.help or None,
                key=f"pct_{key}",
            )
            set_value(key, float(value))
        elif field.type == "choice":
            options = field.choices or []
            seed = current_value if current_value in options else (default if default in options else (options[0] if options else None))
            idx = _choice_index(options, seed)
            value = st.radio(
                field.label,
                options,
                index=idx,
                horizontal=True,
                help=field.help or None,
                key=f"rad_{key}",
            ) if options else ""
            set_value(key, value)
        elif field.type == "bool":
            base = bool(current_value if current_value is not None else (default or False))
            value = st.checkbox(
                field.label,
                value=base,
                help=field.help or None,
                key=f"chk_{key}",
            )
            set_value(key, bool(value))
        else:
            text_default = "" if current_value is None else str(current_value)
            value = st.text_input(
                field.label,
                value=text_default,
                help=field.help or None,
                key=f"txt_{key}",
            )
            set_value(key, value)

        if field.help and field.type not in {"money", "int", "percent", "choice", "bool"}:
            st.caption(field.help)

        value_for_validation = get_value(key)
        is_empty = value_for_validation in (None, "", [])
        if field.type in {"money", "int", "percent"}:
            is_empty = value_for_validation is None

        if field.required and is_empty:
            errors[key] = "This field is required."
        elif field.validate:
            message = field.validate(value_for_validation)
            if message:
                errors[key] = message

    if errors:
        st.error("Please fix the highlighted issues.")
        for k, msg in errors.items():
            st.caption(f"• **{k}** — {msg}")

    return (len(errors) == 0), errors


def income_total(ans: Dict[str, Any]) -> float:
    keys = [key for key in ans if key.startswith("inc_")]
    total = float(sum(float(ans.get(key, 0) or 0) for key in keys))
    ans["cp_income_total"] = round(total, 2)
    return ans["cp_income_total"]


def expenses_total(ans: Dict[str, Any]) -> float:
    expense_keys = {key for key in ans if key.startswith("exp_")}
    housing_keys = {"home_rent", "home_mortgage", "home_property_tax", "home_insurance"}
    mods_keys = {"mods_ongoing_monthly"}
    caregiver_keys = {"cg_out_of_pocket"}

    keys = set()
    keys.update(expense_keys)
    keys.update({key for key in housing_keys if key in ans})
    keys.update({key for key in mods_keys if key in ans})
    keys.update({key for key in caregiver_keys if key in ans})

    total = float(sum(float(ans.get(key, 0) or 0) for key in keys))
    ans["cp_expenses_total"] = round(total, 2)
    return ans["cp_expenses_total"]


def assets_total(ans: Dict[str, Any]) -> float:
    keys = [key for key in ans if key.startswith("assets_")]
    total = float(sum(float(ans.get(key, 0) or 0) for key in keys))
    ans["cp_assets_total"] = round(total, 2)
    return ans["cp_assets_total"]


def compute_gap(ans: Dict[str, Any]) -> float:
    income = income_total(ans)
    expenses = expenses_total(ans)
    gap = income - expenses
    ans["cp_monthly_gap_estimate"] = round(gap, 2)
    return ans["cp_monthly_gap_estimate"]
