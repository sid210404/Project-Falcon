"""
Indicator Layer

Draws technical indicators on the price chart.
"""

import pandas as pd
import plotly.graph_objects as go

from app.visualization.models.chart_settings import ChartSettings
from app.visualization.themes import dark


INDICATORS = {
    "EMA20": {
        "enabled_by": "show_ema20",
        "label": "EMA 20",
        "color": dark.EMA20,
        "width": 2,
    },
    "EMA50": {
        "enabled_by": "show_ema50",
        "label": "EMA 50",
        "color": dark.EMA50,
        "width": 2,
    },
    "VWAP": {
        "enabled_by": "show_vwap",
        "label": "VWAP",
        "color": dark.VWAP,
        "width": 2,
    },
    "opening_high": {
        "enabled_by": "show_orb",
        "label": "ORB High",
        "color": dark.ORB_HIGH,
        "width": 1,
    },
    "opening_low": {
        "enabled_by": "show_orb",
        "label": "ORB Low",
        "color": dark.ORB_LOW,
        "width": 1,
    },
}


def add_indicator_layer(
    fig: go.Figure,
    df: pd.DataFrame,
    settings: ChartSettings,
) -> None:
    """
    Draw enabled indicators.
    """

    for column, metadata in INDICATORS.items():

        # Skip if indicator is disabled
        if not getattr(settings, metadata["enabled_by"]):
            continue

        # Skip if dataframe doesn't contain indicator
        if column not in df.columns:
            continue

        fig.add_trace(

            go.Scatter(

                x=df["datetime"],

                y=df[column],

                mode="lines",

                name=metadata["label"],

                line=dict(
                    color=metadata["color"],
                    width=metadata["width"],
                    dash="dash" if "opening" in column else "solid",
                    ),

                hovertemplate=(
                    f"<b>{column}</b><br>"
                    "Value: %{y:.2f}"
                    "<extra></extra>"
                ),

            ),

            row=1,
            col=1,

        )