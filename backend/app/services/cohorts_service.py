"""
Backs GET /api/dashboard/cohorts - the TOTAL INBORN CASES / TOTAL OUTBORN
CASES cohort_summary() cards from app.py.

Attachment age now shows the actual computed value (minutes + case count)
via get_{prefix}_{nvd,csection}_attachment_stats() - the hardcoded
"1h 45m"-style display strings previously shown alongside it have been
removed per explicit instruction; nothing hardcoded is displayed here
anymore.
"""
from __future__ import annotations

from typing import Any

from app.services.indicators_bridge import indicators, to_native


def _cohort_card(prefix: str) -> dict[str, Any]:
    """prefix is 'inborn' or 'outborn' - selects the matching
    get_<prefix>_* indicator functions."""
    total_cases_fn = getattr(indicators, f"get_{prefix}_count")
    nvd_count_fn = getattr(indicators, f"get_{prefix}_nvd_count")
    csection_count_fn = getattr(indicators, f"get_{prefix}_csection_count")
    ssc_nvd_fn = getattr(indicators, f"get_{prefix}_nvd_ssc_under_2h_count")
    ssc_csection_fn = getattr(indicators, f"get_{prefix}_csection_ssc_under_2h_count")
    kmc_nvd_fn = getattr(indicators, f"get_{prefix}_nvd_avg_kmc")
    kmc_csection_fn = getattr(indicators, f"get_{prefix}_csection_avg_kmc")
    bf_nvd_fn = getattr(indicators, f"get_{prefix}_nvd_bf_count")
    bf_csection_fn = getattr(indicators, f"get_{prefix}_csection_bf_count")
    attach_nvd_stats_fn = getattr(indicators, f"get_{prefix}_nvd_attachment_stats")
    attach_csection_stats_fn = getattr(indicators, f"get_{prefix}_csection_attachment_stats")

    nvd_case_count, nvd_minutes, nvd_min, nvd_max = attach_nvd_stats_fn()
    csection_case_count, csection_minutes, csection_min, csection_max = attach_csection_stats_fn()

    return {
        "total_cases": to_native(total_cases_fn()),
        "delivery": {
            "nvd": to_native(nvd_count_fn()),
            "csection": to_native(csection_count_fn()),
        },
        "ssc_under_2h": {
            "nvd": to_native(ssc_nvd_fn()),
            "csection": to_native(ssc_csection_fn()),
        },
        "avg_kmc": {
            "nvd": to_native(kmc_nvd_fn()),
            "csection": to_native(kmc_csection_fn()),
        },
        "exclusive_bf": {
            "nvd": to_native(bf_nvd_fn()),
            "csection": to_native(bf_csection_fn()),
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
    }


def get_cohort_summary() -> dict[str, Any]:
    return {
        "inborn": _cohort_card("inborn"),
        "outborn": _cohort_card("outborn"),
    }
