from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional


Predicate = Callable[[Dict[str, Any]], bool]


@dataclass(frozen=True)
class ModuleCard:
    key: str
    title: str
    blurb: str
    route: str
    icon: str
    visible_if: Optional[Predicate] = None
    note: Optional[str] = None


def _flatten(source: Dict[str, Any], target: Dict[str, Any]) -> None:
    """Recursively inline nested dict values into a flat lookup."""
    for key, value in source.items():
        if isinstance(value, dict):
            _flatten(value, target)
        else:
            target[key] = value


def _answers(ss) -> Dict[str, Any]:
    """Return a flattened view of Cost Planner answers from session_state."""
    aggregate: Dict[str, Any] = {}

    cp_answers = ss.get("cp_answers")
    if isinstance(cp_answers, dict):
        _flatten(cp_answers, aggregate)

    cp_state = ss.get("cost_planner")
    if isinstance(cp_state, dict):
        _flatten(cp_state, aggregate)

    return aggregate


def _gcp(ss) -> Dict[str, Any]:
    """Return Guided Care Plan answers if present."""
    answers = ss.get("gcp_answers")
    return answers if isinstance(answers, dict) else {}


def always(_: Dict[str, Any]) -> bool:
    return True


def _as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value).strip().lower()


def _as_float(value: Any) -> float:
    try:
        if value is None:
            return 0.0
        if isinstance(value, (int, float)):
            return float(value)
        text = str(value).strip().replace(",", "").replace("$", "")
        return float(text) if text else 0.0
    except Exception:
        return 0.0


def owns_home(data: Dict[str, Any]) -> bool:
    candidates = [
        data.get("home_owns"),
        data.get("owns_home"),
        data.get("home_status"),
        data.get("housing_status"),
        data.get("residence_status"),
        data.get("home_type"),
        data.get("primary_residence_status"),
    ]
    for value in candidates:
        token = _as_text(value)
        if not token:
            continue
        if token in {"owner", "own", "owns", "owning", "homeowner", "yes", "true", "y"}:
            return True
        if token in {"rent", "renter", "tenant", "leasing", "no", "false", "n"}:
            return False

    if isinstance(data.get("owns_home"), bool):
        return bool(data["owns_home"])

    if _as_float(data.get("home_equity")) > 0:
        return True

    return False


def has_mortgage(data: Dict[str, Any]) -> bool:
    candidates = [
        data.get("home_mortgage"),
        data.get("has_mortgage"),
        data.get("mortgage_status"),
    ]
    for value in candidates:
        token = _as_text(value)
        if token in {"true", "yes", "y", "active", "current"}:
            return True
        if token in {"false", "no", "n"}:
            return False
    return False


def considering_move_or_sale(data: Dict[str, Any]) -> bool:
    candidates = [
        data.get("home_move_plan"),
        data.get("considering_move"),
        data.get("plan_move"),
        data.get("move_plan"),
        data.get("home_transition_plan"),
    ]
    for value in candidates:
        token = _as_text(value)
        if token in {"true", "yes", "y", "downsizing", "selling", "sale", "sell", "move", "moving"}:
            return True
    return False


def has_informal_caregiver(data: Dict[str, Any]) -> bool:
    candidates = [
        data.get("caregiver_support_level"),
        data.get("caregiver_support"),
        data.get("caregiver_type"),
        data.get("informal_support_level"),
        data.get("caregiver_hours"),
    ]
    for value in candidates:
        token = _as_text(value)
        if not token:
            continue
        if token in {"none", "no_support", "no", "false", "0"}:
            continue
        return True
    return False


def has_assets(data: Dict[str, Any]) -> bool:
    numeric_keys = [
        "assets_total_estimate",
        "assets_any_total",
        "assets_liquid_total",
        "assets_total_effective",
        "home_equity",
    ]
    if any(_as_float(data.get(key)) > 0 for key in numeric_keys):
        return True

    flag_keys = [
        "has_savings",
        "has_investments",
        "has_hsa",
        "has_ira",
        "has_401k",
        "has_other_assets",
    ]
    if any(_as_text(data.get(key)) in {"true", "yes", "y"} for key in flag_keys):
        return True

    return owns_home(data)


def has_benefit_opportunity(_: Dict[str, Any]) -> bool:
    return True


def has_liquidity_needs(data: Dict[str, Any]) -> bool:
    gap_keys = [
        "cp_monthly_gap_estimate",
        "monthly_gap",
        "gap_amount",
        "cost_gap",
    ]
    if any(abs(_as_float(data.get(key))) > 0 for key in gap_keys):
        return True

    flag = _as_text(data.get("cashflow_concern"))
    return flag in {"true", "yes", "y", "concern", "high"}


MODULES: list[ModuleCard] = [
    ModuleCard(
        key="income",
        title="Income",
        blurb="List monthly income sources like Social Security, pensions, work, annuities, investment drawdowns, and other recurring payments.",
        route="app_pages/cost_planner_v2/cost_planner_income_v2.py",
        icon="🧾",
        visible_if=always,
        note="Always visible.",
    ),
    ModuleCard(
        key="expenses",
        title="Expenses",
        blurb="Capture current monthly spending—housing, utilities, transportation, food, insurance, and care—to compare directly with income.",
        route="app_pages/cost_planner_v2/cost_planner_expenses_v2.py",
        icon="🧮",
        visible_if=always,
        note="Always visible.",
    ),
    ModuleCard(
        key="benefits",
        title="Benefits & Coverage",
        blurb="Check eligibility and record programs like Medicare, VA benefits, SNAP, and state supports that may offset monthly costs.",
        route="app_pages/cost_planner_v2/cost_planner_benefits_v2.py",
        icon="🎖️",
        visible_if=has_benefit_opportunity,
        note="Usually visible—helpful even if you’re unsure about benefits.",
    ),
    ModuleCard(
        key="home",
        title="Home & Housing",
        blurb="Document housing status (own, rent, with family), mortgage or rent amounts, property taxes, insurance, and any planned moves.",
        route="app_pages/cost_planner_v2/cost_planner_home_v2.py",
        icon="🏠",
        visible_if=always,
        note="Always visible; details adjust based on ownership status.",
    ),
    ModuleCard(
        key="home_mods",
        title="Home Modifications",
        blurb="Estimate one-time home updates—ramps, grab bars, bathroom or lighting changes—and any maintenance needed to stay safely at home.",
        route="app_pages/cost_planner_v2/cost_planner_home_mods_v2.py",
        icon="🔧",
        visible_if=owns_home,
        note="Appears when home ownership is indicated.",
    ),
    ModuleCard(
        key="liquidity",
        title="Liquidity & Gap Planning",
        blurb="When monthly costs exceed income, explore how to bridge the gap with savings drawdowns, asset sales, or short-term financing.",
        route="app_pages/cost_planner_v2/cost_planner_liquidity_v2.py",
        icon="💵",
        visible_if=has_liquidity_needs,
        note="Appears when a cash-flow gap or concern is flagged.",
    ),
    ModuleCard(
        key="caregiver",
        title="Caregiver Support",
        blurb="Track informal caregiver hours, burnout risk, and out-of-pocket costs so we can flag when paid help may be needed.",
        route="app_pages/cost_planner_v2/cost_planner_caregiver_v2.py",
        icon="👥",
        visible_if=has_informal_caregiver,
        note="Appears when caregiver help is present or expected.",
    ),
    ModuleCard(
        key="assets",
        title="Assets & Savings",
        blurb="List savings accounts, investments, retirement funds, HSAs, vehicles, and real estate used for what-if projections.",
        route="app_pages/cost_planner_v2/cost_planner_assets_v2.py",
        icon="🏦",
        visible_if=has_assets,
        note="Appears when assets or home equity are in play.",
    ),
    ModuleCard(
        key="timeline",
        title="Timeline & Scenarios",
        blurb="Lay out the next 12–24 months—care needs, cost changes, or big events like moves or surgeries that shape the plan.",
        route="app_pages/cost_planner_v2/cost_planner_timeline_v2.py",
        icon="📈",
        visible_if=always,
        note="Always visible.",
    ),
]


__all__ = [
    "ModuleCard",
    "MODULES",
    "always",
    "_answers",
    "_gcp",
    "owns_home",
    "has_assets",
    "has_liquidity_needs",
]
