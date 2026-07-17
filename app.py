import streamlit as st

from components.kpi_cards import kpi_card
from components.cohort_summary import cohort_summary
from components.filters import render_filters
from components.dashboard_header import render_dashboard_header

from services.indicators import *

st.set_page_config(
    page_title="IKMC Dashboard",
    layout="wide"
)

# ==================================================
# HEADER
# ==================================================

render_dashboard_header(
    title="iKMC Monitoring System",
    subtitle="Facility-wide monitoring of SSC, KMC, breastfeeding compliance, cohort performance, and discharge outcomes."
)

# ==================================================
# FILTERS
# ==================================================

filters = render_filters()

# ==================================================
# KPI CARDS
# ==================================================

st.markdown("### Key Performance Indicators (KPIs)")

col1, col2, col3 = st.columns(3)

with col1:
    kpi_card(
        "PRE-SCREENED",
        get_total_screening_records()
    )

with col2:
    kpi_card(
        "SCREENED",
        get_total_screened()
    )

with col3:
    kpi_card(
        "ELIGIBLE FOR ENROLLMENT",
        get_total_eligible()
    )

# ==================================================
# COHORT SUMMARY
# ==================================================

st.markdown("### Cohort Summary")

left, right = st.columns(2)

# ==================================================
# INBORN
# ==================================================

with left:
    cohort_summary(
        title="TOTAL INBORN CASES",

        total_cases=get_inborn_count(),

        delivery_nvd=get_inborn_nvd_count(),
        delivery_csection=get_inborn_csection_count(),

        ssc_nvd=get_inborn_nvd_ssc_under_2h_count(),
        ssc_csection=get_inborn_csection_ssc_under_2h_count(),

        kmc_nvd=f"{get_inborn_nvd_avg_kmc()} hrs/day",
        kmc_csection=f"{get_inborn_csection_avg_kmc()} hrs/day",

        bf_nvd=get_inborn_nvd_bf_count(),
        bf_csection=get_inborn_csection_bf_count(),

        # Keep these until we improve the calculation
        attachment_nvd="1h 45m",
        attachment_csection="2h 10m",
    )

# ==================================================
# OUTBORN
# ==================================================

with right:
    cohort_summary(
        title="TOTAL OUTBORN CASES",

        total_cases=get_outborn_count(),

        delivery_nvd=get_outborn_nvd_count(),
        delivery_csection=get_outborn_csection_count(),

        ssc_nvd=get_outborn_nvd_ssc_under_2h_count(),
        ssc_csection=get_outborn_csection_ssc_under_2h_count(),

        kmc_nvd=f"{get_outborn_nvd_avg_kmc()} hrs/day",
        kmc_csection=f"{get_outborn_csection_avg_kmc()} hrs/day",

        bf_nvd=get_outborn_nvd_bf_count(),
        bf_csection=get_outborn_csection_bf_count(),

        # Keep these until we improve the calculation
        attachment_nvd="1h 55m",
        attachment_csection="3h 45m",
    )

    # ==================================================
# DATA QUALITY
# ==================================================

st.divider()

st.markdown("## System Validation & Data Quality")

col1, col2, col3 = st.columns(3)

with col1:
    kpi_card(
        "SCREENING RECORDS WITHOUT BABY IDs",
        get_missing_babyid_count()
    )

with col2:
    kpi_card(
        "DUPLICATE BABIES",
        get_duplicate_babyid_count()
    )

with col3:
    kpi_card(
        "UNMATCHED RECORDS",
        get_merge_mismatch_count()
    )
st.caption(
    "Summary of data completeness and integrity checks performed across source datasets."
)
col1, col2, col3 = st.columns(3)

with col1:
    kpi_card(
        "MISSING DAILY CARE",
        get_missing_dailycare_count()
    )

with col2:
    kpi_card(
        "DISCHARGE DUPLICATES",
        get_duplicate_discharge_count()
    )

with col3:
    kpi_card(
        "VALIDATION STATUS",
        get_validation_status()
    )


st.markdown("---")

with st.expander("🔍 View Validation Details"):

    st.subheader("Screening Records Without Baby IDs")

    st.dataframe(
        get_missing_babyid_df(),
        use_container_width=True
    )

    st.subheader("Duplicate Baby IDs")

    st.dataframe(
        get_duplicate_babyid_df(),
        use_container_width=True
    )

    st.subheader("Merge Mismatches")

    st.dataframe(
        get_merge_mismatch_df(),
        use_container_width=True
    )

    st.subheader("Missing Daily Care")

    st.dataframe(
        get_missing_dailycare_df(),
        use_container_width=True
    )

    st.subheader("Duplicate Discharge Records")

    st.dataframe(
        get_duplicate_discharge_df(),
        use_container_width=True
    ) 