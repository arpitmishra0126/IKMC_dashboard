import streamlit as st

from components.dashboard_header import render_dashboard_header
from components.filters import render_filters
from components.kpi_cards import kpi_card

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
    "--"
)

# ==================================================
# NVD
# ==================================================

st.markdown("### Average iKMC - NVD")

st.markdown("#### NVD")

col1, col2 = st.columns(2)

with col1:
    kpi_card("SSC <2 HRS", "--")

with col2:
    kpi_card("AVG KMC", "--")

col3, col4 = st.columns(2)

with col3:
    kpi_card("EXCLUSIVE BF", "--")

with col4:
    kpi_card("ATTACHMENT", "--")


# ==================================================
# C-SECTION
# ==================================================

st.markdown("### Average iKMC - C-Section")

st.markdown("#### C-Section")

col1, col2 = st.columns(2)

with col1:
    kpi_card("SSC <2 HRS", "--")

with col2:
    kpi_card("AVG KMC", "--")

col3, col4 = st.columns(2)

with col3:
    kpi_card("EXCLUSIVE BF", "--")

with col4:
    kpi_card("ATTACHMENT", "--")

