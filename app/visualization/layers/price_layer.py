import pandas as pd
import plotly.graph_objects as go


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
        ),
        row=1,
        col=1,
    )