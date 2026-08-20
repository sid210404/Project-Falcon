"""
Falcon Analytics Dashboard.
"""

import streamlit as st

from app.dashboard.components.analytics import (
    charts,
    overview,
    risk_analysis,
    trade_analysis,
)


def render():

    st.title("📊 Analytics")

    result = st.session_state.get("backtest_result")

    if result is None:

        st.info("Run a backtest first.")

        return

    overview_tab, trades_tab, risk_tab, charts_tab = st.tabs(
        [
            "📊 Overview",
            "📈 Trades",
            "⚠ Risk",
            "📊 Charts",
        ]
    )

    with overview_tab:
        overview.render(result)

    with trades_tab:
        trade_analysis.render(result)

    with risk_tab:
        risk_analysis.render(result)

    with charts_tab:
        charts.render(result)