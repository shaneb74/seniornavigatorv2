from __future__ import annotations
from functools import lru_cache
from datetime import datetime, timezone
import sys
import types
from typing import Dict, List, Tuple

if "senior_nav.lib" not in sys.modules:
    sys.modules["senior_nav.lib"] = types.ModuleType("senior_nav.lib")
if "senior_nav.lib.trace" not in sys.modules:
    trace_module = types.ModuleType("senior_nav.lib.trace")

    def _noop_trace(*args, **kwargs):
        return None

    trace_module.trace = _noop_trace
    sys.modules["senior_nav.lib.trace"] = trace_module
    sys.modules["senior_nav.lib"].trace = trace_module

from gcp_pr_tool_bundle.guided_care_plan.engine import *  # noqa: F401,F403
from gcp_pr_tool_bundle.guided_care_plan.engine import evaluate_guided_care  # noqa: F401
from gcp_core.questions import load_questions
from gcp_core.state import ensure_session
from gcp_pr_tool_bundle.guided_care_plan.state import get_answers as _bundle_get_answers
from gcp_core import scoring as gcp_scoring

SECTION_ORDER: List[Tuple[str, List[str]]] = [
    ("financial", ["medicaid_status", "funding_confidence"]),
    ("daily_life_support", ["caregiver_support", "adl_help", "social_isolation", "geographic_access"]),
    ("health_safety", ["cognition", "behavior_risks", "falls", "med_mgmt", "mobility", "supervision", "home_safety"]),
    ("context_prefs", ["chronic"]),
]


@lru_cache(maxsize=1)
def _question_map() -> Dict[str, Dict]:
    grouped: Dict[str, Dict] = {}
    for row in load_questions():
        qid = row["id"]
        entry = grouped.setdefault(
            qid,
            {
                "id": qid,
                "label": row.get("label", "").strip(),
                "type": row.get("type", "single").strip(),
                "choices": [],
                "conditional_show": row.get("conditional_show", "").strip(),
            },
        )
        cid = row.get("choice_id")
        if cid:
            entry["choices"].append(
                {
                    "id": cid,
                    "label": row.get("choice_label", "").strip(),
                }
            )
    return grouped


def questions_for_section(section: str) -> List[Dict]:
    ensure_session()
    mapping = dict(SECTION_ORDER)
    question_ids = mapping.get(section, [])
    qmap = _question_map()
    questions: List[Dict] = []
    for qid in question_ids:
        if qid not in qmap:
            continue
        q = qmap[qid]
        questions.append(
            {
                "id": q["id"],
                "label": q["label"],
                "type": q["type"],
                "choices": list(q["choices"]),
                "conditional_show": q.get("conditional_show", ""),
            }
        )
    return questions


def next_section(current: str) -> str | None:
    for idx, (section, _) in enumerate(SECTION_ORDER):
        if section == current:
            if idx + 1 < len(SECTION_ORDER):
                return SECTION_ORDER[idx + 1][0]
            return None
    return None


def score_answers() -> Dict:
    ensure_session()
    answers = _bundle_get_answers()
    return gcp_scoring.score_answers(answers)


def _label_for(qid: str, token: str | None) -> str | None:
    if not token:
        return None
    question = _question_map().get(qid)
    if not question:
        return token
    for choice in question.get("choices", []):
        if choice.get("id") == token:
            return choice.get("label")
    return token


def build_conversational_summary(answers: Dict, scoring: Dict) -> List[str]:
    bullets: List[str] = []

    support_label = _label_for("caregiver_support", answers.get("caregiver_support")) or "Support not recorded"
    adl_label = _label_for("adl_help", answers.get("adl_help")) or "ADL support not recorded"
    bullets.append(f"Daily support: {support_label}; ADL help {adl_label}.")

    falls_label = _label_for("falls", answers.get("falls")) or "No falls recorded"
    home_label = _label_for("home_safety", answers.get("home_safety")) or "Home safety not reviewed"
    bullets.append(f"Safety snapshot: falls history {falls_label.lower()}, home setup {home_label.lower()}.")

    cognition_label = _label_for("cognition", answers.get("cognition")) or "Cognition not documented"
    behaviors = answers.get("behavior_risks") or []
    if isinstance(behaviors, str):  # defensive
        behaviors = [behaviors]
    behaviors = [b.replace("_", " ").title() for b in behaviors if b and b != "none"]
    if behaviors:
        behavior_text = "; behaviour flags: " + ", ".join(behaviors)
    else:
        behavior_text = ""
    bullets.append(f"Memory & behaviour: {cognition_label}{behavior_text}.")

    supervision_label = _label_for("supervision", answers.get("supervision")) or "Supervision details not noted"
    if scoring["risk_flags"].get("support_gap"):
        supervision_label = f"{supervision_label} (limited coverage)"
    bullets.append(f"Supervision & caregivers: {supervision_label}.")

    if scoring["risk_flags"].get("med_mgmt_complex"):
        med_label = _label_for("med_mgmt", answers.get("med_mgmt")) or "Medication plan not recorded"
        bullets.append(f"Medication management: {med_label.lower()} requires structured oversight.")

    setting_map = {
        "remain_at_home": "Stay at home with periodic check-ins",
        "home_with_support": "Home with additional in-home support",
        "assisted_living": "Transition to assisted living",
        "memory_care": "Transition to memory care",
        "skilled_nursing": "Consider skilled nursing care",
    }
    setting_label = setting_map.get(scoring["recommended_setting"], "Continue monitoring with your advisor")
    bullets.append(f"What this means: {setting_label} — {scoring['rationale'][0]}")

    # Ensure 4-7 bullets
    return bullets[:7]


def snapshot(answers: Dict, scoring: Dict) -> Dict:
    return {
        "version": "gcp.v1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "answers": answers,
        "scoring": scoring,
        "recommendation": {
            "setting": scoring.get("recommended_setting"),
            "acuity": scoring.get("acuity_level"),
        },
    }
