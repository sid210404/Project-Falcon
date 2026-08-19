import streamlit as st


def render_sidebar() -> str:
    """
    Render the Project Falcon sidebar.

    Returns
    -------
    str
        Selected page.
    """

    st.sidebar.title("🦅 Project Falcon")

    page = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Home",
            "📈 Backtest",
            "📊 Analytics",
            "⚙ Optimization",
            "📄 Reports",
            "⚙ Settings",
        ],
    )

    st.sidebar.markdown("---")

    st.sidebar.subheader("Project")

    st.sidebar.caption("Version 3.0")

    st.sidebar.caption("Falcon Quant Platform")

    return page