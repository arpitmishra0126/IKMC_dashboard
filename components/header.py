import streamlit as st


def render_header(title: str, subtitle: str = ""):
    """Render the page header with title and subtitle."""
    col1, col2 = st.columns([0.8, 0.2])
    
    with col1:
        st.title(title)
        if subtitle:
            st.markdown(f"*{subtitle}*")
    
    with col2:
        st.write("")  # Spacer
    
    st.markdown("---")
