import streamlit as st
from datetime import datetime

def render_dashboard_header(
    title: str,
    subtitle: str,
    data_sync_time=None,
    data_available_till=None,
):

    if "last_refresh" not in st.session_state:
        st.session_state["last_refresh"] = datetime.now()

    st.markdown("<br>", unsafe_allow_html=True)

    st.title(title)
    st.caption(subtitle)

    info_col, btn_col = st.columns([8, 2])

    with info_col:

        st.caption(
            f"🔄 Dashboard Refreshed: "
            f"{st.session_state['last_refresh'].strftime('%d-%b-%Y | %I:%M %p')}"
        )

        if data_sync_time:
            st.caption(
                f"☁️ Last Data Sync: "
                f"{data_sync_time.strftime('%d-%b-%Y | %I:%M %p')}"
            )

        if data_available_till:
            st.caption(
                f"📅 Data Available Till: {data_available_till}"
            )

    with btn_col:

        if st.button(
            "🔄 Refresh Dashboard",
            key=f"refresh_{title}",
            use_container_width=True,
        ):
            st.session_state["last_refresh"] = datetime.now()
            st.cache_data.clear()
            st.rerun()

    st.divider()