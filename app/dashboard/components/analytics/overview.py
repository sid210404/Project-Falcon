"""
Overview section of Analytics Dashboard.
"""

import streamlit as st


def render(result):

    stats = result.statistics

    st.subheader("📊 Portfolio Overview")

    row1 = st.columns(5)

    row1[0].metric(
        "Net Profit",
        f"₹{stats['net_profit']:,.2f}",
    )

    row1[1].metric(
        "Return %",
        f"{stats['return_pct']:.2f}%",
    )

    row1[2].metric(
        "Trades",
        stats["trades"],
    )

    row1[3].metric(
        "Win Rate",
        f"{stats['win_rate']:.2f}%",
    )

    row1[4].metric(
        "Profit Factor",
        f"{stats['profit_factor']:.2f}",
    )