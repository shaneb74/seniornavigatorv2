# pages/contextual_welcome_self.py
try:
    from pages.contextual_welcome_base import render  # Streamlit package import
except Exception:
    from contextual_welcome_base import render        # fallback when executed directly
render("you")


if st.button("Continue", type="primary", use_container_width=True):
    from hub import safe_switch_page
    safe_switch_page("hub.py")

