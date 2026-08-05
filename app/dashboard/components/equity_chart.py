"""
Equity Curve Chart
"""

import plotly.graph_objects as go
import streamlit as st


def render_equity_curve(result):
    """
    Render portfolio equity curve.
    """

    equity_curve = result.portfolio.equity_curve

    if not equity_curve:
        st.info("No equity curve available.")
        return

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=list(range(len(equity_curve))),
            y=equity_curve,
            mode="lines",
            name="Equity",
        )
    )

    fig.update_layout(
        title="Equity Curve",
        xaxis_title="Trades",
        yaxis_title="Portfolio Value (₹)",
        height=450,
        template="plotly_white",
        hovermode="x unified",
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20,
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )