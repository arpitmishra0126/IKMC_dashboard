"""
The single point of contact between the FastAPI backend and the existing,
unmodified business logic in the repo-root `services` package
(services/indicators.py, services/loader.py, services/api_service.py,
services/config.py).

Per the migration ground rules (docs/MIGRATION_DECISIONS.md,
docs/API_MIGRATION_PLAN.md):
- No calculation is reimplemented here. Every value returned by this module
  is the direct return value of an existing `services.indicators` /
  `services.loader` function.
- None of the documented business-logic ambiguities (filters, NVD
  definition, outborn definition, validation status coverage, hardcoded
  attachment values) are resolved here - they are surfaced as-is.
"""
from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

# Triggers the repo-root sys.path bootstrap as a side effect before the
# `services` package (which lives outside backend/) is imported below.
from app.core.config import settings  # noqa: F401

import services.indicators as indicators
import services.loader as loader


def to_native(value: Any) -> Any:
    """Convert numpy/pandas scalar types returned by the existing indicator
    functions into plain, JSON-serializable Python types. This is a type
    coercion only - it does not alter any computed value."""
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return None if np.isnan(value) else float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, float) and pd.isna(value):
        return None
    return value


def dataframe_to_records(df: pd.DataFrame) -> list[dict[str, Any]]:
    """Convert a DataFrame returned by an existing validation/detail
    indicator function into JSON-serializable records, preserving the
    existing column set and row content unchanged."""
    records: list[dict[str, Any]] = []
    for row in df.to_dict(orient="records"):
        records.append({key: to_native(value) for key, value in row.items()})
    return records


def clear_cache() -> None:
    """Clears the existing st.cache_data caches used by services/loader.py,
    forcing the next call to re-run load_all_data(). This mirrors what the
    "Refresh Dashboard" button in components/dashboard_header.py already
    does today (st.cache_data.clear()) - no new refresh behavior is
    introduced."""
    import streamlit as st

    st.cache_data.clear()
