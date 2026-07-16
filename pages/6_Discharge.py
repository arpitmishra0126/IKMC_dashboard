import streamlit as st

from components.dashboard_header import render_dashboard_header
from components.filters import render_filters
from components.kpi_cards import kpi_card

from services.indicators import (
    get_total_discharged,
    get_total_referred,
    get_total_lama,
    get_total_death,

    get_inborn_nvd_discharged,
    get_inborn_nvd_referred,
    get_inborn_nvd_lama,
    get_inborn_nvd_death,

    get_inborn_csection_discharged,
    get_inborn_csection_referred,
    get_inborn_csection_lama,
    get_inborn_csection_death,

    get_outborn_nvd_discharged,
    get_outborn_nvd_referred,
    get_outborn_nvd_lama,
    get_outborn_nvd_death,

    get_outborn_csection_discharged,
    get_outborn_csection_referred,
    get_outborn_csection_lama,
    get_outborn_csection_death,
    get_total_still_admitted,
)

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
        get_total_discharged()
    )

with col2:
    kpi_card(
        "REFERRED",
        get_total_referred()
    )

with col3:
    kpi_card(
        "LAMA",
        get_total_lama()
    )

with col4:
    kpi_card(
        "DEATH",
        get_total_death()
    )

with col5:
    kpi_card(
        "STILL ADMITTED",
        get_total_still_admitted()
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
        kpi_card(
            "DISCHARGED",
            get_inborn_nvd_discharged()
        )

    with c2:
        kpi_card(
            "REFERRED",
            get_inborn_nvd_referred()
        )

    c3, c4 = st.columns(2)

    with c3:
        kpi_card(
            "LAMA",
            get_inborn_nvd_lama()
        )

    with c4:
        kpi_card(
            "DEATH",
            get_inborn_nvd_death()
        )

with col2:

    st.markdown("#### C-Section")

    c1, c2 = st.columns(2)

    with c1:
        kpi_card(
            "DISCHARGED",
            get_inborn_csection_discharged()
        )

    with c2:
        kpi_card(
            "REFERRED",
            get_inborn_csection_referred()
        )

    c3, c4 = st.columns(2)

    with c3:
        kpi_card(
            "LAMA",
            get_inborn_csection_lama()
        )

    with c4:
        kpi_card(
            "DEATH",
            get_inborn_csection_death()
        )

# ==================================================
# OUTBORN OUTCOMES
# ==================================================

st.markdown("### Outborn Outcomes")

col1, col2 = st.columns(2)

with col1:

    st.markdown("#### NVD")

    c1, c2 = st.columns(2)

    with c1:
        kpi_card(
            "DISCHARGED",
            get_outborn_nvd_discharged()
        )

    with c2:
        kpi_card(
            "REFERRED",
            get_outborn_nvd_referred()
        )

    c3, c4 = st.columns(2)

    with c3:
        kpi_card(
            "LAMA",
            get_outborn_nvd_lama()
        )

    with c4:
        kpi_card(
            "DEATH",
            get_outborn_nvd_death()
        )

with col2:

    st.markdown("#### C-Section")

    c1, c2 = st.columns(2)

    with c1:
        kpi_card(
            "DISCHARGED",
            get_outborn_csection_discharged()
        )

    with c2:
        kpi_card(
            "REFERRED",
            get_outborn_csection_referred()
        )

    c3, c4 = st.columns(2)

    with c3:
        kpi_card(
            "LAMA",
            get_outborn_csection_lama()
        )

    with c4:
        kpi_card(
            "DEATH",
            get_outborn_csection_death()
        )


