import streamlit as st
from datetime import datetime


def render_dashboard_header(title: str, subtitle: str):

    if "last_refresh" not in st.session_state:
        st.session_state["last_refresh"] = datetime.now()

    # breathing room
    st.markdown("<br>", unsafe_allow_html=True)

    st.title(title)

    st.caption(subtitle)

    info_col, btn_col = st.columns([8, 2])

    with info_col:

        st.caption(
            f"Last Refreshed: "
            f"{st.session_state['last_refresh'].strftime('%d-%b-%Y | %I:%M %p')}"
        )

    with btn_col:

        if st.button(
            "🔄 Refresh Dashboard",
            key=f"refresh_{title}",
            use_container_width=True
        ):
            st.session_state["last_refresh"] = datetime.now()
            st.cache_data.clear()
            st.rerun()

    st.divider()