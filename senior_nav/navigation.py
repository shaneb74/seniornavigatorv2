"""Navigation helpers and canonical page paths."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Final

import streamlit as st

WELCOME_PAGE: Final[str] = "pages/00_welcome.py"
AUDIENCING_PAGE: Final[str] = "pages/10_audiencing.py"
HUB_PAGE: Final[str] = "pages/20_hub.py"
GCP_PAGE: Final[str] = "pages/30_guided_care_plan.py"
COST_PLANNER_PAGE: Final[str] = "pages/40_cost_planner.py"
DOCUMENTS_PAGE: Final[str] = "pages/50_my_documents.py"
PFMA_PAGE: Final[str] = "pages/60_pfma.py"
AI_ADVISOR_PAGE: Final[str] = "pages/70_ai_advisor.py"


@dataclass(frozen=True)
class NavTarget:
    path: str


def switch_page(path: str) -> None:
    """Attempt to switch pages and gracefully degrade when not available."""

    try:
        st.switch_page(path)  # type: ignore[attr-defined]
    except Exception:
        st.session_state["_sn_pending_nav"] = path
        st.rerun()


def consume_pending_nav() -> None:
    """Run at the top-level to honour any deferred navigation requests."""

    pending = st.session_state.pop("_sn_pending_nav", None)
    if pending:
        try:
            st.switch_page(pending)  # type: ignore[attr-defined]
        except Exception:
            st.error("Navigation requires Streamlit 1.40 or newer.")
            st.stop()
