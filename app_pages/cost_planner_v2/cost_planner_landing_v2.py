# Cost Planner v2 · Landing
from __future__ import annotations
import re
import streamlit as st

# ---------------- Theme helpers (match Income pattern) ----------------
try:
    from ui.cost_planner_template import (
        apply_cost_planner_theme,
        cost_planner_page_container,
        render_app_header,
        render_wizard_hero,
        render_wizard_help,
        render_nav_buttons,
        Metric, NavButton,
    )
except Exception:
    # graceful fallbacks
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
    class Metric:
        def __init__(self, title: str, value: str): self.title, self.value = title, value
    class NavButton:
        def __init__(self, label: str, key: str, type: str = "secondary", icon: str | None = None):
            self.label, self.key, self.type, self.icon = label, key, type, icon
    def render_nav_buttons(buttons=None, prev=None, next=None):
        cols = st.columns(2)
        if prev:
            with cols[0]:
                if st.button(prev.label, key=prev.key, type="secondary", use_container_width=True):
                    _goto("app_pages/cost_planner_v2/cost_planner_modules_hub_v2.py")
        if next:
            with cols[-1]:
                if st.button(next.label, key=next.key, type="primary", use_container_width=True):
                    _goto("app_pages/cost_planner_v2/cost_planner_timeline_v2.py")

# ---------------- Small nav helper ----------------
def _goto(path: str) -> None:
    try:
        st.switch_page(path)  # type: ignore[attr-defined]
    except Exception:
        st.session_state["_target_page"] = path
        st.rerun()

# ---------------- Page content (with pre-start intake) ----------------
def render() -> None:
    apply_cost_planner_theme()

    render_app_header()
    with cost_planner_page_container():
        render_wizard_hero(
            "Cost Planner",
            "A simple, conversational way to estimate care costs or plan your budget in detail."
        )
        render_wizard_help("You can start light and add more later.")

        # Medicaid informational note (does not block planning)
        if st.session_state.get("medicaid_status") == "yes":
            st.info(
                "Note: Our placement service can’t assist with Medicaid-based placement. "
                "You can still complete the Cost Planner and explore budgets."
            )

        # First info card
        with st.container(border=True):
            st.subheader("Cost Planner")
            st.caption(
                "A simple, conversational way to estimate care costs or plan your budget in detail. "
                "You can start light and add more later."
            )

        # How to start
        with st.container(border=True):
            st.subheader("How do you want to start?")
            st.markdown(
                "- **Estimate** — quick monthly care cost using a few inputs "
                "(pulls from Guided Care Plan if available).\n"
                "- **Plan** — detailed modules (income, expenses, benefits, home, assets) "
                "to see your runway."
            )

        # ---- Inline "pre-start" intake ----
        # If they haven't clicked Start yet, show the buttons. After click, show a short form.
        st.session_state.setdefault("cpv2_collecting_prestart", False)

        if not st.session_state["cpv2_collecting_prestart"]:
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Start planning", type="primary", use_container_width=True):
                    st.session_state["cpv2_collecting_prestart"] = True
                    st.rerun()
            with col2:
                if st.button("Jump to Timeline (dev)", use_container_width=True):
                    _goto("app_pages/cost_planner_v2/cost_planner_timeline_v2.py")

        else:
            # Pre-start intake form: ZIP, veteran, home ownership
            with st.container(border=True):
                st.subheader("Before you begin")
                st.caption("These details help us personalize costs and benefits.")

                # Defaults
                zip_default = st.session_state.get("cost_context.zip", "")
                vet_default = st.session_state.get("cost_context.veteran", None)
                home_default = st.session_state.get("cost_context.home_owner", None)

                with st.form("cpv2_prestart_form", clear_on_submit=False):
                    zip_val = st.text_input(
                        "ZIP code (5 digits)",
                        value=zip_default,
                        help="Used only for regionalized cost estimates."
                    )

                    colA, colB = st.columns(2)
                    with colA:
                        vet = st.selectbox(
                            "Are you a U.S. veteran (or spouse/surviving spouse)?",
                            ["Select one…", "Yes", "No"],
                            index=(0 if vet_default is None else (1 if vet_default else 2))
                        )
                    with colB:
                        home = st.selectbox(
                            "Do you (or the person you’re planning for) own a home?",
                            ["Select one…", "Yes", "No"],
                            index=(0 if home_default is None else (1 if home_default else 2))
                        )

                    submitted = st.form_submit_button("Continue", type="primary", use_container_width=True)

                # Validate and persist
                if submitted:
                    # ZIP: must be 5 digits
                    if not re.fullmatch(r"\d{5}", zip_val or ""):
                        st.error("Please enter a valid 5-digit ZIP code.")
                        return

                    # Map selects to booleans
                    vet_bool = True if vet == "Yes" else False if vet == "No" else None
                    home_bool = True if home == "Yes" else False if home == "No" else None

                    if vet_bool is None or home_bool is None:
                        st.error("Please answer all questions to continue.")
                        return

                    # Save to session
                    st.session_state["cost_context.zip"] = zip_val
                    st.session_state["cost_context.veteran"] = vet_bool
                    st.session_state["cost_context.home_owner"] = home_bool

                    # Done collecting
                    st.session_state["cpv2_collecting_prestart"] = False

                    # Proceed to the next page (Modules Hub)
                    _goto("app_pages/cost_planner_v2/cost_planner_modules_hub_v2.py")

            # Optional secondary action while the form is visible
            with st.container():
                if st.button("Cancel", type="secondary"):
                    st.session_state["cpv2_collecting_prestart"] = False
                    st.rerun()

# ✅ Import-time execution under Streamlit
render()