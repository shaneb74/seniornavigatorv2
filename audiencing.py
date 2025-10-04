"""Audiencing state helpers, sanitizer, and routing utilities."""
from __future__ import annotations


from copy import deepcopy
from typing import Any, Dict

import streamlit as st

# ---------------------------------------------------------------------------
# State schema constants
# ---------------------------------------------------------------------------
AUDIENCING_QUALIFIER_KEYS = [
    "is_veteran",
    "has_partner",
    "owns_home",
    "on_medicaid",
    "urgent",
]

URGENT_FEATURE_FLAG = True


def _default_audiencing_state() -> Dict[str, Any]:
    return {
        "entry": None,
        "qualifiers": {key: False for key in AUDIENCING_QUALIFIER_KEYS},
        "route": {"next": None, "meta": {}},
        "people": {"recipient_name": "", "proxy_name": ""},
        "sanitized": {},
    }


def ensure_audiencing_state() -> Dict[str, Any]:
    """Ensure the session contains a valid audiencing state block."""

    state = st.session_state.get("audiencing")
    if not isinstance(state, dict):
        state = _default_audiencing_state()
        st.session_state["audiencing"] = state
    else:
        # Guarantee contract keys
        state.setdefault("entry", None)
        qualifiers = state.setdefault("qualifiers", {})
        for key in AUDIENCING_QUALIFIER_KEYS:
            qualifiers.setdefault(key, False)
        # Clean up any unexpected qualifier keys to keep schema tight
        for stray_key in list(qualifiers.keys()):
            if stray_key not in AUDIENCING_QUALIFIER_KEYS:
                qualifiers.pop(stray_key)
        route = state.setdefault("route", {})
        route.setdefault("next", None)
        route.setdefault("meta", {})
        state.setdefault("people", {"recipient_name": "", "proxy_name": ""})
        state.setdefault("sanitized", {})
    return state


def apply_audiencing_sanitizer(state: Dict[str, Any]) -> Dict[str, Any]:
    """Apply downstream-safe defaults based on qualifier toggles."""

    ensure_audiencing_state()
    qualifiers = state["qualifiers"]
    sanitized = state.setdefault("sanitized", {})

    # Household partner logic
    sanitized["household_size"] = 2 if qualifiers["has_partner"] else 1
    sanitized["partner_included"] = bool(qualifiers["has_partner"])

    # Veteran logic
    sanitized["va_applicable"] = bool(qualifiers["is_veteran"])
    if not sanitized["va_applicable"]:
        sanitized["va_offsets"] = 0
    else:
        sanitized.pop("va_offsets", None)

    # Home ownership logic
    sanitized["homeowner"] = bool(qualifiers["owns_home"])
    sanitized["home_related_support_enabled"] = bool(qualifiers["owns_home"])
    if not qualifiers["owns_home"]:
        sanitized["home_related_support_enabled"] = False

    # Medicaid context
    sanitized["medicaid_context"] = bool(qualifiers["on_medicaid"])
    sanitized["show_medicaid_banner"] = bool(qualifiers["on_medicaid"])

    # Urgency flag
    sanitized["urgent_case"] = bool(qualifiers.get("urgent", False))

    return state


def compute_audiencing_route(
    state: Dict[str, Any], *, urgent_feature_enabled: bool | None = None
) -> Dict[str, Any]:
    """Determine the next module destination based on qualifiers."""

    ensure_audiencing_state()
    qualifiers = state["qualifiers"]
    if urgent_feature_enabled is None:
        urgent_feature_enabled = URGENT_FEATURE_FLAG

    reasons: list[str] = []
    if urgent_feature_enabled and qualifiers.get("urgent", False):
        next_route = "pfma"
        reasons.append("urgent_case")
    else:
        next_route = "contextual_welcome"
        entry = state.get("entry") or "unknown"
        reasons.append(f"entry_{entry}")

    route = state.setdefault("route", {})
    route["next"] = next_route
    route["meta"] = {
        "reasons": reasons,
        "urgent_feature_enabled": urgent_feature_enabled,
    }
    return route


def snapshot_audiencing(state: Dict[str, Any]) -> Dict[str, Any]:
    """Create a canonical snapshot for downstream consumers."""

    ensure_audiencing_state()
    qualifiers = {
        key: bool(state["qualifiers"].get(key, False))
        for key in AUDIENCING_QUALIFIER_KEYS
    }

    snapshot = {
        "entry": state.get("entry"),
        "qualifiers": qualifiers,
        "route": {
            "next": state.get("route", {}).get("next"),
            "meta": deepcopy(state.get("route", {}).get("meta", {})),
        },
        "people": deepcopy(state.get("people", {})),
        "sanitized": deepcopy(state.get("sanitized", {})),
        "visibility": {
            "partner": bool(qualifiers["has_partner"]),
            "home": bool(qualifiers["owns_home"]),
            "veteran": bool(qualifiers["is_veteran"]),
        },
        "flags": {
            "medicaid": bool(qualifiers["on_medicaid"]),
            "urgent": bool(qualifiers["urgent"]),
        },
    }
    return snapshot


def log_audiencing_set(snapshot: Dict[str, Any]) -> None:
    """Append an audiencing_set event to the shared event log."""

    event_log = st.session_state.setdefault("event_log", [])
    event_log.append({"event": "audiencing_set", "snapshot": deepcopy(snapshot)})


def reset_audiencing_state() -> None:
    """Clear the audiencing block (primarily for debugging/tests)."""

    st.session_state["audiencing"] = _default_audiencing_state()
    st.session_state.pop("audiencing_snapshot", None)
