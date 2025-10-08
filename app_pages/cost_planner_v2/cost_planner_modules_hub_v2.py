# Cost Planner v2 · Modules Hub
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

import streamlit as st

from cost_planner_v2.cp_nav import goto
from cost_planner_v2.cp_state import ensure_cp
from ui.components import ModuleCard
from ui.state import get_completion, mark_complete, set_completion

try:
    from ui.cost_planner_template import (
        apply_cost_planner_theme,
        cost_planner_page_container,
        render_app_header,
        render_wizard_hero,
        render_wizard_help,
    )
except Exception:
    def apply_cost_planner_theme():
        st.markdown(
            """
            <style>
              :root{--brand:#0B5CD8;--surface:#f6f8fa;--ink:#111418}
              .sn-card{
                background:var(--surface);
                border:1px solid rgba(0,0,0,.08);
                border-radius:14px;
                padding:clamp(1rem,2vw,1.5rem);
              }
            </style>
            """,
            unsafe_allow_html=True,
        )

    from contextlib import contextmanager

    @contextmanager
    def cost_planner_page_container():
        yield

    def render_app_header():
        st.markdown("### Cost Planner")

    def render_wizard_hero(title: str, subtitle: str = ""):
        st.markdown(f"## {title}")
        if subtitle:
            st.caption(subtitle)

    def render_wizard_help(text: str):
        st.info(text)


@dataclass(frozen=True)
class ModuleConfig:
    id: str
    completion_key: str
    icon: str
    title: str
    subtitle: str
    bullets: List[str]
    target: str
    summary_fn: Callable[[Dict], Optional[str]]


def _cp_modules_store() -> Dict[str, Dict]:
    cp_state = ensure_cp()
    modules = cp_state.setdefault("modules", {})
    if not isinstance(modules, dict):
        modules = {}
        cp_state["modules"] = modules
    return modules  # type: ignore[return-value]


def _cp_data() -> Dict:
    data = st.session_state.get("cost_planner")
    return data if isinstance(data, dict) else {}


def _income_summary(data: Dict) -> Optional[str]:
    derived = data.get("derived", {})
    total = derived.get("income_total")
    if isinstance(total, (int, float)) and total >= 0:
        return f"Monthly net income recorded: ${int(total):,}"
    return "Income sources recorded."


def _assets_summary(data: Dict) -> Optional[str]:
    bucket = data.get("assets", {})
    if isinstance(bucket, dict):
        total = bucket.get("assets_total_effective") or bucket.get("assets_total")
        if isinstance(total, (int, float)):
            return f"Assets categorized; estimated total ${int(total):,}"
    return "Asset inventory saved."


def _liquidity_summary(data: Dict) -> Optional[str]:
    bucket = data.get("liquidity", {})
    if isinstance(bucket, dict):
        liq_total = bucket.get("liquidity_total")
        if isinstance(liq_total, (int, float)):
            return f"Liquidity estimates captured. Planned one-time funds: ${int(liq_total):,}"
    return "Liquidity estimates captured."


def _home_mods_summary(data: Dict) -> Optional[str]:
    bucket = data.get("home_mods", {})
    if isinstance(bucket, dict):
        priorities = bucket.get("priorities")
        if isinstance(priorities, (list, tuple)) and priorities:
            top = [str(p) for p in priorities[:2]]
            return "Top priorities: " + " · ".join(top)
    return "Home modification priorities saved."


def _caregiver_summary(data: Dict) -> Optional[str]:
    bucket = data.get("caregiver", {})
    if isinstance(bucket, dict):
        hours = bucket.get("care_hours_week") or bucket.get("cg_hours_per_week")
        risk = bucket.get("burnout_risk") or bucket.get("cg_burnout_risk")
        if hours is not None or risk is not None:
            hours_txt = f"{hours}" if hours is not None else "—"
            risk_txt = str(risk or "—")
            return f"Care hours/week: {hours_txt}; Burnout risk: {risk_txt}"
    return "Caregiver support details recorded."


def _timeline_summary(data: Dict) -> Optional[str]:
    bucket = data.get("timeline", {})
    if isinstance(bucket, dict):
        window = bucket.get("target_window") or bucket.get("tl_horizon_months")
        milestone = bucket.get("decision_date") or bucket.get("tl_expected_events")
        if window or milestone:
            window_txt = f"{window}" if window else "—"
            milestone_txt = str(milestone or "—")
            return f"Target window: {window_txt}; Decision milestone: {milestone_txt}"
    return "Timeline preferences saved."


MODULES: List[ModuleConfig] = [
    ModuleConfig(
        id="income",
        completion_key="cp_income",
        icon="💵",
        title="Income",
        subtitle="Record your monthly income sources.",
        bullets=[
            "Add Social Security, pensions, annuities",
            "Include wages, rental, and other income",
            "See your total net each month",
        ],
        target="app_pages/cost_planner_v2/cost_planner_income_v2.py",
        summary_fn=_income_summary,
    ),
    ModuleConfig(
        id="assets",
        completion_key="cp_assets",
        icon="🧾",
        title="Assets",
        subtitle="Catalog savings, investments, and property.",
        bullets=[
            "Enter cash, CDs, brokerage, retirement",
            "Include real estate and vehicles",
            "Get a clear asset inventory",
        ],
        target="app_pages/cost_planner_v2/cost_planner_assets_v2.py",
        summary_fn=_assets_summary,
    ),
    ModuleConfig(
        id="liquidity",
        completion_key="cp_liquidity",
        icon="💧",
        title="Liquidity",
        subtitle="Estimate funds available soon.",
        bullets=[
            "Identify cash-on-hand and near-cash",
            "Estimate what’s available within 30–90 days",
            "Understand flexibility for near-term costs",
        ],
        target="app_pages/cost_planner_v2/cost_planner_liquidity_v2.py",
        summary_fn=_liquidity_summary,
    ),
    ModuleConfig(
        id="home_mods",
        completion_key="cp_home_mods",
        icon="🏠",
        title="Home Modifications",
        subtitle="Plan safety and accessibility improvements.",
        bullets=[
            "Identify key home safety priorities",
            "Estimate costs and timelines",
            "Target fall-prevention improvements",
        ],
        target="app_pages/cost_planner_v2/cost_planner_home_mods_v2.py",
        summary_fn=_home_mods_summary,
    ),
    ModuleConfig(
        id="caregiver",
        completion_key="cp_caregiver",
        icon="👥",
        title="Caregiver Support",
        subtitle="Track hours, stress, and out-of-pocket costs.",
        bullets=[
            "Log weekly care hours",
            "Assess burnout risk level",
            "Note monthly caregiver expenses",
        ],
        target="app_pages/cost_planner_v2/cost_planner_caregiver_v2.py",
        summary_fn=_caregiver_summary,
    ),
    ModuleConfig(
        id="timeline",
        completion_key="cp_timeline",
        icon="🗓️",
        title="Timeline",
        subtitle="Set your target decision and move window.",
        bullets=[
            "Choose decision/placement milestones",
            "Capture key dates that matter",
            "Align planning with your family’s timing",
        ],
        target="app_pages/cost_planner_v2/cost_planner_timeline_v2.py",
        summary_fn=_timeline_summary,
    ),
]


def _resolve_status(module: ModuleConfig, record: Dict) -> str:
    status = record.get("status")
    if status in {"locked", "in_progress", "complete"}:
        return status
    completion_state = get_completion(module.completion_key)
    if completion_state == "complete":
        return "complete"
    has_progress = bool(record.get("progress")) or record.get("result_summary")
    if has_progress:
        return "in_progress"
    return "in_progress"


def _cta_label(status: str, progress: Optional[float]) -> str:
    if status == "complete":
        return "Review Results"
    if status == "in_progress" and progress and progress > 0:
        return "Resume Module"
    return "Open Module"


def render() -> None:
    apply_cost_planner_theme()
    ensure_cp()

    render_app_header()
    with cost_planner_page_container():
        render_wizard_hero(
            "Plan Modules",
            "Review each module to build your Cost Planner at your own pace.",
        )
        render_wizard_help("Your answers save automatically. Return anytime to continue or refine details.")

        modules_store = _cp_modules_store()
        cp_data = _cp_data()

        completed = 0
        total = len(MODULES)

        cards: List[dict] = []
        for module in MODULES:
            record = modules_store.setdefault(module.id, {})
            status = _resolve_status(module, record)
            if status == "complete":
                completed += 1

            progress = record.get("progress")
            if isinstance(progress, (int, float)):
                progress_value: Optional[float] = max(0.0, min(float(progress), 100.0))
            else:
                progress_value = None

            result_summary = record.get("result_summary")
            if not result_summary and status == "complete":
                result_summary = module.summary_fn(cp_data)

            cards.append(
                {
                    "module": module,
                    "status": status,
                    "progress": progress_value,
                    "result_summary": result_summary,
                    "cta_label": _cta_label(status, progress_value),
                }
            )

        if total:
            st.caption(f"Completed {completed} of {total} modules")

        cols = st.columns(3, gap="large")
        for index, payload in enumerate(cards):
            column = cols[index % len(cols)]
            with column:
                ModuleCard(
                    title=payload["module"].title,
                    subtitle=payload["module"].subtitle,
                    bullets=payload["module"].bullets,
                    icon=payload["module"].icon,
                    cta_label=payload["cta_label"],
                    cta_target=payload["module"].target,
                    status=payload["status"],
                    progress=payload["progress"],
                    result_summary=payload["result_summary"],
                )

        core_ids = [module.id for module in MODULES if module.id != "timeline"]
        if core_ids:
            if completed == total:
                mark_complete("cost_planner")
            elif any(get_completion(f"cp_{mod}") != "not_started" for mod in core_ids):
                set_completion("cost_planner", "in_progress")


render()
