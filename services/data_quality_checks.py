"""
Data Quality: "initiation before birth" validation.

NEW validation only - it reads the same datasets as the dashboard
(services.loader.load_all_data()) but does not touch, reuse or alter any
KPI calculation (including the existing SSC <2h logic).

Rule
----
    birth_dt      = eligibility.scr_dob + eligibility.scr_tob
    initiation_dt = <source date> + <source time>
    FLAG only when initiation_dt < birth_dt   (strict: equality is NOT flagged)

Sources (each evaluated independently, one output row per source record):
    SSC                    mother, enr_ssc_rec == 11
                           enr_ssc_init_dt + enr_ssc_init_tm, mother.recordid
    Mother Breastfeeding   mother, enr_bf_bentfed == 11
                           enr_bf_bentfed_hw_dt + enr_bf_bentfed_hw_tm, mother.recordid
    Daily Breastfeeding    daily
                           dmf_bf_bentfed_hw_dt + dmf_bf_bentfed_hw_tm, daily.recordid

Missing / unparseable date or time values yield NaT and are never flagged as
"before birth" (a NaT comparison is False).

Join handling
-------------
Source records link to birth data via baby ID (mother.enr_babyid /
daily.dmf_babyid -> eligibility.scr_babyid). The literal string "null" is not
a baby ID and is excluded. Eligibility can hold several rows for one baby ID;
to avoid fanning out (duplicate flags for one source record) birth is
collapsed to ONE value per baby ID - the earliest birth datetime - so a source
record is flagged only if it precedes every birth record for that baby.
"""
from __future__ import annotations

import pandas as pd

from services.config import FIELD_MAP
from services.loader import load_all_data

SSC_ISSUE = "SSC initiation before birth"
BF_ISSUE = "Breastfeeding initiation before birth"

OUTPUT_COLUMNS = [
    "Record ID",
    "Baby ID",
    "Issue Type",
    "Source",
    "Birth Date",
    "Birth Time",
    "Initiation Date",
    "Initiation Time",
    "Birth DateTime",
    "Initiation DateTime",
    "Gap (hours)",
]


def _to_datetime(date: pd.Series, time: pd.Series) -> pd.Series:
    """date + time -> datetime. Missing/invalid parts become NaT (never raises)."""
    combined = date.astype("string") + " " + time.astype("string")
    return pd.to_datetime(combined, errors="coerce")


def _fmt(value) -> str | None:
    return None if pd.isna(value) else str(value)


def build_birth_lookup(eligibility: pd.DataFrame) -> pd.DataFrame:
    """One row per real baby ID: earliest birth datetime plus its raw date/time."""
    elig = eligibility[["scr_babyid", "scr_dob", "scr_tob"]].copy()
    elig = elig[elig["scr_babyid"].notna() & (elig["scr_babyid"] != "null")]
    elig["birth_dt"] = _to_datetime(elig["scr_dob"], elig["scr_tob"])
    elig = elig.dropna(subset=["birth_dt"]).sort_values("birth_dt", kind="stable")
    return elig.drop_duplicates("scr_babyid", keep="first").set_index("scr_babyid")


def _flag_source(
    source_df: pd.DataFrame,
    birth: pd.DataFrame,
    *,
    baby_col: str,
    date_col: str,
    time_col: str,
    source: str,
    issue: str,
) -> pd.DataFrame:
    df = source_df[source_df[baby_col].notna() & (source_df[baby_col] != "null")].copy()
    df["_birth_dt"] = df[baby_col].map(birth["birth_dt"])
    df["_birth_date"] = df[baby_col].map(birth["scr_dob"])
    df["_birth_time"] = df[baby_col].map(birth["scr_tob"])
    df["_init_dt"] = _to_datetime(df[date_col], df[time_col])

    flagged = df[df["_init_dt"] < df["_birth_dt"]]

    return pd.DataFrame(
        {
            "Record ID": flagged["recordid"].astype(str).values,
            "Baby ID": flagged[baby_col].values,
            "Issue Type": issue,
            "Source": source,
            "Birth Date": flagged["_birth_date"].map(_fmt).values,
            "Birth Time": flagged["_birth_time"].map(_fmt).values,
            "Initiation Date": flagged[date_col].map(_fmt).values,
            "Initiation Time": flagged[time_col].map(_fmt).values,
            "Birth DateTime": flagged["_birth_dt"].dt.strftime("%Y-%m-%d %H:%M:%S").values,
            "Initiation DateTime": flagged["_init_dt"].dt.strftime("%Y-%m-%d %H:%M:%S").values,
            "Gap (hours)": (
                (flagged["_init_dt"] - flagged["_birth_dt"]).dt.total_seconds() / 3600
            ).round(2).values,
        },
        columns=OUTPUT_COLUMNS,
    )


def find_initiation_before_birth(
    eligibility: pd.DataFrame, mother: pd.DataFrame, daily: pd.DataFrame
) -> pd.DataFrame:
    """Pure function over the three datasets; returns one row per flagged record."""
    birth = build_birth_lookup(eligibility)

    ssc_src = mother[mother["enr_ssc_rec"] == 11]
    bf_src = mother[mother["enr_bf_bentfed"] == 11]

    parts = [
        _flag_source(
            ssc_src, birth,
            baby_col=FIELD_MAP["mother_babyid"],
            date_col="enr_ssc_init_dt", time_col="enr_ssc_init_tm",
            source="SSC", issue=SSC_ISSUE,
        ),
        _flag_source(
            bf_src, birth,
            baby_col=FIELD_MAP["mother_babyid"],
            date_col="enr_bf_bentfed_hw_dt", time_col="enr_bf_bentfed_hw_tm",
            source="Mother Breastfeeding", issue=BF_ISSUE,
        ),
        _flag_source(
            daily, birth,
            baby_col=FIELD_MAP["daily_babyid"],
            date_col="dmf_bf_bentfed_hw_dt", time_col="dmf_bf_bentfed_hw_tm",
            source="Daily Breastfeeding", issue=BF_ISSUE,
        ),
    ]
    return pd.concat(parts, ignore_index=True)


def get_initiation_before_birth_df() -> pd.DataFrame:
    data = load_all_data()
    return find_initiation_before_birth(data["eligibility"], data["mother"], data["daily"])


def get_initiation_before_birth_count() -> int:
    return int(len(get_initiation_before_birth_df()))
