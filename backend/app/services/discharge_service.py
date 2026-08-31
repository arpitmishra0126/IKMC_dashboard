"""Backs GET /api/dashboard/discharge - a cohesive rollup of pages/6_Discharge.py."""
from __future__ import annotations

from typing import Any

from app.services.indicators_bridge import indicators, to_native


def _outcome(prefix: str) -> dict[str, Any]:
    """prefix is e.g. 'inborn_nvd', 'inborn_csection', 'outborn_nvd', 'outborn_csection'."""
    return {
        "discharged": to_native(getattr(indicators, f"get_{prefix}_discharged")()),
        "referred": to_native(getattr(indicators, f"get_{prefix}_referred")()),
        "lama": to_native(getattr(indicators, f"get_{prefix}_lama")()),
        "death": to_native(getattr(indicators, f"get_{prefix}_death")()),
    }


def get_discharge_dashboard() -> dict[str, Any]:
    return {
        "summary": {
            "discharged": to_native(indicators.get_total_discharged()),
            "referred": to_native(indicators.get_total_referred()),
            "lama": to_native(indicators.get_total_lama()),
            "death": to_native(indicators.get_total_death()),
            "still_admitted": to_native(indicators.get_total_still_admitted()),
        },
        "inborn": {
            "nvd": _outcome("inborn_nvd"),
            "csection": _outcome("inborn_csection"),
        },
        "outborn": {
            "nvd": _outcome("outborn_nvd"),
            "csection": _outcome("outborn_csection"),
        },
    }
