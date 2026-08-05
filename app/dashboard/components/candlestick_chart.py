"""
Professional Candlestick Chart
"""

import plotly.graph_objects as go
import streamlit as st


def render_candlestick(result):
    """
    Render an interactive candlestick chart.
    """

    df = result.dataframe

    fig = go.Figure()

    # ==========================================================
    # Candles
    # ==========================================================

    fig.add_trace(
        go.Candlestick(
            x=df["datetime"],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name="Price",
        )
    )

    # ==========================================================
    # Buy Signals
    # ==========================================================

    if "signal" in df.columns:

        buys = df[df["signal"] == 1]

        if not buys.empty:

            fig.add_trace(
                go.Scatter(
                    x=buys["datetime"],
                    y=buys["close"],
                    mode="markers",
                    name="Buy",
                    marker=dict(
                        symbol="triangle-up",
                        size=12,
                        color="green",
                    ),
                )
            )

        sells = df[df["signal"] == -1]

        if not sells.empty:

            fig.add_trace(
                go.Scatter(
                    x=sells["datetime"],
                    y=sells["close"],
                    mode="markers",
                    name="Sell",
                    marker=dict(
                        symbol="triangle-down",
                        size=12,
                        color="red",
                    ),
                )
            )

    # ==========================================================
    # Common Indicators
    # ==========================================================

    indicator_columns = [
        "EMA20",
        "EMA50",
        "VWAP",
        "opening_high",
        "opening_low",
    ]

    for column in indicator_columns:

        if column in df.columns:

            fig.add_trace(
                go.Scatter(
                    x=df["datetime"],
                    y=df[column],
                    mode="lines",
                    name=column,
                )
            )

    # ==========================================================
    # Layout
    # ==========================================================

    fig.update_layout(
        title="Candlestick Chart",
        template="plotly_white",
        height=700,
        hovermode="x unified",
        xaxis_rangeslider_visible=False,
        legend=dict(
            orientation="h",
            y=1.02,
            x=0,
        ),
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20,
        ),
    )

    fig.update_xaxes(
        title="Date",
    )

    fig.update_yaxes(
        title="Price",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )