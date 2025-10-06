# Cost Planner · Liquidity (v2)
from __future__ import annotations
import streamlit as st

# ---------------- Theme helpers (same pattern as Income) ----------------
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
                    st.switch_page("app_pages/cost_planner_v2/cost_planner_modules_hub_v2.py")
        if next:
            with cols[-1]:
                if st.button(next.label, key=next.key, type="primary", use_container_width=True):
                    st.switch_page("app_pages/cost_planner_v2/cost_planner_home_mods_v2.py")

# ---------------- Small helpers (content preserved) ----------------
def _cp() -> dict:
    """Get or init cost_planner state bucket."""
    return st.session_state.setdefault("cost_planner", {})

def _ensure_bucket() -> dict:
    cp = _cp()
    return cp.setdefault("liquidity", {
        "planning_to_sell": False,
        "keeping_car": True,
        "car_sale_value": 0,
        "furniture_sale_value": 0,
        "other_sale_value": 0,
        "liquidity_total": 0,
    })

def _save_to_state(vals: dict) -> None:
    cp = _cp()
    liq = cp.setdefault("liquidity", {})
    liq.update(vals)
    # Derive total
    liq["liquidity_total"] = max(0, int(liq.get("car_sale_value", 0))) \
                           + max(0, int(liq.get("furniture_sale_value", 0))) \
                           + max(0, int(liq.get("other_sale_value", 0)))
    # Convenience flag for other modules
    cp.setdefault("flags", {})
    cp["flags"]["keeping_car"] = bool(liq.get("keeping_car", True))

# ---------------- Page content ----------------
def render() -> None:
    # ✅ same bootstrapping as Income
    apply_cost_planner_theme()

    render_app_header()
    with cost_planner_page_container():
        render_wizard_hero("Liquidity", "Moving to care? Selling anything?")
        render_wizard_help(
            "Quick way to add one-time cash from selling a car, furniture, or other items. "
            "We’ll roll this into your **Total Assets Available**."
        )

        # Intro card (keeps your content, uses Streamlit container styling)
        with st.container(border=True):
            st.caption("Optional")
            st.subheader("Moving to care? Selling anything?")
            st.caption(
                "Quick way to add one-time cash from selling a car, furniture, or other items. "
                "We’ll roll this into your Total Assets Available."
            )

        bucket = _ensure_bucket()
        planning = st.toggle(
            "Planning to sell big things?",
            value=bool(bucket.get("planning_to_sell", False)),
            key="liq_planning",
        )

        keeping_car = st.toggle(
            "Keeping the car?",
            value=bool(bucket.get("keeping_car", True)),
            key="liq_keep_car",
            help="If you won’t keep the car, other modules can reduce auto + insurance costs.",
        )

        car_sale = 0
        furn_sale = 0
        other_sale = 0

        if planning:
            with st.container(border=True):
                st.subheader("Sale estimates")
                col1, col2, col3 = st.columns(3)
                with col1:
                    car_sale = st.number_input(
                        "Car sale value ($ one-time)",
                        min_value=0,
                        step=500,
                        value=int(bucket.get("car_sale_value", 0)),
                    )
                with col2:
                    furn_sale = st.number_input(
                        "Furniture / personal items ($ one-time)",
                        min_value=0,
                        step=100,
                        value=int(bucket.get("furniture_sale_value", 0)),
                    )
                with col3:
                    other_sale = st.number_input(
                        "Other (RV, boat, etc.) ($ one-time)",
                        min_value=0,
                        step=250,
                        value=int(bucket.get("other_sale_value", 0)),
                    )
                st.caption("Tip: rough numbers are fine — we’ll treat these as one-time inflows.")

        # Preview total
        preview_total = (car_sale if planning else 0) + (furn_sale if planning else 0) + (other_sale if planning else 0)
        st.info(f"**Cash from Sales (preview):** ${preview_total:,}")

        # Actions (preserved logic; paths updated already)
        def _vals():
            return {
                "planning_to_sell": planning,
                "keeping_car": keeping_car,
                "car_sale_value": car_sale if planning else 0,
                "furniture_sale_value": furn_sale if planning else 0,
                "other_sale_value": other_sale if planning else 0,
            }

        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            if st.button("← Back to Modules", key="liq_back"):
                _save_to_state(_vals())
                st.switch_page("app_pages/cost_planner_v2/cost_planner_modules_hub_v2.py")

        with c2:
            if st.button("Save", key="liq_save"):
                _save_to_state(_vals())
                st.success("Liquidity saved.")

        with c3:
            if st.button("Save & Continue → Home Mods", key="liq_next"):
                _save_to_state(_vals())
                st.switch_page("app_pages/cost_planner_v2/cost_planner_home_mods_v2.py")

# ✅ Import-time execution under Streamlit
render()
