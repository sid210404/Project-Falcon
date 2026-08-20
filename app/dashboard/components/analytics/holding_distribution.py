"""
Holding Time Distribution
"""

import pandas as pd
import plotly.express as px
import streamlit as st


def render(result):

    if not result.portfolio.trades:
        st.info("No trades available.")
        return

    df = pd.DataFrame({

        "holding_minutes": [
            trade.holding_minutes
            for trade in result.portfolio.trades
        ]

    })

    fig = px.histogram(

        df,

        x="holding_minutes",

        nbins=20,

        title="Holding Time Distribution",

    )

    fig.update_layout(

        xaxis_title="Holding Time (minutes)",

        yaxis_title="Number of Trades",

        height=420,

    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )