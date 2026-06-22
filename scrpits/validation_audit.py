import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)

import pandas as pd

from services.indicators import (
    get_eligibility_df,
    get_master_df,
    get_enrollment_master_df,
)

# ==================================================
# LOAD DATA
# ==================================================

eligibility = get_eligibility_df()
master = get_master_df()
enrollment = get_enrollment_master_df()

# ==================================================
# BASIC DATASET INFO
# ==================================================

print("\n" + "=" * 80)
print("DATASET OVERVIEW")
print("=" * 80)

print("Eligibility Rows:", len(eligibility))
print("Enrollment Rows:", len(enrollment))
print("Master Rows:", len(master))

if "dmf_babyid" in master.columns:
    print("Unique Babies:", master["dmf_babyid"].nunique())

# ==================================================
# PLACE OF BIRTH
# ==================================================

print("\n" + "=" * 80)
print("PLACE OF BIRTH (scr_pob)")
print("=" * 80)

print(master["scr_pob"].value_counts(dropna=False))

# ==================================================
# SNCU TYPE
# ==================================================

print("\n" + "=" * 80)
print("SNCU TYPE (scr_sncu_sick)")
print("=" * 80)

print(master["scr_sncu_sick"].value_counts(dropna=False))

# ==================================================
# DELIVERY MODE
# ==================================================

print("\n" + "=" * 80)
print("DELIVERY MODE (scr_del_mode)")
print("=" * 80)

print(master["scr_del_mode"].value_counts(dropna=False))

# ==================================================
# SSC RECEIVED
# ==================================================

print("\n" + "=" * 80)
print("SSC RECEIVED (ROW LEVEL)")
print("=" * 80)

print(master["enr_ssc_rec"].value_counts(dropna=False))

print("\n")

print("=" * 80)
print("SSC RECEIVED (BABY LEVEL)")
print("=" * 80)

ssc_baby = (
    master.groupby("dmf_babyid")["enr_ssc_rec"]
    .first()
)

print(ssc_baby.value_counts(dropna=False))

# ==================================================
# SSC TIMING
# ==================================================

print("\n" + "=" * 80)
print("SSC TIMING VALIDATION")
print("=" * 80)

ssc_df = enrollment.copy()

ssc_df = ssc_df[
    ssc_df["enr_ssc_rec"] == 11
]

birth_dt = pd.to_datetime(
    ssc_df["scr_dob"].astype(str)
    + " "
    + ssc_df["scr_tob"].astype(str),
    errors="coerce"
)

ssc_dt = pd.to_datetime(
    ssc_df["enr_ssc_init_dt"].astype(str)
    + " "
    + ssc_df["enr_ssc_init_tm"].astype(str),
    errors="coerce"
)

ssc_df["ssc_hours"] = (
    ssc_dt - birth_dt
).dt.total_seconds() / 3600

print("SSC Received Babies:", len(ssc_df))

print("\nSSC <= 2 Hours")
print((ssc_df["ssc_hours"] <= 2).sum())

print("\nSSC > 2 Hours")
print((ssc_df["ssc_hours"] > 2).sum())

print("\nMissing SSC Hours")
print(ssc_df["ssc_hours"].isna().sum())

# ==================================================
# KMC VALIDATION
# ==================================================

print("\n" + "=" * 80)
print("KMC DURATION")
print("=" * 80)

print(master["dmf_kmc_dur"].describe())

print("\nKMC >= 480")
print((master["dmf_kmc_dur"] >= 480).sum())

print("\nKMC < 480")
print((master["dmf_kmc_dur"] < 480).sum())

print("\nMissing KMC")
print(master["dmf_kmc_dur"].isna().sum())

# ==================================================
# BREASTFEEDING
# ==================================================

print("\n" + "=" * 80)
print("EXCLUSIVE BREASTFEEDING")
print("=" * 80)

print(master["enr_bf_bentfed"].value_counts(dropna=False))

# ==================================================
# ATTACHMENT
# ==================================================

print("\n" + "=" * 80)
print("ATTACHMENT DATA")
print("=" * 80)

print(
    "Valid Attachment Dates:",
    master["enr_bf_bentfed_hw_dt"].notna().sum()
)

print(
    "Missing Attachment Dates:",
    master["enr_bf_bentfed_hw_dt"].isna().sum()
)

# ==================================================
# PROGRAM CRITERIA FUNNEL
# ==================================================

print("\n" + "=" * 80)
print("PROGRAM CRITERIA FUNNEL")
print("=" * 80)

df = master.copy()

print(
    "START BABIES:",
    df["dmf_babyid"].nunique()
)

df1 = df[
    df["enr_ssc_rec"] == 11
]

print(
    "AFTER SSC RECEIVED:",
    df1["dmf_babyid"].nunique()
)

birth_dt = pd.to_datetime(
    df1["scr_dob"].astype(str)
    + " "
    + df1["scr_tob"].astype(str),
    errors="coerce"
)

ssc_dt = pd.to_datetime(
    df1["enr_ssc_init_dt"].astype(str)
    + " "
    + df1["enr_ssc_init_tm"].astype(str),
    errors="coerce"
)

df1["ssc_hours"] = (
    ssc_dt - birth_dt
).dt.total_seconds() / 3600

df2 = df1[
    df1["ssc_hours"] <= 2
]

print(
    "AFTER SSC <= 2H:",
    df2["dmf_babyid"].nunique()
)

df3 = df2[
    df2["dmf_kmc_dur"] >= 480
]

print(
    "AFTER KMC >= 480:",
    df3["dmf_babyid"].nunique()
)

print("\n")

print(
    df3.groupby("dmf_babyid")["dmf_kmc_dur"]
    .agg(["count", "mean", "max"])
)

# ==================================================
# OUTBORN VALIDATION
# ==================================================

print("\n" + "=" * 80)
print("OUTBORN VALIDATION")
print("=" * 80)

outborn = master[
    master["scr_pob"] == 12
]

print(
    "Outborn Unique Babies:",
    outborn["dmf_babyid"].nunique()
)

print("\nDelivery Mode")

print(
    outborn["scr_del_mode"]
    .value_counts(dropna=False)
)

print("\nSSC Received")

print(
    outborn["enr_ssc_rec"]
    .value_counts(dropna=False)
)

print("\nBF")

print(
    outborn["enr_bf_bentfed"]
    .value_counts(dropna=False)
)

# ==================================================
# END
# ==================================================

print("\n" + "=" * 80)
print("AUDIT COMPLETE")
print("=" * 80)