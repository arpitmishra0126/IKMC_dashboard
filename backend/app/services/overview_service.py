"""Backs GET /api/dashboard/overview - the three top KPI cards from app.py."""
from __future__ import annotations

from typing import Any

from app.services.indicators_bridge import indicators, to_native


def get_overview() -> dict[str, Any]:
    return {
        "pre_screened": to_native(indicators.get_total_screening_records()),
        "screened": to_native(indicators.get_total_screened()),
        "eligible_for_enrollment": to_native(indicators.get_total_eligible()),
    }
