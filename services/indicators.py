from services.loader import load_all_data
from services.config import FIELD_MAP
import pandas as pd

def get_eligibility_df():
    data = load_all_data()
    return data["eligibility"]


# ==================================================
# TOP KPI CARDS
# ==================================================

def get_total_screening_records():
    df = get_eligibility_df()
    return len(df)


def get_total_babies():
    df = get_eligibility_df()

    baby_col = FIELD_MAP["eligibility_babyid"]

    return df[baby_col].nunique()


# ==================================================
# COHORT COUNTS
# ==================================================

def get_inborn_count():
    df = get_eligibility_df()

    return len(
        df[
            df[FIELD_MAP["place_of_birth"]] == 11
        ]
    )


def get_outborn_count():
    df = get_eligibility_df()

    return len(
        df[
            df[FIELD_MAP["place_of_birth"]] == 12
        ]
    )


# ==================================================
# SNCU COUNTS
# ==================================================

def get_msncu_count():
    df = get_eligibility_df()

    return len(
        df[
            df[FIELD_MAP["sncu_type"]] == 11
        ]
    )


def get_pnc_count():
    df = get_eligibility_df()

    return len(
        df[
            df[FIELD_MAP["sncu_type"]] == 12
        ]
    )


def get_inborn_df():
    df = get_eligibility_df()

    return df[
        df[FIELD_MAP["place_of_birth"]] == 11
    ]


def get_outborn_df():
    df = get_eligibility_df()

    return df[
        df[FIELD_MAP["place_of_birth"]] == 12
    ]


# ==================================================
# SNCU DATASETS
# ==================================================

def get_msncu_df():
    df = get_eligibility_df()

    return df[
        df[FIELD_MAP["sncu_type"]] == 11
    ]


def get_pnc_df():
    df = get_eligibility_df()

    return df[
        df[FIELD_MAP["sncu_type"]] == 12
    ]


# ==================================================
# MSNCU COUNTS
# ==================================================

def get_msncu_total_cases():
    return len(get_msncu_df())


def get_msncu_nvd_count():
    df = get_msncu_df()

    return len(
        df[
            df[FIELD_MAP["delivery_mode"]] == 11
        ]
    )


def get_msncu_csection_count():
    df = get_msncu_df()

    return len(
        df[
            df[FIELD_MAP["delivery_mode"]] == 13
        ]
    )


# ==================================================
# PNC COUNTS
# ==================================================

def get_pnc_total_cases():
    return len(get_pnc_df())


def get_pnc_nvd_count():
    df = get_pnc_df()

    return len(
        df[
            df[FIELD_MAP["delivery_mode"]] == 11
        ]
    )


def get_pnc_csection_count():
    df = get_pnc_df()

    return len(
        df[
            df[FIELD_MAP["delivery_mode"]] == 13
        ]
    )

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

    return round(
        avg_minutes / 60,
        1
    )

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

    return df[
        df[FIELD_MAP["sncu_type"]] == 11
    ]


def get_pnc_master_df():

    df = get_master_df()

    return df[
        df[FIELD_MAP["sncu_type"]] == 12
    ]


def get_msncu_nvd_df():

    df = get_msncu_master_df()

    return df[
        df[FIELD_MAP["delivery_mode"]] == 11
    ]


def get_msncu_csection_df():

    df = get_msncu_master_df()

    return df[
        df[FIELD_MAP["delivery_mode"]] == 13
    ]


def get_pnc_nvd_df():

    df = get_pnc_master_df()

    return df[
        df[FIELD_MAP["delivery_mode"]] == 11
    ]


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
# DELIVERY MODE AVG KMC
# ==================================================

def get_msncu_nvd_avg_kmc():

    df = get_msncu_nvd_df()

    print("=" * 50)
    print("INSIDE get_msncu_nvd_avg_kmc")
    print("ROWS:", len(df))
    print("HAS dmf_kmc_dur:", "dmf_kmc_dur" in df.columns)

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

    birth_dt = pd.to_datetime(
        df["scr_dob"].astype(str)
        + " "
        + df["scr_tob"].astype(str)
    )

    attach_dt = pd.to_datetime(
        df["enr_bf_bentfed_hw_dt"].astype(str)
        + " "
        + df["enr_bf_bentfed_hw_tm"].astype(str)
    )

    hours = (
        attach_dt - birth_dt
    ).dt.total_seconds() / 3600

    return round(hours.mean(), 1)


def get_msncu_csection_attachment_hours():

    df = get_msncu_csection_enrollment_df().copy()

    df = df[
        df["enr_bf_bentfed_hw_dt"].notna()
    ]

    if len(df) == 0:
        return 0

    birth_dt = pd.to_datetime(
        df["scr_dob"].astype(str)
        + " "
        + df["scr_tob"].astype(str)
    )

    attach_dt = pd.to_datetime(
        df["enr_bf_bentfed_hw_dt"].astype(str)
        + " "
        + df["enr_bf_bentfed_hw_tm"].astype(str)
    )

    hours = (
        attach_dt - birth_dt
    ).dt.total_seconds() / 3600

    return round(hours.mean(), 1)


def get_pnc_nvd_attachment_hours():

    df = get_pnc_nvd_enrollment_df().copy()

    df = df[
        df["enr_bf_bentfed_hw_dt"].notna()
    ]

    if len(df) == 0:
        return 0

    birth_dt = pd.to_datetime(
        df["scr_dob"].astype(str)
        + " "
        + df["scr_tob"].astype(str)
    )

    attach_dt = pd.to_datetime(
        df["enr_bf_bentfed_hw_dt"].astype(str)
        + " "
        + df["enr_bf_bentfed_hw_tm"].astype(str)
    )

    hours = (
        attach_dt - birth_dt
    ).dt.total_seconds() / 3600

    return round(hours.mean(), 1)


def get_pnc_csection_attachment_hours():

    df = get_pnc_csection_enrollment_df().copy()

    df = df[
        df["enr_bf_bentfed_hw_dt"].notna()
    ]

    if len(df) == 0:
        return 0

    birth_dt = pd.to_datetime(
        df["scr_dob"].astype(str)
        + " "
        + df["scr_tob"].astype(str)
    )

    attach_dt = pd.to_datetime(
        df["enr_bf_bentfed_hw_dt"].astype(str)
        + " "
        + df["enr_bf_bentfed_hw_tm"].astype(str)
    )

    hours = (
        attach_dt - birth_dt
    ).dt.total_seconds() / 3600

    return round(hours.mean(), 1)

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
        (df[FIELD_MAP["sncu_type"]] == 11)
        &
        (df[FIELD_MAP["delivery_mode"]] == 11)
    ]

    return len(df)


def get_msncu_csection_ssc_under_2h_count():

    df = get_ssc_under_2h_df()

    df = df[
        (df[FIELD_MAP["sncu_type"]] == 11)
        &
        (df[FIELD_MAP["delivery_mode"]] == 13)
    ]

    return len(df)


# ==================================================
# PNC SSC <2H
# ==================================================

def get_pnc_nvd_ssc_under_2h_count():

    df = get_ssc_under_2h_df()

    df = df[
        (df[FIELD_MAP["sncu_type"]] == 12)
        &
        (df[FIELD_MAP["delivery_mode"]] == 11)
    ]

    return len(df)


def get_pnc_csection_ssc_under_2h_count():

    df = get_ssc_under_2h_df()

    df = df[
        (df[FIELD_MAP["sncu_type"]] == 12)
        &
        (df[FIELD_MAP["delivery_mode"]] == 13)
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

    return (
        df[
            (df["scr_sncu_sick"] == 11)
            &
            (df["scr_del_mode"] == 11)
        ]["dmf_babyid"]
        .nunique()
    )


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
    return 0


def get_pnc_csection_achieved_count():
    return 0

def get_msncu_nvd_coverage():

    achieved = get_msncu_nvd_achieved_count()
    total = get_msncu_nvd_count()

    return round(
        (achieved / total) * 100,
        1
    )


def get_msncu_csection_coverage():

    achieved = get_msncu_csection_achieved_count()
    total = get_msncu_csection_count()

    return round(
        (achieved / total) * 100,
        1
    )


def get_pnc_nvd_coverage():

    achieved = get_pnc_nvd_achieved_count()
    total = get_pnc_nvd_count()

    return round(
        (achieved / total) * 100,
        1
    )


def get_pnc_csection_coverage():

    achieved = get_pnc_csection_achieved_count()
    total = get_pnc_csection_count()

    return round(
        (achieved / total) * 100,
        1
    )