"""
Endpoint availability + response-schema tests for the FastAPI backend.

These tests check that each endpoint responds successfully and that its
JSON body matches the expected shape (keys/types). They do NOT assert
specific business values - that is test_parity.py's job, checked against
the approved baseline in tests/baseline/baseline_snapshot.json.
"""
import pytest


GET_ENDPOINTS = [
    "/api/health",
    "/api/meta/sync",
    "/api/dashboard/overview",
    "/api/dashboard/cohorts",
    "/api/dashboard/data-quality",
    "/api/dashboard/inborn",
    "/api/dashboard/outborn",
    "/api/dashboard/discharge",
    "/api/validation/missing-baby-ids",
    "/api/validation/duplicate-baby-ids",
    "/api/validation/merge-mismatches",
    "/api/validation/missing-daily-care",
    "/api/validation/discharge-duplicates",
]


@pytest.mark.parametrize("path", GET_ENDPOINTS)
def test_get_endpoint_returns_200(client, path):
    response = client.get(path)
    assert response.status_code == 200, response.text


def test_unknown_validation_check_returns_404(client):
    response = client.get("/api/validation/not-a-real-check")
    assert response.status_code == 404
    body = response.json()
    assert "detail" in body
    assert "known_checks" in body
    assert set(body["known_checks"]) == {
        "missing-baby-ids",
        "duplicate-baby-ids",
        "merge-mismatches",
        "missing-daily-care",
        "discharge-duplicates",
    }


def test_meta_refresh_post_returns_200(client):
    response = client.post("/api/meta/refresh")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "detail" in body


def test_meta_refresh_get_not_allowed(client):
    """/api/meta/refresh is POST-only; confirms it wasn't accidentally
    exposed as a GET (which would make an idempotency-breaking action
    triggerable by e.g. a browser prefetch or crawler)."""
    response = client.get("/api/meta/refresh")
    assert response.status_code == 405


# --------------------------------------------------------------------------
# Response schema checks
# --------------------------------------------------------------------------

def test_meta_sync_schema(client):
    body = client.get("/api/meta/sync").json()
    assert set(body.keys()) == {
        "latest_screening_date",
        "api_fetch_timestamp",
        "data_source",
    }
    assert isinstance(body["data_source"], str)
    # Under the local JSON fixtures (forced by conftest.use_local_json_fixtures)
    # there is no real fetch timestamp - must be explicitly null, never invented.
    assert body["api_fetch_timestamp"] is None
    assert body["latest_screening_date"] is not None


def test_overview_schema(client):
    body = client.get("/api/dashboard/overview").json()
    assert set(body.keys()) == {
        "pre_screened", "screened", "eligible_for_enrollment",
        "discharged", "referred", "lama", "death",
    }
    for key in body:
        assert isinstance(body[key], int)


def test_cohorts_schema(client):
    body = client.get("/api/dashboard/cohorts").json()
    assert set(body.keys()) == {"inborn", "outborn"}
    for cohort in ("inborn", "outborn"):
        card = body[cohort]
        assert set(card.keys()) == {
            "total_cases", "delivery", "ssc_under_2h", "avg_kmc",
            "exclusive_bf", "attachment",
        }
        assert set(card["attachment"].keys()) == {
            "displayed_nvd", "displayed_csection", "is_hardcoded",
            "computed_nvd_hours", "computed_csection_hours",
        }
        assert card["attachment"]["is_hardcoded"] is True


def test_data_quality_schema(client):
    body = client.get("/api/dashboard/data-quality").json()
    assert set(body.keys()) == {
        "missing_baby_ids", "duplicate_babies", "unmatched_records",
        "missing_daily_care", "discharge_duplicates", "validation_status",
    }
    assert isinstance(body["validation_status"], str)


def test_inborn_schema(client):
    body = client.get("/api/dashboard/inborn").json()
    assert set(body.keys()) == {"overall_avg_kmc_hours", "msncu", "pnc"}
    for unit in ("msncu", "pnc"):
        detail = body[unit]
        assert set(detail.keys()) == {
            "avg_kmc", "total_cases", "delivery", "ssc_under_2h",
            "avg_kmc_by_delivery", "exclusive_bf", "attachment_hours",
            "coverage", "nvd_definition_note",
        }
        assert set(detail["coverage"].keys()) == {"nvd", "csection"}
        assert set(detail["coverage"]["nvd"].keys()) == {"percentage", "achieved_count"}


def test_outborn_schema(client):
    body = client.get("/api/dashboard/outborn").json()
    assert set(body.keys()) == {
        "total_cases", "overall_avg_kmc", "nvd", "csection", "outborn_definition_note",
    }
    for unit in ("nvd", "csection"):
        assert set(body[unit].keys()) == {
            "case_count", "ssc_under_2h", "avg_kmc", "exclusive_bf", "attachment_hours",
        }


def test_discharge_schema(client):
    body = client.get("/api/dashboard/discharge").json()
    assert set(body.keys()) == {"summary", "inborn", "outborn"}
    assert set(body["summary"].keys()) == {
        "discharged", "referred", "lama", "death", "still_admitted",
    }
    for cohort in ("inborn", "outborn"):
        assert set(body[cohort].keys()) == {"nvd", "csection"}
        for delivery in ("nvd", "csection"):
            assert set(body[cohort][delivery].keys()) == {
                "discharged", "referred", "lama", "death",
            }


def test_validation_detail_schema(client):
    body = client.get("/api/validation/missing-baby-ids").json()
    assert set(body.keys()) == {"check", "row_count", "columns", "records"}
    assert body["check"] == "missing-baby-ids"
    assert isinstance(body["row_count"], int)
    assert isinstance(body["columns"], list)
    assert isinstance(body["records"], list)
    assert body["row_count"] == len(body["records"])
    if body["records"]:
        assert set(body["records"][0].keys()) == set(body["columns"])
