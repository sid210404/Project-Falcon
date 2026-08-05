import streamlit as st


def render_sidebar() -> str:
    """
    Render the application sidebar.

    Returns
    -------
    str
        Selected page.
    """

    st.sidebar.title("🦅 Project Falcon")

    page = st.sidebar.radio(
        "Navigation",
        [
            "Home",
            "Backtest",
            "Optimization",
            "Reports",
            "Settings",
        ],
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("Version 3.0")

    return page