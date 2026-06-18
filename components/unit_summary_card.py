import streamlit as st


def unit_summary_card(
    title,
    avg_kmc,
    total_cases,
    nvd,
    csection,
    ssc_nvd,
    ssc_csection,
    kmc_nvd,
    kmc_csection,
    bf_nvd,
    bf_csection,
):

    with st.container(border=True):

        top1, top2, top3 = st.columns([4, 1, 1])

        with top1:
            st.subheader(title)

        with top2:
            st.caption("AVG iKMC")
            st.metric("", avg_kmc)

        with top3:
            st.caption("AGGREGATED CASES")
            st.metric("", total_cases)

        st.divider()

        st.markdown(f"**Total Cases: {total_cases}**")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.caption("DELIVERY TYPE")
            st.write(f"NVD: {nvd}")
            st.write(f"C-Section: {csection}")

        with col2:
            st.caption("SSC <2H")
            st.write(ssc_nvd)
            st.write(ssc_csection)

        with col3:
            st.caption("AVG KMC")
            st.write(kmc_nvd)
            st.write(kmc_csection)

        with col4:
            st.caption("EXCLUSIVE BF")
            st.write(bf_nvd)
            st.write(bf_csection)