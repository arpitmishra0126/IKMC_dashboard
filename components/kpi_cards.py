import streamlit as st


def render_kpi_card(label: str, value: str, change: str = "", icon: str = "📊"):
    """Render a KPI card with label, value, and optional change indicator."""
    col = st.container()
    
    with col:
        st.metric(
            label=f"{icon} {label}",
            value=value,
            delta=change if change else None
        )
