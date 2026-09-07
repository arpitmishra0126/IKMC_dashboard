"""
Backs GET /api/dashboard/overview - the three top KPI cards from app.py.

Optional `period` narrows PRE-SCREENED/SCREENED/ELIGIBLE FOR ENROLLMENT to
a recent scr_dof (screening date) window. The window is always anchored to
the latest scr_dof actually present in the data - services.loader.get_last_sync(),
the same value already shown as "Latest screening date" - never to the
server/browser's wall-clock date. Omitting `period` (or "all") reproduces
the exact pre-existing unfiltered values; nothing else changes.
"""
from __future__ import annotations

from typing import Any, Optional

import pandas as pd

from app.services.indicators_bridge import indicators, loader, to_native

_PERIOD_DAYS = {"7d": 7, "30d": 30}


def _resolve_range(period: Optional[str]) -> tuple[Any, Any]:
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


def get_overview(period: Optional[str] = None) -> dict[str, Any]:
    start, end = _resolve_range(period)

    return {
        "pre_screened": to_native(indicators.get_total_screening_records(start, end)),
        "screened": to_native(indicators.get_total_screened(start, end)),
        "eligible_for_enrollment": to_native(indicators.get_total_eligible(start, end)),
    }
