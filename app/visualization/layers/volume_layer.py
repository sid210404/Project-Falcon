"""
Volume Layer

Draws colored volume bars.
"""

import pandas as pd
import plotly.graph_objects as go

from app.visualization.themes import dark


def add_volume_layer(
    fig: go.Figure,
    df: pd.DataFrame,
) -> None:
    """
    Draw the volume layer.
    """

    colors = []

    for _, row in df.iterrows():

        if row["close"] >= row["open"]:
            colors.append(dark.VOLUME_BULL)
        else:
            colors.append(dark.VOLUME_BEAR)

    fig.add_trace(

        go.Bar(

            x=df["datetime"],

            y=df["volume"],

            name="Volume",

            marker=dict(

                color=colors,

                line=dict(width=0),

            ),

            opacity=0.65,

            showlegend=False,

            hovertemplate=
            "<b>Volume</b><br>"
            "%{y:,.0f}"
            "<extra></extra>",

        ),

        row=2,
        col=1,

    )