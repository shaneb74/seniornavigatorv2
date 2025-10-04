# pages/contextual_welcome_loved_one.py
try:
    from pages.contextual_welcome_base import render
except Exception:
    from contextual_welcome_base import render
render("loved")
