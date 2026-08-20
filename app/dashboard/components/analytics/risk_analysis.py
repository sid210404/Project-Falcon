"""
Risk Analysis section.
"""

import streamlit as st


def render(result):

    performance = result.performance
    drawdown = result.drawdown

    st.subheader("⚠ Risk Analysis")

    row = st.columns(4)

    row[0].metric(
        "Sharpe",
        performance["sharpe_ratio"],
    )

    row[1].metric(
        "Max Drawdown",
        f"{drawdown['max_drawdown_pct']:.2f}%",
    )

    row[2].metric(
        "Average RR",
        performance["average_rr"],
    )

    row[3].metric(
        "Win Streak",
        performance["consecutive_wins"],
    )

    row2 = st.columns(2)

    row2[0].metric(
        "Loss Streak",
        performance["consecutive_losses"],
    )

    row2[1].metric(
        "Current Drawdown",
        f"{drawdown['current_drawdown_pct']:.2f}%",
    )