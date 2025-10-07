# Cost Planner · Timeline & Scenarios (v2)
from __future__ import annotations

import streamlit as st
from ui.state import mark_complete, set_completion

from ui.cost_planner_data import MODULE_FIELD_MAP
from ui.cost_planner_forms import render_fields


def render() -> None:
    st.header("Timeline & Scenarios")
    st.caption("Lay out key events over the next 12–24 months that could change costs.")

    fields = MODULE_FIELD_MAP["timeline"]
    valid, _ = render_fields(fields)

    st.markdown("---")
    if st.button("Save & back to Modules", type="primary", disabled=not valid):
        try:
            st.switch_page("app_pages/cost_planner_v2/cost_planner_modules_hub_v2.py")
        except Exception:
            st.session_state["nav_target"] = "app_pages/cost_planner_v2/cost_planner_modules_hub_v2.py"
            st.rerun()


<<<<<<< Updated upstream
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
=======
>>>>>>> Stashed changes
render()
