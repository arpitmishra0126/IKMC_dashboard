import streamlit as st


def render_metric_tiles(metrics: dict):
    """Render multiple metric tiles in a grid layout."""
    cols = st.columns(len(metrics))
    
    for col, (metric_name, metric_value) in zip(cols, metrics.items()):
        with col:
            st.metric(label=metric_name, value=metric_value)
