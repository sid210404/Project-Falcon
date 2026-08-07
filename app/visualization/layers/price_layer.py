"""
Price Layer

Draws candlesticks.
"""

import pandas as pd
import plotly.graph_objects as go

from app.visualization.themes import dark


def add_price_layer(
    fig: go.Figure,
    df: pd.DataFrame,
) -> None:
    """
    Draw the candlestick price layer.
    """

    fig.add_trace(

        go.Candlestick(

            x=df["datetime"],

            open=df["open"],

            high=df["high"],

            low=df["low"],

            close=df["close"],

            name="Price",

            increasing=dict(

                fillcolor=dark.BULL,

                line=dict(

                    color=dark.BULL_BORDER,

                    width=1,

                ),

            ),

            decreasing=dict(

                fillcolor=dark.BEAR,

                line=dict(

                    color=dark.BEAR_BORDER,

                    width=1,

                ),

            ),

            whiskerwidth=0.4,

            opacity=1,

        ),

        row=1,
        col=1,

    )