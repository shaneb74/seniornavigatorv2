from __future__ import annotations

from typing import Any, Dict, List

import streamlit as st

from cost_planner_v2 import _shared as shared
from senior_nav.components import buttons
from ui.theme import inject_theme


st.set_page_config(page_title="Cost Planner · Timeline & Projection", layout="wide")


def _home_mod_adjustments(cp: Dict[str, Any], include: bool) -> List[float]:
    months = [0.0 for _ in range(12)]
    if not include:
        return months
    for mod in cp.get("home_mods", []) or []:
        cost = float(mod.get("cost") or 0.0)
        if cost <= 0:
            continue
        when = (mod.get("when") or "one-time").lower()
        if when in {"one-time", "this year"}:
            months[0] += cost
        elif when == "phase over 2+ years":
            monthly = cost / 12.0
            for idx in range(12):
                months[idx] += monthly
        elif when == "next year":
            # Outside current window
            continue
        else:
            months[0] += cost
    return months


def _projection_rows(
    *,
    cp: Dict[str, Any],
    include_mods: bool,
    include_ltc: bool,
) -> tuple[List[Dict[str, float]], int | None, float]:
    income = float(cp.get("income_total_monthly") or 0.0)
    expenses = float(cp.get("expenses_total_monthly") or 0.0)
    benefits = float(cp.get("benefits_total_monthly") or 0.0)
    relief = float(cp.get("cg_relief_budget_monthly") or 0.0)
    liquidity = float(cp.get("liquidity_total") or 0.0)
    ltc = float(cp.get("ltc_coverage_monthly_equiv") or 0.0) if include_ltc else 0.0

    base_net = income - expenses - relief + benefits + ltc
    mod_adjustments = _home_mod_adjustments(cp, include_mods)

    rows: List[Dict[str, float]] = []
    depletion_month: int | None = None
    liq_remaining = liquidity

    for month_index in range(12):
        mod_cost = mod_adjustments[month_index]
        net = base_net - mod_cost
        liq_remaining += net
        if depletion_month is None and liq_remaining < 0:
            depletion_month = month_index + 1
        rows.append(
            {
                "month_index": month_index + 1,
                "income": income,
                "expenses": expenses,
                "benefits": benefits + ltc,
                "net": net,
                "liq_remaining": liq_remaining,
            }
        )

    return rows, depletion_month, base_net


def _format_net(net: float) -> str:
    sign = "−" if net < 0 else ""
    return f"{sign}${abs(net):,.0f}"


def main() -> None:
    inject_theme()
    cp = shared.cp_state()
    shared.ensure_in_progress("timeline")
    buttons.page_start()

    include_mods = bool(cp.setdefault("timeline_include_mods", True))
    include_ltc = bool(cp.setdefault("timeline_include_ltc_coverage", True))
    show_detail = bool(cp.setdefault("timeline_show_detail", False))

    required_modules = [
        ("income", "Income"),
        ("expenses", "Expenses"),
        ("benefits", "Benefits"),
        ("liquidity", "Liquidity"),
    ]
    missing = [label for key, label in required_modules if shared.status_value(key) != "done"]

    with shared.page_container():
        st.markdown(
            """
            <div style="margin:2rem 0 1.5rem;">
              <h1 style="margin:0 0 .5rem 0;">Timeline & Projection</h1>
              <p style="margin:0;color:var(--ink-muted);">See a simple 12-month view based on your inputs. Adjust the toggles to explore scenarios.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("""<div style='display:flex;justify-content:flex-end;'>""", unsafe_allow_html=True)
        shared.render_reset_link("timeline")
        st.markdown("""</div>""", unsafe_allow_html=True)

        if missing:
            st.warning(
                "Complete the modules to see projections: " + ", ".join(missing),
                icon="ℹ️",
            )
        else:
            income = float(cp.get("income_total_monthly") or 0.0)
            expenses = float(cp.get("expenses_total_monthly") or 0.0)
            benefits = float(cp.get("benefits_total_monthly") or 0.0)
            relief = float(cp.get("cg_relief_budget_monthly") or 0.0)
            liquidity = float(cp.get("liquidity_total") or 0.0)

            st.markdown("""<div style='height:.5rem'></div>""", unsafe_allow_html=True)

            cols = st.columns(2)
            with cols[0]:
                include_mods = st.checkbox(
                    "Include home modification costs",
                    value=include_mods,
                    key="timeline_mods",
                )
                cp["timeline_include_mods"] = include_mods
            with cols[1]:
                include_ltc = st.checkbox(
                    "Include LTC coverage",
                    value=include_ltc,
                    key="timeline_ltc",
                )
                cp["timeline_include_ltc_coverage"] = include_ltc

            rows, depletion_month, base_net = _projection_rows(
                cp=cp,
                include_mods=include_mods,
                include_ltc=include_ltc,
            )
            cp["timeline_projection"] = rows
            cp["timeline_flag_depletion_month"] = depletion_month

            net_summary = _format_net(base_net)
            offsets_value = benefits + (float(cp.get("ltc_coverage_monthly_equiv") or 0.0) if include_ltc else 0.0)

            st.markdown(
                f"""
                <div class='sn-card' style='display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1rem;'>
                  <div><div style='font-size:.75rem;color:var(--ink-muted);text-transform:uppercase;'>Monthly Income</div><div style='font-size:1.2rem;font-weight:600;'>{shared.format_currency(income)}</div></div>
                  <div><div style='font-size:.75rem;color:var(--ink-muted);text-transform:uppercase;'>Monthly Expenses</div><div style='font-size:1.2rem;font-weight:600;'>-{shared.format_currency(expenses)}</div></div>
                  <div><div style='font-size:.75rem;color:var(--ink-muted);text-transform:uppercase;'>Offsets / Benefits</div><div style='font-size:1.2rem;font-weight:600;'>-{shared.format_currency(offsets_value)}</div></div>
                  <div><div style='font-size:.75rem;color:var(--ink-muted);text-transform:uppercase;'>Estimated Net Monthly</div><div style='font-size:1.2rem;font-weight:600;'>{net_summary}</div></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("""<div style='height:1rem'></div>""", unsafe_allow_html=True)

            liq_start = shared.format_currency(liquidity)
            if depletion_month:
                st.info(f"Starting liquidity {liq_start}. Estimated depletion in month {depletion_month}.")
            else:
                st.info(f"Starting liquidity {liq_start}. No depletion within 12 months.")

            show_detail = st.checkbox(
                "Show monthly detail",
                value=show_detail,
                key="timeline_detail",
            )
            cp["timeline_show_detail"] = show_detail

            if show_detail:
                table = {
                    "Month": [row["month_index"] for row in rows],
                    "Net": [row["net"] for row in rows],
                    "Liquidity remaining": [row["liq_remaining"] for row in rows],
                }
                st.dataframe(table, hide_index=True)

            summary = net_summary
            if depletion_month:
                summary += f" · Depletion in {depletion_month} mo"
            else:
                summary += " · 12+ mo runway"
            shared.set_summary("timeline", summary)

            shared.render_nav(
                "pages/cost_planner_v2/cost_planner_assets_v2.py",
                "pages/cost_planner_v2/cost_planner_modules_hub_v2.py",
                next_disabled=False,
                on_continue=lambda: (
                    shared.set_status("timeline", "done"),
                    shared.set_summary("timeline", summary),
                ),
            )

        if missing:
            shared.render_nav(
                "pages/cost_planner_v2/cost_planner_assets_v2.py",
                None,
                next_disabled=True,
            )

    buttons.page_end()


if __name__ == "__main__":
    main()
