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