"""
Baseline snapshot capture for the IKMC Dashboard parity test suite.

Run manually (never automatically) to (re)generate
tests/baseline/baseline_snapshot.json:

    python tests/capture_baseline.py

This executes the EXISTING, UNMODIFIED functions in services/indicators.py
against the local JSON fixtures in data/raw/ and records their outputs.
The resulting file is the frozen "current Streamlit implementation" answer
key that test_baseline_parity.py checks future runs against, and that a
future FastAPI implementation can be diffed against for parity sign-off.

Only regenerate this file deliberately, with a clear reason recorded in the
commit message (e.g. "fixture data updated", "confirmed calculation change
requested by stakeholder") - an unexplained diff in this file is itself a
signal something changed in behavior that needs review.
"""
import hashlib
import json
import sys
import warnings
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

import services.loader as loader
loader.DATA_SOURCE = "json"

import services.indicators as ind

OUT_PATH = Path(__file__).resolve().parent / "baseline" / "baseline_snapshot.json"

# --------------------------------------------------------------------------
# Scalar-returning indicator functions currently consumed by app.py /
# pages/2_Inborn.py / pages/3_Outborn.py / pages/6_Discharge.py
# --------------------------------------------------------------------------
SCALAR_FUNCTIONS = [
    # ---- app.py: top KPI cards ----
    "get_total_screening_records",   # PRE-SCREENED
    "get_total_screened",            # SCREENED
    "get_total_eligible",            # ELIGIBLE FOR ENROLLMENT
    # funnel, not directly on a KPI card but feeds the above chain
    "get_total_alive_babies",
    "get_total_consented",
    "get_total_enrolled",

    # ---- app.py: cohort summary (inborn/outborn totals) ----
    "get_inborn_count",
    "get_outborn_count",
    "get_inborn_nvd_count",
    "get_inborn_csection_count",
    "get_outborn_nvd_count",
    "get_outborn_csection_count",
    "get_inborn_nvd_ssc_under_2h_count",
    "get_inborn_csection_ssc_under_2h_count",
    "get_outborn_nvd_ssc_under_2h_count",
    "get_outborn_csection_ssc_under_2h_count",
    "get_inborn_nvd_avg_kmc",
    "get_inborn_csection_avg_kmc",
    "get_outborn_nvd_avg_kmc",
    "get_outborn_csection_avg_kmc",
    "get_inborn_nvd_bf_count",
    "get_inborn_csection_bf_count",
    "get_outborn_nvd_bf_count",
    "get_outborn_csection_bf_count",
    # real (computed) attachment values - NOT what app.py currently displays
    # for the inborn card (see hardcoded_values section below)
    "get_inborn_nvd_attachment_hours",
    "get_inborn_csection_attachment_hours",
    "get_outborn_nvd_attachment_hours",
    "get_outborn_csection_attachment_hours",

    # ---- app.py: data quality ----
    "get_missing_babyid_count",
    "get_duplicate_babyid_count",
    "get_merge_mismatch_count",
    "get_missing_dailycare_count",
    "get_duplicate_discharge_count",
    "get_validation_status",
    "get_missing_outcome_count",

    # ---- pages/2_Inborn.py: MSNCU ----
    "get_msncu_total_cases",
    "get_msncu_nvd_count",
    "get_msncu_csection_count",
    "get_avg_kmc_hours",
    "get_msncu_avg_kmc",
    "get_msncu_nvd_avg_kmc",
    "get_msncu_csection_avg_kmc",
    "get_msncu_nvd_ssc_under_2h_count",
    "get_msncu_csection_ssc_under_2h_count",
    "get_msncu_nvd_bf_count",
    "get_msncu_csection_bf_count",
    "get_msncu_nvd_attachment_hours",
    "get_msncu_csection_attachment_hours",
    "get_msncu_nvd_achieved_count",
    "get_msncu_csection_achieved_count",
    "get_msncu_nvd_coverage",
    "get_msncu_csection_coverage",

    # ---- pages/2_Inborn.py: PNC ----
    "get_pnc_total_cases",
    "get_pnc_nvd_count",
    "get_pnc_csection_count",
    "get_pnc_avg_kmc",
    "get_pnc_nvd_avg_kmc",
    "get_pnc_csection_avg_kmc",
    "get_pnc_nvd_ssc_under_2h_count",
    "get_pnc_csection_ssc_under_2h_count",
    "get_pnc_nvd_bf_count",
    "get_pnc_csection_bf_count",
    "get_pnc_nvd_attachment_hours",
    "get_pnc_csection_attachment_hours",
    "get_pnc_nvd_achieved_count",
    "get_pnc_csection_achieved_count",
    "get_pnc_nvd_coverage",
    "get_pnc_csection_coverage",

    # ---- pages/3_Outborn.py ----
    "get_outborn_total_cases",
    "get_outborn_avg_kmc",

    # ---- pages/6_Discharge.py ----
    "get_total_discharged",
    "get_total_referred",
    "get_total_lama",
    "get_total_death",
    "get_total_still_admitted",
    "get_inborn_nvd_discharged",
    "get_inborn_nvd_referred",
    "get_inborn_nvd_lama",
    "get_inborn_nvd_death",
    "get_inborn_csection_discharged",
    "get_inborn_csection_referred",
    "get_inborn_csection_lama",
    "get_inborn_csection_death",
    "get_outborn_nvd_discharged",
    "get_outborn_nvd_referred",
    "get_outborn_nvd_lama",
    "get_outborn_nvd_death",
    "get_outborn_csection_discharged",
    "get_outborn_csection_referred",
    "get_outborn_csection_lama",
    "get_outborn_csection_death",

    # ---- not shown on any current page, but part of the funnel/SSC domain
    # and worth pinning since indicators.py exposes them publicly ----
    "get_total_ssc_received",
    "get_total_ssc_not_received",
    "get_ssc_percentage",
    "get_avg_kmc_minutes",
    "get_msncu_count",
    "get_pnc_count",
    "get_msncu_nvd_ssc_count",
    "get_msncu_csection_ssc_count",
    "get_pnc_nvd_ssc_count",
    "get_pnc_csection_ssc_count",
    "get_outborn_nvd_achieved_count",
    "get_outborn_csection_achieved_count",
    "get_outborn_nvd_coverage",
    "get_outborn_csection_coverage",
]

# DataFrame-returning functions backing the "View Validation Details" expander
DATAFRAME_FUNCTIONS = [
    "get_missing_babyid_df",
    "get_duplicate_babyid_df",
    "get_merge_mismatch_df",
    "get_missing_dailycare_df",
    "get_duplicate_discharge_df",
]


def _native(value):
    """Convert numpy/pandas scalar types to plain JSON-serializable Python types."""
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return None if np.isnan(value) else float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    if pd.isna(value) if not isinstance(value, str) else False:
        return None
    return value


def _hash_dataframe(df: pd.DataFrame) -> str:
    """Stable content hash so we can detect row-level drift without storing
    raw record data (which includes research/baby identifiers) in the repo."""
    normalized = df.astype(str).sort_index(axis=1)
    payload = normalized.to_csv(index=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def capture():
    snapshot = {
        "meta": {
            "captured_at": datetime.now().isoformat(),
            "source_module": "services.indicators",
            "data_source_used": "json (local fixtures: data/raw/*.json)",
            "note": (
                "Production DATA_SOURCE in services/config.py is 'api'. "
                "This baseline uses the local JSON fixtures for determinism; "
                "values will differ from a live-API run if upstream data has "
                "changed since data/raw/*.json was last refreshed."
            ),
        },
        "scalar_indicators": {},
        "dataframe_indicators": {},
        "sync_metadata": {},
        "hardcoded_values": {
            "app.py::cohort_summary(TOTAL INBORN CASES).attachment_nvd": "1h 45m",
            "app.py::cohort_summary(TOTAL INBORN CASES).attachment_csection": "2h 10m",
            "app.py::cohort_summary(TOTAL OUTBORN CASES).attachment_nvd": "1h 55m",
            "app.py::cohort_summary(TOTAL OUTBORN CASES).attachment_csection": "3h 45m",
        },
    }

    errors = []

    for name in SCALAR_FUNCTIONS:
        fn = getattr(ind, name, None)
        if fn is None:
            errors.append(f"{name}: function not found on services.indicators")
            continue
        try:
            snapshot["scalar_indicators"][name] = _native(fn())
        except Exception as exc:  # noqa: BLE001 - we want to record every failure
            errors.append(f"{name}: {type(exc).__name__}: {exc}")

    for name in DATAFRAME_FUNCTIONS:
        fn = getattr(ind, name, None)
        if fn is None:
            errors.append(f"{name}: function not found on services.indicators")
            continue
        try:
            df = fn()
            snapshot["dataframe_indicators"][name] = {
                "shape": list(df.shape),
                "columns": list(df.columns),
                "content_hash": _hash_dataframe(df),
            }
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{name}: {type(exc).__name__}: {exc}")

    try:
        last_sync = loader.get_last_sync()
        snapshot["sync_metadata"]["get_last_sync"] = (
            last_sync.isoformat() if pd.notna(last_sync) else None
        )
    except Exception as exc:  # noqa: BLE001
        errors.append(f"get_last_sync: {type(exc).__name__}: {exc}")

    if errors:
        snapshot["capture_errors"] = errors

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(snapshot, indent=2, sort_keys=True), encoding="utf-8")

    print(f"Baseline snapshot written to {OUT_PATH}")
    print(f"  scalar indicators captured   : {len(snapshot['scalar_indicators'])}")
    print(f"  dataframe indicators captured: {len(snapshot['dataframe_indicators'])}")
    if errors:
        print(f"  ERRORS during capture: {len(errors)}")
        for e in errors:
            print("   -", e)


if __name__ == "__main__":
    capture()
