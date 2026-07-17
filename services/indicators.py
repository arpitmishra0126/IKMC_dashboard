from services.loader import load_all_data
from services.config import FIELD_MAP
import pandas as pd
import streamlit as st

def get_eligibility_df():
    data = load_all_data()
    return data["eligibility"]


# ==================================================
# BASE DATASETS - DASHBOARD MEASURES
# ==================================================

def get_prescreened_df():

    return get_eligibility_df().copy()


def get_alive_df():

    df = get_prescreened_df()

    return df[
        df["scr_status_baby"] == 11
    ]


def get_preterm_lbw_df():

    df = get_alive_df().copy()

    return df[
        (
            (df["scr_birthweight"] < 2500)
            |
            (df["scr_inf_ga_weeks"] < 37)
        )
    ]


def get_valid_admission_df():

    df = get_preterm_lbw_df().copy()

    return df[
        (
            (df["scr_pob"] == 11)
        )
        |
        (
            (df["scr_pob"].isin([12, 13, 14]))
            &
            (df["scr_baby_reach_24hrs"] == 11)
        )
    ]


def get_eligible_df():

    df = get_valid_admission_df().copy()

    return df[
        df["scr_mconst_adm"] == 11
    ]


def get_consented_df():

    df = get_eligible_df().copy()

    return df[
        df["scr_mconst"] == 11
    ]

def get_enrolled_df():

    df = get_consented_df().copy()

    return df[
        df["scr_bw_ga_stable"] == 12
    ]

def get_total_enrolled():

    return len(
        get_enrolled_df()
    )

# ==================================================
# TOP KPI CARDS
# ==================================================

def get_total_screening_records():

    return len(get_prescreened_df())


def get_total_alive_babies():

    return len(get_alive_df())


def get_total_screened():

    return len(get_preterm_lbw_df())


def get_total_eligible():

    return len(get_eligible_df())


def get_total_consented():

    return len(get_consented_df())


# ==================================================
# COHORT COUNTS
# ==================================================

def get_inborn_count():
    df = get_inborn_df()
    return df["scr_babyid"].nunique()

def get_outborn_count():
    df = get_outborn_df()
    return df["scr_babyid"].nunique()


# ==================================================
# SNCU COUNTS
# ==================================================

def get_msncu_count():

    df = get_eligible_df()

    return len(
        df[
            df["scr_sncu_sick"] == 11
        ]
    )


def get_pnc_count():

    df = get_eligible_df()

    return len(
        df[
            df["scr_sncu_sick"] == 12
        ]
    )


def get_inborn_df():
    df = get_eligibility_df()
    return df[df["scr_pob"] == 11]


# def get_outborn_df():
#     df = get_eligibility_df()
#
#     return df[
#         df["scr_pob"] == 12
#     ]


# ==================================================
# SNCU DATASETS
# ==================================================

def get_msncu_df():

    df = get_eligibility_df()

    return df[df["scr_sncu_sick"] == 11]


def get_pnc_df():

    df = get_eligibility_df()
    return df[df["scr_sncu_sick"] == 12]


# ==================================================
# MSNCU COUNTS
# ==================================================

def get_msncu_total_cases():
    return get_msncu_master_df()["dmf_babyid"].nunique()


def get_msncu_nvd_count():
    df = get_msncu_nvd_df()
    return df["dmf_babyid"].nunique()


def get_msncu_csection_count():
    df = get_msncu_csection_df()
    return df["dmf_babyid"].nunique()


# ==================================================
# PNC COUNTS
# ==================================================

def get_pnc_total_cases():
    return get_pnc_master_df()["dmf_babyid"].nunique()


def get_pnc_nvd_count():
    df = get_pnc_nvd_df()
    return df["dmf_babyid"].nunique()


def get_pnc_csection_count():
    df = get_pnc_csection_df()
    return df["dmf_babyid"].nunique()

# ==================================================
# SSC INDICATORS
# ==================================================

def get_mother_df():
    data = load_all_data()
    return data["mother"]


def get_total_ssc_received():
    df = get_mother_df()

    return len(
        df[
            df["enr_ssc_rec"] == 11
        ]
    )


def get_total_ssc_not_received():
    df = get_mother_df()

    return len(
        df[
            df["enr_ssc_rec"] == 12
        ]
    )


def get_ssc_percentage():
    df = get_mother_df()

    total = len(df)

    if total == 0:
        return 0

    received = len(
        df[
            df["enr_ssc_rec"] == 11
        ]
    )

    return round(
        (received / total) * 100,
        1
    )

# ==================================================
# KMC INDICATORS
# ==================================================

def get_daily_df():
    data = load_all_data()
    return data["daily"]
    
def get_avg_kmc_minutes():
    df = get_daily_df()

    return round(
        df["dmf_kmc_dur"].mean(),
        1
    )


def get_avg_kmc_hours():

    df = get_daily_df()

    avg_minutes = df["dmf_kmc_dur"].mean()

    if pd.isna(avg_minutes):
        return 0

    return round(avg_minutes / 60, 1)

# ==================================================
# MASTER DATASET
# ==================================================

def get_master_df():

    data = load_all_data()

    eligibility = data["eligibility"]
    mother = data["mother"]
    daily = data["daily"]

    master = eligibility.merge(
        mother,
        left_on=FIELD_MAP["eligibility_babyid"],
        right_on=FIELD_MAP["mother_babyid"],
        how="left"
    )

    master = master.merge(
        daily,
        left_on=FIELD_MAP["eligibility_babyid"],
        right_on=FIELD_MAP["daily_babyid"],
        how="left"
    )

    return master


def test_master_df():

    df = get_master_df()

    print("ROWS:", len(df))
    print("COLUMNS:", len(df.columns))

    print(df.head())


# ==================================================
# ENROLLMENT MASTER DATASET
# ==================================================

def get_enrollment_master_df():

    data = load_all_data()

    eligibility = data["eligibility"]
    mother = data["mother"]

    enrollment = eligibility.merge(
        mother,
        left_on=FIELD_MAP["eligibility_babyid"],
        right_on=FIELD_MAP["mother_babyid"],
        how="left"
    )

    return enrollment

# ==================================================
# FILTERED MASTER DATASETS
# ==================================================

def get_msncu_master_df():
    df = get_master_df()
    return df[(df["scr_pob"] == 11)&(df["scr_sncu_sick"] == 11)]

def get_pnc_master_df():
    df = get_master_df()
    return df[(df["scr_pob"] == 11)&(df["scr_sncu_sick"] == 12)]


def get_msncu_nvd_df():

    df = get_msncu_master_df()

    return df[df[FIELD_MAP["delivery_mode"]].isin([11, 12])]


def get_msncu_csection_df():

    df = get_msncu_master_df()

    return df[
        df[FIELD_MAP["delivery_mode"]] == 13
    ]


def get_pnc_nvd_df():

    df = get_pnc_master_df()

    return df[ df[FIELD_MAP["delivery_mode"]].isin([11, 12])]


def get_pnc_csection_df():

    df = get_pnc_master_df()

    return df[
        df[FIELD_MAP["delivery_mode"]] == 13
    ]


# ==================================================
# ENROLLMENT FILTERED DATASETS
# ==================================================

def get_msncu_enrollment_df():

    df = get_enrollment_master_df()

    return df[
        df[FIELD_MAP["sncu_type"]] == 11
    ]


def get_pnc_enrollment_df():

    df = get_enrollment_master_df()

    return df[
        df[FIELD_MAP["sncu_type"]] == 12
    ]


def get_msncu_nvd_enrollment_df():

    df = get_msncu_enrollment_df()

    return df[
        df[FIELD_MAP["delivery_mode"]] == 11
    ]


def get_msncu_csection_enrollment_df():

    df = get_msncu_enrollment_df()

    return df[
        df[FIELD_MAP["delivery_mode"]] == 13
    ]


def get_pnc_nvd_enrollment_df():

    df = get_pnc_enrollment_df()

    return df[
        df[FIELD_MAP["delivery_mode"]] == 11
    ]


def get_pnc_csection_enrollment_df():

    df = get_pnc_enrollment_df()

    return df[
        df[FIELD_MAP["delivery_mode"]] == 13
    ]


# ==================================================
# AVG KMC
# ==================================================

def get_msncu_avg_kmc():

    df = get_msncu_master_df()

    avg_minutes = df["dmf_kmc_dur"].mean()

    if pd.isna(avg_minutes):
        return 0

    return round(avg_minutes / 60, 1)


def get_pnc_avg_kmc():

    df = get_pnc_master_df()

    avg_minutes = df["dmf_kmc_dur"].mean()

    if pd.isna(avg_minutes):
        return 0

    return round(avg_minutes / 60, 1)


# ==================================================
# OUTBORN AVG KMC
# ==================================================

def get_outborn_avg_kmc():

    df = get_outborn_df()

    avg_minutes = df["dmf_kmc_dur"].mean()

    if pd.isna(avg_minutes):
        return 0

    return round(avg_minutes / 60, 1)


def get_outborn_nvd_avg_kmc():

    df = get_outborn_nvd_df()

    avg_minutes = df["dmf_kmc_dur"].mean()

    if pd.isna(avg_minutes):
        return 0

    return round(avg_minutes / 60, 1)


def get_outborn_csection_avg_kmc():

    df = get_outborn_csection_df()

    avg_minutes = df["dmf_kmc_dur"].mean()

    if pd.isna(avg_minutes):
        return 0

    return round(avg_minutes / 60, 1)


# ==================================================
# DELIVERY MODE AVG KMC
# ==================================================

def get_msncu_nvd_avg_kmc():

    df = get_msncu_nvd_df()

    avg_minutes = df["dmf_kmc_dur"].mean()

    if pd.isna(avg_minutes):
        return 0

    return round(avg_minutes / 60, 1)


def get_msncu_csection_avg_kmc():

    df = get_msncu_csection_df()

    avg_minutes = df["dmf_kmc_dur"].mean()

    if pd.isna(avg_minutes):
        return 0

    return round(avg_minutes / 60, 1)


def get_pnc_nvd_avg_kmc():

    df = get_pnc_nvd_df()

    avg_minutes = df["dmf_kmc_dur"].mean()

    if pd.isna(avg_minutes):
        return 0

    return round(avg_minutes / 60, 1)


def get_pnc_csection_avg_kmc():

    df = get_pnc_csection_df()

    avg_minutes = df["dmf_kmc_dur"].mean()

    if pd.isna(avg_minutes):
        return 0

    return round(avg_minutes / 60, 1)



# ==================================================
# OVERVIEW AVG KMC
# ==================================================

def get_inborn_nvd_avg_kmc():

    df = pd.concat(
        [
            get_msncu_nvd_df(),
            get_pnc_nvd_df()
        ],
        ignore_index=True
    )

    avg = df["dmf_kmc_dur"].mean()

    if pd.isna(avg):
        return 0

    return round(avg / 60, 1)


def get_inborn_csection_avg_kmc():

    df = pd.concat(
        [
            get_msncu_csection_df(),
            get_pnc_csection_df()
        ],
        ignore_index=True
    )

    avg = df["dmf_kmc_dur"].mean()

    if pd.isna(avg):
        return 0

    return round(avg / 60, 1)


# ==================================================
# EXCLUSIVE BREASTFEEDING
# ==================================================

def get_msncu_nvd_bf_count():

    df = get_msncu_nvd_enrollment_df()

    return len(
        df[
            df["enr_bf_bentfed"] == 11
        ]
    )


def get_msncu_csection_bf_count():

    df = get_msncu_csection_enrollment_df()

    return len(
        df[
            df["enr_bf_bentfed"] == 11
        ]
    )


def get_pnc_nvd_bf_count():

    df = get_pnc_nvd_enrollment_df()

    return len(
        df[
            df["enr_bf_bentfed"] == 11
        ]
    )


def get_pnc_csection_bf_count():

    df = get_pnc_csection_enrollment_df()

    return len(
        df[
            df["enr_bf_bentfed"] == 11
        ]
    )

# ==================================================
# SSC RECEIVED
# ==================================================

def get_msncu_nvd_ssc_count():

    df = get_msncu_nvd_enrollment_df()

    return len(
        df[
            df["enr_ssc_rec"] == 11
        ]
    )


def get_msncu_csection_ssc_count():

    df = get_msncu_csection_enrollment_df()

    return len(
        df[
            df["enr_ssc_rec"] == 11
        ]
    )


def get_pnc_nvd_ssc_count():

    df = get_pnc_nvd_enrollment_df()

    return len(
        df[
            df["enr_ssc_rec"] == 11
        ]
    )


def get_pnc_csection_ssc_count():

    df = get_pnc_csection_enrollment_df()

    return len(
        df[
            df["enr_ssc_rec"] == 11
        ]
    )

# ==================================================
# ATTACHMENT AGE
# ==================================================

def get_msncu_nvd_attachment_hours():

    df = get_msncu_nvd_enrollment_df().copy()

    df = df[
        df["enr_bf_bentfed_hw_dt"].notna()
    ]

    if len(df) == 0:
        return 0

    birth_dt = pd.to_datetime(df["scr_dob"].astype(str)+ " "+ df["scr_tob"].astype(str), errors="coerce")
    attach_dt = pd.to_datetime(df["enr_bf_bentfed_hw_dt"].astype(str)+ " "+ df["enr_bf_bentfed_hw_tm"].astype(str),errors="coerce")

    hours = (attach_dt - birth_dt).dt.total_seconds() / 3600
    hours = hours.dropna()

    return round(hours.mean(), 1)


def get_msncu_csection_attachment_hours():

    df = get_msncu_csection_enrollment_df().copy()

    df = df[
        df["enr_bf_bentfed_hw_dt"].notna()
    ]

    if len(df) == 0:
        return 0

   
    birth_dt = pd.to_datetime(df["scr_dob"].astype(str)+ " "+ df["scr_tob"].astype(str), errors="coerce")
    attach_dt = pd.to_datetime(df["enr_bf_bentfed_hw_dt"].astype(str)+ " "+ df["enr_bf_bentfed_hw_tm"].astype(str),errors="coerce")


    hours = (attach_dt - birth_dt).dt.total_seconds() / 3600
    hours = hours.dropna()

    return round(hours.mean(), 1)


def get_pnc_nvd_attachment_hours():

    df = get_pnc_nvd_enrollment_df().copy()

    df = df[
        df["enr_bf_bentfed_hw_dt"].notna()
    ]

    if len(df) == 0:
        return 0

    
    birth_dt = pd.to_datetime(df["scr_dob"].astype(str)+ " "+ df["scr_tob"].astype(str), errors="coerce")
    attach_dt = pd.to_datetime(df["enr_bf_bentfed_hw_dt"].astype(str)+ " "+ df["enr_bf_bentfed_hw_tm"].astype(str),errors="coerce")


    hours = (attach_dt - birth_dt).dt.total_seconds() / 3600
    hours = hours.dropna()

    return round(hours.mean(), 1)


def get_pnc_csection_attachment_hours():

    df = get_pnc_csection_enrollment_df().copy()

    df = df[
        df["enr_bf_bentfed_hw_dt"].notna()
    ]

    if len(df) == 0:
        return 0

  
    birth_dt = pd.to_datetime(df["scr_dob"].astype(str)+ " "+ df["scr_tob"].astype(str), errors="coerce")
    attach_dt = pd.to_datetime(df["enr_bf_bentfed_hw_dt"].astype(str)+ " "+ df["enr_bf_bentfed_hw_tm"].astype(str),errors="coerce")


    hours = (attach_dt - birth_dt).dt.total_seconds() / 3600
    hours = hours.dropna()

    return round(hours.mean(), 1)



# ==================================================
# OVERVIEW ATTACHMENT AGE
# ==================================================

def get_inborn_nvd_attachment_hours():

    values = [
        get_msncu_nvd_attachment_hours(),
        get_pnc_nvd_attachment_hours()
    ]

    values = [v for v in values if v > 0]

    if len(values) == 0:
        return 0

    return round(sum(values) / len(values), 1)


def get_inborn_csection_attachment_hours():

    values = [
        get_msncu_csection_attachment_hours(),
        get_pnc_csection_attachment_hours()
    ]

    values = [v for v in values if v > 0]

    if len(values) == 0:
        return 0

    return round(sum(values) / len(values), 1)


# ==================================================
# SSC WITHIN 2 HOURS
# ==================================================

def get_ssc_under_2h_df():

    df = get_enrollment_master_df().copy()

    df = df[
        df["enr_ssc_rec"] == 11
    ]

    birth_dt = pd.to_datetime(
        df["scr_dob"].astype(str)
        + " "
        + df["scr_tob"].astype(str)
    )

    ssc_dt = pd.to_datetime(
        df["enr_ssc_init_dt"].astype(str)
        + " "
        + df["enr_ssc_init_tm"].astype(str)
    )

    df["ssc_hours_diff"] = (
        ssc_dt - birth_dt
    ).dt.total_seconds() / 3600

    return df[
        df["ssc_hours_diff"] <= 2
    ]


# ==================================================
# MSNCU SSC <2H
# ==================================================

def get_msncu_nvd_ssc_under_2h_count():

    df = get_ssc_under_2h_df()

    df = df[
        (df["scr_sncu_sick"] == 11)
        &
        (df["scr_del_mode"].isin([11, 12]))
    ]

    return len(df)


def get_msncu_csection_ssc_under_2h_count():

    df = get_ssc_under_2h_df()

    df = df[
        (df["scr_sncu_sick"] == 11)
        &
        (df["scr_del_mode"] == 13)
    ]

    return len(df)


# ==================================================
# OUTBORN SSC <2H
# ==================================================

def get_outborn_nvd_ssc_under_2h_count():
    df = get_ssc_under_2h_df()
    df = df[(df["scr_pob"].isin([12, 13, 14]))&(df["scr_del_mode"].isin([11, 12]))]
    return len(df)

def get_outborn_csection_ssc_under_2h_count():
    df = get_ssc_under_2h_df()
    df = df[(df["scr_pob"].isin([12, 13, 14]))&(df["scr_del_mode"] == 13)]
    return len(df)

# ==================================================
# PNC SSC <2H
# ==================================================

def get_pnc_nvd_ssc_under_2h_count():

    df = get_ssc_under_2h_df()

    df = df[
        (df["scr_sncu_sick"] == 12)
        &
        (df["scr_del_mode"].isin([11, 12]))
    ]

    return len(df)


def get_pnc_csection_ssc_under_2h_count():

    df = get_ssc_under_2h_df()

    df = df[
        (df["scr_sncu_sick"] == 12)
        &
        (df["scr_del_mode"] == 13)
    ]

    return len(df)

# ==================================================
# PROGRAM CRITERIA MET
# SSC <2H + KMC >=8H
# ==================================================

def get_program_criteria_df():

    df = get_master_df().copy()

    df = df[
        df["enr_ssc_rec"] == 11
    ]

    birth_dt = pd.to_datetime(
        df["scr_dob"].astype(str)
        + " "
        + df["scr_tob"].astype(str)
    )

    ssc_dt = pd.to_datetime(
        df["enr_ssc_init_dt"].astype(str)
        + " "
        + df["enr_ssc_init_tm"].astype(str)
    )

    df["ssc_hours"] = (
        ssc_dt - birth_dt
    ).dt.total_seconds() / 3600

    df = df[
        df["ssc_hours"] <= 2
    ]

    df = df[
        df["dmf_kmc_dur"] >= 480
    ]

    return df


def get_msncu_nvd_achieved_count():
    df = get_program_criteria_df()
    return (df[(df["scr_sncu_sick"] == 11)&(df["scr_del_mode"].isin([11, 12]))]["dmf_babyid"].nunique())


def get_msncu_csection_achieved_count():

    df = get_program_criteria_df()

    return (
        df[
            (df["scr_sncu_sick"] == 11)
            &
            (df["scr_del_mode"] == 13)
        ]["dmf_babyid"]
        .nunique()
    )


def get_pnc_nvd_achieved_count():

    df = get_program_criteria_df()

    return (df[ (df["scr_sncu_sick"] == 12)& (df["scr_del_mode"].isin([11, 12])) ]["dmf_babyid"].nunique())


def get_pnc_csection_achieved_count():

    df = get_program_criteria_df()

    return (
        df[
            (df["scr_sncu_sick"] == 12)
            &
            (df["scr_del_mode"] == 13)
        ]["dmf_babyid"]
        .nunique()
    )

def get_msncu_nvd_coverage():
    achieved = get_msncu_nvd_achieved_count()
    total = get_msncu_nvd_count()
    if total == 0:
        return 0
    return round((achieved / total) * 100,1)

def get_msncu_csection_coverage():
    achieved = get_msncu_csection_achieved_count()
    total = get_msncu_csection_count()
    if total == 0:
        return 0
    return round((achieved / total) * 100,1)

def get_pnc_nvd_coverage():
    achieved = get_pnc_nvd_achieved_count()
    total = get_pnc_nvd_count()
    if total == 0:
        return 0
    return round((achieved / total) * 100,1)

def get_pnc_csection_coverage():
    achieved = get_pnc_csection_achieved_count()
    total = get_pnc_csection_count()
    if total == 0:
        return 0
    return round((achieved / total) * 100,1)


# ==================================================
# OVERVIEW - INBORN COUNTS
# ==================================================

def get_inborn_nvd_count():
    return (
        get_msncu_nvd_count()
        + get_pnc_nvd_count()
    )


def get_inborn_csection_count():
    return (
        get_msncu_csection_count()
        + get_pnc_csection_count()
    )


def get_inborn_nvd_ssc_under_2h_count():
    return (
        get_msncu_nvd_ssc_under_2h_count()
        + get_pnc_nvd_ssc_under_2h_count()
    )


def get_inborn_csection_ssc_under_2h_count():
    return (
        get_msncu_csection_ssc_under_2h_count()
        + get_pnc_csection_ssc_under_2h_count()
    )


def get_inborn_nvd_bf_count():
    return (
        get_msncu_nvd_bf_count()
        + get_pnc_nvd_bf_count()
    )


def get_inborn_csection_bf_count():
    return (
        get_msncu_csection_bf_count()
        + get_pnc_csection_bf_count()
    )


# ==================================================
# OUTBORN BASE DF
# ==================================================

def get_outborn_df():

    df = get_master_df().copy()

    df = df[
        df["scr_pob"].isin([12, 13, 14])
    ]

    return df


# ==================================================
# OUTBORN COUNTS
# ==================================================

def get_outborn_total_cases():

    df = get_outborn_df()

    return df["dmf_babyid"].nunique()


def get_outborn_nvd_count():

    return (
        get_outborn_nvd_df()["dmf_babyid"]
        .nunique()
    )


def get_outborn_csection_count():

    return (
        get_outborn_csection_df()["dmf_babyid"]
        .nunique()
    )

# ==================================================
# OUTBORN DELIVERY MODE DFS
# ==================================================

    df = df[
        df["scr_del_mode"] == 13
    ]

    return df["dmf_babyid"].nunique()

# ==================================================
# OUTBORN DELIVERY MODE DFS
# ==================================================

def get_outborn_nvd_df():
    df = get_outborn_df()
    return df[df["scr_del_mode"].isin([11, 12])]

def get_outborn_csection_df():
    df = get_outborn_df()
    return df[df["scr_del_mode"] == 13]

# ==================================================
# OUTBORN EXCLUSIVE BREASTFEEDING
# ==================================================

def get_outborn_nvd_bf_count():

    df = get_outborn_nvd_df()

    return (
        df[
            df["enr_bf_bentfed"] == 11
        ]["dmf_babyid"]
        .nunique()
    )


def get_outborn_csection_bf_count():

    df = get_outborn_csection_df()

    return (
        df[
            df["enr_bf_bentfed"] == 11
        ]["dmf_babyid"]
        .nunique()
    )

# ==================================================
# OUTBORN ATTACHMENT AGE
# ==================================================

def get_outborn_nvd_attachment_hours():

    df = get_outborn_nvd_df().copy()

    df = df[
        df["enr_bf_bentfed_hw_dt"].notna()
    ]

    if len(df) == 0:
        return 0

    birth_dt = pd.to_datetime(
        df["scr_dob"].astype(str)
        + " "
        + df["scr_tob"].astype(str),
        errors="coerce"
    )

    attach_dt = pd.to_datetime(
        df["enr_bf_bentfed_hw_dt"].astype(str)
        + " "
        + df["enr_bf_bentfed_hw_tm"].astype(str),
        errors="coerce"
    )

    hours = (
        attach_dt - birth_dt
    ).dt.total_seconds() / 3600

    hours = hours.dropna()

    if len(hours) == 0:
        return 0

    return round(hours.mean(), 1)


def get_outborn_csection_attachment_hours():

    df = get_outborn_csection_df().copy()

    df = df[
        df["enr_bf_bentfed_hw_dt"].notna()
    ]

    if len(df) == 0:
        return 0

    birth_dt = pd.to_datetime(
        df["scr_dob"].astype(str)
        + " "
        + df["scr_tob"].astype(str),
        errors="coerce"
    )

    attach_dt = pd.to_datetime(
        df["enr_bf_bentfed_hw_dt"].astype(str)
        + " "
        + df["enr_bf_bentfed_hw_tm"].astype(str),
        errors="coerce"
    )

    hours = (
        attach_dt - birth_dt
    ).dt.total_seconds() / 3600

    hours = hours.dropna()

    if len(hours) == 0:
        return 0

    return round(hours.mean(), 1)
# ==================================================
# OUTBORN PROGRAM ACHIEVEMENT
# SSC <2H + KMC >=8H
# ==================================================

def get_outborn_nvd_achieved_count():

    df = get_program_criteria_df()
    return (
            df[(df["scr_pob"].isin([12, 13, 14])) 
            &
            (df["scr_del_mode"].isin([11, 12]))]
            ["dmf_babyid"].nunique()
            )


def get_outborn_csection_achieved_count():

    df = get_program_criteria_df()
    return (
            df[(df["scr_pob"].isin([12, 13, 14]))
            &
            (df["scr_del_mode"] == 13)]
            ["dmf_babyid"].nunique()
            )

# ==================================================
# OUTBORN COVERAGE
# ==================================================

def get_outborn_nvd_coverage():

    achieved = get_outborn_nvd_achieved_count()
    total = get_outborn_nvd_count()

    if total == 0:
        return 0
    return round((achieved / total) * 100,1)

def get_outborn_csection_coverage():

    achieved = get_outborn_csection_achieved_count()
    total = get_outborn_csection_count()

    if total == 0:
        return 0
    return round((achieved / total) * 100,1)


# ==================================================
# DISCHARGE DATASET
# ==================================================

def get_discharge_df():

    data = load_all_data()

    return data["discharge"]


# ==================================================
# DISCHARGE DATASETS
# ==================================================

def get_discharge_master_df():

    discharge = get_discharge_df()

    eligibility = get_eligibility_df()

    return discharge.merge(
        eligibility,
        left_on="dis_babyid",
        right_on="scr_babyid",
        how="left"
    )

def get_inborn_discharge_df():

    df = get_discharge_master_df()

    return df[df["scr_pob"] == 11]


def get_outborn_discharge_df():

    df = get_discharge_master_df()

    return df[
        df["scr_pob"].isin([12, 13, 14])
    ]

def get_inborn_nvd_discharge_df():

    df = get_inborn_discharge_df()

    return df[df["scr_del_mode"].isin([11, 12])]


def get_inborn_csection_discharge_df():

    df = get_inborn_discharge_df()

    return df[df["scr_del_mode"] == 13]


def get_outborn_nvd_discharge_df():

    df = get_outborn_discharge_df()

    return df[df["scr_del_mode"].isin([11, 12])]


def get_outborn_csection_discharge_df():

    df = get_outborn_discharge_df()

    return df[df["scr_del_mode"] == 13]


# ==================================================
# OVERALL DISCHARGE OUTCOMES
# ==================================================

def get_total_discharged():

    df = get_discharge_master_df()

    return (
        df[
            df["dis_inf_outcome"] == 11
        ]["dis_babyid"]
        .nunique()
    )


def get_total_referred():

    df = get_discharge_master_df()

    return (
        df[
            df["dis_inf_outcome"] == 14
        ]["dis_babyid"]
        .nunique()
    )


def get_total_lama():

    df = get_discharge_master_df()

    return (
        df[
            df["dis_inf_outcome"] == 12
        ]["dis_babyid"]
        .nunique()
    )


def get_total_death():

    df = get_discharge_master_df()

    return (
        df[
            df["dis_inf_outcome"] == 13
        ]["dis_babyid"]
        .nunique()
    )

# ==================================================
# INBORN NVD OUTCOMES
# ==================================================

def get_inborn_nvd_discharged():

    df = get_inborn_nvd_discharge_df()

    return (
        df[
            df["dis_inf_outcome"] == 11
        ]["dis_babyid"]
        .nunique()
    )

def get_inborn_nvd_referred():

    df = get_inborn_nvd_discharge_df()

    return (
        df[
            df["dis_inf_outcome"] == 14
        ]["dis_babyid"]
        .nunique()
    )

def get_inborn_nvd_lama():

    df = get_inborn_nvd_discharge_df()

    return (
        df[
            df["dis_inf_outcome"] == 12
        ]["dis_babyid"]
        .nunique()
    )

def get_inborn_nvd_death():

    df = get_inborn_nvd_discharge_df()

    return (
        df[
            df["dis_inf_outcome"] == 13
        ]["dis_babyid"]
        .nunique()
    )

# ==================================================
# INBORN C-SECTION OUTCOMES
# ==================================================

def get_inborn_csection_discharged():

    df = get_inborn_csection_discharge_df()

    return (
        df[
            df["dis_inf_outcome"] == 11
        ]["dis_babyid"]
        .nunique()
    )

def get_inborn_csection_referred():

    df = get_inborn_csection_discharge_df()

    return (
        df[
            df["dis_inf_outcome"] == 14
        ]["dis_babyid"]
        .nunique()
    )

def get_inborn_csection_lama():

    df = get_inborn_csection_discharge_df()

    return (
        df[
            df["dis_inf_outcome"] == 12
        ]["dis_babyid"]
        .nunique()
    )

def get_inborn_csection_death():

    df = get_inborn_csection_discharge_df()

    return (
        df[
            df["dis_inf_outcome"] == 13
        ]["dis_babyid"]
        .nunique()
    )

# ==================================================
# OUTBORN NVD OUTCOMES
# ==================================================

def get_outborn_nvd_discharged():

    df = get_outborn_nvd_discharge_df()

    return (
        df[
            df["dis_inf_outcome"] == 11
        ]["dis_babyid"]
        .nunique()
    )

def get_outborn_nvd_referred():

    df = get_outborn_nvd_discharge_df()

    return (
        df[
            df["dis_inf_outcome"] == 14
        ]["dis_babyid"]
        .nunique()
    )

def get_outborn_nvd_lama():

    df = get_outborn_nvd_discharge_df()

    return (
        df[
            df["dis_inf_outcome"] == 12
        ]["dis_babyid"]
        .nunique()
    )

def get_outborn_nvd_death():

    df = get_outborn_nvd_discharge_df()

    return (
        df[
            df["dis_inf_outcome"] == 13
        ]["dis_babyid"]
        .nunique()
    )

# ==================================================
# OUTBORN C-SECTION OUTCOMES
# ==================================================

def get_outborn_csection_discharged():

    df = get_outborn_csection_discharge_df()

    return (
        df[
            df["dis_inf_outcome"] == 11
        ]["dis_babyid"]
        .nunique()
    )

def get_outborn_csection_referred():

    df = get_outborn_csection_discharge_df()

    return (
        df[
            df["dis_inf_outcome"] == 14
        ]["dis_babyid"]
        .nunique()
    )

def get_outborn_csection_lama():

    df = get_outborn_csection_discharge_df()

    return (
        df[
            df["dis_inf_outcome"] == 12
        ]["dis_babyid"]
        .nunique()
    )

def get_outborn_csection_death():

    df = get_outborn_csection_discharge_df()

    return (
        df[
            df["dis_inf_outcome"] == 13
        ]["dis_babyid"]
        .nunique()
    )

# ==================================================
# STILL ADMITTED
# ==================================================

def get_total_still_admitted():

    df = get_enrollment_master_df()

    consented = (
        df[
            (df["scr_mconst"] == 11)
            &
            (df["scr_mconst_adm"] == 11)
        ]["scr_babyid"]
        .nunique()
    )

    discharged = (
        get_discharge_df()["dis_babyid"]
        .nunique()
    )

    return consented - discharged

# ==================================================
# DATA QUALITY
# ==================================================

def get_missing_babyid_count():

    df = get_eligibility_df()

    return (
        df["scr_babyid"]
        .isin(["null"])
        .sum()
    )

def get_duplicate_babyid_count():

    df = get_eligibility_df()

    ids = df[
        ~df["scr_babyid"].isin(["null"])
    ]["scr_babyid"]

    return (
        ids
        .duplicated()
        .sum()
    )

def get_duplicate_discharge_count():

    df = get_discharge_df()

    return (
        df["dis_babyid"]
        .duplicated()
        .sum()
    )

def get_missing_dailycare_count():

    screening = get_eligibility_df()

    screening_ids = set(
        screening[
            screening["scr_babyid"] != "null"
        ]["scr_babyid"]
        .dropna()
    )

    daily_ids = set(
        get_master_df()["dmf_babyid"]
        .dropna()
    )

    return len(screening_ids - daily_ids)

def get_missing_outcome_count():

    df = get_discharge_master_df()

    valid = [11, 12, 13, 14]

    return (
        ~df["dis_inf_outcome"]
        .isin(valid)
    ).sum()

def get_merge_mismatch_count():

    screening = get_eligibility_df()

    screening_ids = set(
        screening[
            screening["scr_babyid"] != "null"
        ]["scr_babyid"]
        .dropna()
    )

    master_ids = set(
        get_master_df()["scr_babyid"]
        .dropna()
    )

    return len(screening_ids - master_ids)


# ==================================================
# VALIDATION STATUS
# ==================================================

st.caption(
    "Quality indicators highlighting potential data completeness and integrity issues."
)

def get_validation_status():

    duplicate_discharge = get_duplicate_discharge_count()
    merge_mismatch = get_merge_mismatch_count()
    missing_daily = get_missing_dailycare_count()

    if (
        duplicate_discharge == 0
        and merge_mismatch == 0
        and missing_daily == 0
    ):
        return "🟢 Healthy"

    return "🟡 Review Required"

# ==================================================
# DATA QUALITY DATAFRAMES
# ==================================================

def get_missing_babyid_df():

    df = get_eligibility_df()

    return df[
        df["scr_babyid"] == "null"
    ][
        [
            "recordid",
            "scr_research_id",
            "scr_babyid",
            "site_id",
            "facility_id"
        ]
    ]

def get_duplicate_babyid_df():

    df = get_eligibility_df()

    df = df[
        df["scr_babyid"] != "null"
    ]

    dup_ids = df[
        df["scr_babyid"].duplicated(keep=False)
    ]["scr_babyid"].unique()

    return df[
        df["scr_babyid"].isin(dup_ids)
    ][
        [
            "scr_babyid",
            "recordid",
            "scr_research_id",
            "site_id",
            "facility_id"
        ]
    ]

def get_duplicate_discharge_df():

    df = get_discharge_master_df()

    dup_ids = df.loc[
        df["scr_babyid"].duplicated(keep=False),
        "scr_babyid"
    ].unique()

    result = df[
        df["scr_babyid"].isin(dup_ids)
    ].copy()

    result["Duplicate Records"] = (
        result.groupby("scr_babyid")["scr_babyid"]
        .transform("count")
    )

    return result[
        [
            "scr_babyid",
            "recordid_x",
            "dis_dof",
            "dis_inf_outcome",
            "scr_research_id",
            "site_id_y",
            "facility_id_y",
            "Duplicate Records",
        ]
    ].sort_values("scr_babyid")  

def get_missing_dailycare_df():

    screening = get_eligibility_df()

    screening_ids = set(
        screening[
            screening["scr_babyid"] != "null"
        ]["scr_babyid"]
        .dropna()
    )

    daily_ids = set(
        get_master_df()["dmf_babyid"]
        .dropna()
    )

    missing = screening_ids - daily_ids

    return screening[
        screening["scr_babyid"].isin(missing)
    ][[
        "recordid",
        "scr_research_id",
        "scr_babyid",
        "site_id",
        "facility_id"
    ]]

def get_merge_mismatch_df():

    screening = get_eligibility_df()

    screening_ids = set(
        screening[
            screening["scr_babyid"] != "null"
        ]["scr_babyid"]
        .dropna()
    )

    master_ids = set(
        get_master_df()["scr_babyid"]
        .dropna()
    )

    mismatch = screening_ids - master_ids

    return screening[
        screening["scr_babyid"].isin(mismatch)
    ][[
        "recordid",
        "scr_research_id",
        "scr_babyid",
        "site_id",
        "facility_id"
    ]]