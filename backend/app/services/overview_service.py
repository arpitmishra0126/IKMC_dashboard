"""
Backs GET /api/dashboard/overview - the three top KPI cards from app.py,
4 discharge outcome counts (Discharged/Referred/LAMA/Death), the resolved
period date range, and the new period-aware "Total Cases" summary (senior
feedback: Total Cases, Delivery Type, SSC<2h, Avg KMC, Exclusive BF,
Attachment age).

Optional `period` narrows:
- PRE-SCREENED/SCREENED/ELIGIBLE FOR ENROLLMENT by scr_dof (screening date)
- Discharged/Referred/LAMA/Death by dis_inf_dt_outcome (actual infant
  outcome date, not dis_dof/form-completion date)
- total_cases_summary by scr_dof, via the ISOLATED
  services.overview_period_metrics module (not by parameterizing the
  existing Cohort Summary indicator functions - see that module's
  docstring for why)

All of these use the SAME resolved (start, end) boundaries, always
anchored to the latest scr_dof actually present in the data -
services.loader.get_last_sync(), the same value already shown as "Latest
screening date" - never to the server/browser's wall-clock date. Omitting
`period` (or "all") reproduces the exact pre-existing unfiltered values for
every field; nothing else (Still Admitted, Cohort Summary, Data Quality,
Inborn/Outborn/Discharge pages) changes.

`period_start`/`period_end` are additionally returned so the frontend
doesn't need to re-derive them: for a relative period they equal the
filter boundaries; for "all" (no filtering applied, so pre-existing values
are untouched) they instead show the actual earliest/latest scr_dof
present in the data, purely for display.
"""
from __future__ import annotations

from typing import Any, Optional

import pandas as pd

from app.services.indicators_bridge import indicators, loader, to_native
import services.overview_period_metrics as overview_period_metrics

_PERIOD_DAYS = {"7d": 7, "30d": 30}


def _resolve_range(period: Optional[str]) -> tuple[Any, Any]:
    """Filter boundaries only - unchanged from before this feature.
    Returns (None, None) for "all", which means "no filtering applied"
    (existing indicator functions' default behavior)."""
    if not period or period == "all":
        return None, None

    anchor = loader.get_last_sync()
    if pd.isna(anchor):
        return None, None

    if period == "3m":
        start = anchor - pd.DateOffset(months=3)
    elif period in _PERIOD_DAYS:
        start = anchor - pd.Timedelta(days=_PERIOD_DAYS[period])
    else:
        return None, None

    return start, anchor


def _resolve_display_range(period: Optional[str], start: Any, end: Any) -> tuple[Optional[str], Optional[str]]:
    """What to SHOW for the period, as opposed to what was used to filter.
    For a relative period this is identical to the filter boundaries. For
    "all" (where start/end are None - no filtering happens), this instead
    reports the actual earliest/latest scr_dof present in the data, so the
    UI can show a real range instead of "no bound"."""
    if start is not None and end is not None:
        return start.isoformat(), end.isoformat()

    anchor = loader.get_last_sync()
    if pd.isna(anchor):
        return None, None

    data = loader.load_all_data()
    earliest = pd.to_datetime(data["eligibility"]["scr_dof"], errors="coerce").min()

    return (earliest.isoformat() if pd.notna(earliest) else None), anchor.isoformat()


def get_overview(period: Optional[str] = None) -> dict[str, Any]:
    start, end = _resolve_range(period)
    display_start, display_end = _resolve_display_range(period, start, end)
    total_cases_summary = overview_period_metrics.get_overview_total_cases(start, end)

    return {
        "pre_screened": to_native(indicators.get_total_screening_records(start, end)),
        "screened": to_native(indicators.get_total_screened(start, end)),
        "eligible_for_enrollment": to_native(indicators.get_total_eligible(start, end)),
        "discharged": to_native(indicators.get_total_discharged(start, end)),
        "referred": to_native(indicators.get_total_referred(start, end)),
        "lama": to_native(indicators.get_total_lama(start, end)),
        "death": to_native(indicators.get_total_death(start, end)),
        "period_start": display_start,
        "period_end": display_end,
        "total_cases_summary": {
            "total_cases": total_cases_summary["total_cases"],
            "delivery": total_cases_summary["delivery"],
            "ssc_under_2h": total_cases_summary["ssc_under_2h"],
            "avg_kmc": {
                "nvd": to_native(total_cases_summary["avg_kmc"]["nvd"]),
                "csection": to_native(total_cases_summary["avg_kmc"]["csection"]),
            },
            "exclusive_bf": total_cases_summary["exclusive_bf"],
            "attachment_hours": {
                "nvd": to_native(total_cases_summary["attachment_hours"]["nvd"]),
                "csection": to_native(total_cases_summary["attachment_hours"]["csection"]),
            },
        },
    }
