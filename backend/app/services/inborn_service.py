"""
Backs GET /api/dashboard/inborn - a cohesive rollup of pages/2_Inborn.py
(overall average iKMC, MSNCU section, PNC section).

Per docs/MIGRATION_DECISIONS.md #5: the "exclusive_bf" NVD count for both
MSNCU and PNC is computed by get_{msncu,pnc}_nvd_bf_count(), which filters
on scr_del_mode == 11 only, while every other NVD metric on the same unit
(total cases, SSC<2h, avg KMC) is computed by functions using
scr_del_mode.isin([11, 12]). This module does not reconcile that
inconsistency - it is surfaced via `nvd_definition_note` so API consumers
are not misled into assuming all four "NVD" figures share one cohort
definition.

Optional `period`/`from_date`/`to_date` (STUDY ENROLLMENT DATE range - same
_resolve_range() as Overview) narrow total_cases/avg_kmc/delivery/
ssc_under_2h/avg_kmc_by_delivery/exclusive_bf via the isolated
services.overview_period_metrics.get_inborn_unit_period_stats() (reusing
the exact same per-group formulas already verified against these unit's
own indicator functions). Coverage (iKMC coverage/Achieved count) and
Attachment Age are deliberately NOT period-filtered - they keep reading
from the existing, unfiltered get_{prefix}_*_coverage()/
*_achieved_count()/*_attachment_stats() indicator functions regardless of
the selected period, per explicit instruction.
"""
from __future__ import annotations

from typing import Any, Optional

from app.services.indicators_bridge import indicators, to_native
from app.services.overview_service import _resolve_display_range, _resolve_range
import services.overview_period_metrics as overview_period_metrics

_NVD_DEFINITION_NOTE = (
    "exclusive_bf.nvd uses scr_del_mode == 11 only; delivery.nvd, "
    "ssc_under_2h.nvd, and avg_kmc.nvd use scr_del_mode.isin([11, 12]). "
    "See docs/MIGRATION_DECISIONS.md #5 - not reconciled in this API."
)


def _unit_detail(prefix: str, start, end) -> dict[str, Any]:
    """prefix is 'msncu' or 'pnc'."""
    nvd_case_count, nvd_minutes, nvd_min, nvd_max = getattr(indicators, f"get_{prefix}_nvd_attachment_stats")()
    csection_case_count, csection_minutes, csection_min, csection_max = getattr(
        indicators, f"get_{prefix}_csection_attachment_stats"
    )()

    period_stats = overview_period_metrics.get_inborn_unit_period_stats(prefix, start, end)

    return {
        "avg_kmc": to_native(period_stats["avg_kmc"]),
        "total_cases": to_native(period_stats["total_cases"]),
        "delivery": {
            "nvd": to_native(period_stats["delivery"]["nvd"]),
            "csection": to_native(period_stats["delivery"]["csection"]),
        },
        "ssc_under_2h": {
            "nvd": to_native(period_stats["ssc_under_2h"]["nvd"]),
            "csection": to_native(period_stats["ssc_under_2h"]["csection"]),
        },
        "avg_kmc_by_delivery": {
            "nvd": to_native(period_stats["avg_kmc_by_delivery"]["nvd"]),
            "csection": to_native(period_stats["avg_kmc_by_delivery"]["csection"]),
        },
        "exclusive_bf": {
            "nvd": to_native(period_stats["exclusive_bf"]["nvd"]),
            "csection": to_native(period_stats["exclusive_bf"]["csection"]),
        },
        "attachment": {
            "nvd": {
                "minutes": to_native(nvd_minutes),
                "min_minutes": to_native(nvd_min),
                "max_minutes": to_native(nvd_max),
                "case_count": to_native(nvd_case_count),
            },
            "csection": {
                "minutes": to_native(csection_minutes),
                "min_minutes": to_native(csection_min),
                "max_minutes": to_native(csection_max),
                "case_count": to_native(csection_case_count),
            },
        },
        "coverage": {
            "nvd": {
                "percentage": to_native(getattr(indicators, f"get_{prefix}_nvd_coverage")()),
                "achieved_count": to_native(getattr(indicators, f"get_{prefix}_nvd_achieved_count")()),
                "total_count": to_native(getattr(indicators, f"get_{prefix}_nvd_count")()),
            },
            "csection": {
                "percentage": to_native(getattr(indicators, f"get_{prefix}_csection_coverage")()),
                "achieved_count": to_native(getattr(indicators, f"get_{prefix}_csection_achieved_count")()),
                "total_count": to_native(getattr(indicators, f"get_{prefix}_csection_count")()),
            },
        },
        "nvd_definition_note": _NVD_DEFINITION_NOTE,
    }


def get_inborn_dashboard(
    period: Optional[str] = None, from_date: Optional[str] = None, to_date: Optional[str] = None
) -> dict[str, Any]:
    start, end = _resolve_range(period, from_date, to_date)
    display_start, display_end = _resolve_display_range(start, end)
    return {
        "overall_avg_kmc_hours": to_native(indicators.get_avg_kmc_hours()),
        "msncu": _unit_detail("msncu", start, end),
        "pnc": _unit_detail("pnc", start, end),
        "period_start": display_start,
        "period_end": display_end,
    }
