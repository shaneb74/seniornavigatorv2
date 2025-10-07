from __future__ import annotations

"""Streamlit mock-ups for every Cost Planner page.

The product team requested a consistent set of wireframes that demonstrate how the
TurboTax-inspired visual language applies to each `cost_plan*` and
`cost_planner*` page. This module focuses on layout, tone, and interaction affordances
without introducing business logic or page routing side-effects.
"""

from dataclasses import dataclass
from typing import Callable, Dict, List

import streamlit as st

from cost_planner_shared import format_currency


def apply_global_styles() -> None:
    """Inject shared CSS for the Cost Planner mock-ups."""

    st.markdown(
        """
<style>
/* Header and Navigation */
.stAppHeader { background-color: #f0f8ff; padding: 1rem; border-bottom: 1px solid #d3d3d3; }
.stAppHeader h1 { color: #1e90ff; font-size: 24px; margin: 0; }
.nav-bar { display: flex; justify-content: space-between; align-items: center; gap: 1rem; }
.nav-item { color: #4682b4; margin-right: 1rem; text-decoration: none; font-weight: 500; }
.login-btn { background-color: #1e90ff; color: white; padding: 0.5rem 1rem; border-radius: 20px; border: none; font-weight: 600; }

/* Qualifiers Header */
.qual-header { display: flex; align-items: center; padding: 1rem; border-bottom: 1px solid #d3d3d3; gap: 0.75rem; }
.back-btn { color: #1e90ff; font-size: 18px; cursor: pointer; }
.assess-label { color: #808080; font-size: 14px; }
.name-btn { background-color: #f0f8ff; color: #1e90ff; border-radius: 20px; padding: 0.2rem 0.8rem; border: 0; font-weight: 600; }
.question-mode { color: #1e90ff; font-size: 14px; margin-left: auto; }

/* Wizard Styling */
.wizard-hero { background: #f0f8ff; padding: 2rem; text-align: center; border-radius: 20px; margin-bottom: 2rem; }
.wizard-title { font-size: 32px; color: #1e90ff; margin-bottom: 0.5rem; }
.wizard-caption { font-size: 17px; color: #808080; max-width: 720px; margin: 0 auto; }
.wizard-help { background-color: #f0f8ff; color: #606060; padding: 0.75rem 1rem; border-radius: 12px; margin-top: 1.25rem; border: 1px solid #d3d3d3; }
.wizard-button { padding: 0.5rem 1.25rem; border-radius: 20px; font-weight: 600; display: inline-flex; align-items: center; justify-content: center; border: none; cursor: pointer; }
.wizard-button-primary { background-color: #1e90ff; color: white; }
.wizard-button-secondary { background-color: #f0f8ff; color: #1e90ff; border: 1px solid #d3d3d3; }
.wizard-suggestion { padding: 1rem; border-radius: 12px; margin-bottom: 1rem; font-size: 15px; }
.wizard-suggestion-info { background-color: #e6f0fa; color: #1e90ff; }
.wizard-suggestion-warn { background-color: #fff3cd; color: #856404; }
.wizard-suggestion-critical { background-color: #f8d7da; color: #721c24; }

/* Module dashboard cards */
.module-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem; margin: 1.5rem 0; }
.module-card { background: #ffffff; border-radius: 18px; padding: 1.25rem; border: 1px solid #d3d3d3; box-shadow: 0 12px 30px rgba(30, 144, 255, 0.08); display: flex; flex-direction: column; gap: 0.5rem; }
.module-card h4 { margin: 0; font-size: 18px; color: #1e90ff; }
.module-card p { margin: 0; color: #606060; font-size: 14px; }
.module-card .card-status { display: inline-flex; align-items: center; gap: 0.35rem; background: #f0f8ff; color: #1e90ff; padding: 0.15rem 0.75rem; border-radius: 999px; font-size: 13px; font-weight: 600; }
.module-card .card-status.positive { background: #e6f7eb; color: #2e8b57; }
.module-card .card-status.warning { background: #fff3cd; color: #856404; }
.module-card .card-actions { margin-top: auto; display: flex; gap: 0.5rem; }
.module-card .card-actions a { text-decoration: none; }
.module-card .card-actions .wizard-button { width: 100%; }

/* Tables */
.summary-table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
.summary-table th { text-align: left; font-size: 14px; color: #606060; border-bottom: 1px solid #d3d3d3; padding-bottom: 0.5rem; }
.summary-table td { padding: 0.65rem 0; border-bottom: 1px solid #ededed; font-size: 15px; }
.summary-table td.amount { text-align: right; font-weight: 600; color: #1e90ff; }

/* Utility */
.sn-scope.dashboard.cost-planner-wireframe { padding-bottom: 2rem; }
</style>
""",
        unsafe_allow_html=True,
    )


def start_container() -> None:
    st.markdown('<div class="sn-scope dashboard cost-planner-wireframe">', unsafe_allow_html=True)


def end_container() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def render_app_header() -> None:
    st.markdown(
        """
<div class="stAppHeader">
  <div class="nav-bar">
    <h1>Concierge Care Senior Navigator</h1>
    <div>
      <a class="nav-item" href="#">Dashboard</a>
      <a class="nav-item" href="#">Learning Center</a>
      <a class="nav-item" href="#">Get Connected</a>
      <button class="login-btn">Log in or sign up</button>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_assessment_header(section_label: str, *, persona: str = "John", mode: str = "All questions") -> None:
    st.markdown(
        f"""
<div class="qual-header">
  <span class="back-btn">← Back</span>
  <span class="assess-label">{section_label}</span>
  <button class="name-btn">{persona}</button>
  <span class="question-mode">{mode}</span>
</div>
""",
        unsafe_allow_html=True,
    )


def render_wizard_hero(title: str, caption: str) -> None:
    st.markdown("<div class='wizard-hero'>", unsafe_allow_html=True)
    st.markdown(f"<h1 class='wizard-title'>{title}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='wizard-caption'>{caption}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def render_wizard_help(text: str) -> None:
    st.markdown(f"<div class='wizard-help'>{text}</div>", unsafe_allow_html=True)


def render_metrics(metrics: List[Dict[str, str]]) -> None:
    if not metrics:
        return

    cols = st.columns(len(metrics))
    for col, metric in zip(cols, metrics):
        with col:
            st.metric(metric.get("label", ""), metric.get("value", ""), metric.get("delta"))


def render_nav_buttons(buttons: List[Dict[str, str]]) -> None:
    if not buttons:
        return

    cols = st.columns(len(buttons))
    for col, button in zip(cols, buttons):
        with col:
            st.button(
                button.get("label", ""),
                type=button.get("type", "secondary"),
                key=f"nav_{button.get('key', button.get('label', 'btn')).replace(' ', '_').lower()}",
            )


def render_module_cards(cards: List[Dict[str, str]]) -> None:
    if not cards:
        return

    card_html = "<div class='module-grid'>"
    for card in cards:
        status_class = card.get("status_class", "")
        card_html += (
            f"<div class='module-card'>"
            f"  <span class='card-status {status_class}'>{card.get('status', '')}</span>"
            f"  <h4>{card.get('title', '')}</h4>"
            f"  <p>{card.get('body', '')}</p>"
            f"  <div class='card-actions'>"
            f"    <a class='wizard-button wizard-button-primary' href='#'>{card.get('primary_label', 'Open')}</a>"
            f"  </div>"
            f"</div>"
        )
    card_html += "</div>"
    st.markdown(card_html, unsafe_allow_html=True)


def render_fields(page_key: str, fields: List[Dict[str, object]]) -> None:
    for field in fields:
        columns = field.get("columns")
        if columns:
            cols = st.columns(columns)
            for container, item in zip(cols, field.get("items", [])):
                with container:
                    render_field(page_key, item)
        else:
            render_field(page_key, field)


def render_field(page_key: str, field: Dict[str, object]) -> None:
    field_type = field.get("type", "number")
    label = field.get("label", "")
    key = f"{page_key}_{field.get('key', label).replace(' ', '_').lower()}"
    help_text = field.get("help")
    label_visibility = field.get("label_visibility")

    if field_type == "number":
        st.number_input(
            label,
            min_value=field.get("min", 0.0),
            step=field.get("step", 1.0),
            value=field.get("value", 0.0),
            key=key,
            help=help_text,
        )
    elif field_type == "select":
        st.selectbox(
            label,
            field.get("options", []),
            index=field.get("index", 0),
            key=key,
            help=help_text,
        )
    elif field_type == "checkbox":
        st.checkbox(label, value=field.get("value", False), key=key, help=help_text)
    elif field_type == "text":
        st.text_input(label, value=field.get("value", ""), key=key, help=help_text)
    elif field_type == "textarea":
        st.text_area(
            label,
            value=field.get("value", ""),
            key=key,
            help=help_text,
            height=field.get("height", 120),
        )
    elif field_type == "radio":
        st.radio(
            label,
            field.get("options", []),
            index=field.get("index", 0),
            horizontal=field.get("horizontal", False),
            key=key,
            help=help_text,
            label_visibility=label_visibility,
        )
    elif field_type == "slider":
        st.slider(
            label,
            min_value=field.get("min", 0),
            max_value=field.get("max", 100),
            value=field.get("value", 0),
            step=field.get("step", 1),
            key=key,
            help=help_text,
        )


def render_module_page(
    page_key: str,
    *,
    section_label: str = "Guided Cost Plan",
    persona: str = "John",
    mode: str = "Single question",
    title: str,
    caption: str,
    fields: List[Dict[str, object]],
    metrics: List[Dict[str, str]],
    nav_buttons: List[Dict[str, str]],
    helper_text: str,
    callouts: List[Dict[str, str]] | None = None,
) -> None:
    start_container()
    render_assessment_header(section_label, persona=persona, mode=mode)
    st.subheader(title)
    st.caption(caption)

    for callout in callouts or []:
        st.markdown(
            f"<div class='wizard-suggestion wizard-suggestion-{callout.get('tone', 'info')}'>"
            f"{callout.get('text', '')}</div>",
            unsafe_allow_html=True,
        )

    render_fields(page_key, fields)
    render_metrics(metrics)
    render_wizard_help(helper_text)
    render_nav_buttons(nav_buttons)
    end_container()


def render_cost_planner_mode_selector() -> None:
    start_container()
    render_app_header()
    render_wizard_hero("Cost Planner", "Choose how you'd like to plan care costs.")

    col1, col2 = st.columns(2)
    with col1:
        st.button(
            "Explore Costs",
            key="wireframe_explore_mode",
            type="primary",
            width="stretch",
        )
        st.caption("Quick estimate, no login needed.")
    with col2:
        st.button(
            "Plan Costs",
            key="wireframe_plan_mode",
            type="primary",
            width="stretch",
        )
        st.caption("Detailed plan, requires login.")

    st.markdown("---")
    st.caption("© 2025 Concierge Care Senior Navigator™")
    end_container()


def render_cost_planner_qualifiers() -> None:
    start_container()
    render_assessment_header("Assessment: For someone")
    st.subheader("Guided Cost Plan")
    st.markdown(
        "<h3>How would you describe your financial situation when it comes to paying for care? <span style='color: #1e90ff;'>ⓘ</span></h3>",
        unsafe_allow_html=True,
    )
    st.radio(
        "",
        [
            "I don't worry about money",
            "I'm financially comfortable",
            "Cost is a major factor",
            "I may need financial help",
        ],
        horizontal=True,
        label_visibility="collapsed",
        key="qual_financial_situation",
    )

    st.markdown(
        "<h3>Contribution style <span style='color: #1e90ff;'>ⓘ</span></h3>",
        unsafe_allow_html=True,
    )
    contribution = st.radio(
        "",
        ["Unified contribution", "Individual contributions"],
        horizontal=True,
        label_visibility="collapsed",
        key="qual_contribution",
    )
    if contribution == "Individual contributions":
        st.text_input("Add contributor (e.g., Sibling 1)", key="qual_contributor_entry")

    st.markdown(
        "<h3>Do you own your home? <span style='color: #1e90ff;'>ⓘ</span></h3>",
        unsafe_allow_html=True,
    )
    st.radio(
        "",
        ["Yes", "No"],
        horizontal=True,
        label_visibility="collapsed",
        key="qual_owns_home",
    )

    st.markdown(
        "<h3>Are you a veteran? <span style='color: #1e90ff;'>ⓘ</span></h3>",
        unsafe_allow_html=True,
    )
    st.radio(
        "",
        ["Yes", "No"],
        horizontal=True,
        label_visibility="collapsed",
        key="qual_is_veteran",
    )

    render_nav_buttons(
        [
            {"label": "Continue", "type": "primary", "key": "qual_continue"},
            {"label": "Skip", "type": "secondary", "key": "qual_skip"},
        ]
    )
    render_wizard_help("Respond as the person receiving care even if you're filling this out for someone else.")
    end_container()


def render_cost_planner_estimate() -> None:
    start_container()
    render_assessment_header("Guided Cost Plan", mode="All questions")
    st.subheader("Tell us about your situation")
    st.caption("A few quick selections keep your estimate on track.")

    render_fields(
        "estimate",
        [
            {
                "type": "radio",
                "label": "Planning mode",
                "options": ["Estimate costs", "Plan in detail"],
                "horizontal": True,
                "key": "planning_mode",
            },
            {
                "type": "radio",
                "label": "Household structure",
                "options": ["Just me", "Me + partner", "Multi-person"],
                "horizontal": True,
                "key": "household",
            },
            {
                "columns": 2,
                "items": [
                    {
                        "type": "slider",
                        "label": "How soon do you need care?",
                        "min": 0,
                        "max": 12,
                        "value": 3,
                        "step": 1,
                        "help": "0 = now, 12 = a year out",
                        "key": "timeline",
                    },
                    {
                        "type": "number",
                        "label": "Monthly budget target",
                        "value": 4000.0,
                        "step": 100.0,
                        "help": "Helps us frame recommendations and offsets.",
                        "key": "budget",
                    },
                ],
            },
            {
                "type": "checkbox",
                "label": "I'd like to explore financial assistance options",
                "value": True,
                "key": "assistance_interest",
            },
        ],
    )

    render_metrics(
        [
            {"label": "Monthly snapshot", "value": format_currency(4850)},
            {"label": "Potential offsets", "value": format_currency(1650)},
            {"label": "Net out-of-pocket", "value": format_currency(3200)},
        ]
    )

    render_wizard_help("These inputs preview your estimate. You can revisit any time from the module list.")
    render_nav_buttons(
        [
            {"label": "Back", "type": "secondary", "key": "estimate_back"},
            {"label": "Continue to modules", "type": "primary", "key": "estimate_continue"},
        ]
    )
    end_container()


def render_cost_planner_modules() -> None:
    start_container()
    render_assessment_header("Guided Cost Plan", mode="Module view")
    st.subheader("Pick where to focus next")
    st.caption("Work through modules in any order. Navi highlights what's most urgent.")

    render_module_cards(
        [
            {
                "title": "Housing",
                "body": "Base rent, utilities, maintenance, and community fees.",
                "status": "In progress • 2 of 3 complete",
                "status_class": "warning",
                "primary_label": "Open housing",
            },
            {
                "title": "In-home care",
                "body": "Staffing plans, supplemental services, and second-person support.",
                "status": "Not started",
                "status_class": "",
                "primary_label": "Start module",
            },
            {
                "title": "Medical & daily aids",
                "body": "Prescriptions, supplies, transportation, and monitoring.",
                "status": "Ready for review",
                "status_class": "positive",
                "primary_label": "Review items",
            },
            {
                "title": "Benefits & income",
                "body": "Insurance premiums, Social Security, pensions, and VA benefits.",
                "status": "Needs info",
                "status_class": "warning",
                "primary_label": "Add offsets",
            },
            {
                "title": "Upgrades & safety",
                "body": "Home modifications and fall-prevention investments.",
                "status": "Optional",
                "status_class": "",
                "primary_label": "Explore options",
            },
            {
                "title": "Notes & extras",
                "body": "Custom line items, debts, and planner notes for your family.",
                "status": "Draft saved",
                "status_class": "positive",
                "primary_label": "Edit notes",
            },
        ]
    )

    render_metrics(
        [
            {"label": "Modules complete", "value": "4 / 7"},
            {"label": "Monthly snapshot", "value": format_currency(6120)},
            {"label": "Net out-of-pocket", "value": format_currency(3475)},
        ]
    )

    render_wizard_help("Navi suggests completing Housing next so your monthly baseline is accurate before offsets.")
    render_nav_buttons(
        [
            {"label": "Return to estimate", "type": "secondary", "key": "modules_back"},
            {"label": "View skipped items", "type": "secondary", "key": "modules_skipped"},
            {"label": "Go to summary", "type": "primary", "key": "modules_summary"},
        ]
    )
    end_container()


def render_cost_planner_housing() -> None:
    render_module_page(
        "housing",
        title="Housing & living costs",
        caption="Capture recurring housing payments before care or benefits.",
        fields=[
            {
                "type": "number",
                "label": "Monthly housing cost (rent, mortgage, or community fee)",
                "value": 2850.0,
                "step": 50.0,
                "help": "Include base rent, mortgage, or community fees.",
                "key": "base",
            },
            {
                "columns": 2,
                "items": [
                    {
                        "type": "number",
                        "label": "Utilities & services",
                        "value": 210.0,
                        "step": 25.0,
                        "key": "utilities",
                    },
                    {
                        "type": "number",
                        "label": "Maintenance or HOA",
                        "value": 140.0,
                        "step": 25.0,
                        "key": "maintenance",
                    },
                ],
            },
        ],
        metrics=[
            {"label": "Housing subtotal", "value": format_currency(3200)},
        ],
        nav_buttons=[
            {"label": "Skip", "type": "secondary", "key": "housing_skip"},
            {"label": "Save & continue", "type": "primary", "key": "housing_continue"},
        ],
        helper_text="Include rent, mortgage, or assisted living base fees. We hide maintenance if the household rents.",
        callouts=[
            {
                "tone": "info",
                "text": "Navi tip: Owners can explore reverse mortgage counseling in the benefits module.",
            }
        ],
    )


def render_cost_planner_home_care() -> None:
    render_module_page(
        "home_care",
        title="In-home care",
        caption="Capture staffing, add-ons, and second-person coverage.",
        fields=[
            {
                "columns": 2,
                "items": [
                    {
                        "type": "number",
                        "label": "Weekly caregiver hours",
                        "value": 38.0,
                        "step": 1.0,
                        "help": "Total paid hours per week across all caregivers.",
                        "key": "hours",
                    },
                    {
                        "type": "number",
                        "label": "Base hourly rate",
                        "value": 28.0,
                        "step": 1.0,
                        "help": "Hourly cost from your agency or private caregiver.",
                        "key": "rate",
                    },
                ],
            },
            {
                "columns": 2,
                "items": [
                    {
                        "type": "number",
                        "label": "Weekend / night add-ons",
                        "value": 260.0,
                        "step": 25.0,
                        "key": "addons",
                    },
                    {
                        "type": "number",
                        "label": "Second-person support",
                        "value": 340.0,
                        "step": 25.0,
                        "key": "second_person",
                    },
                ],
            },
            {
                "type": "checkbox",
                "label": "Include respite coverage",
                "value": True,
                "key": "respite",
            },
        ],
        metrics=[
            {"label": "Care subtotal", "value": format_currency(4520)},
            {"label": "Hours/week", "value": "38"},
        ],
        nav_buttons=[
            {"label": "Skip", "type": "secondary", "key": "home_care_skip"},
            {"label": "Save & continue", "type": "primary", "key": "home_care_continue"},
        ],
        helper_text="Include agency fees, respite coverage, and any second-person surcharges when applicable.",
        callouts=[
            {
                "tone": "warn",
                "text": "Navi: You're planning more than 40 hours/week. Consider rotating caregivers to avoid overtime rates.",
            }
        ],
    )


def render_cost_planner_daily_aids() -> None:
    render_module_page(
        "daily_aids",
        title="Medical & daily living aids",
        caption="Log recurring medical supplies, prescriptions, and transportation needs.",
        fields=[
            {
                "columns": 2,
                "items": [
                    {
                        "type": "number",
                        "label": "Prescription medications",
                        "value": 185.0,
                        "step": 10.0,
                        "key": "rx",
                    },
                    {
                        "type": "number",
                        "label": "Medical supplies",
                        "value": 95.0,
                        "step": 5.0,
                        "key": "supplies",
                    },
                ],
            },
            {
                "columns": 2,
                "items": [
                    {
                        "type": "number",
                        "label": "Transportation & delivery",
                        "value": 120.0,
                        "step": 10.0,
                        "key": "transport",
                    },
                    {
                        "type": "checkbox",
                        "label": "Chronic condition support needed",
                        "value": True,
                        "key": "chronic",
                    },
                ],
            },
        ],
        metrics=[
            {"label": "Medical subtotal", "value": format_currency(400)},
        ],
        nav_buttons=[
            {"label": "Skip", "type": "secondary", "key": "daily_aids_skip"},
            {"label": "Save & continue", "type": "primary", "key": "daily_aids_continue"},
        ],
        helper_text="Capture prescriptions, medical supplies, and mobility or delivery costs for a full medical picture.",
        callouts=[
            {
                "tone": "info",
                "text": "Navi: Medicare Part D might offset prescriptions over $150/month. Add potential savings in benefits.",
            }
        ],
    )


def render_cost_planner_benefits() -> None:
    render_module_page(
        "benefits",
        section_label="Offsets & benefits",
        mode="All sources",
        title="Benefits & income",
        caption="Log insurance premiums, regular income, and financial assistance.",
        fields=[
            {
                "columns": 2,
                "items": [
                    {
                        "type": "number",
                        "label": "Monthly health premiums",
                        "value": 410.0,
                        "step": 25.0,
                        "key": "health_premium",
                    },
                    {
                        "type": "number",
                        "label": "Long-term care insurance",
                        "value": 0.0,
                        "step": 25.0,
                        "key": "ltc_premium",
                    },
                ],
            },
            {
                "columns": 2,
                "items": [
                    {
                        "type": "number",
                        "label": "Social Security income",
                        "value": 2150.0,
                        "step": 50.0,
                        "key": "ss_income",
                    },
                    {
                        "type": "number",
                        "label": "Pension or annuity",
                        "value": 650.0,
                        "step": 50.0,
                        "key": "pension_income",
                    },
                ],
            },
            {
                "columns": 2,
                "items": [
                    {
                        "type": "number",
                        "label": "VA or other benefits",
                        "value": 450.0,
                        "step": 25.0,
                        "key": "va_benefits",
                    },
                    {
                        "type": "checkbox",
                        "label": "Medicaid application in progress",
                        "value": False,
                        "key": "medicaid_progress",
                    },
                ],
            },
        ],
        metrics=[
            {"label": "Offsets subtotal", "value": format_currency(3250)},
            {"label": "Insurance spend", "value": format_currency(410)},
        ],
        nav_buttons=[
            {"label": "Skip", "type": "secondary", "key": "benefits_skip"},
            {"label": "Save & continue", "type": "primary", "key": "benefits_continue"},
        ],
        helper_text="Track every offset and premium so Navi can surface your true out-of-pocket costs.",
        callouts=[
            {
                "tone": "info",
                "text": "Navi: Upload pension statements in Documents to keep this figure current.",
            }
        ],
    )


def render_cost_planner_freeform() -> None:
    render_module_page(
        "freeform",
        title="Notes & extras",
        caption="Add custom line items, debts, or notes for your family.",
        fields=[
            {
                "type": "text",
                "label": "Custom expense name",
                "value": "Meal delivery",
                "key": "custom_name",
            },
            {
                "type": "number",
                "label": "Monthly amount",
                "value": 180.0,
                "step": 10.0,
                "key": "custom_amount",
            },
            {
                "type": "textarea",
                "label": "Notes for loved ones",
                "value": "Remember to ask the care manager about sliding-scale transportation passes.",
                "key": "notes",
            },
        ],
        metrics=[
            {"label": "Other subtotal", "value": format_currency(180)},
        ],
        nav_buttons=[
            {"label": "Skip", "type": "secondary", "key": "freeform_skip"},
            {"label": "Save & continue", "type": "primary", "key": "freeform_continue"},
        ],
        helper_text="Use this space for one-off costs or context your family should remember during decision-making.",
        callouts=[
            {
                "tone": "info",
                "text": "Navi: Add debt repayments if they impact monthly cash flow.",
            }
        ],
    )


def render_cost_planner_mods() -> None:
    render_module_page(
        "mods",
        section_label="Upgrades & safety",
        mode="Project review",
        title="Home modifications",
        caption="Plan accessibility upgrades or fall-prevention improvements.",
        fields=[
            {
                "type": "select",
                "label": "Project focus",
                "options": [
                    "Bathroom safety",
                    "Ramps & entry",
                    "Lighting",
                    "Smart monitoring",
                ],
                "index": 0,
                "key": "project_focus",
            },
            {
                "columns": 2,
                "items": [
                    {
                        "type": "number",
                        "label": "Estimated one-time cost",
                        "value": 4200.0,
                        "step": 100.0,
                        "key": "project_cost",
                    },
                    {
                        "type": "select",
                        "label": "Urgency",
                        "options": ["Nice to have", "Recommended", "High priority"],
                        "index": 2,
                        "key": "project_urgency",
                    },
                ],
            },
            {
                "type": "textarea",
                "label": "Vendors or resources",
                "value": "Local contractor quoted $4,200. VA grant eligibility TBD.",
                "key": "project_vendors",
            },
        ],
        metrics=[
            {"label": "One-time upgrades", "value": format_currency(4200)},
        ],
        nav_buttons=[
            {"label": "Skip", "type": "secondary", "key": "mods_skip"},
            {"label": "Save & continue", "type": "primary", "key": "mods_continue"},
        ],
        helper_text="Track safety upgrades even if they're one-time purchases so loved ones know what's planned.",
        callouts=[
            {
                "tone": "info",
                "text": "Navi: Some VA programs reimburse bathroom safety upgrades. Flag in benefits if eligible.",
            }
        ],
    )


def render_cost_planner_estimate_summary() -> None:
    start_container()
    render_assessment_header("Guided Cost Plan", mode="Summary view")
    st.subheader("Estimate summary")
    st.caption("Review your monthly totals before confirming the plan.")

    render_metrics(
        [
            {"label": "Monthly costs", "value": format_currency(7320)},
            {"label": "Offsets", "value": format_currency(3250)},
            {"label": "Net out-of-pocket", "value": format_currency(4070)},
            {"label": "Runway (months)", "value": "11"},
        ]
    )

    st.markdown(
        """
<table class="summary-table">
  <thead>
    <tr><th>Category</th><th class="amount">Monthly</th></tr>
  </thead>
  <tbody>
    <tr><td>Housing & living</td><td class="amount">$3,200</td></tr>
    <tr><td>In-home care</td><td class="amount">$4,520</td></tr>
    <tr><td>Medical & daily aids</td><td class="amount">$400</td></tr>
    <tr><td>Other items</td><td class="amount">$180</td></tr>
    <tr><td>Offsets & benefits</td><td class="amount">−$3,250</td></tr>
  </tbody>
</table>
""",
        unsafe_allow_html=True,
    )

    render_wizard_help("Export your estimate as PDF/CSV or continue to confirmation to lock the plan for sharing.")
    render_nav_buttons(
        [
            {"label": "Back to modules", "type": "secondary", "key": "summary_back"},
            {"label": "Download", "type": "secondary", "key": "summary_download"},
            {"label": "Continue", "type": "primary", "key": "summary_continue"},
        ]
    )
    end_container()


def render_cost_plan_confirm() -> None:
    start_container()
    render_assessment_header("Cost plan confirmation", mode="Final review")
    st.subheader("Lock in your plan")
    st.caption("Share the plan, export for professionals, or update the PFMA workflow.")

    render_metrics(
        [
            {"label": "Monthly costs", "value": format_currency(7320)},
            {"label": "Offsets", "value": format_currency(3250)},
            {"label": "Net out-of-pocket", "value": format_currency(4070)},
        ]
    )

    st.checkbox("Share with family hub", value=True, key="confirm_share_family")
    st.checkbox("Send to professional navigator", value=False, key="confirm_share_pro")
    st.checkbox("Trigger PFMA follow-up", value=True, key="confirm_pfma")

    st.text_area(
        "Next steps for the team",
        value="Schedule a benefits review and confirm agency weekend rates.",
        key="confirm_next_steps",
    )

    render_wizard_help("Completing confirmation stores a snapshot for CRM export and kicks off navigator tasks.")
    render_nav_buttons(
        [
            {"label": "Back", "type": "secondary", "key": "confirm_back"},
            {"label": "Share plan", "type": "primary", "key": "confirm_share"},
            {"label": "Finish", "type": "primary", "key": "confirm_finish"},
        ]
    )
    end_container()


def render_cost_planner_skipped() -> None:
    start_container()
    render_assessment_header("Guided Cost Plan", mode="Follow-ups")
    st.subheader("Modules to revisit")
    st.caption("These steps were skipped or only partially completed.")

    skipped_items = [
        "Benefits & income - Add pension statement",
        "Home modifications - Confirm vendor quotes",
        "Notes & extras - Capture sibling commitments",
    ]
    for item in skipped_items:
        st.markdown(f"<div class='wizard-suggestion wizard-suggestion-warn'>{item}</div>", unsafe_allow_html=True)

    render_wizard_help("Finish these modules to unlock expert review and export options.")
    render_nav_buttons(
        [
            {"label": "Return to modules", "type": "secondary", "key": "skipped_back"},
            {"label": "Clear skips", "type": "primary", "key": "skipped_clear"},
        ]
    )
    end_container()


def render_cost_planner_evaluation() -> None:
    start_container()
    render_assessment_header("Expert review", mode="All flags")
    st.subheader("Expert review")
    st.caption("Navi checked your plan and found a few things to confirm.")

    st.markdown(
        "<div class='wizard-suggestion wizard-suggestion-info'>Hey, I'm Navi. Your plan is coming together-here are a few items to double-check.</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='wizard-suggestion wizard-suggestion-warn'>Rx cost looks high for similar households. Could Medicare Part D bring it down?</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='wizard-suggestion wizard-suggestion-critical'>Runway under 12 months. Explore VA Aid & Attendance in benefits.</div>",
        unsafe_allow_html=True,
    )

    render_metrics(
        [
            {"label": "Monthly costs", "value": format_currency(7320)},
            {"label": "Offsets", "value": format_currency(3250)},
            {"label": "Net out-of-pocket", "value": format_currency(4070)},
        ]
    )

    with st.expander("Decision log"):
        st.write(
            "- Recommendation: Assisted living with memory care support\n"
            "- Medicaid short-circuit triggered\n"
            "- Added custom transportation line item"
        )

    render_wizard_help("Resolve critical flags before sharing the plan with family or professionals.")
    render_nav_buttons(
        [
            {"label": "Back to modules", "type": "secondary", "key": "evaluation_back"},
            {"label": "Resolve flags", "type": "primary", "key": "evaluation_resolve"},
            {"label": "Complete review", "type": "primary", "key": "evaluation_complete"},
        ]
    )
    end_container()


apply_global_styles()


@dataclass
class WireframePage:
    key: str
    label: str
    description: str
    render: Callable[[], None]


WIREFRAME_PAGES: List[WireframePage] = [
    WireframePage(
        key="cost_planner",
        label="Cost Planner (mode selector)",
        description="Hero screen that offers Explore vs Plan modes.",
        render=render_cost_planner_mode_selector,
    ),
    WireframePage(
        key="cost_planner_qualifiers",
        label="Cost Planner Qualifiers",
        description="Optional pre-intake step for financial qualifiers and contributors.",
        render=render_cost_planner_qualifiers,
    ),
    WireframePage(
        key="cost_planner_estimate",
        label="Cost Planner Estimate",
        description="Initial intake selections before entering the module dashboard.",
        render=render_cost_planner_estimate,
    ),
    WireframePage(
        key="cost_planner_modules",
        label="Cost Planner Modules",
        description="Dashboard of module tiles showing progress and Navi priorities.",
        render=render_cost_planner_modules,
    ),
    WireframePage(
        key="cost_planner_housing",
        label="Housing module",
        description="Housing & living cost inputs using the module pattern.",
        render=render_cost_planner_housing,
    ),
    WireframePage(
        key="cost_planner_home_care",
        label="Home care module",
        description="Staffing and add-on costs for in-home care.",
        render=render_cost_planner_home_care,
    ),
    WireframePage(
        key="cost_planner_daily_aids",
        label="Medical & daily aids module",
        description="Recurring medical supplies, prescriptions, and transport.",
        render=render_cost_planner_daily_aids,
    ),
    WireframePage(
        key="cost_planner_benefits",
        label="Benefits & income module",
        description="Offsets and premium tracking.",
        render=render_cost_planner_benefits,
    ),
    WireframePage(
        key="cost_planner_freeform",
        label="Notes & extras module",
        description="Custom line items, debts, and planner notes.",
        render=render_cost_planner_freeform,
    ),
    WireframePage(
        key="cost_planner_mods",
        label="Home modifications module",
        description="Safety and accessibility projects.",
        render=render_cost_planner_mods,
    ),
    WireframePage(
        key="cost_planner_estimate_summary",
        label="Estimate summary",
        description="Roll-up of monthly totals, offsets, and categories.",
        render=render_cost_planner_estimate_summary,
    ),
    WireframePage(
        key="cost_plan_confirm",
        label="Cost plan confirmation",
        description="Final confirmation screen before exporting or sharing.",
        render=render_cost_plan_confirm,
    ),
    WireframePage(
        key="cost_planner_skipped",
        label="Skipped modules",
        description="Follow-up list for unfinished modules.",
        render=render_cost_planner_skipped,
    ),
    WireframePage(
        key="cost_planner_evaluation",
        label="Expert review",
        description="Navi's review flags and decision log.",
        render=render_cost_planner_evaluation,
    ),
]


PAGE_LOOKUP: Dict[str, WireframePage] = {page.key: page for page in WIREFRAME_PAGES}


st.sidebar.header("Cost Planner wireframes")
selected_key = st.sidebar.selectbox(
    "Preview a page",
    options=[page.key for page in WIREFRAME_PAGES],
    format_func=lambda key: PAGE_LOOKUP[key].label,
)

selected_page = PAGE_LOOKUP[selected_key]
st.sidebar.write(selected_page.description)

selected_page.render()
