from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional


@dataclass(frozen=True)
class Field:
    key: str
    label: str
    type: str  # "money" | "int" | "percent" | "choice" | "bool" | "text"
    help: str = ""
    choices: Optional[List[str]] = None
    required: bool = False
    default: Any = None
    validate: Optional[Callable[[Any], Optional[str]]] = None  # return error text or None


def _nonneg_number(value: Any) -> Optional[str]:
    try:
        if float(value) < 0:
            return "Must be zero or greater."
    except Exception:
        return "Enter a number."
    return None


def _percent_0_100(value: Any) -> Optional[str]:
    try:
        pct = float(value)
        if pct < 0 or pct > 100:
            return "Enter a percent between 0 and 100."
    except Exception:
        return "Enter a percent (0–100)."
    return None


INCOME_FIELDS: List[Field] = [
    Field("inc_ss_monthly", "Social Security (monthly)", "money", help="Before taxes.", default=0, validate=_nonneg_number),
    Field("inc_pension_monthly", "Pension (monthly)", "money", default=0, validate=_nonneg_number),
    Field("inc_work_wages", "Wages / self-employment (monthly)", "money", default=0, validate=_nonneg_number),
    Field("inc_annuity", "Annuity / guaranteed income (monthly)", "money", default=0, validate=_nonneg_number),
    Field("inc_investment_draw", "Investment drawdown (monthly)", "money", help="Average withdrawal across accounts.", default=0, validate=_nonneg_number),
    Field("inc_other", "Other recurring income (monthly)", "money", default=0, validate=_nonneg_number),
]

EXPENSE_FIELDS: List[Field] = [
    Field("exp_housing_rent", "Rent (monthly)", "money", default=0, validate=_nonneg_number),
    Field("exp_housing_mortgage", "Mortgage (monthly)", "money", default=0, validate=_nonneg_number),
    Field("exp_property_tax", "Property tax (monthly avg)", "money", default=0, validate=_nonneg_number),
    Field("exp_home_insurance", "Home insurance (monthly avg)", "money", default=0, validate=_nonneg_number),
    Field("exp_utilities", "Utilities (electric/gas/water/internet)", "money", default=0, validate=_nonneg_number),
    Field("exp_transportation", "Transportation (fuel, insurance, transit)", "money", default=0, validate=_nonneg_number),
    Field("exp_food", "Food & household", "money", default=0, validate=_nonneg_number),
    Field("exp_health_ins_premiums", "Health insurance premiums", "money", default=0, validate=_nonneg_number),
    Field("exp_rx_out_of_pocket", "Rx & medical out-of-pocket", "money", default=0, validate=_nonneg_number),
    Field("exp_paid_care", "Paid care (in-home, adult day, etc.)", "money", default=0, validate=_nonneg_number),
    Field("exp_misc", "Other expenses", "money", default=0, validate=_nonneg_number),
]

BENEFITS_FIELDS: List[Field] = [
    Field("ben_medicare_plan", "Medicare plan", "choice", choices=["Unknown", "Original + Medigap", "Medicare Advantage", "Not eligible"], default="Unknown"),
    Field("ben_part_d", "Part D (drug plan) in place?", "choice", choices=["Unknown", "Yes", "No"], default="Unknown"),
    Field("ben_va", "VA benefits", "choice", choices=["Unknown", "Yes", "No"], default="Unknown"),
    Field("ben_snap", "SNAP / food assistance", "choice", choices=["Unknown", "Yes", "No"], default="Unknown"),
    Field("ben_state_prog", "State programs (SHIP, HCBS, etc.)", "text", help="Name if known."),
]

VA_DRAWER_KEYS = {
    "ben_va_status": "Unknown|Yes|No",
    "ben_va_service_era": "Unknown|WWII|Korea|Vietnam|Gulf War/Post-9/11|Other",
    "ben_va_discharge": "Unknown|Honorable/General|Other/Uncharacterized",
    "ben_va_disability_rating": "Unknown|0%|10%|30%|50%|70%|100%",
    "ben_va_survivor_status": "Unknown|No|Surviving spouse/dependent",
    "ben_va_auto_estimate": "bool",
    "ben_va_cond_*": "bool flags for cognitive/behavioral conditions",
    "profile_marital_status": "Unknown|Single|Married/partnered|Widowed",
    "inc_va_monthly": "float — VA benefit estimate flowing into income totals",
}

HOME_FIELDS: List[Field] = [
    Field("home_status", "Housing status", "choice", choices=["Own", "Rent", "With family / other"], required=True, default="Own"),
    Field("home_mortgage", "Monthly mortgage", "money", default=0, validate=_nonneg_number),
    Field("home_rent", "Monthly rent", "money", default=0, validate=_nonneg_number),
    Field("home_property_tax", "Property tax (monthly avg)", "money", default=0, validate=_nonneg_number),
    Field("home_insurance", "Homeowners/renters insurance (monthly avg)", "money", default=0, validate=_nonneg_number),
    Field("home_move_plan", "Considering move / sale within 12–24 months?", "choice", choices=["No", "Yes — downsizing", "Yes — sell home", "Yes — move to care setting"], default="No"),
]

HOME_MODS_FIELDS: List[Field] = [
    Field("mods_one_time", "One-time modifications (total estimate)", "money", default=0, validate=_nonneg_number),
    Field("mods_ongoing_monthly", "Ongoing home maintenance (monthly)", "money", default=0, validate=_nonneg_number),
]

LIQUIDITY_FIELDS: List[Field] = [
    Field("liq_gap_known", "Do you expect a monthly gap?", "choice", choices=["Unknown", "No", "Yes — small", "Yes — moderate", "Yes — large"], default="Unknown"),
    Field("liq_gap_estimate", "Estimated monthly gap (+ means costs > income)", "money", default=0, validate=_nonneg_number),
    Field("liq_bridge_sources", "Gap coverage sources", "text", help="E.g., savings drawdown, short-term asset sale, family support."),
]

CAREGIVER_FIELDS: List[Field] = [
    Field("cg_hours_per_week", "Informal caregiver hours per week", "int", default=0, validate=_nonneg_number),
    Field("cg_burnout_risk", "Caregiver burnout risk", "choice", choices=["Unknown", "Low", "Moderate", "High"], default="Unknown"),
    Field("cg_out_of_pocket", "Caregiver out-of-pocket (monthly)", "money", default=0, validate=_nonneg_number),
]

ASSETS_FIELDS: List[Field] = [
    Field("assets_cash", "Cash / savings", "money", default=0, validate=_nonneg_number),
    Field("assets_investments", "Investments (brokerage, CDs)", "money", default=0, validate=_nonneg_number),
    Field("assets_retirement", "Retirement accounts (IRA/401k/403b)", "money", default=0, validate=_nonneg_number),
    Field("assets_hsa", "HSA / MSA", "money", default=0, validate=_nonneg_number),
    Field("assets_vehicle_value", "Vehicles (resale value)", "money", default=0, validate=_nonneg_number),
    Field("assets_other", "Other assets", "money", default=0, validate=_nonneg_number),
]

TIMELINE_FIELDS: List[Field] = [
    Field("tl_horizon_months", "Planning horizon (months)", "int", default=12, validate=_nonneg_number),
    Field("tl_expected_events", "Expected events", "text", help="E.g., surgery, move, selling a home, travel, seasonal help."),
    Field("tl_cost_change_pct", "Expected monthly cost change (%)", "percent", default=0, validate=_percent_0_100),
]

MODULE_FIELD_MAP: Dict[str, List[Field]] = {
    "income": INCOME_FIELDS,
    "expenses": EXPENSE_FIELDS,
    "benefits": BENEFITS_FIELDS,
    "home": HOME_FIELDS,
    "home_mods": HOME_MODS_FIELDS,
    "liquidity": LIQUIDITY_FIELDS,
    "caregiver": CAREGIVER_FIELDS,
    "assets": ASSETS_FIELDS,
    "timeline": TIMELINE_FIELDS,
}
