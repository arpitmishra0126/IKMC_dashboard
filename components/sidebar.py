import streamlit as st


def render_sidebar():
    """Render the sidebar with navigation and filters."""
    with st.sidebar:
        st.title("🎯 IKMC Dashboard")
        
        st.markdown("---")
        st.subheader("Filters")
        
        # Add your filter widgets here
        date_range = st.date_input("Select date range", value=[])
        facility = st.multiselect("Facility", ["All"])
        
        st.markdown("---")
        st.subheader("Navigation")
        st.write("Use the page selector at the top to navigate")
