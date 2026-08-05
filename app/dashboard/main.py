import streamlit as st
from app.dashboard.state import initialize

from app.dashboard.components.sidebar import render_sidebar
from app.dashboard.pages import (
    home,
    backtest,
    optimization,
    reports,
    settings,
)


def run_dashboard():

    st.set_page_config(
        page_title="Project Falcon",
        page_icon="🦅",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    initialize()
    page = render_sidebar()

    if page == "Home":
        home.render()

    elif page == "Backtest":
        backtest.render()

    elif page == "Optimization":
        optimization.render()

    elif page == "Reports":
        reports.render()

    elif page == "Settings":
        settings.render()


if __name__ == "__main__":
    run_dashboard()