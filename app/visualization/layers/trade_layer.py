"""
Trade Layer

Draws executed trades on the price chart.
"""

import plotly.graph_objects as go

from app.visualization.themes import dark


def add_trade_layer(
    fig: go.Figure,
    result,
) -> None:
    """
    Draw completed trades.
    """

    trades = result.portfolio.trades

    if not trades:
        return

    # ===========================
    # Entries
    # ===========================

    fig.add_trace(

        go.Scatter(

            x=[trade.entry_time for trade in trades],

            y=[trade.entry_price for trade in trades],

            mode="markers",

            name="Entry",

            marker=dict(

                symbol="triangle-up",

                size=dark.MARKER_SIZE,

                color=dark.BULL,

                line=dict(
                    color="white",
                    width=1,
                ),

            ),

            hovertemplate=(
                "<b>ENTRY</b><br>"
                "Price: ₹%{y:.2f}<br>"
                "Time: %{x}<extra></extra>"
            ),

        ),

        row=1,
        col=1,

    )

    # ===========================
    # Exits
    # ===========================

    fig.add_trace(

        go.Scatter(

            x=[trade.exit_time for trade in trades],

            y=[trade.exit_price for trade in trades],

            mode="markers",

            name="Exit",

            marker=dict(

                symbol="triangle-down",

                size=dark.MARKER_SIZE,

                color=dark.BEAR,

                line=dict(
                    color="white",
                    width=1,
                ),

            ),

            hovertemplate=(
                "<b>EXIT</b><br>"
                "Price: ₹%{y:.2f}<br>"
                "Time: %{x}<extra></extra>"
            ),

        ),

        row=1,
        col=1,

    )