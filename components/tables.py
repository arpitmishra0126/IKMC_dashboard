import streamlit as st
import pandas as pd


def render_table(data: pd.DataFrame, title: str = "", use_container_width: bool = True):
    """Render a data table."""
    if title:
        st.subheader(title)
    
    st.dataframe(data, use_container_width=use_container_width)
