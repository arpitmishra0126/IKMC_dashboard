import streamlit as st

from components.kpi_cards import kpi_card
from components.cohort_summary import cohort_summary
from components.filters import render_filters

from services.indicators import (
    get_total_screening_records,
    get_total_babies,
    get_inborn_count,
    get_outborn_count,
    get_msncu_count,
    get_pnc_count,
)

st.set_page_config(
    page_title="IKMC Dashboard",
    layout="wide"
)

from components.dashboard_header import render_dashboard_header

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
        "ELIGIBLE FOR ENROLLMENT",
        get_total_babies()
    )

with col3:
    kpi_card(
        "TOTAL ENROLLED",
        "1510"
    )

# ==================================================
# COHORT SUMMARY
# ==================================================

st.markdown("### Cohort Summary")

left, right = st.columns(2)

with left:
    cohort_summary(
        title="TOTAL INBORN CASES",
        total_cases=get_inborn_count(),

        delivery_nvd=720,
        delivery_csection=258,

        ssc_nvd=590,
        ssc_csection=135,

        kmc_nvd="4.8 hrs/day",
        kmc_csection="3.9 hrs/day",

        bf_nvd=510,
        bf_csection=172,

        attachment_nvd="1h 45m",
        attachment_csection="2h 10m",
    )

with right:
    cohort_summary(
        title="TOTAL OUTBORN CASES",
        total_cases=get_outborn_count(),

        delivery_nvd=350,
        delivery_csection=182,

        ssc_nvd=201,
        ssc_csection=77,

        kmc_nvd="4.1 hrs/day",
        kmc_csection="3.5 hrs/day",

        bf_nvd=245,
        bf_csection=104,

        attachment_nvd="1h 55m",
        attachment_csection="3h 45m",
    )

