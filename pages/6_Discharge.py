import streamlit as st

from components.dashboard_header import render_dashboard_header
from components.filters import render_filters
from components.kpi_cards import kpi_card

# ==================================================
# HEADER
# ==================================================

render_dashboard_header(
    title="Discharge Outcomes & Compliance Registry",
    subtitle="Clinical outcomes, referral patterns, mortality tracking and discharge compliance indicators."
)

# ==================================================
# FILTERS
# ==================================================

filters = render_filters()

# ==================================================
# OVERALL OUTCOMES
# ==================================================

st.markdown("### Outcome Summary")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    kpi_card(
        "DISCHARGED",
        "--"
    )

with col2:
    kpi_card(
        "REFERRED",
        "--"
    )

with col3:
    kpi_card(
        "LAMA",
        "--"
    )

with col4:
    kpi_card(
        "DEATH",
        "--"
    )

with col5:
    kpi_card(
        "STILL ADMITTED",
        "--"
    )

# ==================================================
# INBORN OUTCOMES
# ==================================================

st.markdown("### Inborn Outcomes")

col1, col2 = st.columns(2)

with col1:

    st.markdown("#### NVD")

    c1, c2 = st.columns(2)

    with c1:
        kpi_card("DISCHARGED", "--")

    with c2:
        kpi_card("REFERRED", "--")

    c3, c4 = st.columns(2)

    with c3:
        kpi_card("LAMA", "--")

    with c4:
        kpi_card("DEATH", "--")

with col2:

    st.markdown("#### C-Section")

    c1, c2 = st.columns(2)

    with c1:
        kpi_card("DISCHARGED", "--")

    with c2:
        kpi_card("REFERRED", "--")

    c3, c4 = st.columns(2)

    with c3:
        kpi_card("LAMA", "--")

    with c4:
        kpi_card("DEATH", "--")

# ==================================================
# OUTBORN OUTCOMES
# ==================================================

st.markdown("### Outborn Outcomes")

col1, col2 = st.columns(2)

with col1:

    st.markdown("#### NVD")

    c1, c2 = st.columns(2)

    with c1:
        kpi_card("DISCHARGED", "--")

    with c2:
        kpi_card("REFERRED", "--")

    c3, c4 = st.columns(2)

    with c3:
        kpi_card("LAMA", "--")

    with c4:
        kpi_card("DEATH", "--")

with col2:

    st.markdown("#### C-Section")

    c1, c2 = st.columns(2)

    with c1:
        kpi_card("DISCHARGED", "--")

    with c2:
        kpi_card("REFERRED", "--")

    c3, c4 = st.columns(2)

    with c3:
        kpi_card("LAMA", "--")

    with c4:
        kpi_card("DEATH", "--")

# ==================================================
# COMPLIANCE VS OUTCOME
# ==================================================

st.markdown("### Compliance vs Outcome")

col1, col2 = st.columns(2)

with col1:

    kpi_card(
        "PROGRAM CRITERIA MET",
        "Pending Validation"
    )

with col2:

    kpi_card(
        "PROGRAM CRITERIA NOT MET",
        "Pending Validation"
    )

