"""
Backs GET /api/dashboard/overview - the three top KPI cards from app.py,
4 discharge outcome counts (Discharged/Referred/LAMA/Death), the resolved
period date range, and the period-aware "Total Cases" summary (senior
feedback: Total Cases, Delivery Type, SSC<2h, Avg KMC, Exclusive BF,
Attachment age).

The "Reporting Period" filter (relative buttons + custom From/To) narrows:
- PRE-SCREENED/SCREENED/ENROLLED (+ enrolled_msncu/enrolled_stable) by
  eligibility.scr_dof (the SCREENING DATE - NOT mother.enr_dof, the
  enrollment date; enr_dof is populated only for the small subset of
  babies who were actually enrolled, so filtering this screening-stage
  funnel by it collapsed these KPIs to the same tiny enrolled-only count
  - see services.indicators._filter_by_scr_dof / get_eligibility_df).
  ENROLLED represents the CONSENTED population (scr_mconst == 11 on top
  of Eligible - services.indicators.get_overview_enrolled_total(), which
  wraps the existing get_consented_df()), per the verified ICMR source
  structure (Eligible -> Consent refused / could not be administered ->
  Consented -> Enrolled PT/LBW requiring M-SNCU / Enrolled Stable
  PT/LBW). enrolled_msncu/enrolled_stable split that same Consented
  population by scr_sncu_sick (11/12) - see
  get_overview_enrolled_msncu_total()/get_overview_enrolled_stable_total().
  This replaces the old ELIGIBLE FOR ENROLLMENT card. It is NOT the same
  as services.indicators.get_total_enrolled()/get_enrolled_df(), which
  add an unrelated scr_bw_ga_stable == 12 filter not part of this
  structure - those functions are left unchanged/unused here, in case
  anything else still relies on them.
- Discharged/Referred/LAMA/Death by dis_inf_dt_outcome (actual infant
  outcome date, not dis_dof/form-completion date) - unchanged by this
  feature, still its own field; only the shared boundary dates shift
- total_cases_summary by the same mother.enr_dof, via the ISOLATED
  services.overview_period_metrics module (not by parameterizing the
  existing Cohort Summary indicator functions - see that module's
  docstring for why)

All of these use the SAME resolved (start, end) boundaries. For the
relative buttons (7d/30d/3m), that range is always anchored to the latest
enr_dof actually present in the data - services.loader.
get_last_enrollment_date() - never to the server/browser's wall-clock
date. A custom range is anchored to the exact from_date/to_date given
(both inclusive - to_date has no time component in the data, so a plain
`<=` comparison already includes that whole day). Omitting `period` (or
"all") reproduces the exact pre-existing unfiltered values for every
field; nothing else (Still Admitted, Cohort Summary, Data Quality,
Inborn/Outborn/Discharge pages) changes.

`period_start`/`period_end` are additionally returned so the frontend
doesn't need to re-derive them: for a relative or custom period they equal
the filter boundaries; for "all" (no filtering applied, so pre-existing
values are untouched) they instead show the actual earliest/latest
enr_dof present in the data, purely for display.
"""
from __future__ import annotations

from typing import Any, Optional

import pandas as pd

from app.core.exceptions import InvalidDateRangeError
from app.services.indicators_bridge import indicators, loader, to_native
import services.overview_period_metrics as overview_period_metrics

_PERIOD_DAYS = {"7d": 7, "30d": 30}


def _resolve_range(
    period: Optional[str], from_date: Optional[str] = None, to_date: Optional[str] = None
) -> tuple[Any, Any]:
    """Filter boundaries. A custom from_date/to_date pair takes priority
    over `period` when both are given. Returns (None, None) for "all" with
    no custom range, which means "no filtering applied" (existing
    indicator functions' default behavior)."""
    if from_date is not None or to_date is not None:
        if from_date is None or to_date is None:
            raise InvalidDateRangeError("Both from_date and to_date are required together.")

        start = pd.to_datetime(from_date, errors="coerce")
        end = pd.to_datetime(to_date, errors="coerce")
        if pd.isna(start) or pd.isna(end):
            raise InvalidDateRangeError("from_date/to_date must be valid dates (YYYY-MM-DD).")
        if start > end:
            raise InvalidDateRangeError("from_date cannot be after to_date.")

        return start, end

    if not period or period == "all":
        return None, None

    anchor = loader.get_last_enrollment_date()
    if pd.isna(anchor):
        return None, None

    if period == "3m":
        start = anchor - pd.DateOffset(months=3)
    elif period in _PERIOD_DAYS:
        start = anchor - pd.Timedelta(days=_PERIOD_DAYS[period])
    else:
        return None, None

    return start, anchor


def _resolve_display_range(start: Any, end: Any) -> tuple[Optional[str], Optional[str]]:
    """What to SHOW for the period, as opposed to what was used to filter.
    For a relative or custom period this is identical to the filter
    boundaries. For "all" (where start/end are None - no filtering
    happens), this instead reports the actual earliest/latest enr_dof
    present in the data, so the UI can show a real range instead of "no
    bound"."""
    if start is not None and end is not None:
        return start.isoformat(), end.isoformat()

    anchor = loader.get_last_enrollment_date()
    if pd.isna(anchor):
        return None, None

    data = loader.load_all_data()
    earliest = pd.to_datetime(data["mother"]["enr_dof"], errors="coerce").min()

    return (earliest.isoformat() if pd.notna(earliest) else None), anchor.isoformat()


def get_overview(
    period: Optional[str] = None, from_date: Optional[str] = None, to_date: Optional[str] = None
) -> dict[str, Any]:
    start, end = _resolve_range(period, from_date, to_date)
    display_start, display_end = _resolve_display_range(start, end)
    total_cases_summary = overview_period_metrics.get_overview_total_cases(start, end)

    return {
        "pre_screened": to_native(indicators.get_total_screening_records(start, end)),
        "screened": to_native(indicators.get_total_screened(start, end)),
        "enrolled": to_native(indicators.get_overview_enrolled_total(start, end)),
        "enrolled_msncu": to_native(indicators.get_overview_enrolled_msncu_total(start, end)),
        "enrolled_stable": to_native(indicators.get_overview_enrolled_stable_total(start, end)),
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
            "attachment": {
                "nvd": total_cases_summary["attachment"]["nvd"],
                "csection": total_cases_summary["attachment"]["csection"],
            },
        },
    }
