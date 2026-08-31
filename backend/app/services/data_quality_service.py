"""
Backs GET /api/dashboard/data-quality - the data-quality KPI cards from
app.py (not the detail tables, which are served by /api/validation/{check}).

Per docs/MIGRATION_DECISIONS.md #7: get_validation_status() does not
incorporate missing_baby_ids or duplicate_babies into its "Healthy" /
"Review Required" decision. That behavior is reproduced unchanged here -
this module does not alter get_validation_status()'s inputs.
"""
from __future__ import annotations

from typing import Any

from app.services.indicators_bridge import indicators, to_native


def get_data_quality() -> dict[str, Any]:
    return {
        "missing_baby_ids": to_native(indicators.get_missing_babyid_count()),
        "duplicate_babies": to_native(indicators.get_duplicate_babyid_count()),
        "unmatched_records": to_native(indicators.get_merge_mismatch_count()),
        "missing_daily_care": to_native(indicators.get_missing_dailycare_count()),
        "discharge_duplicates": to_native(indicators.get_duplicate_discharge_count()),
        "validation_status": indicators.get_validation_status(),
    }
