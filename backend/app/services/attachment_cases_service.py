"""
Backs GET /api/dashboard/attachment-cases - the per-case audit list behind
the Attachment Age popover (click a Min/Avg/Max box or the case count on
any Attachment Age panel - Overview, Cohort Summary, Inborn, Outborn).

Every scope below reads from the SAME underlying per-case rows that
services.indicators / services.overview_period_metrics already merge to
compute the displayed min/avg/max/case_count (see
get_*_attachment_cases() / get_overview_attachment_cases() - verified by
direct comparison to aggregate over identically to the existing
get_*_attachment_stats() output). This module does not create, derive, or
approximate a separate dataset - it only shapes those same rows into a
JSON response.
"""
from __future__ import annotations

from typing import Any, Optional

import pandas as pd

from app.core.exceptions import UnknownAttachmentScopeError
from app.services.indicators_bridge import indicators, to_native
from app.services.overview_service import _resolve_range
import services.overview_period_metrics as overview_period_metrics

# scope (matches the frontend's AttachmentScope) -> services.indicators
# function name. Covers every leaf cohort/delivery-type group (Inborn
# page's MSNCU/PNC, Outborn page) plus the Cohort Summary's combined
# Inborn card (MSNCU + PNC).
_SCOPE_TO_FUNCTION = {
    "msncu_nvd": "get_msncu_nvd_attachment_cases",
    "msncu_csection": "get_msncu_csection_attachment_cases",
    "pnc_nvd": "get_pnc_nvd_attachment_cases",
    "pnc_csection": "get_pnc_csection_attachment_cases",
    "outborn_nvd": "get_outborn_nvd_attachment_cases",
    "outborn_csection": "get_outborn_csection_attachment_cases",
    "inborn_nvd": "get_inborn_nvd_attachment_cases",
    "inborn_csection": "get_inborn_csection_attachment_cases",
}

# The Overview page's own combined (MSNCU + PNC + Outborn) card, which is
# also period-aware - handled separately since it goes through the
# isolated services.overview_period_metrics module instead.
_OVERVIEW_SCOPES = {"overview_nvd": "nvd", "overview_csection": "csection"}


def known_scopes() -> list[str]:
    return sorted([*_SCOPE_TO_FUNCTION.keys(), *_OVERVIEW_SCOPES.keys()])


def _rows_to_cases(df: pd.DataFrame) -> list[dict[str, Any]]:
    cases = []
    for row in df.to_dict(orient="records"):
        minutes = row["_minutes"]
        cases.append(
            {
                "scr_babyid": to_native(row["scr_babyid"]),
                "recordid": to_native(row["dct_recordid"]),
                "minutes": to_native(round(minutes, 1)) if pd.notna(minutes) else None,
            }
        )
    return cases


def get_attachment_cases(
    scope: str,
    period: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
) -> dict[str, Any]:
    if scope in _OVERVIEW_SCOPES:
        section = _OVERVIEW_SCOPES[scope]
        start, end = _resolve_range(period, from_date, to_date)
        df = overview_period_metrics.get_overview_attachment_cases(section, start, end)
    elif scope in _SCOPE_TO_FUNCTION:
        fn = getattr(indicators, _SCOPE_TO_FUNCTION[scope])
        df = fn()
    else:
        raise UnknownAttachmentScopeError(scope, known_scopes())

    return {"scope": scope, "cases": _rows_to_cases(df)}
