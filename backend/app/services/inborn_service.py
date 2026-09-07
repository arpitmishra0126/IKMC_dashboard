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
"""
from __future__ import annotations

from typing import Any

from app.services.indicators_bridge import indicators, to_native

_NVD_DEFINITION_NOTE = (
    "exclusive_bf.nvd uses scr_del_mode == 11 only; delivery.nvd, "
    "ssc_under_2h.nvd, and avg_kmc.nvd use scr_del_mode.isin([11, 12]). "
    "See docs/MIGRATION_DECISIONS.md #5 - not reconciled in this API."
)


def _unit_detail(prefix: str) -> dict[str, Any]:
    """prefix is 'msncu' or 'pnc'."""
    nvd_case_count, nvd_minutes, nvd_min, nvd_max = getattr(indicators, f"get_{prefix}_nvd_attachment_stats")()
    csection_case_count, csection_minutes, csection_min, csection_max = getattr(
        indicators, f"get_{prefix}_csection_attachment_stats"
    )()

    return {
        "avg_kmc": to_native(getattr(indicators, f"get_{prefix}_avg_kmc")()),
        "total_cases": to_native(getattr(indicators, f"get_{prefix}_total_cases")()),
        "delivery": {
            "nvd": to_native(getattr(indicators, f"get_{prefix}_nvd_count")()),
            "csection": to_native(getattr(indicators, f"get_{prefix}_csection_count")()),
        },
        "ssc_under_2h": {
            "nvd": to_native(getattr(indicators, f"get_{prefix}_nvd_ssc_under_2h_count")()),
            "csection": to_native(getattr(indicators, f"get_{prefix}_csection_ssc_under_2h_count")()),
        },
        "avg_kmc_by_delivery": {
            "nvd": to_native(getattr(indicators, f"get_{prefix}_nvd_avg_kmc")()),
            "csection": to_native(getattr(indicators, f"get_{prefix}_csection_avg_kmc")()),
        },
        "exclusive_bf": {
            "nvd": to_native(getattr(indicators, f"get_{prefix}_nvd_bf_count")()),
            "csection": to_native(getattr(indicators, f"get_{prefix}_csection_bf_count")()),
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
            },
            "csection": {
                "percentage": to_native(getattr(indicators, f"get_{prefix}_csection_coverage")()),
                "achieved_count": to_native(getattr(indicators, f"get_{prefix}_csection_achieved_count")()),
            },
        },
        "nvd_definition_note": _NVD_DEFINITION_NOTE,
    }


def get_inborn_dashboard() -> dict[str, Any]:
    return {
        "overall_avg_kmc_hours": to_native(indicators.get_avg_kmc_hours()),
        "msncu": _unit_detail("msncu"),
        "pnc": _unit_detail("pnc"),
    }
