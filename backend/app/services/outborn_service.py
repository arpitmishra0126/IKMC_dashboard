"""
Backs GET /api/dashboard/outborn - a cohesive rollup of pages/3_Outborn.py.

Per docs/MIGRATION_DECISIONS.md #6: every outborn-scoped indicator function
used here (get_outborn_total_cases, get_outborn_avg_kmc, and the NVD/
C-section splits) filters on scr_pob.isin([12, 13, 14]) in the existing
code, which differs from KPI_FORMULA_DEFINITIONS.txt (documented as
scr_pob == 12 only). This module follows the code, unchanged, per the
"code is source of truth" rule - it does not narrow the cohort to match the
document.

Optional `period`/`from_date`/`to_date` (STUDY ENROLLMENT DATE range - same
_resolve_range() as Overview) narrow total_cases/overall_avg_kmc/case_count/
ssc_under_2h/avg_kmc/exclusive_bf via the isolated
services.overview_period_metrics.get_outborn_period_stats() (reusing the
exact same per-group formulas already verified against Outborn's own
indicator functions). Coverage (iKMC coverage/Achieved count) and
Attachment Age are deliberately NOT period-filtered - they keep reading
from the existing, unfiltered get_{prefix}_coverage()/*_achieved_count()/
*_attachment_stats() indicator functions regardless of the selected
period, per explicit instruction.
"""
from __future__ import annotations

from typing import Any, Optional

from app.services.indicators_bridge import indicators, to_native
from app.services.overview_service import _resolve_display_range, _resolve_range
import services.overview_period_metrics as overview_period_metrics

_OUTBORN_DEFINITION_NOTE = (
    "All figures below use scr_pob.isin([12, 13, 14]) per the existing "
    "implementation. KPI_FORMULA_DEFINITIONS.txt documents scr_pob == 12 "
    "only. See docs/MIGRATION_DECISIONS.md #6 - not reconciled in this API."
)


def _delivery_unit(prefix: str, section_stats: dict[str, Any]) -> dict[str, Any]:
    """prefix is 'outborn_nvd' or 'outborn_csection'."""
    case_count, minutes, min_minutes, max_minutes = getattr(indicators, f"get_{prefix}_attachment_stats")()

    return {
        "case_count": to_native(section_stats["case_count"]),
        "ssc_under_2h": to_native(section_stats["ssc_under_2h"]),
        "avg_kmc": to_native(section_stats["avg_kmc"]),
        "exclusive_bf": to_native(section_stats["exclusive_bf"]),
        "coverage": {
            "percentage": to_native(getattr(indicators, f"get_{prefix}_coverage")()),
            "achieved_count": to_native(getattr(indicators, f"get_{prefix}_achieved_count")()),
            "total_count": to_native(getattr(indicators, f"get_{prefix}_count")()),
        },
        "attachment": {
            "minutes": to_native(minutes),
            "min_minutes": to_native(min_minutes),
            "max_minutes": to_native(max_minutes),
            "case_count": to_native(case_count),
        },
    }


def get_outborn_dashboard(
    period: Optional[str] = None, from_date: Optional[str] = None, to_date: Optional[str] = None
) -> dict[str, Any]:
    start, end = _resolve_range(period, from_date, to_date)
    display_start, display_end = _resolve_display_range(start, end)
    period_stats = overview_period_metrics.get_outborn_period_stats(start, end)

    return {
        "total_cases": to_native(period_stats["total_cases"]),
        "overall_avg_kmc": to_native(period_stats["overall_avg_kmc"]),
        "nvd": _delivery_unit("outborn_nvd", period_stats["nvd"]),
        "csection": _delivery_unit("outborn_csection", period_stats["csection"]),
        "outborn_definition_note": _OUTBORN_DEFINITION_NOTE,
        "period_start": display_start,
        "period_end": display_end,
    }
