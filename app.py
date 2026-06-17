import streamlit as st
from services.loader import load_all_data

st.set_page_config(
    page_title="IKMC Dashboard",
    layout="wide"
)

st.title("IKMC Dashboard")

data = load_all_data()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Eligibility Records",
        len(data["eligibility"])
    )

with col2:
    st.metric(
        "Mother Records",
        len(data["mother"])
    )

with col3:
    st.metric(
        "Daily Care Records",
        len(data["daily"])
    )

with col4:
    st.metric(
        "Discharge Records",
        len(data["discharge"])
    )