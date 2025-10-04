"""Wizard registry and loader for the cost planner."""
from __future__ import annotations

import importlib.util
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Callable, List

from . import state


@dataclass(frozen=True)
class Step:
    key: str
    label: str
    path: str
    drawer_key: str | None = None


STEPS: List[Step] = [
    Step("mode", "Mode", "ui/pages/cp/00_mode_selection.py"),
    Step("qualifiers", "Qualifiers", "ui/pages/cp/01_qualifiers.py"),
    Step("housing", "Housing", "ui/pages/cp/10_housing.py", drawer_key="housing"),
    Step("care", "Care", "ui/pages/cp/20_care.py", drawer_key="care"),
    Step("medical", "Medical", "ui/pages/cp/30_medical.py", drawer_key="medical"),
    Step(
        "insurance_benefits",
        "Insurance & Benefits",
        "ui/pages/cp/40_insurance_benefits.py",
        drawer_key="insurance_benefits",
    ),
    Step("debts_other", "Debts & Other", "ui/pages/cp/50_debts_other.py", drawer_key="debts_other"),
    Step("review", "Review", "ui/pages/cp/60_review.py"),
    Step("summary", "Summary", "ui/pages/cp/70_summary.py"),
    Step("confirm", "Confirm", "ui/pages/cp/80_confirm.py"),
]


def get_steps() -> List[Step]:
    return STEPS


def get_current_step() -> Step:
    index = max(0, min(state.get_progress(), len(STEPS) - 1))
    return STEPS[index]


def get_step_index(step: Step) -> int:
    return STEPS.index(step)


def set_current_step(index: int) -> None:
    capped = max(0, min(index, len(STEPS) - 1))
    state.set_progress(capped)


@lru_cache(maxsize=None)
def load_step_module(step: Step):
    """Dynamically load the module for a step."""
    path = Path(step.path)
    module_name = "cp_" + "_".join(path.with_suffix("").parts)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load step module at {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_step(step: Step) -> None:
    module = load_step_module(step)
    render: Callable[[], None] | None = getattr(module, "render", None)
    if render is None:
        raise AttributeError(f"Step module {step.path} must define a render() function")
    render()
