import streamlit as st


def render_alert(message: str, alert_type: str = "info"):
    """
    Render an alert message.
    
    Args:
        message: The alert message
        alert_type: 'info', 'warning', or 'error'
    """
    if alert_type == "warning":
        st.warning(message)
    elif alert_type == "error":
        st.error(message)
    else:
        st.info(message)


def render_success(message: str):
    """Render a success alert."""
    st.success(message)
