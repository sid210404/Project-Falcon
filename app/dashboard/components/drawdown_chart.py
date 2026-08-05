"""
Drawdown Curve Component
"""

import plotly.graph_objects as go
import streamlit as st


def render_drawdown_curve(result):
    """
    Render portfolio drawdown curve.
    """

    drawdown = result.drawdown.get("drawdown_curve", [])

    if not drawdown:
        st.info("No drawdown data available.")
        return

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=list(range(len(drawdown))),
            y=drawdown,
            mode="lines",
            fill="tozeroy",
            name="Drawdown",
        )
    )

    fig.update_layout(
        title="Drawdown Curve",
        xaxis_title="Trades",
        yaxis_title="Drawdown (%)",
        height=400,
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