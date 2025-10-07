from __future__ import annotations
from __future__ import annotations
from typing import Dict, List


SEVERE_COGNITION = {"moderate", "severe", "serious_confusion", "frequent_memory_issues"}
LIMITED_SUPPORT = {"none", "few_days_week"}
HIGH_ADL_NEED = {"4-5", "6+"}
ISOLATION_HIGH = {"rarely", "almost_never"}
MOBILITY_LIMITED = {"cane_or_walker", "wheelchair"}


def _as_list(value) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str) and value:
        return [value]
    return []


def score_answers(answers: Dict) -> Dict:
    cognition = (answers.get("cognition") or "").strip()
    falls = (answers.get("falls") or "none").strip()
    behavior = _as_list(answers.get("behavior_risks"))
    supervision = (answers.get("supervision") or "always").strip()
    home = (answers.get("home_safety") or "safe").strip()
    med_mgmt = (answers.get("med_mgmt") or "simple").strip()
    caregiver = (answers.get("caregiver_support") or "24_7").strip()
    adl = (answers.get("adl_help") or "0-1").strip()
    isolation = (answers.get("social_isolation") or "daily_or_often").strip()
    mobility = (answers.get("mobility") or "no_issues").strip()

    risk_flags = {
        "cognition_severe": cognition in SEVERE_COGNITION,
        "wandering_risk": any(token in {"wandering", "exit_seeking", "agitation"} for token in behavior),
        "falls_risk": falls in {"one", "recurrent"},
        "supervision_gap": supervision in {"rarely", "never"},
        "home_unsafe": home in {"some_risks", "unsafe"},
        "med_mgmt_complex": med_mgmt in {"several", "complex"},
        "support_gap": caregiver in LIMITED_SUPPORT,
        "adl_high": adl in HIGH_ADL_NEED,
        "isolation_high": isolation in ISOLATION_HIGH,
        "mobility_limitations": mobility in MOBILITY_LIMITED,
    }

    score = 0.0
    if risk_flags["cognition_severe"]:
        score += 2.0
    if risk_flags["wandering_risk"]:
        score += 1.0
    if risk_flags["falls_risk"]:
        score += 1.5 if falls == "recurrent" else 1.0
    if risk_flags["supervision_gap"]:
        score += 1.0
    if risk_flags["home_unsafe"]:
        score += 0.75
    if risk_flags["med_mgmt_complex"]:
        score += 0.75
    if risk_flags["support_gap"]:
        score += 0.75
    if risk_flags["adl_high"]:
        score += 1.0
    if risk_flags["isolation_high"]:
        score += 0.5
    if risk_flags["mobility_limitations"]:
        score += 0.5

    if score <= 2.0:
        acuity = "low"
    elif score <= 4.5:
        acuity = "moderate"
    else:
        acuity = "high"

    # Determine recommended setting
    if risk_flags["cognition_severe"] and risk_flags["wandering_risk"] and (
        risk_flags["supervision_gap"] or risk_flags["home_unsafe"]
    ):
        recommended_setting = "memory_care"
    elif risk_flags["med_mgmt_complex"] and mobility == "wheelchair" and risk_flags["supervision_gap"]:
        recommended_setting = "skilled_nursing"
    elif acuity == "high" or (
        risk_flags["home_unsafe"] and risk_flags["support_gap"]
    ):
        recommended_setting = "assisted_living"
    elif risk_flags["support_gap"] or risk_flags["adl_high"] or risk_flags["home_unsafe"]:
        recommended_setting = "home_with_support"
    else:
        recommended_setting = "remain_at_home"

    rationale: List[str] = []
    if risk_flags["adl_high"]:
        rationale.append("Needs help with multiple daily activities, requiring routine assistance.")
    if risk_flags["support_gap"]:
        rationale.append("Limited caregiver availability at home.")
    if risk_flags["cognition_severe"]:
        rationale.append("Cognition concerns suggest close monitoring and structured support.")
    if risk_flags["wandering_risk"]:
        rationale.append("Behavioral risks (wandering/agitation) benefit from secure supervision.")
    if risk_flags["falls_risk"]:
        rationale.append("Recent falls raise safety considerations.")
    if risk_flags["home_unsafe"]:
        rationale.append("Home environment has safety hazards to address.")
    if not rationale:
        rationale.append("Current supports appear stable; continue monitoring periodically.")

    return {
        "risk_flags": risk_flags,
        "acuity_level": acuity,
        "recommended_setting": recommended_setting,
        "rationale": rationale,
    }
