# Cost Planner Wireframe Alignment

This document maps the Streamlit wireframes in `cost_planner_wireframes.py` to the existing Cost Planner pages so the team can see where the new visual design overlaps with production flows.

## Wireframe coverage at a glance

| Wireframe section | Intended production page | Notes |
| --- | --- | --- |
| Entry mode selector (Page 1) | `pages/cost_planner.py` | Wireframe adds header/hero polish to the existing mode selection that seeds `care_context` and routes to the estimate flow.【F:cost_planner_wireframes.py†L61-L107】【F:pages/cost_planner.py†L9-L55】 |
| Qualifiers (Page 2) | *(No one-to-one page)* | Current flow jumps from the mode selector into `cost_planner_estimate.py`, which pulls qualifier answers from session state instead of presenting a dedicated screen. Implementing the wireframe would require adding a new qualifiers step before that page.【F:cost_planner_wireframes.py†L109-L170】【F:pages/cost_planner_estimate.py†L22-L84】 |
| Housing module (Page 3) | `pages/cost_planner_housing.py` | The housing wireframe mirrors the production inputs; both capture base rent, utilities, and maintenance before showing the subtotal metric.【F:cost_planner_wireframes.py†L172-L238】【F:pages/cost_planner_housing.py†L19-L76】 |
| Expert review (Page 4) | `pages/cost_planner_evaluation.py` | The expert review wireframe matches the existing evaluation drawer that builds expert flags, shows Navi copy, and surfaces metrics for monthly costs and offsets.【F:cost_planner_wireframes.py†L240-L290】【F:pages/cost_planner_evaluation.py†L21-L76】 |

## Page-by-page evaluation

The following table covers every page whose filename starts with `cost_plan` or `cost_planner`, summarising what it currently does and how (or if) the new wireframes apply.

| Page | Current behaviour | Wireframe relationship |
| --- | --- | --- |
| `pages/cost_plan_confirm.py` | Final confirmation screen with metrics, CRM export, and PFMA handoff triggers.【F:pages/cost_plan_confirm.py†L22-L68】 | Not represented in the wireframes; would need bespoke styling if the new visual language is adopted. |
| `pages/cost_planner.py` | Establishes session defaults, offers **Estimate Costs** vs **Plan Costs**, and routes to the estimate entry page or hub.【F:pages/cost_planner.py†L9-L53】 | Direct match for wireframe Page&nbsp;1. Adopt hero/header styles from the wireframe for consistency.【F:cost_planner_wireframes.py†L61-L107】 |
| `pages/cost_planner_benefits.py` | Captures insurance premiums, income, and benefit offsets with conditional fields based on qualifiers, then updates the offsets subtotal.【F:pages/cost_planner_benefits.py†L26-L142】 | Not modelled in the wireframes; would follow the module styling introduced elsewhere if we extend the new visuals. |
| `pages/cost_planner_daily_aids.py` | Records prescription, supply, and transportation costs while surfacing chronic condition guidance, then updates the medical subtotal.【F:pages/cost_planner_daily_aids.py†L18-L70】 | Not covered in the wireframes; should mirror the Housing module layout if we want visual parity. |
| `pages/cost_planner_estimate.py` | Main entry form that confirms planner mode, household structure, captures liquid assets for planning mode, and surfaces running totals.【F:pages/cost_planner_estimate.py†L28-L129】 | Wireframe Page&nbsp;2 would slot before this page if we introduce a dedicated qualifier step; otherwise this page keeps the existing copy/controls. |
| `pages/cost_planner_estimate_summary.py` | Presents totals, category breakdown, custom items, and export options (PDF/CSV/JSON) before routing to confirmation.【F:pages/cost_planner_estimate_summary.py†L25-L110】 | Outside the four wireframes; apply the new header/metric styling separately if desired. |
| `pages/cost_planner_evaluation.py` | Builds expert flags from gaps between Guided Care Plan data and inputs, lists decision log entries, and shows key metrics.【F:pages/cost_planner_evaluation.py†L26-L76】 | Aligns with wireframe Page&nbsp;4; primary gap is swapping placeholder Navi copy for actual flag output. |
| `pages/cost_planner_freeform.py` | Handles debts, miscellaneous expenses, custom line items, and planner notes before routing to expert review.【F:pages/cost_planner_freeform.py†L17-L101】 | Not depicted in the wireframes; consider reusing the housing-style layout for consistency. |
| `pages/cost_planner_home_care.py` | Collects staffing, add-ons, supplemental services, and second-person support while reflecting Guided Care Plan recommendations.【F:pages/cost_planner_home_care.py†L27-L94】 | Not in the wireframes; new styling would mirror other module pages. |
| `pages/cost_planner_housing.py` | Captures housing costs with qualifier-driven helper text and updates the housing subtotal metric.【F:pages/cost_planner_housing.py†L19-L76】 | Directly modelled by wireframe Page&nbsp;3; only visual polish differs.【F:cost_planner_wireframes.py†L172-L238】 |
| `pages/cost_planner_mods.py` | Prototype age-in-place upgrade chooser with static yes/no buttons and no cost hooks yet.【F:pages/cost_planner_mods.py†L31-L58】 | Wireframes do not cover this concept; needs bespoke design work. |
| `pages/cost_planner_modules.py` | Presents module tiles with status, linking into the estimate/housing/care/benefits flows or back to mode selection.【F:pages/cost_planner_modules.py†L21-L74】 | Not referenced in the wireframe bundle; retains dashboard tile layout unless redesigned. |
| `pages/cost_planner_skipped.py` | Stub screen listing skipped modules with a CTA to revisit them.【F:pages/cost_planner_skipped.py†L31-L50】 | Not covered by the wireframes; consider applying the same hero and tile styling if kept. |

## Key takeaways

- Only the entry mode, housing, and expert review pages have direct counterparts in the provided wireframes; the qualifiers concept is new and would require an additional step in the production flow.
- Module-specific drawers (care, medical, benefits, freeform, upgrades) will need tailored design updates if the TurboTax-inspired styling becomes the standard.
- Downstream summary and confirmation pages are outside the scope of the wireframes and should be addressed separately if we want a unified look and feel.
