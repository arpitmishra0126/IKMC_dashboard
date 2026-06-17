import streamlit as st

st.set_page_config(
    page_title="IKMC Dashboard",
    layout="wide"
)

st.title("IKMC Dashboard")

st.markdown("""
Welcome to the IKMC Monitoring Dashboard.

Use the navigation menu on the left to explore:

- Overview
- Inborn
- Outborn
- MSNCU
- PNC
- Discharge
- Data Quality
""")