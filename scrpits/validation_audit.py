import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)

from services.indicators import *

# ==================================================
# DASHBOARD MEASURES
# ==================================================

print("\n" + "=" * 80)
print("DASHBOARD MEASURES")
print("=" * 80)

print(f"PRE-SCREENED               : {get_total_screening_records()}")
print(f"ALIVE                      : {get_total_alive_babies()}")
print(f"SCREENED (PT/LBW)          : {get_total_screened()}")
print(f"ELIGIBLE FOR ENROLLMENT    : {get_total_eligible()}")
print(f"CONSENTED                  : {get_total_consented()}")
print(f"ENROLLED                   : {get_total_enrolled()}")

# ==================================================
# FUNNEL VALIDATION
# ==================================================

alive = get_alive_df()
screened = get_preterm_lbw_df()
eligible = get_eligible_df()
consented = get_consented_df()
enrolled = get_enrolled_df()

print("\n" + "=" * 80)
print("FUNNEL VALIDATION")
print("=" * 80)

print(f"Alive Records              : {len(alive)}")
print(f"Screened Records           : {len(screened)}")
print(f"Eligible Records           : {len(eligible)}")
print(f"Consented Records          : {len(consented)}")
print(f"Enrolled Records           : {len(enrolled)}")

print()

print(f"Alive → Screened Lost      : {len(alive) - len(screened)}")
print(f"Screened → Eligible Lost   : {len(screened) - len(eligible)}")
print(f"Eligible → Consented Lost  : {len(eligible) - len(consented)}")
print(f"Consented → Enrolled Lost  : {len(consented) - len(enrolled)}")

# ==================================================
# ELIGIBILITY VALIDATION
# ==================================================

print("\n" + "=" * 80)
print("ELIGIBILITY VALIDATION")
print("=" * 80)

print("\nscr_mconst_adm")
print(
    screened["scr_mconst_adm"]
    .value_counts(dropna=False)
)

print("\nscr_mconst")
print(
    eligible["scr_mconst"]
    .value_counts(dropna=False)
)

print("\nscr_bw_ga_stable")
print(
    consented["scr_bw_ga_stable"]
    .value_counts(dropna=False)
)

# ==================================================
# ENROLLED SAMPLE
# ==================================================

print("\n" + "=" * 80)
print("ENROLLED SAMPLE")
print("=" * 80)

cols = [
    "recordid",
    "scr_research_id",
    "scr_pob",
    "scr_mconst_adm",
    "scr_mconst",
    "scr_bw_ga_stable",
]

cols = [c for c in cols if c in enrolled.columns]

print(
    enrolled[cols].head(20)
)

print("\n" + "=" * 80)
print("INBORN PAGE VALIDATION")
print("=" * 80)

print(f"MSNCU Total                 : {get_msncu_count()}")
print(f"MSNCU NVD                   : {get_msncu_nvd_count()}")
print(f"MSNCU C-Section             : {get_msncu_csection_count()}")

print()

print(f"PNC Total                   : {get_pnc_count()}")
print(f"PNC NVD                     : {get_pnc_nvd_count()}")
print(f"PNC C-Section               : {get_pnc_csection_count()}")

print()

print(f"MSNCU Avg KMC               : {get_msncu_avg_kmc()}")
print(f"MSNCU NVD Avg KMC           : {get_msncu_nvd_avg_kmc()}")
print(f"MSNCU C-Section Avg KMC     : {get_msncu_csection_avg_kmc()}")

print()

print(f"PNC Avg KMC                 : {get_pnc_avg_kmc()}")
print(f"PNC NVD Avg KMC             : {get_pnc_nvd_avg_kmc()}")
print(f"PNC C-Section Avg KMC       : {get_pnc_csection_avg_kmc()}")


print("\n" + "=" * 80)
print("MSNCU DATASET VALIDATION")
print("=" * 80)

msncu = get_msncu_master_df()

print("Rows               :", len(msncu))
print("Unique Babies      :", msncu["dmf_babyid"].nunique())

print()

print("Delivery Mode")
print(
    msncu["scr_del_mode"]
    .value_counts(dropna=False)
)

print("\n" + "=" * 80)
print("MSNCU ELIGIBILITY VS MASTER")
print("=" * 80)

eligible = get_msncu_df()
master = get_msncu_master_df()

print("Eligibility Rows       :", len(eligible))
print("Eligibility Babies     :", eligible["scr_babyid"].nunique())

print()

print("Master Rows            :", len(master))
print("Master Babies          :", master["dmf_babyid"].nunique())


print("\n" + "=" * 80)
print("PNC ELIGIBILITY VS MASTER")
print("=" * 80)

eligible = get_pnc_df()
master = get_pnc_master_df()

print("Eligibility Rows       :", len(eligible))
print("Eligibility Babies     :", eligible["scr_babyid"].nunique())

print()

print("Master Rows            :", len(master))
print("Master Babies          :", master["dmf_babyid"].nunique())

print()

print("Delivery Mode")
print(
    master["scr_del_mode"]
    .value_counts(dropna=False)
)


print("\n" + "=" * 80)
print("MISSING PNC BABY")
print("=" * 80)

eligible_ids = set(
    get_pnc_df()["scr_babyid"].dropna().astype(str)
)

master_ids = set(
    get_pnc_master_df()["dmf_babyid"].dropna().astype(str)
)

missing = eligible_ids - master_ids

print("Missing Baby IDs")
print(missing)

print()

print(
    get_pnc_df()[
        get_pnc_df()["scr_babyid"].astype(str).isin(missing)
    ][
        [
            "scr_babyid",
            "recordid",
            "scr_research_id",
            "scr_pob",
            "scr_sncu_sick"
        ]
    ]
)

print("\n" + "=" * 80)
print("TRACE BABY : E14060152")
print("=" * 80)

baby = "E14060152"

print("\nELIGIBILITY")
print(
    get_eligibility_df()[
        get_eligibility_df()["scr_babyid"] == baby
    ][
        [
            "scr_babyid",
            "recordid",
            "scr_research_id",
            "scr_pob",
            "scr_sncu_sick",
            "scr_mconst_adm",
            "scr_mconst",
            "scr_bw_ga_stable",
        ]
    ]
)

print("\nMOTHER")
print(
    get_mother_df()[
        get_mother_df()["enr_babyid"] == baby
    ]
)

print("\nDAILY")
print(
    get_daily_df()[
        get_daily_df()["dmf_babyid"] == baby
    ]
)

print("\nMASTER")
print(
    get_master_df()[
        get_master_df()["scr_babyid"] == baby
    ][
        [
            "scr_babyid",
            "enr_babyid",
            "dmf_babyid",
        ]
    ]
)

print(get_msncu_nvd_df()[["scr_babyid", "dmf_babyid"]].head(10))


print("\n" + "=" * 80)
print("INBORN OVERVIEW CHECK")
print("=" * 80)

print("Eligibility Babies :", get_inborn_count())

print(
    "Master Babies      :",
    get_master_df()[
        get_master_df()["scr_pob"] == 11
    ]["dmf_babyid"].nunique()
)

print(
    "MSNCU + PNC Babies :",
    get_msncu_nvd_count()
    + get_msncu_csection_count()
    + get_pnc_nvd_count()
    + get_pnc_csection_count()
)


print("\n" + "=" * 80)
print("BABIES WITH MULTIPLE DELIVERY MODES")
print("=" * 80)

df = get_master_df()

delivery = (
    df.groupby("dmf_babyid")["scr_del_mode"]
      .nunique()
)

problem = delivery[delivery > 1]

print("Babies :", len(problem))

print(problem.head(20))


print("\n" + "=" * 80)
print("BABIES PRESENT IN BOTH MSNCU AND PNC")
print("=" * 80)

msncu = set(get_msncu_master_df()["dmf_babyid"].dropna())
pnc = set(get_pnc_master_df()["dmf_babyid"].dropna())

both = msncu & pnc

print("MSNCU Babies :", len(msncu))
print("PNC Babies   :", len(pnc))
print("Both         :", len(both))

print(list(sorted(both))[:20])


print("\nMSNCU Place of Birth")

print(
    get_msncu_master_df()["scr_pob"]
    .value_counts(dropna=False)
)

print("\nPNC Place of Birth")

print(
    get_pnc_master_df()["scr_pob"]
    .value_counts(dropna=False)
)

print("\n" + "=" * 80)
print("INBORN MASTER COVERAGE")
print("=" * 80)

eligible = set(
    get_inborn_df()["scr_babyid"].dropna().astype(str)
)

master = set(
    get_master_df()[
        get_master_df()["scr_pob"] == 11
    ]["dmf_babyid"].dropna().astype(str)
)

print("Eligible Babies :", len(eligible))
print("Master Babies   :", len(master))
print("Missing in Master:", len(eligible - master))

print("\nFirst 20 Missing Babies:")
print(sorted(list(eligible - master))[:20])

print("\n" + "=" * 80)
print("INBORN BABIES WITH MULTIPLE DELIVERY MODES")
print("=" * 80)

df = get_master_df()
df = df[df["scr_pob"] == 11]

problem = (
    df.groupby("dmf_babyid")["scr_del_mode"]
      .nunique()
)

problem = problem[problem > 1]

print(problem)
print("Count:", len(problem))


print("\n" + "=" * 80)
print("INBORN DELIVERY AUDIT")
print("=" * 80)

df = get_master_df()
df = df[df["scr_pob"] == 11]

# One row per baby
baby = (
    df.groupby("dmf_babyid")
      .agg(
          delivery_modes=("scr_del_mode", lambda x: sorted(set(x.dropna()))),
          n_modes=("scr_del_mode", "nunique"),
          records=("scr_del_mode", "count"),
      )
      .reset_index()
)

print("Unique babies:", len(baby))
print()

print("Distribution of delivery mode counts")
print(baby["n_modes"].value_counts())

print()

print("Babies with >1 delivery mode")
print(
    baby[baby["n_modes"] > 1]
)

print("\n" + "=" * 80)
print("OUTBORN PAGE VALIDATION")
print("=" * 80)

print(f"Total Outborn            : {get_outborn_total_cases()}")

print()

print(f"NVD Cases                : {get_outborn_nvd_count()}")
print(f"C-Section Cases          : {get_outborn_csection_count()}")

print()

print(f"Overall Avg KMC          : {get_outborn_avg_kmc()}")
print(f"NVD Avg KMC              : {get_outborn_nvd_avg_kmc()}")
print(f"C-Section Avg KMC        : {get_outborn_csection_avg_kmc()}")

print()

print(f"NVD SSC <2H              : {get_outborn_nvd_ssc_under_2h_count()}")
print(f"C-Section SSC <2H        : {get_outborn_csection_ssc_under_2h_count()}")

print()

print(f"NVD BF                  : {get_outborn_nvd_bf_count()}")
print(f"C-Section BF            : {get_outborn_csection_bf_count()}")

print()

print(f"NVD Attachment          : {get_outborn_nvd_attachment_hours()}")
print(f"C-Section Attachment    : {get_outborn_csection_attachment_hours()}")

print("=" * 80)
print("MSNCU DELIVERY DEBUG")
print("=" * 80)

print("Master Babies :", get_msncu_master_df()["dmf_babyid"].nunique())
print("NVD Babies    :", get_msncu_nvd_df()["dmf_babyid"].nunique())
print("CS Babies     :", get_msncu_csection_df()["dmf_babyid"].nunique())

print()

print(get_msncu_master_df()["scr_pob"].value_counts(dropna=False))


print("\n" + "=" * 80)
print("PNC COVERAGE VALIDATION")
print("=" * 80)

print(f"PNC NVD Total          : {get_pnc_nvd_count()}")
print(f"PNC NVD Achieved       : {get_pnc_nvd_achieved_count()}")
print(f"PNC NVD Coverage       : {get_pnc_nvd_coverage()}")

print()

print(f"PNC C-Section Total    : {get_pnc_csection_count()}")
print(f"PNC C-Section Achieved : {get_pnc_csection_achieved_count()}")
print(f"PNC C-Section Coverage : {get_pnc_csection_coverage()}")

#================================================================================
#PNC COVERAGE VALIDATION
#================================================================================
print("\n" + "=" * 80)
print("PNC KMC >= 480 CHECK")
print("=" * 80)

df = get_pnc_master_df()

print(
    df[
        df["dmf_kmc_dur"] >= 480
    ][
        [
            "dmf_babyid",
            "dmf_kmc_dur",
            "scr_del_mode",
        ]
    ].head(20)
)

print()

print(
    "Count:",
    (
        df["dmf_kmc_dur"] >= 480
    ).sum()
)

print("\n" + "=" * 80)
print("PROGRAM CRITERIA DEBUG")
print("=" * 80)

df = get_master_df().copy()

print("Master rows:", len(df))

print()

print("SSC Recommended")
print(df["enr_ssc_rec"].value_counts(dropna=False))

df1 = df[df["enr_ssc_rec"] == 11]

print("\nAfter enr_ssc_rec == 11")
print(len(df1))

birth_dt = pd.to_datetime(
    df1["scr_dob"].astype(str) + " " + df1["scr_tob"].astype(str),
    errors="coerce"
)

ssc_dt = pd.to_datetime(
    df1["enr_ssc_init_dt"].astype(str) + " " + df1["enr_ssc_init_tm"].astype(str),
    errors="coerce"
)

df1["ssc_hours"] = (
    ssc_dt - birth_dt
).dt.total_seconds() / 3600

print("\nSSC Hours Summary")
print(df1["ssc_hours"].describe())

print()

print("SSC <=2 hrs")
print((df1["ssc_hours"] <= 2).sum())

df2 = df1[df1["ssc_hours"] <= 2]

print()

print("After SSC filter")
print(len(df2))

print()

print("KMC >=480")
print((df2["dmf_kmc_dur"] >= 480).sum())

print("\n" + "=" * 80)
print("PROGRAM CRITERIA BREAKDOWN")
print("=" * 80)

df = get_program_criteria_df()

print("scr_sncu_sick")
print(df["scr_sncu_sick"].value_counts(dropna=False))

print()

print("scr_del_mode")
print(df["scr_del_mode"].value_counts(dropna=False))

print()

print("Place of Birth")
print(df["scr_pob"].value_counts(dropna=False))