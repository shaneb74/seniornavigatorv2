from __future__ import annotations

from typing import Any, Dict

"""
VA MAPR/A&A rules (configurable). Update annually.
Numbers below are *placeholders* for development and MUST be validated
against the latest VA MAPR tables before production.
We separate: Veteran (single), Veteran+spouse, Surviving spouse (DIC/pension).
Tiers: BASE (pension), HOUSEBOUND, AID_ATTENDANCE.

MAPR dict units: USD/year.
"""

MAPR_2024: Dict[str, Dict[str, float]] = {
    "VET_SINGLE": {
        "BASE": 16800.0,
        "HOUSEBOUND": 20500.0,
        "AID_ATTENDANCE": 27900.0,
    },
    "VET_MARRIED": {
        "BASE": 22100.0,
        "HOUSEBOUND": 25800.0,
        "AID_ATTENDANCE": 33300.0,
    },
    "SURVIVOR": {
        "BASE": 11400.0,
        "HOUSEBOUND": 14000.0,
        "AID_ATTENDANCE": 18600.0,
    },
}


def pick_category(ans: Dict[str, Any]) -> str:
    survivor = ans.get("ben_va_survivor_status") == "Surviving spouse/dependent"
    if survivor:
        return "SURVIVOR"
    married = ans.get("profile_marital_status") == "Married/partnered"
    return "VET_MARRIED" if married else "VET_SINGLE"


def pick_tier(ans: Dict[str, Any]) -> str:
    setting = str(ans.get("gcp_reco_setting") or ans.get("care_setting_expected", "")).lower()
    cognition_severe = str(ans.get("gcp_health_cognition_level", "")).lower() in (
        "serious confusion",
        "severe",
        "advanced dementia",
    )
    caregiver_most = str(ans.get("dl_support_amount", "")).lower() in (
        "support most/all of the time",
        "most days",
    )
    if any(flag in setting for flag in ("assisted", "memory", "nursing", "board & care")) or (
        cognition_severe and caregiver_most
    ):
        return "AID_ATTENDANCE"

    mobility_cov = str(ans.get("safety_supervision", "")).lower()
    if "not covered" in mobility_cov or "uncertain" in mobility_cov:
        return "HOUSEBOUND"

    return "BASE"


def to_annual(value) -> float:
    try:
        return float(value) * 12.0
    except Exception:
        return 0.0


def _num(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return float(default)


def gather_income(ans: Dict[str, Any]) -> float:
    total_monthly = 0.0
    for key, value in ans.items():
        if not key.startswith("inc_"):
            continue
        if key == "inc_va_monthly":
            continue
        total_monthly += _num(value, 0.0)
    return total_monthly * 12.0


def gather_medical_deductions(ans: Dict[str, Any]) -> float:
    keys = (
        "exp_med_premiums_monthly",
        "exp_rx_out_of_pocket_monthly",
        "exp_home_care_monthly",
        "exp_al_monthly",
        "exp_memory_care_monthly",
        "exp_nursing_home_monthly",
    )
    monthly_total = sum(_num(ans.get(key, 0.0), 0.0) for key in keys)
    return monthly_total * 12.0


def estimate_pension(
    ans: Dict[str, Any],
    mapr_table: Dict[str, Dict[str, float]] = MAPR_2024,
) -> Dict[str, float]:
    category = pick_category(ans)
    tier = pick_tier(ans)
    mapr = float(mapr_table.get(category, {}).get(tier, 0.0))

    income_annual = gather_income(ans)
    medical_annual = gather_medical_deductions(ans)

    med_threshold = 0.05 * mapr
    med_deductible = max(0.0, medical_annual - med_threshold)

    countable = max(0.0, income_annual - med_deductible)
    pension_annual = max(0.0, mapr - countable)
    pension_monthly = round(pension_annual / 12.0, 2)

    return {
        "mapr": round(mapr, 2),
        "income_annual": round(income_annual, 2),
        "med_allowed": round(medical_annual, 2),
        "med_threshold": round(med_threshold, 2),
        "med_deductible": round(med_deductible, 2),
        "countable": round(countable, 2),
        "pension_annual": round(pension_annual, 2),
        "pension_monthly": pension_monthly,
        "category": category,
        "tier": tier,
    }
