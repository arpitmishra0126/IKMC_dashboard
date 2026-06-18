import streamlit as st


def coverage_card(
    coverage,
    achieved
):

    with st.container(border=True):

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("iKMC Coverage")
            st.metric("Coverage", coverage)

        with col2:
            st.metric(
                "Achieved Count",
                achieved
            )