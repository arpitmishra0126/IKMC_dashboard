import streamlit as st


def kpi_card(title, value):
    with st.container(border=True):
        st.caption(title)
        st.markdown(
            f"""
            <h1 style='margin-top:0px;'>
                {value}
            </h1>
            """,
            unsafe_allow_html=True
        )