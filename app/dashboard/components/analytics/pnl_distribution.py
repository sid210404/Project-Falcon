"""
PnL Distribution Chart
"""

import pandas as pd
import plotly.express as px
import streamlit as st


def render(result):

    if not result.portfolio.trades:

        st.info("No trades available.")
        return

    df = pd.DataFrame(
        [trade.__dict__ for trade in result.portfolio.trades]
    )

    fig = px.histogram(
        df,
        x="pnl",
        nbins=20,
        title="PnL Distribution",
    )

    fig.update_layout(
        xaxis_title="PnL (₹)",
        yaxis_title="Number of Trades",
        bargap=0.1,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )