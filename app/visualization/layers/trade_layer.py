"""
Trade Layer

Draws executed trades.
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

    # =====================================================
    # Entry Markers
    # =====================================================

    fig.add_trace(

        go.Scatter(

            x=[t.entry_time for t in trades],

            y=[t.entry_price for t in trades],

            mode="markers",

            name="Entries",

            showlegend=False,

            marker=dict(

                symbol="triangle-up",

                size=14,

                color=dark.BULL,

                line=dict(

                    color="white",

                    width=1,

                ),

            ),

            customdata=[

                (
                    t.quantity,
                    t.entry_time.strftime("%Y-%m-%d %H:%M"),
                )

                for t in trades

            ],

            hovertemplate=
            "<b>🟢 BUY</b><br><br>"

            "Price: ₹%{y:.2f}<br>"

            "Quantity: %{customdata[0]}<br>"

            "Time: %{customdata[1]}"

            "<extra></extra>",

        ),

        row=1,
        col=1,

    )

    # =====================================================
    # Exit Markers
    # =====================================================

    fig.add_trace(

        go.Scatter(

            x=[t.exit_time for t in trades],

            y=[t.exit_price for t in trades],

            mode="markers",

            name="Exits",

            showlegend=False,

            marker=dict(

                symbol="triangle-down",

                size=14,

                color=dark.BEAR,

                line=dict(

                    color="white",

                    width=1,

                ),

            ),

            customdata=[

                (

                    t.pnl,

                    t.return_pct,

                    t.exit_reason,

                    t.quantity,

                    t.exit_time.strftime("%Y-%m-%d %H:%M"),

                )

                for t in trades

            ],

            hovertemplate=

            "<b>🔴 SELL</b><br><br>"

            "Price: ₹%{y:.2f}<br>"

            "Quantity: %{customdata[3]}<br>"

            "PnL: ₹%{customdata[0]:.2f}<br>"

            "Return: %{customdata[1]:.2f}%<br>"

            "Exit: %{customdata[2]}<br>"

            "Time: %{customdata[4]}"

            "<extra></extra>",

        ),

        row=1,
        col=1,

    )