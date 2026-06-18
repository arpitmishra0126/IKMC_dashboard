import streamlit as st


def metric_card(
    title,
    value,
    subtitle="",
):

    with st.container(border=True):

        st.caption(title)

        st.markdown(
            f"## {value}"
        )

        if subtitle:
            st.caption(subtitle)