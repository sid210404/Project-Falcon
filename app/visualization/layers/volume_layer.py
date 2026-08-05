import pandas as pd
import plotly.graph_objects as go

from app.visualization.themes import dark


def add_volume_layer(
    fig: go.Figure,
    df: pd.DataFrame,
) -> None:
    """
    Draw the volume subplot.
    """

    if "volume" not in df.columns:
        return

    colors = [
        dark.VOLUME_BULL if close >= open_
        else dark.VOLUME_BEAR
        for open_, close in zip(df["open"], df["close"])
    ]

    fig.add_trace(
        go.Bar(
            x=df["datetime"],
            y=df["volume"],
            marker_color=colors,
            name="Volume",
        ),
        row=2,
        col=1,
    )