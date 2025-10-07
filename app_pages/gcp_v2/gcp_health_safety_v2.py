from __future__ import annotations
import streamlit as st
<<<<<<< Updated upstream
from ui.theme import inject_theme
from gcp_v2.schema import questions_for_section
from ui.gcp_form import render_section, nav_buttons
=======
from gcp_core.engine import questions_for_section
import gcp_core.state as gcp_state
from gcp_core.state import ensure_session, set_section_complete
import ui.gcp_form as gcp_form
from ui.gcp_form import render_section
>>>>>>> Stashed changes

inject_theme()

if st.query_params.get("dbg") == "1":
    answers = st.session_state.get("gcp_answers", {})
    raw = gcp_state.get_answer(answers, gcp_form.COGNITION_QID)
    st.info(
        f"Debug: cognition raw={raw!r}, token={gcp_form._current_cognition_token(answers)!r}, "
        f"severe={gcp_form._is_severe_cognition(answers)}"
    )

st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)
st.markdown("## Health & Safety")
render_section("health_safety", questions_for_section("health_safety"))
nav_buttons("pages/gcp_v2/gcp_daily_life_v2.py", "pages/gcp_v2/gcp_context_prefs_v2.py")
