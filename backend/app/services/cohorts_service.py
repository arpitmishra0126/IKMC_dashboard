"""
Backs GET /api/dashboard/cohorts - the TOTAL INBORN CASES / TOTAL OUTBORN
CASES cohort_summary() cards from app.py.

Per docs/MIGRATION_DECISIONS.md #3: app.py currently displays four
hardcoded attachment-time strings on these cards instead of the values
computed by get_*_attachment_hours(). This module reproduces that same
hardcoded display value (so the API faithfully mirrors current production
behavior) while ALSO surfacing the real computed value alongside it and an
explicit `is_hardcoded` flag - so the frontend/consumers can see the
discrepancy instead of it being silently hidden. No value is changed or
"fixed" here; both are exposed and the API makes clear which is which.
"""
from __future__ import annotations

from typing import Any

from app.services.indicators_bridge import indicators, to_native

# Exact literal strings currently hardcoded in app.py (TOTAL INBORN CASES /
# TOTAL OUTBORN CASES cards). See docs/MIGRATION_DECISIONS.md #3.
_HARDCODED_ATTACHMENT = {
    "inborn": {"nvd": "1h 45m", "csection": "2h 10m"},
    "outborn": {"nvd": "1h 55m", "csection": "3h 45m"},
}


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
    attach_nvd_fn = getattr(indicators, f"get_{prefix}_nvd_attachment_hours")
    attach_csection_fn = getattr(indicators, f"get_{prefix}_csection_attachment_hours")

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
            "displayed_nvd": _HARDCODED_ATTACHMENT[prefix]["nvd"],
            "displayed_csection": _HARDCODED_ATTACHMENT[prefix]["csection"],
            "is_hardcoded": True,
            "computed_nvd_hours": to_native(attach_nvd_fn()),
            "computed_csection_hours": to_native(attach_csection_fn()),
        },
    }


def get_cohort_summary() -> dict[str, Any]:
    return {
        "inborn": _cohort_card("inborn"),
        "outborn": _cohort_card("outborn"),
    }
