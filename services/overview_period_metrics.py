"""
Isolated, period-aware calculation path for the Overview page's "Total
Cases" summary (senior feedback: Total Cases, Delivery Type, SSC < 2h,
Average KMC, Exclusive BF, Attachment age - combined across Inborn +
Outborn, split NVD vs. C-Section).

Why this file exists instead of parameterizing services/indicators.py
--------------------------------------------------------------------
Threading optional start/end through the ~20 existing MSNCU/PNC/Outborn
indicator functions (and everything they're built on - get_master_df,
get_enrollment_master_df, get_ssc_under_2h_df, ...) was judged too
invasive for this feature. Per explicit instruction, this module instead
reimplements the SAME formulas as a small, self-contained calculation
path that starts from a scr_dof-filtered eligibility slice, so:

- services/indicators.py is completely unchanged - zero lines touched,
  not even additions.
- Every existing caller (Cohort Summary, Inborn page, Outborn page,
  Discharge page, tests, the baseline snapshot) is completely unaffected.

Every formula below is copied verbatim from the matching
services.indicators.py function - see the comment above each block for
exactly which function(s) it mirrors. Nothing here invents a new
definition. Two known, pre-existing inconsistencies are deliberately
PRESERVED rather than reconciled (see docs/MIGRATION_DECISIONS.md #5):
  1. MSNCU/PNC's Exclusive BF and Attachment age use a stricter NVD
     definition (scr_del_mode == 11 only) than every other metric
     (scr_del_mode.isin([11, 12])). Outborn has no such split - it uses
     isin([11, 12]) consistently for every metric.
  2. MSNCU/PNC's BF count is a row count (len()); Outborn's BF count is
     a unique-baby count (.nunique()) - matching each source function
     exactly.

Combining Inborn + Outborn for a single metric follows whichever pattern
services/indicators.py already uses to combine MSNCU + PNC into "Inborn",
generalized to three groups (MSNCU, PNC, Outborn):
  - Counts (delivery, SSC<2h, exclusive BF): summed, per
    get_inborn_nvd_count() = get_msncu_nvd_count() + get_pnc_nvd_count().
  - Avg KMC: pooled recompute over the combined raw rows, per
    get_inborn_nvd_avg_kmc() = mean(dmf_kmc_dur) over
    pd.concat([msncu_nvd_df, pnc_nvd_df]).
  - Attachment age: mean of each group's own mean (excluding empty/zero
    groups), per get_inborn_nvd_attachment_hours() = mean of
    [msncu_nvd_attachment_hours, pnc_nvd_attachment_hours].
"""
from __future__ import annotations

import pandas as pd

from services.config import FIELD_MAP
from services.loader import load_all_data

_DELIVERY_MODE = FIELD_MAP["delivery_mode"]


def _filter_by_scr_dof(df: pd.DataFrame, start=None, end=None) -> pd.DataFrame:
    """Same semantics as indicators._filter_by_scr_dof, reimplemented here
    so this module has no import-time dependency on services.indicators."""
    if start is None or end is None:
        return df
    dof = pd.to_datetime(df["scr_dof"], errors="coerce")
    return df[(dof >= start) & (dof <= end)]


def _avg_kmc_hours(df: pd.DataFrame) -> float:
    """Mirrors get_*_avg_kmc(): mean(dmf_kmc_dur) / 60, round 1, 0 if empty/NaN."""
    if len(df) == 0:
        return 0.0
    avg_minutes = df["dmf_kmc_dur"].mean()
    if pd.isna(avg_minutes):
        return 0.0
    return round(avg_minutes / 60, 1)


def _earliest_initiation_df(daily: pd.DataFrame) -> pd.DataFrame:
    """Mirrors services.indicators.get_earliest_initiation_df(): one row
    per baby (dmf_babyid) with the earliest qualifying DCT initiation
    datetime (`_initiation_dt`) - confirmed official source (senior
    sign-off) for Attachment Age / early initiation, replacing the old
    mother.enr_bf_bentfed_hw_dt/tm field. A variable only qualifies where
    its value is 11 ("Yes"); if both dmf_bf_bentfed_hw and dmf_exp_bmilk_hw
    are Yes, the earlier of the two recorded date/times is used - achieved
    by pooling every qualifying candidate per baby and taking the overall
    minimum. "null" is a literal placeholder babyid (same known data rule
    as outborn's dmf_babyid = "null" exclusion) and is dropped here so it
    can't act as a fake shared merge key."""
    daily = daily[daily["dmf_babyid"] != "null"]

    bf = daily.loc[
        daily["dmf_bf_bentfed_hw"] == 11,
        ["dmf_babyid", "dmf_bf_bentfed_hw_dt", "dmf_bf_bentfed_hw_tm"],
    ].rename(columns={"dmf_bf_bentfed_hw_dt": "_dt", "dmf_bf_bentfed_hw_tm": "_tm"})

    exp = daily.loc[
        daily["dmf_exp_bmilk_hw"] == 11,
        ["dmf_babyid", "dmf_exp_bmilk_hw_dt", "dmf_exp_bmilk_hw_tm"],
    ].rename(columns={"dmf_exp_bmilk_hw_dt": "_dt", "dmf_exp_bmilk_hw_tm": "_tm"})

    candidates = pd.concat([bf, exp], ignore_index=True)
    candidates["_initiation_dt"] = pd.to_datetime(
        candidates["_dt"].astype(str) + " " + candidates["_tm"].astype(str), errors="coerce"
    )
    candidates = candidates.dropna(subset=["_initiation_dt"])

    return candidates.groupby("dmf_babyid", as_index=False)["_initiation_dt"].min()


def _attachment_stats(df: pd.DataFrame, initiation: pd.DataFrame) -> tuple[int, float, float, float]:
    """Mirrors services.indicators._attachment_stats(): `df` is the
    already cohort/delivery-filtered population (scr_babyid/scr_dob/
    scr_tob) - the cohort/delivery definition is untouched, only the
    initiation-timestamp source changed to `initiation` (DCT-based, see
    _earliest_initiation_df()). Returns (case_count, mean_minutes,
    min_minutes, max_minutes); case_count is unique babies with a
    qualifying DCT initiation timestamp."""
    df = df[df["scr_babyid"] != "null"]
    merged = df.merge(initiation, left_on="scr_babyid", right_on="dmf_babyid", how="inner")
    merged = merged.drop_duplicates(subset=["scr_babyid"])
    case_count = len(merged)
    if case_count == 0:
        return 0, 0.0, 0.0, 0.0
    birth_dt = pd.to_datetime(
        merged["scr_dob"].astype(str) + " " + merged["scr_tob"].astype(str), errors="coerce"
    )
    minutes = (merged["_initiation_dt"] - birth_dt).dt.total_seconds() / 60
    # Physically-impossible negative ages (initiation before birth) come
    # from pre-existing conflicting duplicate eligibility records for the
    # same baby (see services.indicators._attachment_stats), not a
    # calculation bug - excluded from min/avg/max the same way an
    # unparseable (NaT) value already is; still counted in case_count.
    minutes = minutes.dropna()
    minutes = minutes[minutes >= 0]
    if len(minutes) == 0:
        return case_count, 0.0, 0.0, 0.0
    mean_minutes = round(minutes.mean(), 1)
    min_minutes = round(minutes.min(), 1)
    max_minutes = round(minutes.max(), 1)
    return case_count, mean_minutes, min_minutes, max_minutes


def _ssc_under_2h_count(enrollment_slice: pd.DataFrame) -> int:
    """Mirrors get_ssc_under_2h_df() + the scr_sncu_sick/scr_pob + del_mode
    filters applied by get_{msncu,pnc,outborn}_*_ssc_under_2h_count():
    enr_ssc_rec == 11 AND (ssc_dt - birth_dt) <= 2h, on the already
    cohort/delivery-mode-filtered enrollment slice passed in."""
    if len(enrollment_slice) == 0:
        return 0
    df = enrollment_slice[enrollment_slice["enr_ssc_rec"] == 11]
    if len(df) == 0:
        return 0
    birth_dt = pd.to_datetime(df["scr_dob"].astype(str) + " " + df["scr_tob"].astype(str), errors="coerce")
    ssc_dt = pd.to_datetime(
        df["enr_ssc_init_dt"].astype(str) + " " + df["enr_ssc_init_tm"].astype(str), errors="coerce"
    )
    hours_diff = (ssc_dt - birth_dt).dt.total_seconds() / 3600
    return int((hours_diff <= 2).sum())


class _Group:
    """One of MSNCU / PNC / Outborn, holding its own master + enrollment
    slices (already scr_dof-filtered) split by NVD/C-section using
    whichever definition that group's real indicators.py functions use."""

    def __init__(self, master: pd.DataFrame, enrollment: pd.DataFrame, *, strict_nvd_for_bf: bool):
        self.master_nvd = master[master[_DELIVERY_MODE].isin([11, 12])]
        self.master_csection = master[master[_DELIVERY_MODE] == 13]

        self.enrollment_nvd = enrollment[enrollment[_DELIVERY_MODE].isin([11, 12])]
        self.enrollment_csection = enrollment[enrollment[_DELIVERY_MODE] == 13]

        # MSNCU/PNC's BF/attachment source (get_{msncu,pnc}_nvd_enrollment_df)
        # filters scr_del_mode == 11 strictly, not isin([11, 12]) - see
        # docs/MIGRATION_DECISIONS.md #5. Outborn has no such split.
        if strict_nvd_for_bf:
            self.bf_attachment_nvd = enrollment[enrollment[_DELIVERY_MODE] == 11]
        else:
            self.bf_attachment_nvd = self.master_nvd
        self.bf_attachment_csection = (
            enrollment[enrollment[_DELIVERY_MODE] == 13] if strict_nvd_for_bf else self.master_csection
        )
        self._bf_row_count = strict_nvd_for_bf  # len() for MSNCU/PNC, nunique() for Outborn

    def delivery_count(self, section: str) -> int:
        df = self.master_nvd if section == "nvd" else self.master_csection
        return int(df["dmf_babyid"].nunique())

    def ssc_under_2h(self, section: str) -> int:
        df = self.enrollment_nvd if section == "nvd" else self.enrollment_csection
        return _ssc_under_2h_count(df)

    def avg_kmc_rows(self, section: str) -> pd.DataFrame:
        return self.master_nvd if section == "nvd" else self.master_csection

    def bf_count(self, section: str) -> int:
        df = self.bf_attachment_nvd if section == "nvd" else self.bf_attachment_csection
        matched = df[df["enr_bf_bentfed"] == 11]
        return int(len(matched)) if self._bf_row_count else int(matched["dmf_babyid"].nunique())

    def attachment_stats(self, section: str, initiation: pd.DataFrame) -> tuple[int, float, float, float]:
        df = self.bf_attachment_nvd if section == "nvd" else self.bf_attachment_csection
        return _attachment_stats(df, initiation)


def get_overview_total_cases(start=None, end=None) -> dict:
    """
    Period-aware Total Cases summary for the Overview page: unique baby
    count plus Delivery Type / SSC<2h / Avg KMC / Exclusive BF /
    Attachment age, combined across Inborn (MSNCU + PNC) + Outborn,
    split NVD vs. C-Section. See module docstring for exactly which
    services.indicators.py functions each piece mirrors.
    """
    data = load_all_data()
    eligibility = _filter_by_scr_dof(data["eligibility"], start, end)
    mother = data["mother"]
    daily = data["daily"]

    enrollment = eligibility.merge(
        mother, left_on=FIELD_MAP["eligibility_babyid"], right_on=FIELD_MAP["mother_babyid"], how="left"
    )
    master = enrollment.merge(
        daily, left_on=FIELD_MAP["eligibility_babyid"], right_on=FIELD_MAP["daily_babyid"], how="left"
    )

    # ---- Total Cases: get_inborn_count() + get_outborn_count() ----
    inborn_elig = eligibility[eligibility["scr_pob"] == 11]
    outborn_master_all = master[master["scr_pob"].isin([12, 13, 14])]
    total_cases = int(inborn_elig["scr_babyid"].nunique()) + int(outborn_master_all["dmf_babyid"].nunique())

    # ---- Three groups, mirroring get_msncu_master_df / get_pnc_master_df / get_outborn_df ----
    # (master requires BOTH scr_pob==11 AND scr_sncu_sick==X)
    msncu_mask_master = (master["scr_pob"] == 11) & (master["scr_sncu_sick"] == 11)
    pnc_mask_master = (master["scr_pob"] == 11) & (master["scr_sncu_sick"] == 12)
    outborn_mask_master = master["scr_pob"].isin([12, 13, 14])

    # Enrollment-based cohort filters (used for SSC<2h/BF/attachment) mirror
    # get_msncu_enrollment_df()/get_pnc_enrollment_df() EXACTLY: these check
    # ONLY scr_sncu_sick, with NO scr_pob condition - confirmed against
    # services/indicators.py:315-321. Reproduced as-is, not "fixed".
    msncu_mask_enr = enrollment["scr_sncu_sick"] == 11
    pnc_mask_enr = enrollment["scr_sncu_sick"] == 12
    outborn_mask_enr = enrollment["scr_pob"].isin([12, 13, 14])

    msncu = _Group(master[msncu_mask_master], enrollment[msncu_mask_enr], strict_nvd_for_bf=True)
    pnc = _Group(master[pnc_mask_master], enrollment[pnc_mask_enr], strict_nvd_for_bf=True)
    outborn = _Group(master[outborn_mask_master], enrollment[outborn_mask_enr], strict_nvd_for_bf=False)

    groups = [msncu, pnc, outborn]

    # DCT initiation timestamps aren't themselves period-filtered - only
    # which babies are in scope is (via the already scr_dof-filtered
    # `eligibility` feeding every group above), matching how the old
    # mother-based timestamp was pulled in regardless of its own date.
    initiation = _earliest_initiation_df(daily)

    def summed(method: str, section: str) -> int:
        return sum(getattr(g, method)(section) for g in groups)

    def pooled_avg_kmc(section: str) -> float:
        rows = pd.concat([g.avg_kmc_rows(section) for g in groups], ignore_index=True)
        return _avg_kmc_hours(rows)

    def combined_attachment(section: str) -> dict:
        stats = [g.attachment_stats(section, initiation) for g in groups]
        total_count = sum(count for count, _, _, _ in stats)
        # Mirrors get_inborn_nvd_attachment_hours()'s own combination
        # pattern exactly (mean of each group's own mean, excluding
        # values <= 0), generalized from 2 groups (MSNCU+PNC) to 3
        # (MSNCU+PNC+Outborn).
        minute_values = [mean for _, mean, _, _ in stats if mean > 0]
        mean_minutes = round(sum(minute_values) / len(minute_values), 1) if minute_values else 0.0
        # min/max: the true min/max across each group's own min/max
        # (only groups with at least one recorded case contribute).
        mins = [mn for count, _, mn, _ in stats if count > 0]
        maxes = [mx for count, _, _, mx in stats if count > 0]
        min_minutes = min(mins) if mins else 0.0
        max_minutes = max(maxes) if maxes else 0.0
        return {
            "minutes": mean_minutes,
            "min_minutes": min_minutes,
            "max_minutes": max_minutes,
            "case_count": total_count,
        }

    return {
        "total_cases": total_cases,
        "delivery": {
            "nvd": summed("delivery_count", "nvd"),
            "csection": summed("delivery_count", "csection"),
        },
        "ssc_under_2h": {
            "nvd": summed("ssc_under_2h", "nvd"),
            "csection": summed("ssc_under_2h", "csection"),
        },
        "avg_kmc": {
            "nvd": pooled_avg_kmc("nvd"),
            "csection": pooled_avg_kmc("csection"),
        },
        "exclusive_bf": {
            "nvd": summed("bf_count", "nvd"),
            "csection": summed("bf_count", "csection"),
        },
        "attachment": {
            "nvd": combined_attachment("nvd"),
            "csection": combined_attachment("csection"),
        },
    }
