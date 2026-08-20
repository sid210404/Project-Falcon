"""
Win Loss Pie Chart
"""

import plotly.graph_objects as go
import streamlit as st


def render(result):

    wins = result.statistics["wins"]
    losses = result.statistics["losses"]

    fig = go.Figure()

    fig.add_trace(

        go.Pie(

            labels=["Winning Trades", "Losing Trades"],

            values=[wins, losses],

            hole=0.45,

            textinfo="label+percent",

            hovertemplate=(
                "<b>%{label}</b><br>"
                "Trades: %{value}<br>"
                "Percentage: %{percent}"
                "<extra></extra>"
            ),

        )

    )

    fig.update_layout(

        title="Win vs Loss",

        height=450,

        legend=dict(

            orientation="h",

            y=1.05,

        ),

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )