"""Backs GET /api/dashboard/discharge - a cohesive rollup of pages/6_Discharge.py.

Optional `start`/`end` (STUDY ENROLLMENT DATE range - see overview_service.py
for the resolution logic reused here) narrow every discharge/referred/lama/
death count by dis_inf_dt_outcome (actual infant outcome date), via the
existing get_total_*()/get_{cohort}_{delivery}_*() indicator functions,
which already accept optional start/end for exactly this purpose (added
for the Overview page's discharge mini-cards). `still_admitted` is a
point-in-time census figure (currently-admitted count), not a discharge
event count, so it is NOT period-filtered - get_total_still_admitted()
takes no arguments and none are passed.
"""
from __future__ import annotations

from typing import Any, Optional

from app.services.indicators_bridge import indicators, to_native
from app.services.overview_service import _resolve_display_range, _resolve_range


def _outcome(prefix: str, start: Optional[Any], end: Optional[Any]) -> dict[str, Any]:
    """prefix is e.g. 'inborn_nvd', 'inborn_csection', 'outborn_nvd', 'outborn_csection'."""
    return {
        "discharged": to_native(getattr(indicators, f"get_{prefix}_discharged")(start, end)),
        "referred": to_native(getattr(indicators, f"get_{prefix}_referred")(start, end)),
        "lama": to_native(getattr(indicators, f"get_{prefix}_lama")(start, end)),
        "death": to_native(getattr(indicators, f"get_{prefix}_death")(start, end)),
    }


def get_discharge_dashboard(
    period: Optional[str] = None, from_date: Optional[str] = None, to_date: Optional[str] = None
) -> dict[str, Any]:
    start, end = _resolve_range(period, from_date, to_date)
    display_start, display_end = _resolve_display_range(start, end)
    return {
        "summary": {
            "discharged": to_native(indicators.get_total_discharged(start, end)),
            "referred": to_native(indicators.get_total_referred(start, end)),
            "lama": to_native(indicators.get_total_lama(start, end)),
            "death": to_native(indicators.get_total_death(start, end)),
            "still_admitted": to_native(indicators.get_total_still_admitted()),
        },
        "inborn": {
            "nvd": _outcome("inborn_nvd", start, end),
            "csection": _outcome("inborn_csection", start, end),
        },
        "outborn": {
            "nvd": _outcome("outborn_nvd", start, end),
            "csection": _outcome("outborn_csection", start, end),
        },
        "period_start": display_start,
        "period_end": display_end,
    }
