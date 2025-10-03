"""Guided Care Plan shared utilities."""

from .state import ensure_gcp_session, render_stepper, get_question_meta, QUESTION_ORDER
from .engine import evaluate_guided_care

from ui.theme import inject_theme

def ensure_gcp_theme():
    inject_theme()

__all__ = [
    "ensure_gcp_session",
    "render_stepper",
    "get_question_meta",
    "QUESTION_ORDER",
    "evaluate_guided_care",
]
