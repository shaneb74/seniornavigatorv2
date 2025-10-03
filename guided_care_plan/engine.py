"""Rule-based evaluation for the Guided Care Plan."""

from __future__ import annotations

from typing import Dict, List, Tuple

from .state import QUESTION_ORDER

SENIOR_SETTINGS = ["home", "assisted", "memory"]
CARE_INTENSITIES = ["low", "med", "high"]


def _score_daily_life(answers: Dict[str, str]) -> int:
    """Score daily life items to gauge baseline support."""

    score = 0
    adl_score = {
        "none": 0,
        "one_two": 1,
        "three_four": 2,
        "most": 3,
    }.get(answers.get("adl_help"), 0)
    support_score = {
        "robust": 0,
        "intermittent": 1,
        "limited": 2,
        "none": 3,
    }.get(answers.get("caregiver_support"), 0)
    living_score = {
        "own_home": 0,
        "with_family": 1,
        "senior_apartment": 1,
        "assisted_setting": 2,
        "other": 1,
    }.get(answers.get("living_now"), 0)

    score += adl_score + support_score + living_score
    return score


def _score_health_safety(answers: Dict[str, str]) -> Tuple[int, List[str]]:
    """Score safety indicators and capture notable flags."""

    score = 0
    flags: List[str] = []

    falls = answers.get("falls", "none")
    falls_score = {"none": 0, "one": 1, "multiple": 3}.get(falls, 0)
    if falls_score:
        flags.append("falls")
    score += falls_score

    cognition = answers.get("cognition", "clear")
    cognition_score = {
        "clear": 0,
        "mild_changes": 1,
        "moderate_changes": 2,
        "significant_changes": 3,
    }.get(cognition, 0)
    if cognition_score >= 2:
        flags.append("cognition")
    score += cognition_score

    behaviors = answers.get("behavior_risks", "none")
    behavior_score = {
        "none": 0,
        "occasional": 1,
        "frequent": 2,
        "high_risk": 3,
    }.get(behaviors, 0)
    if behavior_score >= 2:
        flags.append("behaviors")
    score += behavior_score

    med_mgmt = answers.get("med_mgmt", "simple")
    med_score = {
        "simple": 0,
        "organized": 1,
        "help_needed": 2,
        "complex": 3,
    }.get(med_mgmt, 0)
    if med_score >= 2:
        flags.append("med_mgmt")
    score += med_score

    home = answers.get("home_safety", "safe")
    home_score = {
        "safe": 0,
        "minor_updates": 1,
        "needs_mods": 2,
        "unsafe": 3,
    }.get(home, 0)
    if home_score >= 2:
        flags.append("home_safety")
    score += home_score

    supervision = answers.get("supervision", "minimal")
    supervision_score = {
        "minimal": 0,
        "daytime": 1,
        "extended": 2,
        "around_clock": 3,
    }.get(supervision, 0)
    if supervision_score >= 2:
        flags.append("supervision")
    score += supervision_score

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

    if answers.get("falls") in {"one", "multiple"}:
        safety_flags.append("falls")
    if answers.get("behavior_risks") in {"frequent", "high_risk"}:
        safety_flags.append("behaviors")
    if answers.get("med_mgmt") in {"help_needed", "complex"}:
        safety_flags.append("med_mgmt")
    if answers.get("home_safety") in {"needs_mods", "unsafe"}:
        safety_flags.append("home_safety")

    if "Dementia or Alzheimer's" in chronic_conditions or answers.get("behavior_risks") == "high_risk":
        recommended = "memory"
    elif total_score >= 11 or answers.get("supervision") == "around_clock":
        recommended = "assisted"
    else:
        recommended = "home"

    if recommended == "home" and answers.get("living_now") == "assisted_setting":
        recommended = "assisted"

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
    chosen = answers.get("funding_confidence")
    if chosen:
        return str(chosen)

    caregiver = answers.get("caregiver_support", "robust")
    medicaid = (
        isinstance(audiencing, dict)
        and audiencing.get("qualifiers", {}).get("on_medicaid")
    )
    if medicaid:
        return "concerned"
    if caregiver in {"robust", "intermittent"}:
        return "confident"
    if caregiver == "limited":
        return "balanced"
    return "unsure"


def _build_decision_trace(
    recommended_setting: str,
    intensity: str,
    safety_flags: List[str],
    chronic_conditions: List[str],
    preferences: List[str],
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

    if chronic_conditions and chronic_conditions != ["None"]:
        trace.append(
            "Chronic conditions to plan around: "
            + ", ".join(cond for cond in chronic_conditions if cond != "None")
            + "."
        )

    filtered_preferences = [pref for pref in preferences if pref != "No strong preference"]
    if filtered_preferences:
        trace.append(
            "Preferences noted: "
            + ", ".join(filtered_preferences)
            + "."
        )
    return trace


def evaluate_guided_care(
    answers: Dict[str, object],
    audiencing: Dict[str, object] | None = None,
) -> Dict[str, object]:
    """Evaluate answers and return the Guided Care Plan outcome."""

    audiencing = audiencing or {}

    normalized_answers = {key: answers.get(key) for key in QUESTION_ORDER}
    chronic_conditions = list(normalized_answers.get("chronic") or [])
    preferences = list(normalized_answers.get("preferences") or [])
    if "None" in chronic_conditions and len(chronic_conditions) > 1:
        chronic_conditions = [cond for cond in chronic_conditions if cond != "None"]

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
        preferences,
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
