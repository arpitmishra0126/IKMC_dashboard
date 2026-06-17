import streamlit as st


def render_filters():

    with st.container(border=True):

        st.subheader("Clinical Focus Filters")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            facility = st.selectbox(
                "Facility",
                ["All Facilities"]
            )

        with col2:
            site = st.selectbox(
                "Site",
                ["All Sites"]
            )

        with col3:
            from_date = st.date_input(
                "From Date"
            )

        with col4:
            to_date = st.date_input(
                "To Date"
            )

    return {
        "facility": facility,
        "site": site,
        "from_date": from_date,
        "to_date": to_date,
    }