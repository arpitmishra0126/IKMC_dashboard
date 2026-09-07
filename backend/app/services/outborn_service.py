"""
Backs GET /api/dashboard/outborn - a cohesive rollup of pages/3_Outborn.py.

Per docs/MIGRATION_DECISIONS.md #6: every outborn-scoped indicator function
used here (get_outborn_total_cases, get_outborn_avg_kmc, and the NVD/
C-section splits) filters on scr_pob.isin([12, 13, 14]) in the existing
code, which differs from KPI_FORMULA_DEFINITIONS.txt (documented as
scr_pob == 12 only). This module follows the code, unchanged, per the
"code is source of truth" rule - it does not narrow the cohort to match the
document.
"""
from __future__ import annotations

from typing import Any

from app.services.indicators_bridge import indicators, to_native

_OUTBORN_DEFINITION_NOTE = (
    "All figures below use scr_pob.isin([12, 13, 14]) per the existing "
    "implementation. KPI_FORMULA_DEFINITIONS.txt documents scr_pob == 12 "
    "only. See docs/MIGRATION_DECISIONS.md #6 - not reconciled in this API."
)


def _delivery_unit(prefix: str) -> dict[str, Any]:
    """prefix is 'outborn_nvd' or 'outborn_csection'."""
    case_count, minutes = getattr(indicators, f"get_{prefix}_attachment_stats")()

    return {
        "case_count": to_native(getattr(indicators, f"get_{prefix}_count")()),
        "ssc_under_2h": to_native(getattr(indicators, f"get_{prefix}_ssc_under_2h_count")()),
        "avg_kmc": to_native(getattr(indicators, f"get_{prefix}_avg_kmc")()),
        "exclusive_bf": to_native(getattr(indicators, f"get_{prefix}_bf_count")()),
        "attachment": {"minutes": to_native(minutes), "case_count": to_native(case_count)},
    }


def get_outborn_dashboard() -> dict[str, Any]:
    return {
        "total_cases": to_native(indicators.get_outborn_total_cases()),
        "overall_avg_kmc": to_native(indicators.get_outborn_avg_kmc()),
        "nvd": _delivery_unit("outborn_nvd"),
        "csection": _delivery_unit("outborn_csection"),
        "outborn_definition_note": _OUTBORN_DEFINITION_NOTE,
    }
