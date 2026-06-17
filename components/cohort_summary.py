import streamlit as st


def cohort_summary(
    title,
    total_cases,

    delivery_nvd,
    delivery_csection,

    ssc_nvd,
    ssc_csection,

    kmc_nvd,
    kmc_csection,

    bf_nvd,
    bf_csection,

    attachment_nvd,
    attachment_csection,
):
    with st.container(border=True):

        st.subheader(title)

        st.markdown(
            f"""
            <h1 style="margin-top:0;">
                {total_cases}
            </h1>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.caption("DELIVERY TYPE")
            st.write(f"NVD: {delivery_nvd}")
            st.write(f"C-Section: {delivery_csection}")

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

        with col5:
            st.caption("ATTACHMENT")
            st.write(attachment_nvd)
            st.write(attachment_csection)