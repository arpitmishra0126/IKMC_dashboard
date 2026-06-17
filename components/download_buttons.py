import streamlit as st
import pandas as pd


def render_download_button(data: pd.DataFrame, filename: str, format: str = "csv"):
    """
    Render a download button for data export.
    
    Args:
        data: DataFrame to download
        filename: Name of the file to download
        format: 'csv' or 'excel'
    """
    if format == "excel":
        # Convert to Excel
        buffer = io.BytesIO()
        data.to_excel(buffer, index=False)
        buffer.seek(0)
        
        st.download_button(
            label="📥 Download Excel",
            data=buffer,
            file_name=f"{filename}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        # Convert to CSV
        csv = data.to_csv(index=False)
        
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"{filename}.csv",
            mime="text/csv"
        )


def render_export_buttons(data: pd.DataFrame, filename: str):
    """Render both CSV and Excel export buttons."""
    col1, col2 = st.columns(2)
    
    with col1:
        csv = data.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"{filename}.csv",
            mime="text/csv"
        )
    
    with col2:
        st.write("Excel export coming soon")
