from __future__ import annotations

from typing import Any, Dict, Tuple

import streamlit as st

from ui.va_rules import estimate_pension

VA_FLAG = "_va_drawer_open"
_MEDICAL_KEYS = (
    "exp_med_premiums_monthly",
    "exp_rx_out_of_pocket_monthly",
    "exp_home_care_monthly",
    "exp_al_monthly",
    "exp_memory_care_monthly",
    "exp_nursing_home_monthly",
)


def _ans() -> Dict[str, Any]:
    st.session_state.setdefault("cp_answers", {})
    answers = st.session_state["cp_answers"]
    for key in _MEDICAL_KEYS:
        answers.setdefault(key, 0.0)
    answers.setdefault("inc_va_monthly", 0.0)
    return answers


def open_drawer() -> None:
    st.session_state[VA_FLAG] = True


def close_drawer() -> None:
    st.session_state[VA_FLAG] = False


def is_open() -> bool:
    return bool(st.session_state.get(VA_FLAG, False))


def _num(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return float(default)


def _ensure_choice(value, choices):
    if value in choices:
        return value
    return choices[0]


def render_in_sidebar() -> Tuple[bool, float]:
    if not is_open():
        return False, _num(_ans().get("inc_va_monthly", 0))

    answers = _ans()

    with st.sidebar:
        st.markdown("### 🇺🇸 Veterans Benefits")
        st.caption(
            "Provide a few details to see if VA pension/Aid & Attendance might apply. "
            "This is an estimate, not a determination."
        )

        status_choices = ["Unknown", "Yes", "No"]
        answers["ben_va_status"] = st.radio(
            "Does the person (or survivor) have potential VA eligibility?",
            status_choices,
            index=status_choices.index(_ensure_choice(answers.get("ben_va_status", "Unknown"), status_choices)),
            horizontal=True,
        )

        era_choices = ["Unknown", "WWII", "Korea", "Vietnam", "Gulf War/Post-9/11", "Other"]
        answers["ben_va_service_era"] = st.selectbox(
            "Service era (if known)",
            era_choices,
            index=era_choices.index(_ensure_choice(answers.get("ben_va_service_era", "Unknown"), era_choices)),
        )

        discharge_choices = ["Unknown", "Honorable/General", "Other/Uncharacterized"]
        answers["ben_va_discharge"] = st.selectbox(
            "Discharge status",
            discharge_choices,
            index=discharge_choices.index(
                _ensure_choice(answers.get("ben_va_discharge", "Unknown"), discharge_choices)
            ),
        )

        rating_choices = ["Unknown", "0%", "10%", "30%", "50%", "70%", "100%"]
        answers["ben_va_disability_rating"] = st.selectbox(
            "VA disability rating (if any)",
            rating_choices,
            index=rating_choices.index(
                _ensure_choice(str(answers.get("ben_va_disability_rating", "Unknown")), rating_choices)
            ),
        )

        survivor_choices = ["Unknown", "No", "Surviving spouse/dependent"]
        answers["ben_va_survivor_status"] = st.selectbox(
            "Are you a surviving spouse or dependent?",
            survivor_choices,
            index=survivor_choices.index(
                _ensure_choice(answers.get("ben_va_survivor_status", "Unknown"), survivor_choices)
            ),
        )

        marital_choices = ["Unknown", "Single", "Married/partnered", "Widowed"]
        answers["profile_marital_status"] = st.selectbox(
            "Current marital status",
            marital_choices,
            index=marital_choices.index(
                _ensure_choice(answers.get("profile_marital_status", "Unknown"), marital_choices)
            ),
        )

        st.markdown("---")
        st.caption("**Possible conditions related to cognitive/behavioral symptoms** (check all that apply):")
        condition_labels = {
            "ben_va_cond_wandering": "Wandering",
            "ben_va_cond_aggression": "Aggression",
            "ben_va_cond_elopement": "Elopement / Exit-seeking",
            "ben_va_cond_confusion": "Confusion / disorientation",
            "ben_va_cond_sundown": "Sundowning",
            "ben_va_cond_repetitive": "Repetitive questioning",
            "ben_va_cond_judgment": "Poor judgment",
            "ben_va_cond_hoarding": "Hoarding",
            "ben_va_cond_sleep": "Sleep disturbances",
        }
        for field_key, label in condition_labels.items():
            answers[field_key] = st.checkbox(label, value=bool(answers.get(field_key, False)))

        st.markdown("---")
        st.subheader("Estimate (optional)")
        auto = st.checkbox(
            "Auto-estimate Aid & Attendance / pension",
            value=bool(answers.get("ben_va_auto_estimate", True)),
        )
        answers["ben_va_auto_estimate"] = auto

        current_estimate = _num(answers.get("inc_va_monthly", 0))

        if auto:
            calc = estimate_pension(answers)
            estimate = calc["pension_monthly"]
            st.metric("Estimated monthly VA benefit", f"${estimate:,.0f}")
            with st.expander("See calculation details", expanded=False):
                st.write(
                    {
                        "MAPR category": calc.get("category"),
                        "MAPR tier": calc.get("tier"),
                        "MAPR (annual)": calc["mapr"],
                        "Annual income (pre-VA)": calc["income_annual"],
                        "Medical allowed (annual)": calc["med_allowed"],
                        "Medical threshold (5% of MAPR)": calc["med_threshold"],
                        "Medical deductible": calc["med_deductible"],
                        "Countable income": calc["countable"],
                        "Estimated VA pension (annual)": calc["pension_annual"],
                    }
                )
        else:
            estimate = st.number_input(
                "Monthly VA benefit (manual entry)",
                min_value=0.0,
                value=current_estimate,
                step=25.0,
            )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save", type="primary", use_container_width=True):
                answers["inc_va_monthly"] = round(float(estimate), 2)
                close_drawer()
                st.rerun()
                return True, float(answers["inc_va_monthly"])
        with col2:
            if st.button("Close", use_container_width=True):
                close_drawer()
                st.rerun()
                return False, float(estimate)

        st.caption(
            "**Note:** VA decisions depend on service, discharge, financials, medical needs, and official rules. "
            "This tool provides a planning estimate only."
        )

    return False, _num(answers.get("inc_va_monthly", 0))
