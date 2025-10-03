"""Shared helpers for the Senior Navigator Cost Planner module."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import streamlit as st


ROOT = Path(__file__).resolve().parent
FIELD_SPEC_PATH = ROOT / "cost_planner_user_data_inputs_only.csv"
FIELD_MAP_PATH = ROOT / "cost_planner_user_data_map.csv"


@dataclass
class FieldSpec:
    field_id: str
    label: str
    category: str
    required: bool
    helper: str
    default: float


@lru_cache(maxsize=1)
def load_field_specs() -> Dict[str, FieldSpec]:
    specs: Dict[str, FieldSpec] = {}
    if not FIELD_SPEC_PATH.exists():
        raise FileNotFoundError(f"Missing Cost Planner field spec: {FIELD_SPEC_PATH}")

    with FIELD_SPEC_PATH.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            field_id = row["field_id"].strip()
            specs[field_id] = FieldSpec(
                field_id=field_id,
                label=row.get("label", "").strip(),
                category=row.get("category", "").strip(),
                required=row.get("required", "").strip().lower() in {"true", "1", "yes", "required"},
                helper=row.get("helper_text", "").strip(),
                default=float(row.get("default_value", "0") or 0),
            )
    return specs


@lru_cache(maxsize=1)
def load_field_map() -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    if not FIELD_MAP_PATH.exists():
        raise FileNotFoundError(f"Missing Cost Planner field mapping: {FIELD_MAP_PATH}")

    with FIELD_MAP_PATH.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            field_id = row["field_id"].strip()
            normalized = row["normalized_key"].strip()
            mapping[field_id] = normalized
    return mapping


def ensure_core_state() -> None:
    """Ensure required session state blocks exist and honor audience gates."""
    st.session_state.setdefault(
        "audiencing",
        {
            "entry": "self",
            "qualifiers": {
                "is_veteran": False,
                "has_partner": False,
                "owns_home": False,
                "on_medicaid": False,
                "urgent": False,
            },
            "route": {"next": None},
        },
    )
    st.session_state.setdefault(
        "gcp",
        {
            "recommended_setting": None,
            "care_intensity": None,
            "safety_flags": [],
            "chronic_conditions": [],
            "payment_context": None,
            "funding_confidence": None,
            "audiencing_snapshot": None,
            "DecisionTrace": None,
        },
    )
    cost_defaults = {
        "mode": "tinkering",
        "household": "single",
        "inputs": {},
        "subtotals": {
            "housing": 0.0,
            "care": 0.0,
            "medical": 0.0,
            "insurance": 0.0,
            "debts": 0.0,
            "other": 0.0,
            "offsets": 0.0,
        },
        "monthly_total": 0.0,
        "net_out_of_pocket": 0.0,
        "assets": 0.0,
        "runway_months": None,
        "decision_log": [],
        "expert_flags": [],
        "snapshot_for_crm": {},
    }
    cp = st.session_state.setdefault("cost_planner", cost_defaults)

    aud = st.session_state["audiencing"]
    quals = aud.get("qualifiers", {})

    if not quals.get("has_partner", False):
        cp["household"] = "single"
    cp.setdefault("custom_line_items", [])
    cp.setdefault("notes", "")
    cp.setdefault("other_base", 0.0)

    # Seed decision log contextually
    if quals.get("on_medicaid"):
        if "Medicaid short-circuit" not in cp["decision_log"]:
            cp["decision_log"].append("Medicaid short-circuit")
        gcp_state = st.session_state["gcp"]
        if gcp_state.get("payment_context") != "medicaid":
            gcp_state["payment_context"] = "medicaid"

    recommended = st.session_state["gcp"].get("recommended_setting")
    if recommended and all(
        entry != f"Recommendation: {recommended}" for entry in cp["decision_log"]
    ):
        cp["decision_log"].append(f"Recommendation: {recommended}")


def inputs_dict() -> Dict[str, float]:
    ensure_core_state()
    return st.session_state["cost_planner"]["inputs"]


def get_numeric(field_id: str) -> float:
    value = inputs_dict().get(field_id)
    if value is None:
        spec = load_field_specs().get(field_id)
        return spec.default if spec else 0.0
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def set_numeric(field_id: str, value: float) -> None:
    inputs_dict()[field_id] = float(value or 0.0)


def summarize_categories(keys: Iterable[str], mapping: Dict[str, str]) -> float:
    normalized_inputs = {
        mapping[fid]: float(inputs_dict().get(fid, 0) or 0)
        for fid in mapping
    }
    return sum(normalized_inputs.get(k, 0.0) for k in keys)


def recompute_costs() -> None:
    ensure_core_state()
    cp = st.session_state["cost_planner"]
    mapping = load_field_map()

    def total(*normalized: str) -> float:
        total_value = 0.0
        for fid, norm in mapping.items():
            if norm in normalized:
                total_value += float(cp["inputs"].get(fid, 0) or 0)
        return total_value

    cp["subtotals"]["housing"] = total("housing_rent", "housing_util", "housing_maint")
    cp["subtotals"]["care"] = total("care_base", "care_level_addon", "care_second_person", "care_suppl_services")
    cp["subtotals"]["medical"] = total("med_rx", "med_supplies", "med_transport")
    cp["subtotals"]["insurance"] = total("ins_health", "ins_ltc", "ins_other")
    cp["subtotals"]["debts"] = total("debt_cc", "debt_loans")
    cp["subtotals"]["other"] = total("other_misc")

    offsets_income = total("inc_ss", "inc_pension", "inc_annuity", "inc_other")
    offsets_benefits = total("off_va", "off_medicaid", "off_ltc_payout")
    cp["subtotals"]["offsets"] = offsets_income + offsets_benefits

    cp["monthly_total"] = sum(
        v for k, v in cp["subtotals"].items() if k != "offsets"
    )
    cp["net_out_of_pocket"] = max(0.0, cp["monthly_total"] - cp["subtotals"]["offsets"])

    if cp["mode"] == "planning":
        assets_value = float(cp["inputs"].get("assets_total", 0) or 0)
        cp["assets"] = assets_value
        cp["runway_months"] = (
            assets_value / cp["net_out_of_pocket"] if cp["net_out_of_pocket"] > 0 else None
        )
    else:
        cp["assets"] = 0.0
        cp["runway_months"] = None

    cp["snapshot_for_crm"] = {
        "audiencing": st.session_state.get("audiencing_snapshot")
        or st.session_state.get("audiencing"),
        "gcp": st.session_state.get("gcp"),
        "inputs": cp["inputs"],
        "subtotals": cp["subtotals"],
        "monthly_total": cp["monthly_total"],
        "net_out_of_pocket": cp["net_out_of_pocket"],
        "assets": cp["assets"],
        "runway_months": cp["runway_months"],
        "decision_log": cp["decision_log"],
        "expert_flags": cp["expert_flags"],
        "custom_line_items": cp.get("custom_line_items", []),
        "notes": cp.get("notes", ""),
    }


def format_currency(value: float) -> str:
    return f"${value:,.0f}" if value else "$0"


def audiencing_badges() -> Tuple[str, List[str]]:
    aud = st.session_state.get("audiencing", {})
    entry = aud.get("entry", "self")
    quals = aud.get("qualifiers", {})
    badges = []
    if quals.get("on_medicaid"):
        badges.append("Medicaid")
    if quals.get("is_veteran"):
        badges.append("Veteran")
    if quals.get("has_partner"):
        badges.append("Partner household")
    if quals.get("owns_home"):
        badges.append("Owns home")
    if quals.get("urgent"):
        badges.append("Urgent")
    return entry, badges


def expert_flag(flag: str) -> None:
    ensure_core_state()
    cp = st.session_state["cost_planner"]
    if flag not in cp["expert_flags"]:
        cp["expert_flags"].append(flag)


def add_decision_log(entry: str) -> None:
    ensure_core_state()
    cp = st.session_state["cost_planner"]
    if entry not in cp["decision_log"]:
        cp["decision_log"].append(entry)
