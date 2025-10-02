from copy import deepcopy
import streamlit as st

def apply_audiencing_sanitizer(state: dict) -> dict:
    s = deepcopy(state or {})
    aud = st.session_state.get("audiencing", {}).get("qualifiers", {})

    is_veteran  = bool(aud.get("is_veteran", False))
    has_partner = bool(aud.get("has_partner", False))
    owns_home   = bool(aud.get("owns_home", False))

    if not is_veteran:
        if "benefits" in s:
            s.setdefault("benefits", {})
            s["benefits"]["va_estimate"] = 0
            s["benefits"]["va_eligibility_checks"] = []

    if not has_partner:
        if "household" in s:
            s.setdefault("household", {})
            s["household"]["mode"] = "single"
            s["household"].pop("split", None)
        if "persons" in s and isinstance(s["persons"], dict):
            s["persons"].pop("p2", None)

    if not owns_home:
        if "home_mods" in s and isinstance(s["home_mods"], dict):
            for k in list(s["home_mods"].keys()):
                s["home_mods"][k] = 0
        if "housing_decisions" in s and isinstance(s["housing_decisions"], dict):
            for k in ["sell", "heloc", "reverse_mortgage"]:
                v = s["housing_decisions"].get(k, None)
                if isinstance(v, dict):
                    for subk in list(v.keys()):
                        v[subk] = 0
                    s["housing_decisions"][k] = v
                else:
                    s["housing_decisions"][k] = 0
        if "expenses" in s and isinstance(s["expenses"], dict):
            s["expenses"]["home_utilities"] = 0

    return s
