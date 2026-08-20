"""
Analytics Charts Dashboard
"""

import streamlit as st

from app.dashboard.components.analytics import (
    exit_reason_chart,
    holding_distribution,
    pnl_distribution,
    win_loss_pie,
)


def render(result):

    row1 = st.columns(2)

    with row1[0]:

        pnl_distribution.render(result)

    with row1[1]:

        win_loss_pie.render(result)

    st.divider()

    row2 = st.columns(2)

    with row2[0]:

        holding_distribution.render(result)

    with row2[1]:

        exit_reason_chart.render(result)