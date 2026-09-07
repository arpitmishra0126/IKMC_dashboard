"""
Parity tests: FastAPI endpoint responses vs. the approved baseline in
tests/baseline/baseline_snapshot.json (captured directly from
services.indicators - see repo-root tests/capture_baseline.py).

This is the concrete evidence for:

    CURRENT STREAMLIT IMPLEMENTATION  ==  NEW FASTAPI IMPLEMENTATION

Each entry below maps a dotted path into an endpoint's JSON response to the
services.indicators function name whose baseline value it must equal. If an
indicator function is renamed/removed, or if a response field's computation
is later changed, these tests fail loudly.

Values are read from the SAME local JSON fixtures the baseline was captured
against (tests/conftest.py forces DATA_SOURCE = "json" for the whole
session), so no tolerance/approximation beyond float rounding is needed.
"""
import math

import pytest

# --------------------------------------------------------------------------
# path -> baseline scalar_indicators key, grouped by endpoint
# --------------------------------------------------------------------------

OVERVIEW_MAP = {
    "pre_screened": "get_total_screening_records",
    "screened": "get_total_screened",
    "eligible_for_enrollment": "get_total_eligible",
    "discharged": "get_total_discharged",
    "referred": "get_total_referred",
    "lama": "get_total_lama",
    "death": "get_total_death",
}

DATA_QUALITY_MAP = {
    "missing_baby_ids": "get_missing_babyid_count",
    "duplicate_babies": "get_duplicate_babyid_count",
    "unmatched_records": "get_merge_mismatch_count",
    "missing_daily_care": "get_missing_dailycare_count",
    "discharge_duplicates": "get_duplicate_discharge_count",
    "validation_status": "get_validation_status",
}


def _cohort_map(prefix: str) -> dict:
    return {
        "total_cases": f"get_{prefix}_count",
        "delivery.nvd": f"get_{prefix}_nvd_count",
        "delivery.csection": f"get_{prefix}_csection_count",
        "ssc_under_2h.nvd": f"get_{prefix}_nvd_ssc_under_2h_count",
        "ssc_under_2h.csection": f"get_{prefix}_csection_ssc_under_2h_count",
        "avg_kmc.nvd": f"get_{prefix}_nvd_avg_kmc",
        "avg_kmc.csection": f"get_{prefix}_csection_avg_kmc",
        "exclusive_bf.nvd": f"get_{prefix}_nvd_bf_count",
        "exclusive_bf.csection": f"get_{prefix}_csection_bf_count",
        "attachment.computed_nvd_hours": f"get_{prefix}_nvd_attachment_hours",
        "attachment.computed_csection_hours": f"get_{prefix}_csection_attachment_hours",
    }


COHORTS_MAP = {
    "inborn": _cohort_map("inborn"),
    "outborn": _cohort_map("outborn"),
}


def _inborn_unit_map(prefix: str) -> dict:
    return {
        "avg_kmc": f"get_{prefix}_avg_kmc",
        "total_cases": f"get_{prefix}_total_cases",
        "delivery.nvd": f"get_{prefix}_nvd_count",
        "delivery.csection": f"get_{prefix}_csection_count",
        "ssc_under_2h.nvd": f"get_{prefix}_nvd_ssc_under_2h_count",
        "ssc_under_2h.csection": f"get_{prefix}_csection_ssc_under_2h_count",
        "avg_kmc_by_delivery.nvd": f"get_{prefix}_nvd_avg_kmc",
        "avg_kmc_by_delivery.csection": f"get_{prefix}_csection_avg_kmc",
        "exclusive_bf.nvd": f"get_{prefix}_nvd_bf_count",
        "exclusive_bf.csection": f"get_{prefix}_csection_bf_count",
        "attachment_hours.nvd": f"get_{prefix}_nvd_attachment_hours",
        "attachment_hours.csection": f"get_{prefix}_csection_attachment_hours",
        "coverage.nvd.percentage": f"get_{prefix}_nvd_coverage",
        "coverage.nvd.achieved_count": f"get_{prefix}_nvd_achieved_count",
        "coverage.csection.percentage": f"get_{prefix}_csection_coverage",
        "coverage.csection.achieved_count": f"get_{prefix}_csection_achieved_count",
    }


INBORN_MAP = {
    "overall_avg_kmc_hours": "get_avg_kmc_hours",
    "msncu": _inborn_unit_map("msncu"),
    "pnc": _inborn_unit_map("pnc"),
}


def _outborn_unit_map(prefix: str) -> dict:
    return {
        "case_count": f"get_{prefix}_count",
        "ssc_under_2h": f"get_{prefix}_ssc_under_2h_count",
        "avg_kmc": f"get_{prefix}_avg_kmc",
        "exclusive_bf": f"get_{prefix}_bf_count",
        "attachment_hours": f"get_{prefix}_attachment_hours",
    }


OUTBORN_MAP = {
    "total_cases": "get_outborn_total_cases",
    "overall_avg_kmc": "get_outborn_avg_kmc",
    "nvd": _outborn_unit_map("outborn_nvd"),
    "csection": _outborn_unit_map("outborn_csection"),
}


def _discharge_outcome_map(prefix: str) -> dict:
    return {
        "discharged": f"get_{prefix}_discharged",
        "referred": f"get_{prefix}_referred",
        "lama": f"get_{prefix}_lama",
        "death": f"get_{prefix}_death",
    }


DISCHARGE_MAP = {
    "summary": {
        "discharged": "get_total_discharged",
        "referred": "get_total_referred",
        "lama": "get_total_lama",
        "death": "get_total_death",
        "still_admitted": "get_total_still_admitted",
    },
    "inborn": {
        "nvd": _discharge_outcome_map("inborn_nvd"),
        "csection": _discharge_outcome_map("inborn_csection"),
    },
    "outborn": {
        "nvd": _discharge_outcome_map("outborn_nvd"),
        "csection": _discharge_outcome_map("outborn_csection"),
    },
}


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def _get_by_path(obj: dict, dotted_path: str):
    node = obj
    for part in dotted_path.split("."):
        node = node[part]
    return node


def _flatten(mapping: dict, prefix: str = "") -> list[tuple[str, str]]:
    """Turns a nested {response_path: baseline_key | nested_dict} map into a
    flat list of (full_response_path, baseline_key) pairs."""
    pairs: list[tuple[str, str]] = []
    for key, value in mapping.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            pairs.extend(_flatten(value, full_key))
        else:
            pairs.append((full_key, value))
    return pairs


def _assert_matches_baseline(response_value, baseline_value, label):
    if isinstance(baseline_value, float) or isinstance(response_value, float):
        assert response_value is not None and baseline_value is not None, (
            f"{label}: expected {baseline_value!r}, got {response_value!r}"
        )
        assert math.isclose(response_value, baseline_value, rel_tol=0, abs_tol=1e-9), (
            f"{label}: expected {baseline_value!r}, got {response_value!r}"
        )
    else:
        assert response_value == baseline_value, (
            f"{label}: expected {baseline_value!r}, got {response_value!r}"
        )


# --------------------------------------------------------------------------
# parametrized parity tests, one per (endpoint, field)
# --------------------------------------------------------------------------

@pytest.mark.parametrize("field_path,baseline_key", _flatten(OVERVIEW_MAP))
def test_overview_parity(client, baseline, field_path, baseline_key):
    body = client.get("/api/dashboard/overview").json()
    _assert_matches_baseline(
        _get_by_path(body, field_path),
        baseline["scalar_indicators"][baseline_key],
        f"/api/dashboard/overview::{field_path} vs {baseline_key}",
    )


@pytest.mark.parametrize("field_path,baseline_key", _flatten(DATA_QUALITY_MAP))
def test_data_quality_parity(client, baseline, field_path, baseline_key):
    body = client.get("/api/dashboard/data-quality").json()
    _assert_matches_baseline(
        _get_by_path(body, field_path),
        baseline["scalar_indicators"][baseline_key],
        f"/api/dashboard/data-quality::{field_path} vs {baseline_key}",
    )


@pytest.mark.parametrize("field_path,baseline_key", _flatten(COHORTS_MAP))
def test_cohorts_parity(client, baseline, field_path, baseline_key):
    body = client.get("/api/dashboard/cohorts").json()
    _assert_matches_baseline(
        _get_by_path(body, field_path),
        baseline["scalar_indicators"][baseline_key],
        f"/api/dashboard/cohorts::{field_path} vs {baseline_key}",
    )


@pytest.mark.parametrize("field_path,baseline_key", _flatten(INBORN_MAP))
def test_inborn_parity(client, baseline, field_path, baseline_key):
    body = client.get("/api/dashboard/inborn").json()
    _assert_matches_baseline(
        _get_by_path(body, field_path),
        baseline["scalar_indicators"][baseline_key],
        f"/api/dashboard/inborn::{field_path} vs {baseline_key}",
    )


@pytest.mark.parametrize("field_path,baseline_key", _flatten(OUTBORN_MAP))
def test_outborn_parity(client, baseline, field_path, baseline_key):
    body = client.get("/api/dashboard/outborn").json()
    _assert_matches_baseline(
        _get_by_path(body, field_path),
        baseline["scalar_indicators"][baseline_key],
        f"/api/dashboard/outborn::{field_path} vs {baseline_key}",
    )


@pytest.mark.parametrize("field_path,baseline_key", _flatten(DISCHARGE_MAP))
def test_discharge_parity(client, baseline, field_path, baseline_key):
    body = client.get("/api/dashboard/discharge").json()
    _assert_matches_baseline(
        _get_by_path(body, field_path),
        baseline["scalar_indicators"][baseline_key],
        f"/api/dashboard/discharge::{field_path} vs {baseline_key}",
    )


@pytest.mark.parametrize(
    "check,baseline_key",
    [
        ("missing-baby-ids", "get_missing_babyid_df"),
        ("duplicate-baby-ids", "get_duplicate_babyid_df"),
        ("merge-mismatches", "get_merge_mismatch_df"),
        ("missing-daily-care", "get_missing_dailycare_df"),
        ("discharge-duplicates", "get_duplicate_discharge_df"),
    ],
)
def test_validation_detail_parity(client, baseline, check, baseline_key):
    """
    Checks row_count and columns against the baseline's DataFrame shape.
    Does NOT recompute the baseline's row-content hash here: the baseline
    hash is taken over the raw DataFrame (services.indicators return value)
    before JSON serialization, and JSON round-tripping changes how NaN/None
    values stringify (e.g. NaN -> "nan" vs JSON null -> "None"), which would
    produce a false-positive mismatch unrelated to any real data drift.
    Row-level content parity is already covered by the repo-root
    tests/test_baseline_parity.py, which hashes the DataFrame directly.
    """
    body = client.get(f"/api/validation/{check}").json()
    expected = baseline["dataframe_indicators"][baseline_key]

    assert body["row_count"] == expected["shape"][0], (
        f"/api/validation/{check}: row_count mismatch"
    )
    assert body["columns"] == expected["columns"], (
        f"/api/validation/{check}: columns mismatch"
    )


def test_sync_metadata_parity(client, baseline):
    body = client.get("/api/meta/sync").json()
    assert body["latest_screening_date"] == baseline["sync_metadata"]["get_last_sync"], (
        "GET /api/meta/sync::latest_screening_date vs get_last_sync()"
    )
