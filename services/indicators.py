from services.loader import load_all_data
from services.config import FIELD_MAP


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