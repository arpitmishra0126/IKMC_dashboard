"""Unit tests for services/data_quality_checks.py (pure, offline, no API)."""
import pandas as pd
import pytest

from services.data_quality_checks import (
    BF_ISSUE, OUTPUT_COLUMNS, SSC_ISSUE, find_initiation_before_birth,
)


def _elig(babyid, dob, tob):
    return pd.DataFrame([{"recordid": "1", "scr_babyid": babyid, "scr_dob": dob, "scr_tob": tob}])


def _mother(rec="9001", babyid="E1", ssc=11, bf=12, ssc_dt=None, ssc_tm=None, bf_dt=None, bf_tm=None):
    return pd.DataFrame([{
        "recordid": rec, "enr_babyid": babyid, "enr_ssc_rec": ssc, "enr_bf_bentfed": bf,
        "enr_ssc_init_dt": ssc_dt, "enr_ssc_init_tm": ssc_tm,
        "enr_bf_bentfed_hw_dt": bf_dt, "enr_bf_bentfed_hw_tm": bf_tm,
    }])


EMPTY_DAILY = pd.DataFrame(columns=["recordid", "dmf_babyid", "dmf_bf_bentfed_hw_dt", "dmf_bf_bentfed_hw_tm"])


def _ssc(dob, tob, dt, tm):
    return find_initiation_before_birth(_elig("E1", dob, tob), _mother(ssc_dt=dt, ssc_tm=tm), EMPTY_DAILY)


def test_same_day_earlier_is_flagged():
    r = _ssc("2026-08-11", "10:00:00", "2026-08-11", "09:30:00")
    assert len(r) == 1 and r.iloc[0]["Gap (hours)"] == -0.5


def test_previous_day_is_flagged():
    assert len(_ssc("2026-08-11", "10:00:00", "2026-08-10", "23:00:00")) == 1


def test_exact_equality_not_flagged():
    assert _ssc("2026-08-11", "10:00:00", "2026-08-11", "10:00:00").empty


def test_later_not_flagged():
    assert _ssc("2026-08-11", "10:00:00", "2026-08-11", "10:30:00").empty


@pytest.mark.parametrize("dt,tm", [(None, None), (None, "09:00:00"), ("2026-08-11", None), ("bad", "xx")])
def test_missing_or_orphan_is_not_before_birth(dt, tm):
    assert _ssc("2026-08-11", "10:00:00", dt, tm).empty


def test_live_regression_case():
    r = find_initiation_before_birth(
        _elig("E14060414", "2026-08-11", "13:05:00"),
        _mother(rec="14061602", babyid="E14060414", ssc_dt="2026-08-11", ssc_tm="01:10:00"),
        EMPTY_DAILY,
    )
    assert len(r) == 1
    row = r.iloc[0]
    assert list(r.columns) == OUTPUT_COLUMNS
    assert (row["Record ID"], row["Baby ID"], row["Source"], row["Issue Type"]) == (
        "14061602", "E14060414", "SSC", SSC_ISSUE)
    assert row["Birth DateTime"] == "2026-08-11 13:05:00"
    assert row["Initiation DateTime"] == "2026-08-11 01:10:00"


def test_ssc_only_evaluated_when_received():
    r = find_initiation_before_birth(
        _elig("E1", "2026-08-11", "10:00:00"),
        _mother(ssc=12, ssc_dt="2026-08-10", ssc_tm="01:00:00"), EMPTY_DAILY)
    assert r.empty


def test_mother_breastfeeding_requires_status_11_and_labels_source():
    kw = dict(bf_dt="2026-08-10", bf_tm="01:00:00")
    e = _elig("E1", "2026-08-11", "10:00:00")
    assert find_initiation_before_birth(e, _mother(bf=12, **kw), EMPTY_DAILY).empty
    r = find_initiation_before_birth(e, _mother(bf=11, **kw), EMPTY_DAILY)
    assert list(r["Source"]) == ["Mother Breastfeeding"] and list(r["Issue Type"]) == [BF_ISSUE]
    assert list(r["Record ID"]) == ["9001"]


def test_daily_breastfeeding_uses_daily_recordid():
    daily = pd.DataFrame([{"recordid": "7001", "dmf_babyid": "E1",
                           "dmf_bf_bentfed_hw_dt": "2026-08-11", "dmf_bf_bentfed_hw_tm": "09:59:00"}])
    r = find_initiation_before_birth(_elig("E1", "2026-08-11", "10:00:00"), _mother(ssc=12), daily)
    assert list(r["Source"]) == ["Daily Breastfeeding"] and list(r["Record ID"]) == ["7001"]


def test_null_baby_id_not_used_as_join_key_and_no_fanout():
    elig = pd.concat([
        _elig("null", "2026-08-11", "10:00:00"),
        _elig("E1", "2026-08-11", "10:00:00"),
        _elig("E1", "2026-08-11", "12:00:00"),  # duplicate baby id: must not duplicate flags
    ], ignore_index=True)
    r = find_initiation_before_birth(
        elig, pd.concat([_mother(babyid="null", ssc_dt="2026-08-01", ssc_tm="01:00:00"),
                         _mother(rec="9002", babyid="E1", ssc_dt="2026-08-11", ssc_tm="09:00:00")]),
        EMPTY_DAILY)
    assert list(r["Record ID"]) == ["9002"]
