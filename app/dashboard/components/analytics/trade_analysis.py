"""
Trade Analysis section.
"""

import streamlit as st


def render(result):

    stats = result.statistics
    performance = result.performance

    st.subheader("📈 Trade Analysis")

    row1 = st.columns(4)

    row1[0].metric(
        "Average Winner",
        f"₹{stats['average_win']:,.2f}",
    )

    row1[1].metric(
        "Average Loser",
        f"₹{stats['average_loss']:,.2f}",
    )

    row1[2].metric(
        "Best Trade",
        f"₹{stats['best_trade']:,.2f}",
    )

    row1[3].metric(
        "Worst Trade",
        f"₹{stats['worst_trade']:,.2f}",
    )

    row2 = st.columns(2)

    row2[0].metric(
        "Average Holding",
        f"{performance['average_holding_minutes']:.2f} min",
    )

    row2[1].metric(
        "Expectancy",
        f"₹{performance['expectancy']:,.2f}",
    )