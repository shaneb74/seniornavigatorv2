"""Ensure cost planner pages are importable."""
from __future__ import annotations

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from senior_nav.cost_planner import wizard


def test_cp_step_modules_define_render() -> None:
    for step in wizard.STEPS:
        path = Path(step.path)
        assert path.exists(), f"Step file missing: {path}"
        module = wizard.load_step_module(step)
        assert hasattr(module, "render"), f"Step {step.key} missing render()"
