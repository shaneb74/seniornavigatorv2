"""Rule-based evaluation for the Guided Care Plan."""
from __future__ import annotations


from typing import Dict, List, Tuple

from .state import QUESTION_ORDER

SENIOR_SETTINGS = ["home", "assisted", "memory"]
CARE_INTENSITIES = ["low", "med", "high"]

CHRONIC_FRIENDLY_LABELS = {
    "diabetes": "Diabetes",
    "parkinson": "Parkinson's",
    "stroke": "Stroke",
    "copd": "COPD",
    "chf": "Heart failure (CHF)",
    "other": "Other condition",
}


def _score_daily_life(answers: Dict[str, str]) -> int:
    score = 0
    score_map = {
        "adl_help": {
            "0-1": 0,
            "2-3": 1,
            "4-5": 2,
            "6+": 3,
        },
        "med_mgmt": {
            "simple": 0,
            "several": 1,
            "complex": 3,
        },
        "caregiver_support": {
            "24_7": 0,
            "most_days": 1,
            "few_days_week": 2,
            "none": 3,
        },
    }
    for key, mapping in score_map.items():
        score += mapping.get(answers.get(key, ""), 0)
    return score


def _score_health_safety(answers: Dict[str, str]) -> Tuple[int, List[str]]:
    score = 0
    flags: List[str] = []

    falls = answers.get("falls", "none")
    if falls == "recurrent":
        score += 3
        flags.append("falls")
    elif falls == "one":
        score += 1
        flags.append("falls")

    cognition = answers.get("cognition", "normal")
    cognition_score = {
        "normal": 0,
        "mild": 1,
        "moderate": 2,
        "severe": 3,
    }.get(cognition, 0)
    score += cognition_score
    if cognition_score >= 2:
        flags.append("cognition")

    raw_behaviors = answers.get("behavior_risks") or []
    if isinstance(raw_behaviors, str):
        raw_behaviors = [raw_behaviors]
    behaviors = {item for item in raw_behaviors if item and item != "none"}
    if not behaviors:
        behavior_score = 0
    elif {"wandering", "exit_seeking"} & behaviors:
        behavior_score = 3
    else:
        behavior_score = 2
    score += behavior_score
    if behavior_score >= 2:
        flags.append("behavior")

    supervision = answers.get("supervision", "always")
    supervision_score = {
        "always": 0,
        "sometimes": 1,
        "rarely": 2,
        "never": 3,
    }.get(supervision, 0)
    score += supervision_score
    if supervision_score >= 2:
        flags.append("supervision")

    return score, flags


def _derive_setting(
    daily_score: int,
    safety_score: int,
    answers: Dict[str, str],
    chronic_conditions: List[str],
) -> Tuple[str, str, List[str]]:
    """Compute the recommended setting, intensity, and safety flags."""

    total_score = daily_score + safety_score
    safety_flags: List[str] = []

    behavior_answers = answers.get("behavior_risks") or []
    if isinstance(behavior_answers, str):
        behavior_answers = [behavior_answers]
    behavior_set = {item for item in behavior_answers if item and item != "none"}

    if answers.get("falls") in {"one", "recurrent"}:
        safety_flags.append("falls")
    if behavior_set:
        safety_flags.append("behaviors")
    if answers.get("med_mgmt") in {"several", "complex"}:
        safety_flags.append("med_mgmt")

    if {"wandering", "exit_seeking"} & behavior_set:
        recommended = "memory"
    elif total_score >= 9 or answers.get("supervision") == "never":
        recommended = "assisted"
    else:
        recommended = "home"

    if total_score <= 4:
        intensity = "low"
    elif total_score <= 8:
        intensity = "med"
    else:
        intensity = "high"

    return recommended, intensity, safety_flags


def _derive_payment_context(audiencing: Dict[str, object]) -> str:
    qualifiers = audiencing.get("qualifiers", {}) if isinstance(audiencing, dict) else {}
    if qualifiers.get("on_medicaid"):
        return "medicaid"
    return "private"


def _derive_funding_confidence(answers: Dict[str, str], audiencing: Dict[str, object]) -> str:
    caregiver = answers.get("caregiver_support", "24_7")
    medicaid = (
        isinstance(audiencing, dict)
        and audiencing.get("qualifiers", {}).get("on_medicaid")
    )
    if medicaid:
        return "supported"
    if caregiver in {"24_7", "most_days"}:
        return "stable"
    if caregiver == "few_days_week":
        return "watch"
    return "stretched"


def _build_decision_trace(
    recommended_setting: str,
    intensity: str,
    safety_flags: List[str],
    chronic_conditions: List[str],
) -> List[str]:
    trace: List[str] = []
    if recommended_setting == "memory":
        trace.append("Memory care is recommended because of cognition changes and behavior patterns.")
    elif recommended_setting == "assisted":
        trace.append("Assisted living is recommended to provide daily help and reliable supervision.")
    else:
        trace.append("Home-based supports are recommended with added services as needed.")

    if intensity == "high":
        trace.append("Care intensity is high based on the combined daily living and safety scores.")
    elif intensity == "med":
        trace.append("Care intensity is moderate; add support for higher-risk areas.")
    else:
        trace.append("Care intensity is low; current supports are working well.")

    if safety_flags:
        flag_readout = ", ".join(sorted(set(safety_flags)))
        trace.append(f"Watch these safety areas: {flag_readout}.")

    filtered_chronic = [cond for cond in chronic_conditions if cond and cond != "none"]
    if filtered_chronic:
        friendly = [
            CHRONIC_FRIENDLY_LABELS.get(cond, cond.replace("_", " ").title())
            for cond in filtered_chronic
        ]
        trace.append(
            "Chronic conditions to plan around: " + ", ".join(friendly) + "."
        )
    return trace


def evaluate_guided_care(
    answers: Dict[str, object],
    audiencing: Dict[str, object] | None = None,
) -> Dict[str, object]:
    """Evaluate answers and return the Guided Care Plan outcome."""

    audiencing = audiencing or {}

    normalized_answers = {key: answers.get(key) for key in QUESTION_ORDER}

    behavior_risks = normalized_answers.get("behavior_risks") or []
    if isinstance(behavior_risks, str):
        behavior_risks = [behavior_risks]
    normalized_answers["behavior_risks"] = behavior_risks

    chronic_conditions = list(normalized_answers.get("chronic") or [])
    if "none" in chronic_conditions and len(chronic_conditions) > 1:
        chronic_conditions = [cond for cond in chronic_conditions if cond != "none"]
    normalized_answers["chronic"] = chronic_conditions

    daily_score = _score_daily_life(normalized_answers)
    safety_score, safety_flag_details = _score_health_safety(normalized_answers)
    recommended_setting, intensity, base_flags = _derive_setting(
        daily_score, safety_score, normalized_answers, chronic_conditions
    )
    payment_context = _derive_payment_context(audiencing)
    funding_confidence = _derive_funding_confidence(normalized_answers, audiencing)

    safety_flags = sorted(set(base_flags + safety_flag_details))

    decision_trace = _build_decision_trace(
        recommended_setting,
        intensity,
        safety_flags,
        chronic_conditions,
    )

    return {
        "recommended_setting": recommended_setting,
        "care_intensity": intensity,
        "safety_flags": safety_flags,
        "chronic_conditions": chronic_conditions,
        "payment_context": payment_context,
        "funding_confidence": funding_confidence,
        "audiencing_snapshot": audiencing,
        "DecisionTrace": decision_trace,
    }
