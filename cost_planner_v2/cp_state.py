"""
cp_state.py — shared state + helpers for Cost Planner v2

- Stores everything under st.session_state["cp"] (single namespace).
- Path-based getters/setters: cp_get("income.income_total"), cp_set("benefits.benefits_total", 1200)
- Numeric coercion with currency-safe parsing (_to_num)
- Derived values: monthly_all_in, gap, runway_months
- Lightweight validation flags for Expert Review

This is intentionally dependency-light so pages can import it directly:
    from cost_planner_v2.cp_state import *
"""

from __future__ import annotations
from typing import Any, Dict, Tuple
import math

try:
    import streamlit as st
except Exception:  # allow offline compile/tests
    class _Dummy:
        session_state: Dict[str, Any] = {}
    st = _Dummy()  # type: ignore


# -------------------------------
# Namespace bootstrap & structure
# -------------------------------

def cp_ensure() -> Dict[str, Any]:
    """Ensure and return the cost planner namespace."""
    cp = st.session_state.setdefault("cp", {})
    # minimal shape so pages can read/write safely
    cp.setdefault("qualifiers", {
        "planner_mode": "Plan",
        "has_partner": "none",                # none | unified | split
        "owns_home": False,
        "is_veteran": False,
        "care_setting": "Assisted Living",    # Home | Assisted Living | Memory Care | Skilled
        "partner_maintaining_home": False,
    })
    cp.setdefault("setting_cost", {"monthly_cost": 4200})
    cp.setdefault("income", {"income_total": 0})
    cp.setdefault("expenses", {"other_monthly_total": 0})
    cp.setdefault("caregiver", {"caregiver_cost": 0})
    cp.setdefault("benefits", {"benefits_total": 0})
    cp.setdefault("home", {"reverse_mortgage_monthly": 0, "home_monthly_total": 0, "sale_price": 0})
    cp.setdefault("liquidity", {"liquidity_total": 0, "keeping_car": True})
    cp.setdefault("home_mods", {"mods_monthly_total": 0})
    cp.setdefault("assets", {"assets_total_effective": 0})
    cp.setdefault("derived", {})
    return cp


# -----------------
# Path utils (a.b.c)
# -----------------

def _split(path: str) -> Tuple[str, ...]:
    return tuple([p for p in path.replace("[", ".").replace("]", "").split(".") if p])

def cp_get(path: str, default: Any = None) -> Any:
    """Get a nested value by dotted path, with default."""
    cp = cp_ensure()
    cur: Any = cp
    for part in _split(path):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return default
    return cur

def cp_set(path: str, value: Any) -> None:
    """Set a nested value by dotted path, creating dictionaries as needed."""
    cp = cp_ensure()
    parts = _split(path)
    cur: Any = cp
    for part in parts[:-1]:
        if not isinstance(cur, dict):
            return
        cur = cur.setdefault(part, {})
    if isinstance(cur, dict):
        cur[parts[-1]] = value


# ----------------------
# Numeric coercion (safe)
# ----------------------

def _to_num(x: Any, default: float | int = 0) -> float:
    """Coerce common UI strings to numbers. '$1,200' -> 1200.0"""
    try:
        if x is None:
            return float(default)
        if isinstance(x, (int, float)):
            return float(x)
        if isinstance(x, dict):
            # if a dict slipped through (e.g., accidental sub-obj), try common keys
            for k in ("value", "amount", "total"):
                if k in x:
                    return _to_num(x[k], default)
            return float(default)
        s = str(x).strip()
        if not s:
            return float(default)
        s = s.replace(",", "").replace("$", "")
        return float(s)
    except Exception:
        return float(default)


# -----------------------------
# Convenience setters by module
# -----------------------------

def set_income_total(v: Any) -> None:
    cp_set("income.income_total", _to_num(v, 0))

def set_expenses_total(v: Any) -> None:
    cp_set("expenses.other_monthly_total", _to_num(v, 0))

def set_benefits_total(v: Any) -> None:
    cp_set("benefits.benefits_total", _to_num(v, 0))

def set_caregiver_cost(v: Any) -> None:
    cp_set("caregiver.caregiver_cost", _to_num(v, 0))

def set_mods_monthly_total(v: Any) -> None:
    cp_set("home_mods.mods_monthly_total", _to_num(v, 0))

def set_assets_total_effective(v: Any) -> None:
    cp_set("assets.assets_total_effective", _to_num(v, 0))

def set_liquidity_total(v: Any) -> None:
    cp_set("liquidity.liquidity_total", _to_num(v, 0))

def set_reverse_mortgage_monthly(v: Any) -> None:
    cp_set("home.reverse_mortgage_monthly", _to_num(v, 0))

def set_monthly_care_cost(v: Any) -> None:
    cp_set("setting_cost.monthly_cost", _to_num(v, 0))


# ----------------------------
# Derived math (single source)
# ----------------------------

def derive() -> Dict[str, Any]:
    """
    Compute unified derived values used by Timeline + Expert Review.

    monthly_all_in  = monthly_cost + other_monthly_total + mods_monthly_total + caregiver_cost
    monthly_offsets = income_total + benefits_total + reverse_mortgage_monthly + home_monthly_total
    gap             = monthly_all_in - monthly_offsets
    runway_months   = (assets_total_effective + liquidity_total + sale_price_one_time) / gap  (if gap>0)
    """
    cp = cp_ensure()

    monthly_cost           = _to_num(cp_get("setting_cost.monthly_cost", 0))
    other_monthly_total    = _to_num(cp_get("expenses.other_monthly_total", 0))
    mods_monthly_total     = _to_num(cp_get("home_mods.mods_monthly_total", 0))
    caregiver_cost         = _to_num(cp_get("caregiver.caregiver_cost", 0))

    income_total           = _to_num(cp_get("income.income_total", 0))
    benefits_total         = _to_num(cp_get("benefits.benefits_total", 0))
    rm_monthly             = _to_num(cp_get("home.reverse_mortgage_monthly", 0))
    rent_income_monthly    = _to_num(cp_get("home.home_monthly_total", 0))

    assets_total_effective = _to_num(cp_get("assets.assets_total_effective", 0))
    liquidity_total        = _to_num(cp_get("liquidity.liquidity_total", 0))
    sale_price_one_time    = _to_num(cp_get("home.sale_price", 0))

    monthly_all_in  = monthly_cost + other_monthly_total + mods_monthly_total + caregiver_cost
    monthly_offsets = income_total + benefits_total + rm_monthly + rent_income_monthly
    gap = monthly_all_in - monthly_offsets

    if gap <= 0:
        runway_months = math.inf  # unlimited
    else:
        runway_months = (assets_total_effective + liquidity_total + sale_price_one_time) / gap

    derived = {
        "monthly_all_in": round(monthly_all_in, 2),
        "monthly_offsets": round(monthly_offsets, 2),
        "gap": round(gap, 2),
        "runway_months": float("inf") if math.isinf(runway_months) else round(runway_months, 1),
    }
    cp_set("derived", derived)
    return derived


# ---------------------------------
# Simple validation flags / messages
# ---------------------------------

def expert_review_flags() -> Dict[str, Any]:
    """Return lightweight flags the Expert Review page can surface."""
    owns_home = bool(cp_get("qualifiers.owns_home", False))
    income_total = _to_num(cp_get("income.income_total", 0))
    benefits_total = _to_num(cp_get("benefits.benefits_total", 0))
    medicaid_status = str(cp_get("benefits.medicaid_status", "") or "")
    home_equity = _to_num(cp_get("assets.home_equity", 0))  # optional, not always present
    runway = derive().get("runway_months", 0)

    flags = []
    if income_total <= 0:
        flags.append("No income entered — is that right?")
    if not owns_home and home_equity > 0:
        flags.append("You marked renter but listed home equity — double-check?")
    if benefits_total <= 0 and medicaid_status.lower() in ("", "unsure"):
        flags.append("Consider reviewing Medicaid options.")
    if not math.isinf(runway) and runway < 24:
        flags.append("Tight runway — talk to an advisor?")

    return {
        "flags": flags,
        "runway_months": runway,
        "gap": cp_get("derived.gap", 0),
        "monthly_all_in": cp_get("derived.monthly_all_in", 0),
    }


# -------------
# Page helpers
# -------------

def nav_to(page_path: str) -> None:
    """Safe navigation helper."""
    try:
        import streamlit as st  # re-import in case of offline compile
        st.switch_page(page_path)  # type: ignore[attr-defined]
    except Exception:
        try:
            st.query_params["next"] = page_path
            st.experimental_rerun()
        except Exception:
            pass


# Make sure namespace exists on import
cp_ensure()
