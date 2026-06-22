from services.indicators import (
    get_msncu_total_cases,
    get_msncu_nvd_count,
    get_msncu_csection_count,
    get_pnc_total_cases,
    get_pnc_nvd_count,
    get_pnc_csection_count,
    get_total_ssc_received,
    get_ssc_percentage,
    get_msncu_avg_kmc,
    get_pnc_avg_kmc,
    get_msncu_nvd_avg_kmc,
    get_msncu_csection_avg_kmc,
    get_pnc_nvd_avg_kmc,
    get_pnc_csection_avg_kmc,
    get_msncu_nvd_bf_count,
    get_msncu_csection_bf_count,
    get_pnc_nvd_bf_count,
    get_pnc_csection_bf_count,
    #get_msncu_nvd_ssc_count,
    #get_msncu_csection_ssc_count,
    #get_pnc_nvd_ssc_count,
    #get_pnc_csection_ssc_count,
    get_msncu_nvd_attachment_hours,
    get_msncu_csection_attachment_hours,
    get_pnc_nvd_attachment_hours,
    get_pnc_csection_attachment_hours,
    get_msncu_nvd_ssc_under_2h_count,
    get_msncu_csection_ssc_under_2h_count,
    get_pnc_nvd_ssc_under_2h_count,
    get_pnc_csection_ssc_under_2h_count,
    get_msncu_nvd_achieved_count,
    get_msncu_csection_achieved_count,
    get_pnc_nvd_achieved_count,
    get_pnc_csection_achieved_count,
    get_msncu_nvd_coverage,
    get_msncu_csection_coverage,
    get_pnc_nvd_coverage,
    get_pnc_csection_coverage,
)
from services.indicators import get_avg_kmc_hours

import streamlit as st

from components.filters import render_filters

# ==================================================
# PAGE HEADER
# ==================================================
from components.dashboard_header import render_dashboard_header

render_dashboard_header(
    title="Inborn Cohort Compliance Registry",
    subtitle="Detailed metrics, SSC & KMC progress indexes for births completed within facility."
)
# ==================================================
# FILTERS
# ==================================================

render_filters()

# ==================================================
# OVERALL AVG IKMC
# ==================================================

st.markdown("### Inborn Cohort Analytics Panel")

with st.container(border=True):

    st.metric(
        "OVERALL AVG. iKMC",
        f"{get_avg_kmc_hours()} hrs/day"
    )

# ==================================================
# MSNCU SECTION
# ==================================================

st.markdown("---")
st.subheader("MSNCU (Mother Sick Newborn Care Unit)")

# ==================================================
# MSNCU SUMMARY
# ==================================================

with st.container(border=True):

    top1, top2, top3 = st.columns([4, 1, 1])

    with top1:
        st.markdown("### Summary")

    with top2:
        st.metric(
            "AVG iKMC",
            f"{get_msncu_avg_kmc()} hrs/day"
        )

    with top3:
        st.metric(
            "AGGREGATED CASES",
            get_msncu_total_cases()
        )

    st.divider()

    st.markdown("")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.caption("DELIVERY TYPE")
        st.write(f"NVD: {get_msncu_nvd_count()}")
        st.write(f"C-Section: {get_msncu_csection_count()}")

    with c2:
        st.caption("SSC <2H")
        st.write(f"NVD : {get_msncu_nvd_ssc_under_2h_count()}")
        st.write(f"C-Section : {get_msncu_csection_ssc_under_2h_count()}")

    with c3:
        st.caption("AVG KMC")
        st.write(f"{get_msncu_nvd_avg_kmc()} hrs/day")
        st.write(f"{get_msncu_csection_avg_kmc()} hrs/day")

    with c4:
        st.caption("EXCLUSIVE BF")
        st.write(f"NVD : {get_msncu_nvd_bf_count()}")
        st.write(f"C-Section : {get_msncu_csection_bf_count()}")

st.divider()

a1, a2 = st.columns(2)

with a1:
    st.caption("ATTACHMENT AGE (HRS)")
    st.write(f"NVD : {get_msncu_nvd_attachment_hours()}")

with a2:
    st.caption("ATTACHMENT AGE (HRS)")
    st.write(f"C-Section : {get_msncu_csection_attachment_hours()}")

# ==================================================
# MSNCU NVD
# ==================================================

st.markdown("#### MSNCU - Normal Vaginal Delivery (NVD)")

with st.container(border=True):

    st.markdown("##### iKMC Coverage")
    st.caption("SSC < 2 hrs + Avg KMC ≥ 8 hrs/day")

    cov1, cov2 = st.columns(2)

    with cov1:
        st.metric(
            "Coverage",
            f"{get_msncu_nvd_coverage()}%"
        )

    with cov2:
        st.metric(
            "Achieved Count",
            get_msncu_nvd_achieved_count()
        )

    st.divider()

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.caption("SSC WITHIN 2 HOURS")
        st.markdown(f"## {get_msncu_nvd_ssc_under_2h_count()}")

    with row1_col2:
        with st.container(border=True):
            st.caption("AVERAGE KMC CONTINUOUS")
            st.markdown(f"## {get_msncu_nvd_avg_kmc()} hrs")

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        with st.container(border=True):
            st.caption("EXCLUSIVE BREASTFEEDING")
            st.markdown(f"## {get_msncu_nvd_bf_count()}")

    with row2_col2:
        with st.container(border=True):
            st.caption("AGE AT FIRST ATTACHMENT")
            st.markdown(f"## {get_msncu_nvd_attachment_hours()} hrs")

# ==================================================
# MSNCU C-SECTION
# ==================================================

st.markdown("#### MSNCU - C-Section")

with st.container(border=True):

    st.markdown("##### iKMC Coverage")

    cov1, cov2 = st.columns(2)

    with cov1:
        st.metric(
            "Coverage",
            f"{get_msncu_csection_coverage()}%"
        )

    with cov2:
        st.metric(
            "Achieved Count",
            get_msncu_csection_achieved_count()
        )

    st.divider()

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        with st.container(border=True):
            st.caption("SSC WITHIN 2 HOURS")
            st.markdown(f"## {get_msncu_csection_ssc_under_2h_count()}")

    with row1_col2:
        with st.container(border=True):
            st.caption("AVERAGE KMC CONTINUOUS")
            st.markdown(f"## {get_msncu_csection_avg_kmc()} hrs")

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        with st.container(border=True):
            st.caption("EXCLUSIVE BREASTFEEDING")
            st.markdown(f"## {get_msncu_csection_bf_count()}")

    with row2_col2:
        with st.container(border=True):
            st.caption("AGE AT FIRST ATTACHMENT")
            st.markdown(f"## {get_msncu_csection_attachment_hours()} hrs")

# ==================================================
# PNC SECTION
# ==================================================

st.markdown("---")
st.subheader("PNC (Post Natal Care)")

# ==================================================
# PNC SUMMARY
# ==================================================

with st.container(border=True):

    top1, top2, top3 = st.columns([4, 1, 1])

    with top1:
        st.markdown("### Summary")

    with top2:
        st.metric(
            "AVG iKMC",
            f"{get_pnc_avg_kmc()} hrs/day"
        )

    with top3:
        st.metric(
            "AGGREGATED CASES",
            get_pnc_total_cases()
        )

    st.divider()

    st.markdown("")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.caption("DELIVERY TYPE")
        st.write(f"NVD: {get_pnc_nvd_count()}")
        st.write(f"C-Section: {get_pnc_csection_count()}")

    with c2:
        st.caption("SSC <2H")
        st.write(f"NVD : {get_pnc_nvd_ssc_under_2h_count()}")
        st.write(f"C-Section : {get_pnc_csection_ssc_under_2h_count()}")

    with c3:
        st.caption("AVG KMC")
        st.write(f"{get_pnc_nvd_avg_kmc()} hrs/day")
        st.write(f"{get_pnc_csection_avg_kmc()} hrs/day")

    with c4:
        st.caption("EXCLUSIVE BF")
        st.write(f"NVD : {get_pnc_nvd_bf_count()}")
        st.write(f"C-Section : {get_pnc_csection_bf_count()}")

st.divider()

a1, a2 = st.columns(2)

with a1:
    st.caption("ATTACHMENT AGE (HRS)")
    st.write(f"NVD : {get_pnc_nvd_attachment_hours()}")

with a2:
    st.caption("ATTACHMENT AGE (HRS)")
    st.write(f"C-Section : {get_pnc_csection_attachment_hours()}")

# ==================================================
# PNC NVD
# ==================================================

st.markdown("#### PNC - Normal Vaginal Delivery (NVD)")

with st.container(border=True):

    st.markdown("##### iKMC Coverage")

    cov1, cov2 = st.columns(2)

    with cov1:
        st.metric(
            "Coverage",
            f"{get_pnc_nvd_coverage()}%"
        )

    with cov2:
        st.metric(
            "Achieved Count",
            get_pnc_nvd_achieved_count()
        )

    st.divider()

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        with st.container(border=True):
            st.caption("SSC WITHIN <2 HRS")
            st.markdown(f"## {get_pnc_nvd_ssc_under_2h_count()}")

    with row1_col2:
        with st.container(border=True):
            st.caption("AVERAGE KMC CONTINUOUS")
            st.markdown(f"## {get_pnc_nvd_avg_kmc()} hrs")

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        with st.container(border=True):
            st.caption("EXCLUSIVE BREASTFEEDING")
            st.markdown(f"## {get_pnc_nvd_bf_count()}")

    with row2_col2:
        with st.container(border=True):
            st.caption("AGE AT FIRST ATTACHMENT")
            st.markdown(f"## {get_pnc_nvd_attachment_hours()} hrs")

# ==================================================
# PNC C-SECTION
# ==================================================

st.markdown("#### PNC - C-Section")

with st.container(border=True):

    st.markdown("##### iKMC Coverage")

    cov1, cov2 = st.columns(2)

    with cov1:
        st.metric(
            "Coverage",
            f"{get_pnc_csection_coverage()}%"
        )

    with cov2:
        st.metric(
            "Achieved Count",
            get_pnc_csection_achieved_count()
        )

    st.divider()

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        with st.container(border=True):
            st.caption("SSC WITHIN <2 HRS")
            st.markdown(f"## {get_pnc_csection_ssc_under_2h_count()}")

    with row1_col2:
        with st.container(border=True):
            st.caption("AVERAGE KMC CONTINUOUS")
            st.markdown(f"## {get_pnc_csection_avg_kmc()} hrs")

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        with st.container(border=True):
            st.caption("EXCLUSIVE BREASTFEEDING")
            st.markdown(f"## {get_pnc_csection_bf_count()}")

    with row2_col2:
        with st.container(border=True):
            st.caption("AGE AT FIRST ATTACHMENT")
            st.markdown(f"## {get_pnc_csection_attachment_hours()} hrs")

