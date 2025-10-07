# Cost Planner · Your Money Timeline (v2)
from __future__ import annotations
import math
import streamlit as st
from ui.state import mark_complete, set_completion

# ---------------- Theme helpers (match working Income pattern) ----------------
try:
    from ui.cost_planner_template import (
        apply_cost_planner_theme,
        cost_planner_page_container,
        render_app_header,
        render_wizard_hero,
        render_wizard_help,
    )
except Exception:
    # graceful fallbacks (won’t crash if helpers are missing)
    def apply_cost_planner_theme():
        st.markdown("""
        <style>
          :root{--brand:#0B5CD8;--surface:#f6f8fa;--ink:#111418}
          .sn-card{
            background:var(--surface);
            border:1px solid rgba(0,0,0,.08);
            border-radius:14px;
            padding:clamp(1rem,2vw,1.5rem);
          }
        </style>
        """, unsafe_allow_html=True)
    from contextlib import contextmanager
    @contextmanager
    def cost_planner_page_container(): yield
    def render_app_header(): st.markdown("### Cost Planner")
    def render_wizard_hero(title: str, subtitle: str = ""):
        st.markdown(f"## {title}")
        if subtitle: st.caption(subtitle)
    def render_wizard_help(text: str): st.info(text)

# ---------------- Local helpers (functionality preserved) ----------------
def _to_num(x, default=0):
    """Coerce x into a float: handles None, dicts, and '$1,234' strings."""
    try:
        if x is None:
            return float(default)
        if isinstance(x, (int, float)):
            return float(x)
        if isinstance(x, dict):
            for k in ('value', 'amount', 'monthly', 'total'):
                if k in x:
                    return _to_num(x[k], default)
            return float(default)
        if isinstance(x, str):
            t = x.strip().replace(',', '').replace('$', '')
            if t == '':
                return float(default)
            return float(t)
        return float(x)
    except Exception:
        return float(default)

def _cp() -> dict:
    return st.session_state.setdefault("cost_planner", {})

def _get(path: str, default=0):
    """Fetch nested cp keys like 'income.income_total'."""
    d = _cp()
    for part in path.split("."):
        if not isinstance(d, dict):
            return default
        d = d.get(part, {})
    return d if isinstance(d, (int, float)) else (default if d in (None, "", False) else d)

def _fmt_money(v: float | int) -> str:
    try:
        return f"${int(v):,}"
    except Exception:
        return "$0"

def goto(page: str) -> None:
    st.switch_page(f"app_pages/cost_planner_v2/{page}")

# ---------------- Page content (style fixed, functionality unchanged) ----------------
def render() -> None:
    # same bootstrapping as Income (no set_page_config here)
    apply_cost_planner_theme()

    render_app_header()
    with cost_planner_page_container():
        render_wizard_hero("Your Money Timeline", "Here’s how long your money lasts")
        render_wizard_help(
            "We total your monthly costs and compare them to your monthly income & benefits. "
            "Then we estimate how long your assets could cover the gap."
        )

        # --- Pull inputs (robust defaults) ---
        monthly_cost = int(round(_to_num(_get("setting_cost.monthly_cost", 0))))          # from Setting & Cost
        other_monthly_total = int(round(_to_num(_get("expenses.other_monthly_total", 0))))# from Other Monthly Costs
        mods_monthly_total = int(round(_to_num(_get("home_mods.mods_monthly_total", 0)))) # from Home Mods
        income_total = int(round(_to_num(_get("income.income_total", 0))))                # from Income
        benefits_total = int(round(_to_num(_get("benefits.benefits_total", 0))))          # from Benefits
        assets_total_effective = int(round(_to_num(_get("assets.assets_total_effective", 0))))  # from Assets

        # Caregiver Support (include if user added it)
        caregiver_cost = 0
        caregiver_type = _get("caregiver.caregiver_type", "")
        include_caregiver = bool(_get("caregiver.include_caregiver_cost", False))
        if str(caregiver_type).lower() == "hired aide" and include_caregiver:
            caregiver_cost = int(round(_to_num(_get("caregiver.caregiver_cost", 3600))))

        # Liquidity (one-time) for display + fallback assets if assets not entered
        liquidity_total = int(round(_to_num(_get("liquidity.liquidity_total", 0))))
        keeping_car = bool(_get("flags.keeping_car", True))

        # --- Calculations ---
        monthly_all_in = monthly_cost + other_monthly_total + mods_monthly_total + caregiver_cost
        inflows = income_total + benefits_total
        gap = monthly_all_in - inflows

        # Prefer assets_total_effective; fall back to liquidity if assets missing
        effective_assets = assets_total_effective if assets_total_effective > 0 else liquidity_total

        if gap <= 0:
            runway_label = "Unlimited"
            runway_detail = "Monthly income + benefits cover your monthly costs."
        else:
            months = math.floor(effective_assets / gap) if effective_assets > 0 else 0
            runway_label = f"{months} months"
            runway_detail = "Based on current assets divided by your monthly shortfall (gap)."

        # --- Summary cards (use Streamlit containers for consistent styling) ---
        left, right = st.columns([1.05, 0.95], gap="large")

        with left:
            with st.container(border=True):
                st.subheader("Monthly snapshot")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.caption("Total monthly care cost")
                    st.markdown(f"**{_fmt_money(monthly_cost)}**")
                    st.caption("Other monthly expenses")
                    st.markdown(f"**{_fmt_money(other_monthly_total)}**")
                    st.caption("Home mods (monthly)")
                    st.markdown(f"**{_fmt_money(mods_monthly_total)}**")
                    st.caption("Caregiver add-on")
                    st.markdown(f"**{_fmt_money(caregiver_cost)}**")
                with col_b:
                    st.caption("Monthly income")
                    st.markdown(f"**{_fmt_money(income_total)}**")
                    st.caption("Monthly benefits")
                    st.markdown(f"**{_fmt_money(benefits_total)}**")
                    st.caption("All-in monthly")
                    st.markdown(f"**{_fmt_money(monthly_all_in)}**")
                    st.caption("Monthly gap")
                    st.markdown(f"**{_fmt_money(gap)}**")

            with st.container(border=True):
                st.subheader("One-time funds (assets)")
                col_c, col_d = st.columns(2)
                with col_c:
                    st.caption("Assets total")
                    st.markdown(f"**{_fmt_money(assets_total_effective)}**  \n*from Assets*")
                    st.caption("Liquidity (one-time)")
                    st.markdown(f"**{_fmt_money(liquidity_total)}**  \n*Liquidity Nudge*")
                with col_d:
                    st.caption("Assets used in calc")
                    st.markdown(f"**{_fmt_money(effective_assets)}**")
                    st.caption("Car kept?")
                    st.markdown(f"**{'Yes' if keeping_car else 'No'}**")

                if assets_total_effective > 0:
                    st.caption(
                        "Assets entered are used for runway; Liquidity is already included if you added it on the Assets page."
                    )
                elif liquidity_total > 0:
                    st.caption("No Assets entered—using Liquidity Nudge amount for runway.")
                else:
                    st.caption("Add Assets or Liquidity to see your runway.")

        with right:
            with st.container(border=True):
                st.subheader("Runway estimate")
                st.markdown(f"**{runway_label}**")
                st.caption(runway_detail)
                if gap > 0 and (effective_assets <= 0 or (effective_assets / gap) < 24):
                    st.warning("Tight runway — consider talking to an advisor.")

        # --- Actions (same functionality) ---
        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button("← Back to Modules", key="tm_back", width="stretch"):
                set_completion("cp_timeline", "in_progress")
                goto("cost_planner_modules_hub_v2.py")
        with c2:
            if st.button("Continue → Expert Review", key="tm_next", width="stretch"):
                mark_complete("cp_timeline")
                st.switch_page("app_pages/expert_review.py")

# ✅ Import-time execution under Streamlit
render()
