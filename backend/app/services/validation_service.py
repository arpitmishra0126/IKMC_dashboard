"""
Backs GET /api/validation/{check} - the "View Validation Details" expander
detail tables from app.py.

Per docs/MIGRATION_DECISIONS.md #4: get_missing_babyid_df() /
get_duplicate_babyid_df() (via get_missing_babyid_count() /
get_duplicate_babyid_count()) filter on the literal string "null", not on
real NaN/None. That behavior is reproduced unchanged - this module does not
alter the underlying filter logic, only exposes the resulting rows.
"""
from __future__ import annotations

from typing import Any

from app.core.exceptions import UnknownValidationCheckError
from app.services.indicators_bridge import dataframe_to_records, indicators

# check name (URL path segment) -> services.indicators function name
_CHECK_TO_FUNCTION = {
    "missing-baby-ids": "get_missing_babyid_df",
    "duplicate-baby-ids": "get_duplicate_babyid_df",
    "merge-mismatches": "get_merge_mismatch_df",
    "missing-daily-care": "get_missing_dailycare_df",
    "discharge-duplicates": "get_duplicate_discharge_df",
}


def known_checks() -> list[str]:
    return sorted(_CHECK_TO_FUNCTION.keys())


def get_validation_detail(check: str) -> dict[str, Any]:
    func_name = _CHECK_TO_FUNCTION.get(check)
    if func_name is None:
        raise UnknownValidationCheckError(check, known_checks())

    fn = getattr(indicators, func_name)
    df = fn()

    return {
        "check": check,
        "row_count": len(df),
        "columns": list(df.columns),
        "records": dataframe_to_records(df),
    }
