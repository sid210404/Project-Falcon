"""
Exit Reason Analysis
"""

import pandas as pd
import plotly.express as px
import streamlit as st


def render(result):

    if not result.portfolio.trades:

        st.info("No trades available.")
        return

    df = pd.DataFrame(
        [trade.to_dict() for trade in result.portfolio.trades]
    )

    counts = (
        df["exit_reason"]
        .value_counts()
        .reset_index()
    )

    counts.columns = [
        "Reason",
        "Trades",
    ]

    fig = px.bar(

        counts,

        x="Reason",

        y="Trades",

        title="Exit Reasons",

    )

    fig.update_layout(

        height=420,

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )