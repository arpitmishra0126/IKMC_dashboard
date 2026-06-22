import streamlit as st

from components.dashboard_header import render_dashboard_header
from components.filters import render_filters
from components.kpi_cards import kpi_card

from services.indicators import (
    get_outborn_total_cases,
    get_outborn_nvd_count,
    get_outborn_csection_count,
    get_outborn_nvd_ssc_under_2h_count,
    get_outborn_csection_ssc_under_2h_count,
    get_outborn_avg_kmc,
    get_outborn_nvd_avg_kmc,
    get_outborn_csection_avg_kmc,
)

# ==================================================
# HEADER
# ==================================================

render_dashboard_header(
    title="Outborn Cohort Compliance Registry",
    subtitle="Detailed metrics, SSC & KMC progress indexes for outborn admissions."
)

# ==================================================
# FILTERS
# ==================================================

filters = render_filters()

# ==================================================
# OVERALL AVG iKMC
# ==================================================

st.markdown("### Overall Average iKMC")

kpi_card(
    "OVERALL AVG iKMC",
    f"{get_outborn_avg_kmc()} hrs/day"
)

# ==================================================
# NVD
# ==================================================

st.markdown("### Average iKMC - NVD")

st.markdown(
    f"#### NVD ({get_outborn_nvd_count()} Cases)"
)

col1, col2 = st.columns(2)

with col1:
    kpi_card(
        "SSC <2 HRS",
        get_outborn_nvd_ssc_under_2h_count()
    )

with col2:
    kpi_card(
        "AVG KMC",
        f"{get_outborn_nvd_avg_kmc()} hrs/day"
    )

col3, col4 = st.columns(2)

with col3:
    kpi_card(
        "EXCLUSIVE BF",
        "--"
    )

with col4:
    kpi_card(
        "ATTACHMENT",
        "--"
    )

# ==================================================
# C-SECTION
# ==================================================

st.markdown("### Average iKMC - C-Section")

st.markdown(
    f"#### C-Section ({get_outborn_csection_count()} Cases)"
)

col1, col2 = st.columns(2)

with col1:
    kpi_card(
        "SSC <2 HRS",
        get_outborn_csection_ssc_under_2h_count()
    )

with col2:
    kpi_card(
        "AVG KMC",
        f"{get_outborn_csection_avg_kmc()} hrs/day"
    )

col3, col4 = st.columns(2)

with col3:
    kpi_card(
        "EXCLUSIVE BF",
        "--"
    )

with col4:
    kpi_card(
        "ATTACHMENT",
        "--"
    )